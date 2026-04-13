#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
RAN digit task with robust Persian / RTL instruction rendering.

Key idea:
- Welcome / instruction / end screens are rendered as images with Pillow
- RTL shaping and wrapping are handled manually
- PsychoPy only displays the rendered image
- Only SPACE advances text screens
"""

import argparse
import csv
import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path

import arabic_reshaper
import numpy as np
import pandas as pd
import sounddevice as sd
import soundfile as sf
import yaml
from bidi.algorithm import get_display
from psychopy import core, event, logging, visual
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager

date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# ========================================= Args =========================================================

parser = argparse.ArgumentParser(description="Run the RAN digit test.")
parser.add_argument('--participant_folder', type=str, required=True, help="Path to the participant folder.")
args = parser.parse_args()
results_folder = args.participant_folder

# ========================================= Config =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
config_path = PROJECT_ROOT / 'configs' / 'config.yaml'
experiment_config_path = PROJECT_ROOT / 'configs' / 'experiment.yaml'
digits_path = PROJECT_ROOT / 'tasks' / 'RAN' / 'digits.yaml'

with config_path.open('r', encoding='utf-8') as file:
    config_data = yaml.safe_load(file)

language = str(config_data['language']).strip()
country_code = config_data['country_code']
lab_number = config_data['lab_number']
random_seed = config_data['random_seed']
font_name = config_data['font']

np.random.seed(random_seed)

with digits_path.open('r', encoding='utf-8') as file:
    ran_data = yaml.safe_load(file)

digits = [
    [int(char) for line in block.strip().splitlines() for char in line.split() if char.isdigit()]
    for block in ran_data['items']['numbers']
]

if experiment_config_path.exists():
    with experiment_config_path.open('r', encoding='utf-8') as file:
        expInfo = yaml.safe_load(file)
        participant_id_str = str(expInfo['participant_id'])
        while len(participant_id_str) < 3:
            participant_id_str = "0" + participant_id_str
        participant_id = participant_id_str
else:
    expInfo = {'participant_id': 999, 'session_id': 2}
    participant_id = "999"

rtl_langs = {'fa', 'fas', 'ar', 'ara', 'ur', 'urd', 'he', 'heb'}

# ========================================= Helpers =========================================================


def resolve_table_file(base_path_without_ext, file_label='input file'):
    candidate_extensions = ('.xlsx', '.csv')
    base_path = Path(base_path_without_ext)
    for extension in candidate_extensions:
        candidate_path = base_path.with_suffix(extension)
        if candidate_path.exists():
            return str(candidate_path)

    tried_paths = ", ".join(str(base_path.with_suffix(ext)) for ext in candidate_extensions)
    raise FileNotFoundError(f"Could not find {file_label}. Tried: {tried_paths}")


def sanitize_text(value):
    if value is None:
        return ''

    s = str(value)
    s = s.replace('\\n', '\n')
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    s = unicodedata.normalize("NFC", s)

    cleaned = []
    for ch in s:
        code = ord(ch)
        cat = unicodedata.category(ch)

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


def is_rtl_language(language_code):
    return str(language_code).lower() in rtl_langs


def normalize_instruction_text(text):
    """
    Only blank lines separate paragraphs.
    Single newlines inside a paragraph become spaces.
    """
    text = sanitize_text(text).strip()
    if not text:
        return ''

    paragraphs = re.split(r'\n\s*\n+', text)
    cleaned = []

    for p in paragraphs:
        p = re.sub(r'[\n\t]+', ' ', p)
        p = re.sub(r'\s+', ' ', p).strip()
        if p:
            cleaned.append(p)

    return '\n\n'.join(cleaned)


def shape_rtl_line(line):
    reshaped = arabic_reshaper.reshape(line)
    return get_display(reshaped)


def get_instruction_column_name(df, language_code):
    available = {str(c).strip().lower(): c for c in df.columns}
    lang = str(language_code).strip().lower()

    alias_map = {
        'fa': ['fa', 'fas', 'persian'],
        'fas': ['fa', 'fas', 'persian'],
        'en': ['en', 'eng', 'english'],
        'eng': ['en', 'eng', 'english'],
        'ar': ['ar', 'ara', 'arabic'],
        'ara': ['ar', 'ara', 'arabic'],
        'he': ['he', 'heb', 'hebrew'],
        'heb': ['he', 'heb', 'hebrew'],
        'ur': ['ur', 'urd', 'urdu'],
        'urd': ['ur', 'urd', 'urdu'],
    }

    candidates = [lang]
    candidates.extend(alias_map.get(lang, []))

    for cand in candidates:
        if cand in available:
            return available[cand]

    raise KeyError(
        f"Could not find a matching language column for '{language_code}'. "
        f"Available columns: {list(df.columns)}"
    )


def resolve_font_path(preferred_font_name):
    """
    Resolve a system font path from a font family name.
    Falls back to DejaVu Sans.
    """
    try:
        path = font_manager.findfont(preferred_font_name, fallback_to_default=False)
        if path and Path(path).exists():
            return path
    except Exception:
        pass

    fallback = font_manager.findfont("DejaVu Sans")
    if fallback and Path(fallback).exists():
        return fallback

    raise FileNotFoundError(
        f"Could not resolve a font path for '{preferred_font_name}'."
    )


def measure_text_pil(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_paragraph_ltr(draw, paragraph, font, max_width_px):
    words = paragraph.split()
    if not words:
        return []

    lines = []
    current = []

    for word in words:
        candidate = ' '.join(current + [word])
        width, _ = measure_text_pil(draw, candidate, font)

        if width <= max_width_px or not current:
            current.append(word)
        else:
            lines.append(' '.join(current))
            current = [word]

    if current:
        lines.append(' '.join(current))

    return lines


def wrap_paragraph_rtl(draw, paragraph, font, max_width_px):
    """
    Wrap in logical order, but measure the final visual shaped line.
    """
    words = paragraph.split()
    if not words:
        return []

    lines = []
    current = []

    for word in words:
        candidate_logical = ' '.join(current + [word])
        candidate_visual = shape_rtl_line(candidate_logical)
        width, _ = measure_text_pil(draw, candidate_visual, font)

        if width <= max_width_px or not current:
            current.append(word)
        else:
            lines.append(' '.join(current))
            current = [word]

    if current:
        lines.append(' '.join(current))

    return lines


def text_to_logical_lines(text, rtl, draw, font, max_width_px):
    text = normalize_instruction_text(text)
    if not text:
        return []

    paragraphs = text.split('\n\n')
    all_lines = []

    for i, p in enumerate(paragraphs):
        if rtl:
            lines = wrap_paragraph_rtl(draw, p, font, max_width_px)
        else:
            lines = wrap_paragraph_ltr(draw, p, font, max_width_px)

        all_lines.extend(lines)
        if i < len(paragraphs) - 1:
            all_lines.append('')

    return all_lines


def render_text_screen_to_image(
    text,
    language_code,
    font_path,
    image_width=1800,
    image_height=1100,
    font_size=62,
    margin_px=180,
    line_spacing_px=26,
    bg_color='white',
    text_color='black',
    out_path='text_screen.png'
):
    """
    Render text to a PNG image. For RTL text, wrap and shape manually.
    """
    rtl = is_rtl_language(language_code)

    image = Image.new('RGB', (image_width, image_height), color=bg_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)

    max_width_px = image_width - 2 * margin_px

    logical_lines = text_to_logical_lines(
        text=text,
        rtl=rtl,
        draw=draw,
        font=font,
        max_width_px=max_width_px
    )

    display_lines = []
    line_heights = []

    for line in logical_lines:
        if line == '':
            display_lines.append('')
            line_heights.append(font_size // 2)
            continue

        display_line = shape_rtl_line(line) if rtl else line
        _, h = measure_text_pil(draw, display_line, font)
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

        w, h = measure_text_pil(draw, line, font)
        x = (image_width - w) // 2
        draw.text((x, y), line, font=font, fill=text_color)
        y += h + line_spacing_px

    image.save(out_path)
    return out_path


def show_rendered_text_screen(
    win,
    text,
    language_code,
    font_path,
    output_dir,
    image_name,
    font_size
):
    img_path = Path(output_dir) / image_name

    render_text_screen_to_image(
        text=text,
        language_code=language_code,
        font_path=font_path,
        image_width=1800,
        image_height=1100,
        font_size=font_size,
        margin_px=180,
        line_spacing_px=max(20, font_size // 3),
        out_path=str(img_path)
    )

    stim = visual.ImageStim(
        win=win,
        image=str(img_path),
        pos=(0, 0),
        size=(1.8, 1.1),
        units='norm'
    )
    stim.draw()
    win.flip()
    event.clearEvents()
    event.waitKeys(keyList=['space'])

def show_ltr_text_screen(win, text, font_name, height=0.085, wrap_width=1.25):
    stim = visual.TextStim(
        win=win,
        text=text,
        font=font_name if font_name else "Arial",
        pos=(0, 0),
        height=height,
        wrapWidth=wrap_width,
        ori=0.0,
        color='black',
        colorSpace='rgb',
        opacity=None,
        languageStyle='LTR',
        alignText='center',
        anchorHoriz='center',
        anchorVert='center',
        depth=0.0
    )
    stim.draw()
    win.flip()
    event.clearEvents()
    event.waitKeys(keyList=['space'])


def show_text_screen(win, text, language_code, font_name, font_path, output_dir, image_name, height=0.07):
    if is_rtl_language(language_code):
        font_size = 72 if height >= 0.1 else 62
        show_rendered_text_screen(
            win=win,
            text=text,
            language_code=language_code,
            font_path=font_path,
            output_dir=output_dir,
            image_name=image_name,
            font_size=font_size
        )
    else:
        show_ltr_text_screen(
            win=win,
            text=text,
            font_name=font_name,
            height=height,
            wrap_width=1.4
        )


# ========================================= Paths / outputs =========================================================

output_path = PROJECT_ROOT / 'data' / results_folder / 'RAN'
output_path.mkdir(parents=True, exist_ok=True)

filename = str(
    output_path / (
    f"{language}{country_code}{lab_number}"
    f"_{participant_id}_PT{expInfo['session_id']}_{date}"
    )
)

save_audio_path = output_path / (
    f"audio_{language}{country_code}{lab_number}"
    f"_{participant_id}_PT{expInfo['session_id']}_{date}"
)
save_audio_path.mkdir(parents=True, exist_ok=True)

rendered_text_dir = output_path / f"rendered_text_{date}"
rendered_text_dir.mkdir(parents=True, exist_ok=True)

save_csv_path = output_path

# ========================================= Recording =========================================================

recording = []
recording_start_time = 0
num_trials = 2


def start_recording(samplerate=44100, channels=1, device_index=0, dtype='float32'):
    global recording, recording_start_time
    recording_start_time = core.getTime()
    recording = []

    def callback(indata, frames, time_info, status):
        recording.extend(indata.copy())

    stream = sd.InputStream(
        samplerate=samplerate,
        device=device_index,
        channels=channels,
        dtype=dtype,
        callback=callback
    )
    stream.start()
    return stream


def stop_and_save_recording(stream, filename_out, samplerate=44100):
    global recording
    stream.stop()
    stream.close()
    recording_stop_time = core.getTime()
    sf.write(filename_out, recording, samplerate)
    reading_time = recording_stop_time - recording_start_time
    recording.clear()
    return reading_time


# ========================================= Load instructions =========================================================

print(sd.query_devices())

instructions_path = resolve_table_file(
    str(PROJECT_ROOT / 'languages' / language / 'instructions' / f'RAN_instructions_{language.lower()}'),
    file_label='RAN instructions file'
)

if instructions_path.endswith('.csv'):
    instructions_df = pd.read_csv(instructions_path)
else:
    instructions_df = pd.read_excel(instructions_path)

screen_col = None
for c in instructions_df.columns:
    if str(c).strip().lower() == 'screen':
        screen_col = c
        break
if screen_col is None:
    raise KeyError(f"No 'screen' column found. Available columns: {list(instructions_df.columns)}")

lang_col = get_instruction_column_name(instructions_df, language)
instructions_df = instructions_df.set_index(screen_col)

welcome_raw = sanitize_text(instructions_df.loc['Welcome_text', lang_col])
instructions_raw = sanitize_text(instructions_df.loc['RAN_instructions', lang_col])
done_raw = sanitize_text(instructions_df.loc['done_text', lang_col])

# ========================================= Window / logging =========================================================

logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.ERROR)

win = visual.Window(
    fullscr=True,
    screen=0,
    winType='pyglet',
    allowGUI=False,
    allowStencil=False,
    monitor='testMonitor',
    color='white',
    colorSpace='rgb',
    blendMode='avg',
    useFBO=True,
    units='norm',
    checkTiming=False
)

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

win.recordFrameIntervals = False
expInfo['frameRate'] = None

if is_rtl_language(language):
    font_path = resolve_font_path("DejaVu Sans")
else:
    font_path = None

# ========================================= Screens =========================================================
show_text_screen(
    win=win,
    text=welcome_raw,
    language_code=language,
    font_name=font_name,
    font_path=font_path,
    output_dir=rendered_text_dir,
    image_name='welcome.png',
    height=0.12
)

show_text_screen(
    win=win,
    text=instructions_raw,
    language_code=language,
    font_name=font_name,
    font_path=font_path,
    output_dir=rendered_text_dir,
    image_name='instructions.png',
    height=0.07
)

# ========================================= Main experiment =========================================================

results = []

for trial in range(num_trials):
    fixation = visual.TextStim(
        win=win,
        name='fix_cross',
        text='+',
        font='Courier New',
        pos=(0, 0),
        height=0.1,
        wrapWidth=None,
        ori=0.0,
        color='black',
        colorSpace='rgb',
        opacity=None,
        languageStyle='LTR',
        alignText='center',
        anchorHoriz='center',
        anchorVert='center',
        depth=0.0
    )
    fixation.draw()
    win.flip()
    core.wait(0.5)

    matrix = np.array(digits[trial]).reshape((5, 10))
    matrix_content = matrix.astype(str)
    digits_matrix_str = '; '.join([' '.join(row) for row in matrix_content])

    matrix_str = '\n\n'.join([' '.join(row) for row in matrix_content])
    matrix_display = visual.TextStim(
        win=win,
        text=matrix_str,
        pos=(0, 0),
        font='Courier New',
        height=0.15,
        wrapWidth=1.2,
        color='black',
        colorSpace='rgb',
        languageStyle='LTR',
        alignText='center',
        anchorHoriz='center',
        anchorVert='center'
    )
    matrix_display.draw()
    win.flip()

    audio_filename = save_audio_path / (
        f"{language}{country_code}{lab_number}_{expInfo['participant_id']}"
        f"_S{expInfo['session_id']}_trial{trial + 1}.wav"
    )
    stream = start_recording()

    event.clearEvents()
    continue_trial = True
    while continue_trial:
        allKeys = event.getKeys()
        for thisKey in allKeys:
            if thisKey == 'space':
                continue_trial = False
                break
            elif thisKey == 'escape':
                win.close()
                core.quit()

        if not continue_trial:
            break

    reading_time = stop_and_save_recording(stream, audio_filename)
    results.append([
        expInfo['participant_id'],
        expInfo['session_id'],
        trial + 1,
        reading_time,
        digits_matrix_str
    ])

# ========================================= Save results =========================================================

csv_filename = save_csv_path / (
    f"{language}{country_code}{lab_number}_{expInfo['participant_id']}"
    f"_S{expInfo['session_id']}_{date}.csv"
)

with csv_filename.open('w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Participant_id', 'Session_id', 'Trial', 'Reading_Time', 'Digits_Matrix'])
    csvwriter.writerows(results)

# ========================================= End screen =========================================================

show_text_screen(
    win=win,
    text=done_raw,
    language_code=language,
    font_name=font_name,
    font_path=font_path,
    output_dir=rendered_text_dir,
    image_name='done.png',
    height=0.07
)

win.close()
# core.quit()