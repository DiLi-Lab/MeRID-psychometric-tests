#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment implements the Stroop and Flanker tasks.
Based on the original stroop-simon-german project: https://github.com/DiLi-Lab/stroop-simon-german
(The original project does not include a LICENSE file)
Based on paradigms:
- Stroop: Stroop, J. R. (1935). Studies of interference in serial verbal reactions.
- Flanker: Eriksen, B. A., & Eriksen, C. W. (1974). Effects of noise letters.

Modifications:
- Changed from separate Stroop + Simon to combined Stroop + Flanker
- Added YAML-based configuration
- Modified data output to CSV format

Copyright (C) 2024-2026 MultiplEYE Projects
"""

import argparse
import ast
import os  # handy system and path functions
import re
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml
import unicodedata
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from psychopy import visual, core, data, event, logging, prefs
from psychopy.constants import (NOT_STARTED, STARTED, FINISHED)

# Avoid psychtoolbox import warning by forcing event backend.
prefs.hardware['keyboardBackend'] = 'event'
from psychopy.hardware import keyboard

try:
    import pyglet
except Exception:
    pyglet = None

try:
    import arabic_reshaper
except Exception:
    arabic_reshaper = None

try:
    from bidi.algorithm import get_display
except Exception:
    try:
        from bidi import algorithm as bidialg
        get_display = bidialg.get_display
    except Exception:
        get_display = None

HAS_RTL_SUPPORT = arabic_reshaper is not None and get_display is not None

# # Ensure that relative paths start from the same directory as this script
# _thisDir = os.path.dirname(os.path.abspath(__file__))

date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run the Stroop and Flanker test.")
parser.add_argument('--participant_folder', type=str, required=True, help="Path to the participant folder.")
args = parser.parse_args()
results_folder = args.participant_folder

# Path to the YAML file contains the language and experiment configurations
PROJECT_ROOT = Path(__file__).resolve().parents[2]
config_path = PROJECT_ROOT / 'configs' / 'config.yaml'
experiment_config_path = PROJECT_ROOT / 'configs' / 'experiment.yaml'

# Load the YAML file
with config_path.open('r', encoding='utf-8') as file:
    config_data = yaml.safe_load(file)
language = config_data['language']
country_code = config_data['country_code']
lab_number = config_data['lab_number']
font = config_data['font']

rtl_langs = {'fa', 'fas', 'persian', 'ar', 'ara', 'he', 'heb', 'ur', 'urd'}
language_code = str(language).strip().lower()
is_rtl = language_code in rtl_langs
language_style = 'Arabic' if is_rtl else 'LTR'
display_font = font if font else "Arial Unicode MS"


def sanitize_text(value):
    if value is None:
        return ''

    s = str(value).replace('\\n', '\n')
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    s = unicodedata.normalize("NFC", s)

    cleaned = []
    for ch in s:
        code = ord(ch)
        cat = unicodedata.category(ch)
        # Windows/Pyglet text rendering can fail on non-BMP code points
        # (e.g., emoji), raising: ord() expected a character, but string of length 2.
        if os.name == 'nt' and code > 0xFFFF:
            continue
        if 0xD800 <= code <= 0xDFFF:
            continue
        if code > 0x10FFFF:
            continue
        if cat in {'Cs', 'Co', 'Cn'}:
            continue
        if cat == 'Cc' and ch not in ('\n', '\t'):
            continue
        cleaned.append(ch)
    return ''.join(cleaned)


def is_rtl_language(value):
    return str(value).strip().lower() in rtl_langs


def normalize_instruction_text(text):
    """
    Match RAN behavior:
    - blank lines separate paragraphs
    - single newlines become spaces inside paragraph
    """
    text = sanitize_text(text).strip()
    if not text:
        return ''

    paragraphs = re.split(r'\n\s*\n+', text)
    cleaned = []
    for paragraph in paragraphs:
        paragraph = re.sub(r'[\n\t]+', ' ', paragraph)
        paragraph = re.sub(r'\s+', ' ', paragraph).strip()
        if paragraph:
            cleaned.append(paragraph)
    return '\n\n'.join(cleaned)


def resolve_font_path(preferred_font_name):
    try:
        path = font_manager.findfont(preferred_font_name, fallback_to_default=False)
        if path and Path(path).exists():
            return path
    except Exception:
        pass

    fallback = font_manager.findfont("DejaVu Sans")
    if fallback and Path(fallback).exists():
        return fallback
    raise FileNotFoundError(f"Could not resolve a font path for '{preferred_font_name}'.")


def pick_rtl_render_font_path():
    def report(family):
        logging.warning(f"Using RTL font family: {family}")
        print(f"Using RTL font family: {family}", flush=True)

    for family in ("DejaVu Sans", "Vazirmatn", "Noto Naskh Arabic", "Noto Sans Arabic", "Tahoma"):
        try:
            path = resolve_font_path(family)
            report(family)
            return path
        except Exception:
            continue

    for family, path in (
        ("Al Bayan", "/System/Library/Fonts/Supplemental/Al Bayan.ttc"),
        ("Arial Unicode MS", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    ):
        if Path(path).exists():
            report(family)
            return path

    fallback_family = display_font if display_font else "DejaVu Sans"
    path = resolve_font_path(fallback_family)
    logging.warning(f"No preferred RTL font found, fallback family: {fallback_family}")
    print(f"No preferred RTL font found, fallback family: {fallback_family}", flush=True)
    return path


def shape_rtl_line(line):
    reshaped = arabic_reshaper.reshape(line)
    return get_display(reshaped)


def set_text_with_rtl_fallback(stim, value):
    text = sanitize_text(value)
    try:
        stim.setText(text)
    except AttributeError as exc:
        # Some PsychoPy builds expose Arabic style but miss internal reshaper.
        if is_rtl and "arabic_reshaper" in str(exc):
            stim.languageStyle = 'LTR'
            stim.setText(shape_rtl_line(text))
            return
        raise


def measure_text_pil(draw, text, font_obj):
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_paragraph_ltr(draw, paragraph, font_obj, max_width_px):
    words = paragraph.split()
    if not words:
        return []

    lines = []
    current = []
    for word in words:
        candidate = ' '.join(current + [word])
        width, _ = measure_text_pil(draw, candidate, font_obj)
        if width <= max_width_px or not current:
            current.append(word)
        else:
            lines.append(' '.join(current))
            current = [word]
    if current:
        lines.append(' '.join(current))
    return lines


def wrap_paragraph_rtl(draw, paragraph, font_obj, max_width_px):
    words = paragraph.split()
    if not words:
        return []

    lines = []
    current = []
    for word in words:
        candidate_logical = ' '.join(current + [word])
        candidate_visual = shape_rtl_line(candidate_logical)
        width, _ = measure_text_pil(draw, candidate_visual, font_obj)
        if width <= max_width_px or not current:
            current.append(word)
        else:
            lines.append(' '.join(current))
            current = [word]

    if current:
        lines.append(' '.join(current))
    return lines


def text_to_logical_lines(text, rtl, draw, font_obj, max_width_px):
    text = normalize_instruction_text(text)
    if not text:
        return []

    paragraphs = text.split('\n\n')
    all_lines = []
    for i, paragraph in enumerate(paragraphs):
        if rtl:
            all_lines.extend(wrap_paragraph_rtl(draw, paragraph, font_obj, max_width_px))
        else:
            all_lines.extend(wrap_paragraph_ltr(draw, paragraph, font_obj, max_width_px))
        if i < len(paragraphs) - 1:
            all_lines.append('')
    return all_lines


def render_text_screen_to_image(
    text,
    language_code,
    font_path,
    out_path,
    image_width=1800,
    image_height=1100,
    font_size=62,
    margin_px=180,
    line_spacing_px=26,
    bg_color='white',
    text_color='black'
):
    rtl = is_rtl_language(language_code)

    image = Image.new('RGBA', (image_width, image_height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font_obj = ImageFont.truetype(font_path, font_size)

    max_width_px = image_width - 2 * margin_px
    logical_lines = text_to_logical_lines(text, rtl, draw, font_obj, max_width_px)

    display_lines = []
    line_heights = []
    for line in logical_lines:
        if line == '':
            display_lines.append('')
            line_heights.append(font_size // 2)
            continue
        display_line = shape_rtl_line(line) if rtl else line
        _, h = measure_text_pil(draw, display_line, font_obj)
        display_lines.append(display_line)
        line_heights.append(h)

    total_height = 0
    for i, h in enumerate(line_heights):
        total_height += h
        if i < len(line_heights) - 1:
            total_height += line_spacing_px

    y = (image_height - total_height) // 2
    for i, line in enumerate(display_lines):
        if line == '':
            y += line_heights[i] + line_spacing_px
            continue
        w, h = measure_text_pil(draw, line, font_obj)
        x = (image_width - w) // 2
        draw.text((x, y), line, font=font_obj, fill=(0, 0, 0, 255) if text_color == 'black' else text_color)
        y += h + line_spacing_px

    image.save(out_path)


def convert_text_screen_to_image_stim(source_stim, image_name, font_path, output_dir, text_override=None):
    text_source = text_override if text_override is not None else getattr(source_stim, 'text', '')
    text = sanitize_text(text_source)
    if not text:
        return source_stim

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    image_width_px = 1800
    image_height_px = 1000 if source_stim.height >= 0.05 else 850
    font_size_px = 62 if source_stim.height >= 0.05 else 48
    image_path = output_dir / image_name
    render_text_screen_to_image(
        text=text,
        language_code=language_code,
        font_path=font_path,
        out_path=str(image_path),
        image_width=image_width_px,
        image_height=image_height_px,
        font_size=font_size_px,
        margin_px=180,
        line_spacing_px=max(20, font_size_px // 3)
    )

    width_units = source_stim.wrapWidth if source_stim.wrapWidth else min(win.size[0] / win.size[1] * 0.9, 1.45)
    height_units = 0.65 if source_stim.height >= 0.05 else 0.55
    return visual.ImageStim(
        win=win,
        name=source_stim.name,
        image=str(image_path),
        units='height',
        pos=source_stim.pos,
        size=(width_units, height_units),
        ori=source_stim.ori,
        color=[1, 1, 1],
        colorSpace='rgb',
        opacity=source_stim.opacity,
        interpolate=True,
        depth=source_stim.depth
    )


def normalize_key_name(key_name):
    """
    Normalize key names so comparisons work on macOS and Windows.
    """
    if key_name is None:
        return None

    # Some macOS backends return key names as list/tuple payloads like:
    # ['space', 19.1098]. Extract the textual key token first.
    if isinstance(key_name, (list, tuple)) and len(key_name) > 0:
        key_name = key_name[0]

    # Some backends may stringify that payload:
    # "['space', 19.1098]". Parse it if possible.
    elif isinstance(key_name, str) and key_name.startswith('[') and key_name.endswith(']'):
        try:
            parsed = ast.literal_eval(key_name)
            if isinstance(parsed, (list, tuple)) and len(parsed) > 0:
                key_name = parsed[0]
        except (SyntaxError, ValueError):
            pass

    raw_key = str(key_name)
    raw_key_map = {
        ' ': 'space',
        '\n': 'return',
        '\r': 'return',
        '\r\n': 'return',
    }
    if raw_key in raw_key_map:
        normalized = raw_key_map[raw_key]
    else:
        normalized = raw_key.strip().lower().replace('-', '_')

    key_map = {
        'spacebar': 'space',
        'space': 'space',
        'space_char': 'space',
        'esc': 'escape',
        'enter': 'return',
        'return': 'return',
        'newline': 'return',
        'period': '.',
        'comma': ',',
        'slash': '/',
        'leftarrow': 'left',
        'rightarrow': 'right',
        'uparrow': 'up',
        'downarrow': 'down',
    }
    normalized = key_map.get(normalized, normalized)

    for prefix in ('num_', 'numpad_', 'kp_'):
        if normalized.startswith(prefix):
            suffix = normalized[len(prefix):]
            if len(suffix) == 1 and suffix.isdigit():
                return suffix

    return normalized


def key_aliases(key_name):
    normalized = normalize_key_name(key_name)
    aliases = {normalized}

    if normalized == 'space':
        aliases.add('spacebar')
    elif normalized == 'return':
        aliases.add('enter')
    elif normalized == '.':
        aliases.add('period')
    elif normalized == ',':
        aliases.add('comma')
    elif normalized == '/':
        aliases.add('slash')
    elif normalized in {'left', 'right', 'up', 'down'}:
        aliases.add(f'{normalized}arrow')
    elif normalized and len(normalized) == 1 and normalized.isdigit():
        aliases.update({f'num_{normalized}', f'numpad_{normalized}', f'kp_{normalized}'})

    aliases.discard(None)
    return list(aliases)


def expand_key_list(*keys):
    expanded = []
    seen = set()
    for key in keys:
        for alias in key_aliases(key):
            if alias not in seen:
                seen.add(alias)
                expanded.append(alias)
    return expanded


def is_key_match(pressed_key, expected_key):
    return normalize_key_name(pressed_key) == normalize_key_name(expected_key)


def get_first_matching_keypress(key_events, expected_keys):
    """
    Return the latest keypress matching any expected key alias.
    """
    for key_event in reversed(key_events):
        if any(is_key_match(key_event.name, expected_key) for expected_key in expected_keys):
            return key_event
    return None


def get_first_matching_keyname(key_names, expected_keys):
    """
    Return the latest key name matching any expected key alias.
    """
    for key_name in reversed(key_names):
        if any(is_key_match(key_name, expected_key) for expected_key in expected_keys):
            return key_name
    return None


_key_backend_warning_shown = False


def _quit_if_escape_in_key_events(key_events):
    if get_first_matching_keypress(key_events, ("escape",)):
        core.quit()


def _quit_if_escape_in_key_names(key_names):
    if get_first_matching_keyname(key_names, ("escape",)):
        core.quit()


def safe_event_get_keys(key_list=None):
    """
    Read keys via psychopy.event without crashing on backend glitches.
    """
    global _key_backend_warning_shown
    try:
        keys = event.getKeys(keyList=key_list)
        _quit_if_escape_in_key_names(keys)
        return keys
    except Exception as exc:
        if not _key_backend_warning_shown:
            logging.info(f"event.getKeys failed on this backend: {exc}")
            _key_backend_warning_shown = True
        return []


def safe_keyboard_get_keys(keyboard_component, key_list=None):
    """
    Read keys via psychopy.hardware.keyboard safely.
    """
    global _key_backend_warning_shown
    try:
        keys = keyboard_component.getKeys(keyList=key_list, waitRelease=False)
        _quit_if_escape_in_key_events(keys)
        return keys
    except Exception as exc:
        if not _key_backend_warning_shown:
            logging.info(f"keyboard.getKeys failed on this backend: {exc}")
            _key_backend_warning_shown = True
        return []


def escape_pressed(default_keyboard):
    """
    Unified Escape handling across keyboard backends.
    """
    keyboard_events = safe_keyboard_get_keys(default_keyboard, ["escape"])
    if get_first_matching_keypress(keyboard_events, ("escape",)):
        return True
    fallback_keys = safe_event_get_keys(["escape"])
    return get_first_matching_keyname(fallback_keys, ("escape",)) is not None


def resolve_table_file(base_path_without_ext, file_label='input file'):
    """
    Resolve a table file path, preferring xlsx but allowing csv.
    """
    candidate_extensions = ('.xlsx', '.csv')
    base_path = Path(base_path_without_ext)
    for extension in candidate_extensions:
        candidate_path = base_path.with_suffix(extension)
        if candidate_path.exists():
            return str(candidate_path)

    tried_paths = ", ".join(str(base_path.with_suffix(ext)) for ext in candidate_extensions)
    raise FileNotFoundError(f"Could not find {file_label}. Tried: {tried_paths}")


def load_table_file(table_path, **kwargs):
    """
    Load a tabular file from csv/xlsx based on file extension.
    """
    table_path = Path(table_path)
    if table_path.suffix.lower() == '.csv':
        return pd.read_csv(table_path, **kwargs)

    # pandas/openpyxl can fail on malformed xlsx merge metadata in some files.
    excel_kwargs = dict(kwargs)
    excel_kwargs.pop('encoding', None)  # not used by read_excel
    try:
        return pd.read_excel(table_path, **excel_kwargs)
    except Exception as excel_error:
        fallback_csv_path = table_path.with_suffix('.csv')
        if fallback_csv_path.exists():
            return pd.read_csv(fallback_csv_path, **kwargs)

        # Final fallback: strip malformed merge metadata from worksheet XML.
        try:
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
                sanitized_path = temp_file.name

            with zipfile.ZipFile(table_path, 'r') as source_zip, zipfile.ZipFile(sanitized_path, 'w') as target_zip:
                for item in source_zip.infolist():
                    data = source_zip.read(item.filename)
                    if item.filename.startswith('xl/worksheets/sheet') and item.filename.endswith('.xml'):
                        try:
                            xml_text = data.decode('utf-8')
                            xml_text = re.sub(r'<mergeCells[^>]*>.*?</mergeCells>', '', xml_text, flags=re.DOTALL)
                            data = xml_text.encode('utf-8')
                        except UnicodeDecodeError:
                            pass
                    target_zip.writestr(item, data)

            try:
                return pd.read_excel(sanitized_path, **excel_kwargs)
            finally:
                if Path(sanitized_path).exists():
                    os.remove(sanitized_path)
        except Exception:
            raise excel_error


if experiment_config_path.exists():
    # Load the experiment configuration if the file exists
    with experiment_config_path.open('r', encoding='utf-8') as file:
        expInfo = yaml.safe_load(file)
        participant_id = str(expInfo['participant_id']).zfill(3)
else:
    # Set default values if the file does not exist
    expInfo = {'participant_id': 999, 'session_id': 2}
    participant_id = "999"

# Create folder for audio and csv data
output_path = PROJECT_ROOT / 'data' / results_folder / 'Stroop_Flanker'
output_path.mkdir(parents=True, exist_ok=True)
rendered_text_dir = output_path / f"rendered_text_{date}"
rendered_text_dir.mkdir(parents=True, exist_ok=True)
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = str(
    output_path / (
        f"{language}{country_code}{lab_number}"
        f"_{participant_id}_PT{expInfo['session_id']}_{date}"
    )
)
print(filename)
# Load instruction/stimulus tables from xlsx or csv
instructions_path = resolve_table_file(
    str(PROJECT_ROOT / 'languages' / language / 'instructions' / f'Stroop_Flanker_instructions_{language.lower()}'),
    file_label='Stroop-Flanker instructions file'
)
stroop_practice_path = resolve_table_file(
    str(PROJECT_ROOT / 'languages' / language / 'Stroop-Flanker' / f'Stroop_practice_trials_{language.lower()}'),
    file_label='Stroop practice trials file'
)
stroop_stim_path = resolve_table_file(
    str(PROJECT_ROOT / 'languages' / language / 'Stroop-Flanker' / f'StroopStim_{language.lower()}'),
    file_label='Stroop stimulus file'
)
flanker_stim_path = resolve_table_file(
    str(PROJECT_ROOT / 'languages' / language / 'Stroop-Flanker' / f'FlankerStim_{language.lower()}'),
    file_label='Flanker stimulus file'
)

instructions_df = load_table_file(instructions_path, index_col='screen')

welcome_text = instructions_df.loc['Welcome_text', language]
welcome_text = normalize_instruction_text(welcome_text)
welcome_text_raw = welcome_text

stroop_instructions = instructions_df.loc['stroop_instructions', language]
stroop_instructions = normalize_instruction_text(stroop_instructions)
stroop_instructions_raw = stroop_instructions

flanker_instructions = instructions_df.loc['flanker_instructions', language]
flanker_instructions = normalize_instruction_text(flanker_instructions)
flanker_instructions_raw = flanker_instructions

done_text = instructions_df.loc['done_text', language]
done_text = normalize_instruction_text(done_text)
done_text_raw = done_text

start_warning_text = instructions_df.loc['start_warning_text', language]
start_warning_text = normalize_instruction_text(start_warning_text)
start_warning_text_raw = start_warning_text

Goodbyetext = instructions_df.loc['Goodbyetext', language]
Goodbyetext = normalize_instruction_text(Goodbyetext)
goodbye_text_raw = Goodbyetext

if is_rtl and not HAS_RTL_SUPPORT:
    raise ImportError(
        "RTL text rendering requires 'arabic_reshaper' and 'python-bidi'. "
        "Please install both packages in this PsychoPy environment."
    )


# Function to get the correct_key for a given color
def get_correct_key_for_color(df, color):
    color_rows = df[df['color'] == color]
    if color_rows['correct_key'].nunique() == 1:
        return color_rows['correct_key'].iloc[0]
    else:
        raise ValueError(f"Not all 'correct_key' values are the same for color '{color}'.")


stroop_stimulus = load_table_file(stroop_practice_path)
stroop_blue_key = get_correct_key_for_color(stroop_stimulus, 'blue')
stroop_yellow_key = get_correct_key_for_color(stroop_stimulus, 'yellow')
stroop_red_key = get_correct_key_for_color(stroop_stimulus, 'red')
# Accept both Space and Return aliases across platforms.
CONTINUE_KEYS = tuple(expand_key_list('space', 'return'))
LEFT_RIGHT_KEYS = expand_key_list('left', 'right')
STROOP_RESPONSE_KEYS = expand_key_list(stroop_blue_key, stroop_red_key, stroop_yellow_key)

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name='Stroop_Flanker', version='',
                                 extraInfo=expInfo, runtimeInfo=None,
                                 # originPath='/Users/cui/Documents/uzh/PhD/Projects/MeRID/Psychometric_Tests/stroop-simon-german/CognControl_lastrun.py',
                                 savePickle=True, saveWideText=True,
                                 dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.ERROR)  # keep console output clean for participants

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

def detect_fullscreen_size(default_size=(1440, 900)):
    if pyglet is None:
        return list(default_size)
    try:
        screen = pyglet.canvas.get_display().get_default_screen()
        return [int(screen.width), int(screen.height)]
    except Exception:
        return list(default_size)


# Setup the Window
fullscreen_size = detect_fullscreen_size()
win = visual.Window(
    size=fullscreen_size, fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')
    
# Warm up the window on Windows / some backends before first real screen
startup_text = visual.TextStim(
    win=win,
    text='',
    color='black',
    pos=(0, 0),
    height=0.05,
    units='norm'
)

for i in range(3):
    startup_text.draw()
    win.flip()
    core.wait(0.2)

event.clearEvents(eventType='keyboard')

# Avoid runtime frame-rate probing to reduce startup warnings on macOS.
expInfo['frameRate'] = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()
try:
    event.globalKeys.clear()
    event.globalKeys.add(key='escape', func=core.quit, name='global_escape_quit')
except Exception as exc:
    logging.warning(f"Could not register global Escape handler: {exc}")

# Initialize components for Routine "WelcomeScreen"
WelcomeScreenClock = core.Clock()
Welcome_text = visual.TextStim(win=win, name='Welcome_text',
                               text='' if is_rtl else welcome_text_raw,
                               font=display_font,
                               pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0,
                               color='black', colorSpace='rgb', opacity=None,
                               languageStyle=language_style,
                               depth=0.0);
Welcome_resp = keyboard.Keyboard()

# Initialize components for Routine "StroopInstructions"
StroopInstructionsClock = core.Clock()
stroop_instructions = visual.TextStim(win=win, name='stroop_instructions',
                                      text='' if is_rtl else stroop_instructions_raw,
                                      font=display_font,
                                      pos=(0, 0), height=0.035, wrapWidth=1.5, ori=0.0,
                                      color='black', colorSpace='rgb', opacity=None,
                                      languageStyle=language_style,
                                      depth=0.0, );
stroop_instruction_key = keyboard.Keyboard()

# Initialize components for Routine "Blank500"
Blank500Clock = core.Clock()
blank = visual.TextStim(win=win, name='blank',
                        text='\n\n',
                        font='Open Sans',
                        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                        color='white', colorSpace='rgb', opacity=None,
                        languageStyle=language_style,
                        depth=0.0);

# Initialize components for Routine "FixationCross"
FixationCrossClock = core.Clock()
fix_cross = visual.TextStim(win=win, name='fix_cross',
                            text='+',
                            font='Courier New',
                            pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                            color='white', colorSpace='rgb', opacity=None,
                            languageStyle=language_style,
                            depth=0.0);

# Initialize components for Routine "StroopPractice"
StroopPracticeClock = core.Clock()
stroop_practice_word = visual.TextStim(win=win, name='stroop_practice_word',
                                       text='',
                                       font=display_font,
                                       pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                       color='white', colorSpace='rgb', opacity=None,
                                       languageStyle=language_style,
                                       depth=0.0);
stroop_practice_key = keyboard.Keyboard()

# Initialize components for Routine "stroop_practice_feedback"
stroop_practice_feedbackClock = core.Clock()
stroop_feedback_text = visual.TextStim(win=win, name='stroop_feedback_text',
                                       text='',
                                       font='Arial Unicode MS',
                                       pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                       color='white', colorSpace='rgb', opacity=None,
                                       languageStyle=language_style,
                                       depth=-1.0);

# Initialize components for Routine "StartWarning"
StartWarningClock = core.Clock()
start_warning_text = visual.TextStim(win=win, name='start_warning_text',
                                     text='' if is_rtl else start_warning_text_raw,
                                     font=display_font,
                                     pos=(0, 0), height=0.035, wrapWidth=1.5, ori=0.0,
                                     color='black', colorSpace='rgb', opacity=None,
                                     languageStyle=language_style,
                                     depth=0.0);

# Initialize components for Routine "StroopTrials"
StroopTrialsClock = core.Clock()
stroop_word = visual.TextStim(win=win, name='stroop_word',
                              text='',
                              font=display_font,
                              pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                              color='white', colorSpace='rgb', opacity=None,
                              languageStyle=language_style,
                              depth=0.0);
stroop_key = keyboard.Keyboard()

# Initialize components for Routine "Done"
DoneClock = core.Clock()
done_text = visual.TextStim(win=win, name='done_text',
                            text='' if is_rtl else done_text_raw,
                            font=display_font,
                            pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0,
                            color='black', colorSpace='rgb', opacity=None,
                            languageStyle=language_style,
                            depth=0.0);
done_key = keyboard.Keyboard()

# Initialize components for Routine "FlankerInstruction"
FlankerInstructionClock = core.Clock()
Flanker_instructions = visual.TextStim(win=win, name='Flanker_instructions',
                                       text='' if is_rtl else flanker_instructions_raw,
                                       font=display_font,
                                       pos=(0, 0), height=0.035, wrapWidth=1.5, ori=0.0,
                                       color='black', colorSpace='rgb', opacity=None,
                                       languageStyle=language_style,
                                       depth=0.0
                                       );
Flanker_instruction_key = keyboard.Keyboard()

# Initialize components for Routine "FlankerPractice"
FlankerPracticeClock = core.Clock()
Flanker_practice_arrows = visual.TextStim(win=win, name='Flanker_practice_arrows',
                                          text='',
                                          font='Courier New',
                                          pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                          color='white', colorSpace='rgb', opacity=None,
                                          languageStyle=language_style,
                                          depth=0.0);
Flanker_practice_key = keyboard.Keyboard()

# Initialize components for Routine "flanker_practice_feedback"
Flanker_practice_feedbackClock = core.Clock()
Flanker_feedback_text = visual.TextStim(win=win, name='flanker_feedback_text',
                                        text='',
                                        font='Arial Unicode MS',
                                        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                        color='white', colorSpace='rgb', opacity=None,
                                        languageStyle=language_style,
                                        depth=-1.0);

# Initialize components for Routine "FlankerTrials"
FlankerTrialsClock = core.Clock()
Flanker_arrows = visual.TextStim(win=win, name='Flanker_arrows',
                                 text='',
                                 font='Courier New',
                                 pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                 color='white', colorSpace='rgb', opacity=None,
                                 languageStyle=language_style,
                                 depth=0.0);
Flanker_key = keyboard.Keyboard()

# Initialize components for Routine "GoodbyeScreen"
GoodbyeScreenClock = core.Clock()
Goodbyetext = visual.TextStim(win=win, name='Goodbyetext',
                              text='' if is_rtl else goodbye_text_raw,
                              font=display_font,
                              pos=(0, 0), height=0.05, wrapWidth=1.5, ori=0.0,
                              color='black', colorSpace='rgb', opacity=None,
                              languageStyle=language_style,
                              depth=0.0);
key_goodbye = keyboard.Keyboard()

if is_rtl:
    rtl_font_path = pick_rtl_render_font_path()
    logging.warning(f"Resolved RTL font path: {rtl_font_path}")
    print(f"Resolved RTL font path: {rtl_font_path}", flush=True)
    Welcome_text = convert_text_screen_to_image_stim(
        Welcome_text, "welcome_text.png", rtl_font_path, rendered_text_dir, text_override=welcome_text_raw
    )
    stroop_instructions = convert_text_screen_to_image_stim(
        stroop_instructions, "stroop_instructions.png", rtl_font_path, rendered_text_dir, text_override=stroop_instructions_raw
    )
    start_warning_text = convert_text_screen_to_image_stim(
        start_warning_text, "start_warning_text.png", rtl_font_path, rendered_text_dir, text_override=start_warning_text_raw
    )
    done_text = convert_text_screen_to_image_stim(
        done_text, "done_text.png", rtl_font_path, rendered_text_dir, text_override=done_text_raw
    )
    Flanker_instructions = convert_text_screen_to_image_stim(
        Flanker_instructions, "flanker_instructions.png", rtl_font_path, rendered_text_dir, text_override=flanker_instructions_raw
    )
    Goodbyetext = convert_text_screen_to_image_stim(
        Goodbyetext, "goodbye_text.png", rtl_font_path, rendered_text_dir, text_override=goodbye_text_raw
    )

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "WelcomeScreen"-------
continueRoutine = True
# update component parameters for each repeat
Welcome_resp.keys = []
Welcome_resp.rt = []
_Welcome_resp_allKeys = []
# keep track of which components have finished
WelcomeScreenComponents = [Welcome_text, Welcome_resp]
for thisComponent in WelcomeScreenComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
WelcomeScreenClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "WelcomeScreen"-------
while continueRoutine:
    # get current time
    t = WelcomeScreenClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=WelcomeScreenClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *Welcome_text* updates
    if Welcome_text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        Welcome_text.frameNStart = frameN  # exact frame index
        Welcome_text.tStart = t  # local t and not account for scr refresh
        Welcome_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Welcome_text, 'tStartRefresh')  # time at next scr refresh
        Welcome_text.setAutoDraw(True)

    # *Welcome_resp* updates
    waitOnFlip = False
    if Welcome_resp.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        Welcome_resp.frameNStart = frameN  # exact frame index
        Welcome_resp.tStart = t  # local t and not account for scr refresh
        Welcome_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Welcome_resp, 'tStartRefresh')  # time at next scr refresh
        Welcome_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(Welcome_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(Welcome_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        win.callOnFlip(event.clearEvents, eventType='keyboard')  # clear event fallback buffer
    if Welcome_resp.status == STARTED and not waitOnFlip:
        theseKeys = safe_keyboard_get_keys(Welcome_resp)
        matched_key = get_first_matching_keypress(theseKeys, CONTINUE_KEYS)
        fallback_keys = safe_event_get_keys(CONTINUE_KEYS)
        matched_fallback_key = get_first_matching_keyname(fallback_keys, CONTINUE_KEYS)
        if matched_key:
            _Welcome_resp_allKeys.append(matched_key)
        elif matched_fallback_key:
            Welcome_resp.keys = normalize_key_name(matched_fallback_key)
            Welcome_resp.rt = Welcome_resp.clock.getTime()
            continueRoutine = False
        if len(_Welcome_resp_allKeys):
            Welcome_resp.keys = normalize_key_name(_Welcome_resp_allKeys[-1].name)
            Welcome_resp.rt = _Welcome_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False

    # check for quit (typically the Esc key)
    if endExpNow or escape_pressed(defaultKeyboard):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in WelcomeScreenComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "WelcomeScreen"-------
for thisComponent in WelcomeScreenComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('Welcome_text.started', Welcome_text.tStartRefresh)
thisExp.addData('Welcome_text.stopped', Welcome_text.tStopRefresh)
# check responses
if Welcome_resp.keys in ['', [], None]:  # No response was made
    Welcome_resp.keys = None
thisExp.addData('Welcome_resp.keys', Welcome_resp.keys)
if Welcome_resp.keys != None:  # we had a response
    thisExp.addData('Welcome_resp.rt', Welcome_resp.rt)
thisExp.addData('Welcome_resp.started', Welcome_resp.tStartRefresh)
thisExp.addData('Welcome_resp.stopped', Welcome_resp.tStopRefresh)
thisExp.nextEntry()
# the Routine "WelcomeScreen" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "StroopInstructions"-------
continueRoutine = True
# update component parameters for each repeat
stroop_instruction_key.keys = []
stroop_instruction_key.rt = []
_stroop_instruction_key_allKeys = []
# keep track of which components have finished
StroopInstructionsComponents = [stroop_instructions, stroop_instruction_key]
for thisComponent in StroopInstructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
StroopInstructionsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "StroopInstructions"-------
while continueRoutine:
    # get current time
    t = StroopInstructionsClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=StroopInstructionsClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *stroop_instructions* updates
    if stroop_instructions.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        stroop_instructions.frameNStart = frameN  # exact frame index
        stroop_instructions.tStart = t  # local t and not account for scr refresh
        stroop_instructions.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(stroop_instructions, 'tStartRefresh')  # time at next scr refresh
        stroop_instructions.setAutoDraw(True)

    # *stroop_instruction_key* updates
    waitOnFlip = False
    if stroop_instruction_key.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        stroop_instruction_key.frameNStart = frameN  # exact frame index
        stroop_instruction_key.tStart = t  # local t and not account for scr refresh
        stroop_instruction_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(stroop_instruction_key, 'tStartRefresh')  # time at next scr refresh
        stroop_instruction_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(stroop_instruction_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(stroop_instruction_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        win.callOnFlip(event.clearEvents, eventType='keyboard')  # clear event fallback buffer
    if stroop_instruction_key.status == STARTED and not waitOnFlip:
        theseKeys = safe_keyboard_get_keys(stroop_instruction_key)
        matched_key = get_first_matching_keypress(theseKeys, CONTINUE_KEYS)
        fallback_keys = safe_event_get_keys(CONTINUE_KEYS)
        matched_fallback_key = get_first_matching_keyname(fallback_keys, CONTINUE_KEYS)
        if matched_key:
            _stroop_instruction_key_allKeys.append(matched_key)
        elif matched_fallback_key:
            stroop_instruction_key.keys = normalize_key_name(matched_fallback_key)
            stroop_instruction_key.rt = stroop_instruction_key.clock.getTime()
            continueRoutine = False
        if len(_stroop_instruction_key_allKeys):
            stroop_instruction_key.keys = normalize_key_name(_stroop_instruction_key_allKeys[-1].name)
            stroop_instruction_key.rt = _stroop_instruction_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False

    # check for quit (typically the Esc key)
    if endExpNow or escape_pressed(defaultKeyboard):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in StroopInstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "StroopInstructions"-------
for thisComponent in StroopInstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('stroop_instructions.started', stroop_instructions.tStartRefresh)
thisExp.addData('stroop_instructions.stopped', stroop_instructions.tStopRefresh)
# check responses
if stroop_instruction_key.keys in ['', [], None]:  # No response was made
    stroop_instruction_key.keys = None
thisExp.addData('stroop_instruction_key.keys', stroop_instruction_key.keys)
if stroop_instruction_key.keys != None:  # we had a response
    thisExp.addData('stroop_instruction_key.rt', stroop_instruction_key.rt)
thisExp.addData('stroop_instruction_key.started', stroop_instruction_key.tStartRefresh)
thisExp.addData('stroop_instruction_key.stopped', stroop_instruction_key.tStopRefresh)
thisExp.nextEntry()
# the Routine "StroopInstructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Blank500"-------
continueRoutine = True
routineTimer.addTime(0.500000)
# update component parameters for each repeat
# keep track of which components have finished
Blank500Components = [blank]
for thisComponent in Blank500Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Blank500Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Blank500"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = Blank500Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Blank500Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *blank* updates
    if blank.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        blank.frameNStart = frameN  # exact frame index
        blank.tStart = t  # local t and not account for scr refresh
        blank.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(blank, 'tStartRefresh')  # time at next scr refresh
        blank.setAutoDraw(True)
    if blank.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > blank.tStartRefresh + .5 - frameTolerance:
            # keep track of stop time/frame for later
            blank.tStop = t  # not accounting for scr refresh
            blank.frameNStop = frameN  # exact frame index
            win.timeOnFlip(blank, 'tStopRefresh')  # time at next scr refresh
            blank.setAutoDraw(False)

    # check for quit (typically the Esc key)
    if endExpNow or escape_pressed(defaultKeyboard):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Blank500Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Blank500"-------
for thisComponent in Blank500Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('blank.started', blank.tStartRefresh)
thisExp.addData('blank.stopped', blank.tStopRefresh)

# set up handler to look after randomisation of conditions etc
stroop_practice_trial = data.TrialHandler(nReps=1.0, method='random',
                                          extraInfo=expInfo, originPath=-1,
                                          trialList=data.importConditions(
                                              stroop_practice_path),
                                          seed=None, name='stroop_practice_trial')
thisExp.addLoop(stroop_practice_trial)  # add the loop to the experiment
thisStroop_practice_trial = stroop_practice_trial.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisStroop_practice_trial.rgb)
if thisStroop_practice_trial != None:
    for paramName in thisStroop_practice_trial:
        exec('{} = thisStroop_practice_trial[paramName]'.format(paramName))

for thisStroop_practice_trial in stroop_practice_trial:
    currentLoop = stroop_practice_trial
    # abbreviate parameter names if possible (e.g. rgb = thisStroop_practice_trial.rgb)
    if thisStroop_practice_trial != None:
        for paramName in thisStroop_practice_trial:
            exec('{} = thisStroop_practice_trial[paramName]'.format(paramName))

    # ------Prepare to start Routine "FixationCross"-------
    continueRoutine = True
    routineTimer.addTime(0.350000)
    # update component parameters for each repeat
    # keep track of which components have finished
    FixationCrossComponents = [fix_cross]
    for thisComponent in FixationCrossComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    FixationCrossClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "FixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = FixationCrossClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=FixationCrossClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *fix_cross* updates
        if fix_cross.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            fix_cross.frameNStart = frameN  # exact frame index
            fix_cross.tStart = t  # local t and not account for scr refresh
            fix_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_cross, 'tStartRefresh')  # time at next scr refresh
            fix_cross.setAutoDraw(True)
        if fix_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix_cross.tStartRefresh + .35 - frameTolerance:
                # keep track of stop time/frame for later
                fix_cross.tStop = t  # not accounting for scr refresh
                fix_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fix_cross, 'tStopRefresh')  # time at next scr refresh
                fix_cross.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or escape_pressed(defaultKeyboard):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in FixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "FixationCross"-------
    for thisComponent in FixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    stroop_practice_trial.addData('fix_cross.started', fix_cross.tStartRefresh)
    stroop_practice_trial.addData('fix_cross.stopped', fix_cross.tStopRefresh)

    # ------Prepare to start Routine "StroopPractice"-------
    continueRoutine = True
    # update component parameters for each repeat
    stroop_practice_word.setColor(color, colorSpace='rgb')
    set_text_with_rtl_fallback(stroop_practice_word, word)
    stroop_practice_key.keys = []
    stroop_practice_key.rt = []
    _stroop_practice_key_allKeys = []
    # keep track of which components have finished
    StroopPracticeComponents = [stroop_practice_word, stroop_practice_key]
    for thisComponent in StroopPracticeComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    StroopPracticeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "StroopPractice"-------
    while continueRoutine:
        # get current time
        t = StroopPracticeClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=StroopPracticeClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *stroop_practice_word* updates
        if stroop_practice_word.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            stroop_practice_word.frameNStart = frameN  # exact frame index
            stroop_practice_word.tStart = t  # local t and not account for scr refresh
            stroop_practice_word.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stroop_practice_word, 'tStartRefresh')  # time at next scr refresh
            stroop_practice_word.setAutoDraw(True)

        # *stroop_practice_key* updates
        waitOnFlip = False
        if stroop_practice_key.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            stroop_practice_key.frameNStart = frameN  # exact frame index
            stroop_practice_key.tStart = t  # local t and not account for scr refresh
            stroop_practice_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stroop_practice_key, 'tStartRefresh')  # time at next scr refresh
            stroop_practice_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(stroop_practice_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(stroop_practice_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
            win.callOnFlip(event.clearEvents, eventType='keyboard')  # clear event fallback buffer
        if stroop_practice_key.status == STARTED and not waitOnFlip:
            theseKeys = safe_keyboard_get_keys(stroop_practice_key)
            matched_key = get_first_matching_keypress(theseKeys, STROOP_RESPONSE_KEYS)
            fallback_keys = safe_event_get_keys()
            matched_fallback_key = get_first_matching_keyname(fallback_keys, STROOP_RESPONSE_KEYS)
            if matched_key:
                _stroop_practice_key_allKeys.append(matched_key)
            elif matched_fallback_key:
                stroop_practice_key.keys = matched_fallback_key
                stroop_practice_key.rt = stroop_practice_key.clock.getTime()
                stroop_practice_key.corr = 1 if is_key_match(stroop_practice_key.keys, correct_key) else 0
                continueRoutine = False
            if len(_stroop_practice_key_allKeys):
                stroop_practice_key.keys = _stroop_practice_key_allKeys[-1].name  # just the last key pressed
                stroop_practice_key.rt = _stroop_practice_key_allKeys[-1].rt
                # was this correct?
                if is_key_match(stroop_practice_key.keys, correct_key):
                    stroop_practice_key.corr = 1
                else:
                    stroop_practice_key.corr = 0
                # a response ends the routine
                continueRoutine = False

        # check for quit (typically the Esc key)
        if endExpNow or escape_pressed(defaultKeyboard):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in StroopPracticeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "StroopPractice"-------
    for thisComponent in StroopPracticeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    stroop_practice_trial.addData('stroop_practice_word.started', stroop_practice_word.tStartRefresh)
    stroop_practice_trial.addData('stroop_practice_word.stopped', stroop_practice_word.tStopRefresh)
    # check responses
    if stroop_practice_key.keys in ['', [], None]:  # No response was made
        stroop_practice_key.keys = None
        # was no response the correct answer?!
        if str(correct_key).lower() == 'none':
            stroop_practice_key.corr = 1;  # correct non-response
        else:
            stroop_practice_key.corr = 0;  # failed to respond (incorrectly)
    # store data for stroop_practice_trial (TrialHandler)
    stroop_practice_trial.addData('stroop_practice_key.keys', stroop_practice_key.keys)
    stroop_practice_trial.addData('stroop_practice_key.corr', stroop_practice_key.corr)
    if stroop_practice_key.keys != None:  # we had a response
        stroop_practice_trial.addData('stroop_practice_key.rt', stroop_practice_key.rt)
    stroop_practice_trial.addData('stroop_practice_key.started', stroop_practice_key.tStartRefresh)
    stroop_practice_trial.addData('stroop_practice_key.stopped', stroop_practice_key.tStopRefresh)
    # the Routine "StroopPractice" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ------Prepare to start Routine "stroop_practice_feedback"-------
    continueRoutine = True
    routineTimer.addTime(1.000000)
    # update component parameters for each repeat
    if (stroop_practice_key.corr == 1):
        feedback_text = "✓"
    elif (stroop_practice_key.corr == 0):
        feedback_text = "x"
    stroop_feedback_text.setText(feedback_text)
    # keep track of which components have finished
    stroop_practice_feedbackComponents = [stroop_feedback_text]
    for thisComponent in stroop_practice_feedbackComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    stroop_practice_feedbackClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "stroop_practice_feedback"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = stroop_practice_feedbackClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=stroop_practice_feedbackClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *stroop_feedback_text* updates
        if stroop_feedback_text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            stroop_feedback_text.frameNStart = frameN  # exact frame index
            stroop_feedback_text.tStart = t  # local t and not account for scr refresh
            stroop_feedback_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stroop_feedback_text, 'tStartRefresh')  # time at next scr refresh
            stroop_feedback_text.setAutoDraw(True)
        if stroop_feedback_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > stroop_feedback_text.tStartRefresh + 1.0 - frameTolerance:
                # keep track of stop time/frame for later
                stroop_feedback_text.tStop = t  # not accounting for scr refresh
                stroop_feedback_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(stroop_feedback_text, 'tStopRefresh')  # time at next scr refresh
                stroop_feedback_text.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or escape_pressed(defaultKeyboard):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in stroop_practice_feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "stroop_practice_feedback"-------
    for thisComponent in stroop_practice_feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    stroop_practice_trial.addData('stroop_feedback_text.started', stroop_feedback_text.tStartRefresh)
    stroop_practice_trial.addData('stroop_feedback_text.stopped', stroop_feedback_text.tStopRefresh)
    thisExp.nextEntry()

# completed 1.0 repeats of 'stroop_practice_trial'


# ------Prepare to start Routine "StartWarning"-------
continueRoutine = True
routineTimer.addTime(6.000000)
# update component parameters for each repeat
# keep track of which components have finished
StartWarningComponents = [start_warning_text]
for thisComponent in StartWarningComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
StartWarningClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "StartWarning"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = StartWarningClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=StartWarningClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *start_warning_text* updates
    if start_warning_text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        start_warning_text.frameNStart = frameN  # exact frame index
        start_warning_text.tStart = t  # local t and not account for scr refresh
        start_warning_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_warning_text, 'tStartRefresh')  # time at next scr refresh
        start_warning_text.setAutoDraw(True)
    if start_warning_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > start_warning_text.tStartRefresh + 6.0 - frameTolerance:
            # keep track of stop time/frame for later
            start_warning_text.tStop = t  # not accounting for scr refresh
            start_warning_text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(start_warning_text, 'tStopRefresh')  # time at next scr refresh
            start_warning_text.setAutoDraw(False)

    # check for quit (typically the Esc key)
    if endExpNow or escape_pressed(defaultKeyboard):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in StartWarningComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "StartWarning"-------
for thisComponent in StartWarningComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('start_warning_text.started', start_warning_text.tStartRefresh)
thisExp.addData('start_warning_text.stopped', start_warning_text.tStopRefresh)

# set up handler to look after randomisation of conditions etc
Stroop_trials = data.TrialHandler(nReps=4.0, method='random',
                                  extraInfo=expInfo, originPath=-1,
                                  trialList=data.importConditions(
                                      stroop_stim_path),
                                  seed=None, name='Stroop_trials')
thisExp.addLoop(Stroop_trials)  # add the loop to the experiment
thisStroop_trial = Stroop_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisStroop_trial.rgb)
if thisStroop_trial != None:
    for paramName in thisStroop_trial:
        exec('{} = thisStroop_trial[paramName]'.format(paramName))

for thisStroop_trial in Stroop_trials:
    currentLoop = Stroop_trials
    # abbreviate parameter names if possible (e.g. rgb = thisStroop_trial.rgb)
    if thisStroop_trial != None:
        for paramName in thisStroop_trial:
            exec('{} = thisStroop_trial[paramName]'.format(paramName))

    # ------Prepare to start Routine "FixationCross"-------
    continueRoutine = True
    routineTimer.addTime(0.350000)
    # update component parameters for each repeat
    # keep track of which components have finished
    FixationCrossComponents = [fix_cross]
    for thisComponent in FixationCrossComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    FixationCrossClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "FixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = FixationCrossClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=FixationCrossClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *fix_cross* updates
        if fix_cross.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            fix_cross.frameNStart = frameN  # exact frame index
            fix_cross.tStart = t  # local t and not account for scr refresh
            fix_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_cross, 'tStartRefresh')  # time at next scr refresh
            fix_cross.setAutoDraw(True)
        if fix_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix_cross.tStartRefresh + .35 - frameTolerance:
                # keep track of stop time/frame for later
                fix_cross.tStop = t  # not accounting for scr refresh
                fix_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fix_cross, 'tStopRefresh')  # time at next scr refresh
                fix_cross.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or escape_pressed(defaultKeyboard):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in FixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "FixationCross"-------
    for thisComponent in FixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Stroop_trials.addData('fix_cross.started', fix_cross.tStartRefresh)
    Stroop_trials.addData('fix_cross.stopped', fix_cross.tStopRefresh)

    # ------Prepare to start Routine "StroopTrials"-------
    continueRoutine = True
    # update component parameters for each repeat
    stroop_word.setColor(color, colorSpace='rgb')
    set_text_with_rtl_fallback(stroop_word, word)
    stroop_key.keys = []
    stroop_key.rt = []
    _stroop_key_allKeys = []
    # keep track of which components have finished
    StroopTrialsComponents = [stroop_word, stroop_key]
    for thisComponent in StroopTrialsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    StroopTrialsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "StroopTrials"-------
    while continueRoutine:
        # get current time
        t = StroopTrialsClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=StroopTrialsClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *stroop_word* updates
        if stroop_word.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            stroop_word.frameNStart = frameN  # exact frame index
            stroop_word.tStart = t  # local t and not account for scr refresh
            stroop_word.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stroop_word, 'tStartRefresh')  # time at next scr refresh
            stroop_word.setAutoDraw(True)

        # *stroop_key* updates
        waitOnFlip = False
        if stroop_key.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            stroop_key.frameNStart = frameN  # exact frame index
            stroop_key.tStart = t  # local t and not account for scr refresh
            stroop_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stroop_key, 'tStartRefresh')  # time at next scr refresh
            stroop_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(stroop_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(stroop_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
            win.callOnFlip(event.clearEvents, eventType='keyboard')  # clear event fallback buffer
        if stroop_key.status == STARTED and not waitOnFlip:
            theseKeys = safe_keyboard_get_keys(stroop_key)
            matched_key = get_first_matching_keypress(theseKeys, STROOP_RESPONSE_KEYS)
            fallback_keys = safe_event_get_keys()
            matched_fallback_key = get_first_matching_keyname(fallback_keys, STROOP_RESPONSE_KEYS)
            if matched_key:
                _stroop_key_allKeys.append(matched_key)
            elif matched_fallback_key:
                stroop_key.keys = matched_fallback_key
                stroop_key.rt = stroop_key.clock.getTime()
                stroop_key.corr = 1 if is_key_match(stroop_key.keys, correct_key) else 0
                continueRoutine = False
            if len(_stroop_key_allKeys):
                stroop_key.keys = _stroop_key_allKeys[-1].name  # just the last key pressed
                stroop_key.rt = _stroop_key_allKeys[-1].rt
                # was this correct?
                if is_key_match(stroop_key.keys, correct_key):
                    stroop_key.corr = 1
                else:
                    stroop_key.corr = 0
                # a response ends the routine
                continueRoutine = False

        # check for quit (typically the Esc key)
        if endExpNow or escape_pressed(defaultKeyboard):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in StroopTrialsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "StroopTrials"-------
    for thisComponent in StroopTrialsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Stroop_trials.addData('stroop_word.started', stroop_word.tStartRefresh)
    Stroop_trials.addData('stroop_word.stopped', stroop_word.tStopRefresh)
    # check responses
    if stroop_key.keys in ['', [], None]:  # No response was made
        stroop_key.keys = None
        # was no response the correct answer?!
        if str(correct_key).lower() == 'none':
            stroop_key.corr = 1;  # correct non-response
        else:
            stroop_key.corr = 0;  # failed to respond (incorrectly)
    # store data for Stroop_trials (TrialHandler)
    Stroop_trials.addData('stroop_key.keys', stroop_key.keys)
    Stroop_trials.addData('stroop_key.corr', stroop_key.corr)
    if stroop_key.keys != None:  # we had a response
        Stroop_trials.addData('stroop_key.rt', stroop_key.rt)
    Stroop_trials.addData('stroop_key.started', stroop_key.tStartRefresh)
    Stroop_trials.addData('stroop_key.stopped', stroop_key.tStopRefresh)
    # the Routine "StroopTrials" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()

# completed 4.0 repeats of 'Stroop_trials'


# ------Prepare to start Routine "Done"-------
continueRoutine = True
# update component parameters for each repeat
done_key.keys = []
done_key.rt = []
_done_key_allKeys = []
# keep track of which components have finished
DoneComponents = [done_text, done_key]
for thisComponent in DoneComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
DoneClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Done"-------
while continueRoutine:
    # get current time
    t = DoneClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=DoneClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *done_text* updates
    if done_text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        done_text.frameNStart = frameN  # exact frame index
        done_text.tStart = t  # local t and not account for scr refresh
        done_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(done_text, 'tStartRefresh')  # time at next scr refresh
        done_text.setAutoDraw(True)

    # *done_key* updates
    waitOnFlip = False
    if done_key.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        done_key.frameNStart = frameN  # exact frame index
        done_key.tStart = t  # local t and not account for scr refresh
        done_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(done_key, 'tStartRefresh')  # time at next scr refresh
        done_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(done_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(done_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        win.callOnFlip(event.clearEvents, eventType='keyboard')  # clear event fallback buffer
    if done_key.status == STARTED and not waitOnFlip:
        theseKeys = safe_keyboard_get_keys(done_key)
        matched_key = get_first_matching_keypress(theseKeys, CONTINUE_KEYS)
        fallback_keys = safe_event_get_keys(CONTINUE_KEYS)
        matched_fallback_key = get_first_matching_keyname(fallback_keys, CONTINUE_KEYS)
        if matched_key:
            _done_key_allKeys.append(matched_key)
        elif matched_fallback_key:
            done_key.keys = normalize_key_name(matched_fallback_key)
            done_key.rt = done_key.clock.getTime()
            continueRoutine = False
        if len(_done_key_allKeys):
            done_key.keys = normalize_key_name(_done_key_allKeys[-1].name)
            done_key.rt = _done_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False

    # check for quit (typically the Esc key)
    if endExpNow or escape_pressed(defaultKeyboard):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in DoneComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Done"-------
for thisComponent in DoneComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('done_text.started', done_text.tStartRefresh)
thisExp.addData('done_text.stopped', done_text.tStopRefresh)
# check responses
if done_key.keys in ['', [], None]:  # No response was made
    done_key.keys = None
thisExp.addData('done_key.keys', done_key.keys)
if done_key.keys != None:  # we had a response
    thisExp.addData('done_key.rt', done_key.rt)
thisExp.addData('done_key.started', done_key.tStartRefresh)
thisExp.addData('done_key.stopped', done_key.tStopRefresh)
thisExp.nextEntry()
# the Routine "Done" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "FlankerInstruction"-------
continueRoutine = True
# update component parameters for each repeat
Flanker_instruction_key.keys = []
Flanker_instruction_key.rt = []
_Flanker_instruction_key_allKeys = []
# keep track of which components have finished
FlankerInstructionComponents = [Flanker_instructions, Flanker_instruction_key]
for thisComponent in FlankerInstructionComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
FlankerInstructionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "FlankerInstruction"-------
while continueRoutine:
    # get current time
    t = FlankerInstructionClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=FlankerInstructionClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *Flanker_instructions* updates
    if Flanker_instructions.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        Flanker_instructions.frameNStart = frameN  # exact frame index
        Flanker_instructions.tStart = t  # local t and not account for scr refresh
        Flanker_instructions.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Flanker_instructions, 'tStartRefresh')  # time at next scr refresh
        Flanker_instructions.setAutoDraw(True)

    # *Flanker_instruction_key* updates
    waitOnFlip = False
    if Flanker_instruction_key.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        Flanker_instruction_key.frameNStart = frameN  # exact frame index
        Flanker_instruction_key.tStart = t  # local t and not account for scr refresh
        Flanker_instruction_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Flanker_instruction_key, 'tStartRefresh')  # time at next scr refresh
        Flanker_instruction_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(Flanker_instruction_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(Flanker_instruction_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        win.callOnFlip(event.clearEvents, eventType='keyboard')  # clear event fallback buffer
    if Flanker_instruction_key.status == STARTED and not waitOnFlip:
        theseKeys = safe_keyboard_get_keys(Flanker_instruction_key)
        matched_key = get_first_matching_keypress(theseKeys, CONTINUE_KEYS)
        fallback_keys = safe_event_get_keys(CONTINUE_KEYS)
        matched_fallback_key = get_first_matching_keyname(fallback_keys, CONTINUE_KEYS)
        if matched_key:
            _Flanker_instruction_key_allKeys.append(matched_key)
        elif matched_fallback_key:
            Flanker_instruction_key.keys = normalize_key_name(matched_fallback_key)
            Flanker_instruction_key.rt = Flanker_instruction_key.clock.getTime()
            continueRoutine = False
        if len(_Flanker_instruction_key_allKeys):
            Flanker_instruction_key.keys = normalize_key_name(_Flanker_instruction_key_allKeys[-1].name)
            Flanker_instruction_key.rt = _Flanker_instruction_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False

    # check for quit (typically the Esc key)
    if endExpNow or escape_pressed(defaultKeyboard):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in FlankerInstructionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "FlankerInstruction"-------
for thisComponent in FlankerInstructionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('Flanker_instructions.started', Flanker_instructions.tStartRefresh)
thisExp.addData('Flanker_instructions.stopped', Flanker_instructions.tStopRefresh)
# check responses
if Flanker_instruction_key.keys in ['', [], None]:  # No response was made
    Flanker_instruction_key.keys = None
thisExp.addData('Flanker_instruction_key.keys', Flanker_instruction_key.keys)
if Flanker_instruction_key.keys != None:  # we had a response
    thisExp.addData('Flanker_instruction_key.rt', Flanker_instruction_key.rt)
thisExp.addData('Flanker_instruction_key.started', Flanker_instruction_key.tStartRefresh)
thisExp.addData('Flanker_instruction_key.stopped', Flanker_instruction_key.tStopRefresh)
thisExp.nextEntry()
# the Routine "FlankerInstruction" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Blank500"-------
continueRoutine = True
routineTimer.addTime(0.500000)
# update component parameters for each repeat
# keep track of which components have finished
Blank500Components = [blank]
for thisComponent in Blank500Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Blank500Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Blank500"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = Blank500Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Blank500Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *blank* updates
    if blank.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        blank.frameNStart = frameN  # exact frame index
        blank.tStart = t  # local t and not account for scr refresh
        blank.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(blank, 'tStartRefresh')  # time at next scr refresh
        blank.setAutoDraw(True)
    if blank.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > blank.tStartRefresh + .5 - frameTolerance:
            # keep track of stop time/frame for later
            blank.tStop = t  # not accounting for scr refresh
            blank.frameNStop = frameN  # exact frame index
            win.timeOnFlip(blank, 'tStopRefresh')  # time at next scr refresh
            blank.setAutoDraw(False)

    # check for quit (typically the Esc key)
    if endExpNow or escape_pressed(defaultKeyboard):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Blank500Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Blank500"-------
for thisComponent in Blank500Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('blank.started', blank.tStartRefresh)
thisExp.addData('blank.stopped', blank.tStopRefresh)

# set up handler to look after randomisation of conditions etc
Flanker_practice_trials = data.TrialHandler(nReps=2.0, method='random',
                                            extraInfo=expInfo, originPath=-1,
                                            trialList=data.importConditions(
                                                flanker_stim_path),
                                            seed=None, name='Flanker_practice_trials')
thisExp.addLoop(Flanker_practice_trials)  # add the loop to the experiment
thisFlanker_practice_trial = Flanker_practice_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisFlanker_practice_trial.rgb)
if thisFlanker_practice_trial != None:
    for paramName in thisFlanker_practice_trial:
        exec('{} = thisFlanker_practice_trial[paramName]'.format(paramName))

for thisFlanker_practice_trial in Flanker_practice_trials:
    currentLoop = Flanker_practice_trials
    # abbreviate parameter names if possible (e.g. rgb = thisFlanker_practice_trial.rgb)
    if thisFlanker_practice_trial != None:
        for paramName in thisFlanker_practice_trial:
            exec('{} = thisFlanker_practice_trial[paramName]'.format(paramName))

    # ------Prepare to start Routine "FixationCross"-------
    continueRoutine = True
    routineTimer.addTime(0.350000)
    # update component parameters for each repeat
    # keep track of which components have finished
    FixationCrossComponents = [fix_cross]
    for thisComponent in FixationCrossComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    FixationCrossClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "FixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = FixationCrossClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=FixationCrossClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *fix_cross* updates
        if fix_cross.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            fix_cross.frameNStart = frameN  # exact frame index
            fix_cross.tStart = t  # local t and not account for scr refresh
            fix_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_cross, 'tStartRefresh')  # time at next scr refresh
            fix_cross.setAutoDraw(True)
        if fix_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix_cross.tStartRefresh + .35 - frameTolerance:
                # keep track of stop time/frame for later
                fix_cross.tStop = t  # not accounting for scr refresh
                fix_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fix_cross, 'tStopRefresh')  # time at next scr refresh
                fix_cross.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or escape_pressed(defaultKeyboard):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in FixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "FixationCross"-------
    for thisComponent in FixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Flanker_practice_trials.addData('fix_cross.started', fix_cross.tStartRefresh)
    Flanker_practice_trials.addData('fix_cross.stopped', fix_cross.tStopRefresh)

    # ------Prepare to start Routine "FlankerPractice"-------
    continueRoutine = True
    # update component parameters for each repeat
    Flanker_practice_arrows.setColor(color, colorSpace='rgb')
    Flanker_practice_arrows.setText(arrow)
    Flanker_practice_key.keys = []
    Flanker_practice_key.rt = []
    _Flanker_practice_key_allKeys = []
    # keep track of which components have finished
    FlankerPracticeComponents = [Flanker_practice_arrows, Flanker_practice_key]
    for thisComponent in FlankerPracticeComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    FlankerPracticeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "FlankerPractice"-------
    while continueRoutine:
        # get current time
        t = FlankerPracticeClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=FlankerPracticeClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *Flanker_practice_arrows* updates
        if Flanker_practice_arrows.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            Flanker_practice_arrows.frameNStart = frameN  # exact frame index
            Flanker_practice_arrows.tStart = t  # local t and not account for scr refresh
            Flanker_practice_arrows.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Flanker_practice_arrows, 'tStartRefresh')  # time at next scr refresh
            Flanker_practice_arrows.setAutoDraw(True)

        # *Flanker_practice_key* updates
        waitOnFlip = False
        if Flanker_practice_key.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            Flanker_practice_key.frameNStart = frameN  # exact frame index
            Flanker_practice_key.tStart = t  # local t and not account for scr refresh
            Flanker_practice_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Flanker_practice_key, 'tStartRefresh')  # time at next scr refresh
            Flanker_practice_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(Flanker_practice_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(Flanker_practice_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
            win.callOnFlip(event.clearEvents, eventType='keyboard')  # clear event fallback buffer
        if Flanker_practice_key.status == STARTED and not waitOnFlip:
            theseKeys = safe_keyboard_get_keys(Flanker_practice_key)
            matched_key = get_first_matching_keypress(theseKeys, LEFT_RIGHT_KEYS)
            fallback_keys = safe_event_get_keys()
            matched_fallback_key = get_first_matching_keyname(fallback_keys, LEFT_RIGHT_KEYS)
            if matched_key:
                _Flanker_practice_key_allKeys.append(matched_key)
            elif matched_fallback_key:
                Flanker_practice_key.keys = matched_fallback_key
                Flanker_practice_key.rt = Flanker_practice_key.clock.getTime()
                Flanker_practice_key.corr = 1 if is_key_match(Flanker_practice_key.keys, correct_key) else 0
                continueRoutine = False
            if len(_Flanker_practice_key_allKeys):
                Flanker_practice_key.keys = _Flanker_practice_key_allKeys[-1].name  # just the last key pressed
                Flanker_practice_key.rt = _Flanker_practice_key_allKeys[-1].rt
                # was this correct?
                if is_key_match(Flanker_practice_key.keys, correct_key):
                    Flanker_practice_key.corr = 1
                else:
                    Flanker_practice_key.corr = 0
                # a response ends the routine
                continueRoutine = False

        # check for quit (typically the Esc key)
        if endExpNow or escape_pressed(defaultKeyboard):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in FlankerPracticeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "FlankerPractice"-------
    for thisComponent in FlankerPracticeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Flanker_practice_trials.addData('Flanker_practice.started', Flanker_practice_arrows.tStartRefresh)
    Flanker_practice_trials.addData('Flanker_practice.stopped', Flanker_practice_arrows.tStopRefresh)
    # check responses
    if Flanker_practice_key.keys in ['', [], None]:  # No response was made
        Flanker_practice_key.keys = None
        # was no response the correct answer?!
        if str(correct_key).lower() == 'none':
            Flanker_practice_key.corr = 1;  # correct non-response
        else:
            Flanker_practice_key.corr = 0;  # failed to respond (incorrectly)
    # store data for Flanker_practice_trials (TrialHandler)
    Flanker_practice_trials.addData('Flanker_practice_key.keys', Flanker_practice_key.keys)
    Flanker_practice_trials.addData('Flanker_practice_key.corr', Flanker_practice_key.corr)
    if Flanker_practice_key.keys != None:  # we had a response
        Flanker_practice_trials.addData('Flanker_practice_key.rt', Flanker_practice_key.rt)
    Flanker_practice_trials.addData('Flanker_practice_key.started', Flanker_practice_key.tStartRefresh)
    Flanker_practice_trials.addData('Flanker_practice_key.stopped', Flanker_practice_key.tStopRefresh)
    # the Routine "FlankerPractice" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ------Prepare to start Routine "Flanker_practice_feedback"-------
    continueRoutine = True
    routineTimer.addTime(1.000000)
    # update component parameters for each repeat
    if (Flanker_practice_key.corr == 1):
        feedback_text2 = "✓"
    elif (Flanker_practice_key.corr == 0):
        feedback_text2 = "x"
    Flanker_feedback_text.setText(feedback_text2)
    # keep track of which components have finished
    Flanker_practice_feedbackComponents = [Flanker_feedback_text]
    for thisComponent in Flanker_practice_feedbackComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Flanker_practice_feedbackClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "Flanker_practice_feedback"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Flanker_practice_feedbackClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Flanker_practice_feedbackClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *Flanker_feedback_text* updates
        if Flanker_feedback_text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            Flanker_feedback_text.frameNStart = frameN  # exact frame index
            Flanker_feedback_text.tStart = t  # local t and not account for scr refresh
            Flanker_feedback_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Flanker_feedback_text, 'tStartRefresh')  # time at next scr refresh
            Flanker_feedback_text.setAutoDraw(True)
        if Flanker_feedback_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Flanker_feedback_text.tStartRefresh + 1.0 - frameTolerance:
                # keep track of stop time/frame for later
                Flanker_feedback_text.tStop = t  # not accounting for scr refresh
                Flanker_feedback_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(Flanker_feedback_text, 'tStopRefresh')  # time at next scr refresh
                Flanker_feedback_text.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or escape_pressed(defaultKeyboard):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Flanker_practice_feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "Flanker_practice_feedback"-------
    for thisComponent in Flanker_practice_feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Flanker_practice_trials.addData('Flanker_feedback_text.started', Flanker_feedback_text.tStartRefresh)
    Flanker_practice_trials.addData('Flanker_feedback_text.stopped', Flanker_feedback_text.tStopRefresh)
    thisExp.nextEntry()

# completed 2.0 repeats of 'Flanker_practice_trials'


# ------Prepare to start Routine "StartWarning"-------
continueRoutine = True
routineTimer.addTime(6.000000)
# update component parameters for each repeat
# keep track of which components have finished
StartWarningComponents = [start_warning_text]
for thisComponent in StartWarningComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
StartWarningClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "StartWarning"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = StartWarningClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=StartWarningClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *start_warning_text* updates
    if start_warning_text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        start_warning_text.frameNStart = frameN  # exact frame index
        start_warning_text.tStart = t  # local t and not account for scr refresh
        start_warning_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_warning_text, 'tStartRefresh')  # time at next scr refresh
        start_warning_text.setAutoDraw(True)
    if start_warning_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > start_warning_text.tStartRefresh + 6.0 - frameTolerance:
            # keep track of stop time/frame for later
            start_warning_text.tStop = t  # not accounting for scr refresh
            start_warning_text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(start_warning_text, 'tStopRefresh')  # time at next scr refresh
            start_warning_text.setAutoDraw(False)

    # check for quit (typically the Esc key)
    if endExpNow or escape_pressed(defaultKeyboard):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in StartWarningComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "StartWarning"-------
for thisComponent in StartWarningComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('start_warning_text.started', start_warning_text.tStartRefresh)
thisExp.addData('start_warning_text.stopped', start_warning_text.tStopRefresh)

# set up handler to look after randomisation of conditions etc
Flanker_trials = data.TrialHandler(nReps=21.0, method='random',
                                   extraInfo=expInfo, originPath=-1,
                                   trialList=data.importConditions(
                                       flanker_stim_path),
                                   seed=None, name='Flanker_trials')
thisExp.addLoop(Flanker_trials)  # add the loop to the experiment
thisFlanker_trial = Flanker_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisFlanker_trial.rgb)
if thisFlanker_trial != None:
    for paramName in thisFlanker_trial:
        exec('{} = thisFlanker_trial[paramName]'.format(paramName))

for thisFlanker_trial in Flanker_trials:
    currentLoop = Flanker_trials
    # abbreviate parameter names if possible (e.g. rgb = thisFlanker_trial.rgb)
    if thisFlanker_trial != None:
        for paramName in thisFlanker_trial:
            exec('{} = thisFlanker_trial[paramName]'.format(paramName))

    # ------Prepare to start Routine "FixationCross"-------
    continueRoutine = True
    routineTimer.addTime(0.350000)
    # update component parameters for each repeat
    # keep track of which components have finished
    FixationCrossComponents = [fix_cross]
    for thisComponent in FixationCrossComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    FixationCrossClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "FixationCross"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = FixationCrossClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=FixationCrossClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *fix_cross* updates
        if fix_cross.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            fix_cross.frameNStart = frameN  # exact frame index
            fix_cross.tStart = t  # local t and not account for scr refresh
            fix_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_cross, 'tStartRefresh')  # time at next scr refresh
            fix_cross.setAutoDraw(True)
        if fix_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix_cross.tStartRefresh + .35 - frameTolerance:
                # keep track of stop time/frame for later
                fix_cross.tStop = t  # not accounting for scr refresh
                fix_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fix_cross, 'tStopRefresh')  # time at next scr refresh
                fix_cross.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or escape_pressed(defaultKeyboard):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in FixationCrossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "FixationCross"-------
    for thisComponent in FixationCrossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Flanker_trials.addData('fix_cross.started', fix_cross.tStartRefresh)
    Flanker_trials.addData('fix_cross.stopped', fix_cross.tStopRefresh)

    # ------Prepare to start Routine "FlankerTrials"-------
    continueRoutine = True
    # update component parameters for each repeat
    Flanker_arrows.setColor(color, colorSpace='rgb')
    Flanker_arrows.setText(arrow)
    Flanker_key.keys = []
    Flanker_key.rt = []
    _Flanker_key_allKeys = []
    # keep track of which components have finished
    FlankerTrialsComponents = [Flanker_arrows, Flanker_key]
    for thisComponent in FlankerTrialsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    FlankerTrialsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "FlankerTrials"-------
    while continueRoutine:
        # get current time
        t = FlankerTrialsClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=FlankerTrialsClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *Flanker_arrow* updates
        if Flanker_arrows.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            Flanker_arrows.frameNStart = frameN  # exact frame index
            Flanker_arrows.tStart = t  # local t and not account for scr refresh
            Flanker_arrows.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Flanker_arrows, 'tStartRefresh')  # time at next scr refresh
            Flanker_arrows.setAutoDraw(True)

        # *Flanker_key* updates
        waitOnFlip = False
        if Flanker_key.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            Flanker_key.frameNStart = frameN  # exact frame index
            Flanker_key.tStart = t  # local t and not account for scr refresh
            Flanker_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Flanker_key, 'tStartRefresh')  # time at next scr refresh
            Flanker_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(Flanker_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(Flanker_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
            win.callOnFlip(event.clearEvents, eventType='keyboard')  # clear event fallback buffer
        if Flanker_key.status == STARTED and not waitOnFlip:
            theseKeys = safe_keyboard_get_keys(Flanker_key)
            matched_key = get_first_matching_keypress(theseKeys, LEFT_RIGHT_KEYS)
            fallback_keys = safe_event_get_keys()
            matched_fallback_key = get_first_matching_keyname(fallback_keys, LEFT_RIGHT_KEYS)
            if matched_key:
                _Flanker_key_allKeys.append(matched_key)
            elif matched_fallback_key:
                Flanker_key.keys = matched_fallback_key
                Flanker_key.rt = Flanker_key.clock.getTime()
                Flanker_key.corr = 1 if is_key_match(Flanker_key.keys, correct_key) else 0
                continueRoutine = False
            if len(_Flanker_key_allKeys):
                Flanker_key.keys = _Flanker_key_allKeys[-1].name  # just the last key pressed
                Flanker_key.rt = _Flanker_key_allKeys[-1].rt
                # was this correct?
                if is_key_match(Flanker_key.keys, correct_key):
                    Flanker_key.corr = 1
                else:
                    Flanker_key.corr = 0
                # a response ends the routine
                continueRoutine = False

        # check for quit (typically the Esc key)
        if endExpNow or escape_pressed(defaultKeyboard):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in FlankerTrialsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "FlankerTrials"-------
    for thisComponent in FlankerTrialsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Flanker_trials.addData('Flanker_arrow.started', Flanker_arrows.tStartRefresh)
    Flanker_trials.addData('Flanker_arrow.stopped', Flanker_arrows.tStopRefresh)
    # check responses
    if Flanker_key.keys in ['', [], None]:  # No response was made
        Flanker_key.keys = None
        # was no response the correct answer?!
        if str(correct_key).lower() == 'none':
            Flanker_key.corr = 1;  # correct non-response
        else:
            Flanker_key.corr = 0;  # failed to respond (incorrectly)
    # store data for Flanker_trials (TrialHandler)
    Flanker_trials.addData('Flanker_key.keys', Flanker_key.keys)
    Flanker_trials.addData('Flanker_key.corr', Flanker_key.corr)
    if Flanker_key.keys != None:  # we had a response
        Flanker_trials.addData('Flanker_key.rt', Flanker_key.rt)
    Flanker_trials.addData('Flanker_key.started', Flanker_key.tStartRefresh)
    Flanker_trials.addData('Flanker_key.stopped', Flanker_key.tStopRefresh)
    # the Routine "FlankerTrials" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()

# completed 21.0 repeats of 'Flanker_trials'


# ------Prepare to start Routine "GoodbyeScreen"-------
continueRoutine = True
routineTimer.addTime(10.000000)
# update component parameters for each repeat
key_goodbye.keys = []
key_goodbye.rt = []
_key_goodbye_allKeys = []
# keep track of which components have finished
GoodbyeScreenComponents = [Goodbyetext, key_goodbye]
for thisComponent in GoodbyeScreenComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
GoodbyeScreenClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "GoodbyeScreen"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = GoodbyeScreenClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=GoodbyeScreenClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *Goodbyetext* updates
    if Goodbyetext.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        Goodbyetext.frameNStart = frameN  # exact frame index
        Goodbyetext.tStart = t  # local t and not account for scr refresh
        Goodbyetext.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Goodbyetext, 'tStartRefresh')  # time at next scr refresh
        Goodbyetext.setAutoDraw(True)
    if Goodbyetext.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > Goodbyetext.tStartRefresh + 10 - frameTolerance:
            # keep track of stop time/frame for later
            Goodbyetext.tStop = t  # not accounting for scr refresh
            Goodbyetext.frameNStop = frameN  # exact frame index
            win.timeOnFlip(Goodbyetext, 'tStopRefresh')  # time at next scr refresh
            Goodbyetext.setAutoDraw(False)

    # *key_goodbye* updates
    waitOnFlip = False
    if key_goodbye.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        key_goodbye.frameNStart = frameN  # exact frame index
        key_goodbye.tStart = t  # local t and not account for scr refresh
        key_goodbye.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_goodbye, 'tStartRefresh')  # time at next scr refresh
        key_goodbye.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_goodbye.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_goodbye.clearEvents, eventType='keyboard')  # clear events on next screen flip
        win.callOnFlip(event.clearEvents, eventType='keyboard')  # clear event fallback buffer
    if key_goodbye.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > key_goodbye.tStartRefresh + 10 - frameTolerance:
            # keep track of stop time/frame for later
            key_goodbye.tStop = t  # not accounting for scr refresh
            key_goodbye.frameNStop = frameN  # exact frame index
            win.timeOnFlip(key_goodbye, 'tStopRefresh')  # time at next scr refresh
            key_goodbye.status = FINISHED
    if key_goodbye.status == STARTED and not waitOnFlip:
        theseKeys = safe_keyboard_get_keys(key_goodbye)
        matched_key = get_first_matching_keypress(theseKeys, CONTINUE_KEYS)
        fallback_keys = safe_event_get_keys(CONTINUE_KEYS)
        matched_fallback_key = get_first_matching_keyname(fallback_keys, CONTINUE_KEYS)
        if matched_key:
            _key_goodbye_allKeys.append(matched_key)
        elif matched_fallback_key:
            key_goodbye.keys = normalize_key_name(matched_fallback_key)
            key_goodbye.rt = key_goodbye.clock.getTime()
            continueRoutine = False
        if len(_key_goodbye_allKeys):
            key_goodbye.keys = normalize_key_name(_key_goodbye_allKeys[-1].name)
            key_goodbye.rt = _key_goodbye_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False

    # check for quit (typically the Esc key)
    if endExpNow or escape_pressed(defaultKeyboard):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in GoodbyeScreenComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "GoodbyeScreen"-------
for thisComponent in GoodbyeScreenComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('Goodbyetext.started', Goodbyetext.tStartRefresh)
thisExp.addData('Goodbyetext.stopped', Goodbyetext.tStopRefresh)
# check responses
if key_goodbye.keys in ['', [], None]:  # No response was made
    key_goodbye.keys = None
thisExp.addData('key_goodbye.keys', key_goodbye.keys)
if key_goodbye.keys != None:  # we had a response
    thisExp.addData('key_goodbye.rt', key_goodbye.rt)
thisExp.addData('key_goodbye.started', key_goodbye.tStartRefresh)
thisExp.addData('key_goodbye.stopped', key_goodbye.tStopRefresh)
thisExp.nextEntry()

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename + '.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
# core.quit()
