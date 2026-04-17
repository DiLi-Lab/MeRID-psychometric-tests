#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PLAB (Language Analysis) Task - PsychoPy implementation.
This is a custom implementation based on the paper-and-pencil PLAB test.
The original test materials were adapted from a PowerPoint template,
converted to screenshots, and presented as visual stimuli.

Unified text rendering:
- ALL languages use Pillow-rendered text images for:
  * welcome
  * instructions
  * done
  * goodbye
  * question + options blocks
- RTL languages use DejaVu Sans by default
- LTR languages use the configured font (fallback Arial)
- Highlight rectangles are derived from rendered option boxes, so no hard-coded
  option rectangle positions are needed for different machines.
"""

from __future__ import absolute_import, division

import argparse
import ast
import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml
from psychopy import visual, core, data, event, logging
from psychopy.hardware import keyboard

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_RTL_SUPPORT = True
except ImportError:
    HAS_RTL_SUPPORT = False

from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager

date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# ========================================= Args =========================================================

parser = argparse.ArgumentParser(description="Run the PLAB task.")
parser.add_argument('--participant_folder', type=str, required=True, help="Path to the participant folder.")
args = parser.parse_args()
results_folder = args.participant_folder

# ========================================= Config =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
config_path = PROJECT_ROOT / 'configs' / 'config.yaml'
experiment_config_path = PROJECT_ROOT / 'configs' / 'experiment.yaml'

with config_path.open('r', encoding='utf-8') as file:
    config_data = yaml.safe_load(file)

language = str(config_data['language']).strip()
country_code = config_data['country_code']
lab_number = config_data['lab_number']
random_seed = config_data['random_seed']
font = config_data['font']

RTL_LANGS = {'fa', 'fas', 'ar', 'ara', 'he', 'heb', 'ur', 'urd'}
is_rtl = str(language).lower() in RTL_LANGS

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

# ========================================= Paths =========================================================

output_path = PROJECT_ROOT / 'data' / results_folder / 'PLAB'
output_path.mkdir(parents=True, exist_ok=True)

rendered_text_dir = output_path / f'rendered_text_{date}'
rendered_text_dir.mkdir(parents=True, exist_ok=True)

filename = str(
    output_path / (
    f"{language}{country_code}{lab_number}"
    f"_{participant_id}_PT{expInfo['session_id']}_{date}"
    )
)

# ========================================= Helpers =========================================================


def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = text.replace('\\n', '\n')
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = unicodedata.normalize('NFC', text)
    return text


def sanitize_text(text):
    text = normalize_text(text)
    cleaned = []
    for ch in text:
        code = ord(ch)
        cat = unicodedata.category(ch)
        if 0xD800 <= code <= 0xDFFF:
            continue
        if cat in {'Cs', 'Co', 'Cn'}:
            continue
        if cat == 'Cc' and ch not in ('\n', '\t'):
            continue
        cleaned.append(ch)
    return ''.join(cleaned)


def clean_ltr_text(text):
    text = sanitize_text(text)
    text = text.replace('\u200c', '')
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    return text


def normalize_instruction_text(text):
    """
    Preserve explicit line breaks for RTL languages.
    For LTR languages, keep the old paragraph behavior.
    """
    text = sanitize_text(text).strip()
    if not text:
        return ''

    if is_rtl:
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = re.sub(r'[ \t]+', ' ', line).strip()
            cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)

    paragraphs = re.split(r'\n\s*\n+', text)
    cleaned = []
    for p in paragraphs:
        p = re.sub(r'[\n\t]+', ' ', p)
        p = re.sub(r'\s+', ' ', p).strip()
        if p:
            cleaned.append(p)
    return '\n\n'.join(cleaned)


def shape_rtl_line(line):
    if not HAS_RTL_SUPPORT:
        return line
    reshaped = arabic_reshaper.reshape(line)
    return get_display(reshaped)


def visual_line(line, rtl=False):
    line = sanitize_text(line)
    if rtl:
        return shape_rtl_line(line)
    return clean_ltr_text(line)


def resolve_conditions_file(base_path_without_ext, file_label='input file'):
    candidate_extensions = ('.xlsx', '.csv')
    base_path = Path(base_path_without_ext)
    for extension in candidate_extensions:
        candidate_path = base_path.with_suffix(extension)
        if candidate_path.exists():
            return str(candidate_path)

    tried_paths = ", ".join(str(base_path.with_suffix(ext)) for ext in candidate_extensions)
    raise FileNotFoundError(f"Could not find {file_label}. Tried: {tried_paths}")


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


def choose_font_path(language_code, preferred_ltr_font):
    if str(language_code).lower() in RTL_LANGS:
        return resolve_font_path("DejaVu Sans")
    return resolve_font_path(preferred_ltr_font if preferred_ltr_font else "Arial")


def measure_text_pil(draw, text, font_obj):
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_paragraph(draw, paragraph, font_obj, max_width_px, rtl=False):
    words = paragraph.split()
    if not words:
        return []

    lines = []
    current = []

    for word in words:
        candidate_logical = ' '.join(current + [word])
        candidate_visual = visual_line(candidate_logical, rtl=rtl)
        width, _ = measure_text_pil(draw, candidate_visual, font_obj)
        if width <= max_width_px or not current:
            current.append(word)
        else:
            lines.append(' '.join(current))
            current = [word]

    if current:
        lines.append(' '.join(current))

    return lines


def wrap_text_to_lines(text, rtl, draw, font_obj, max_width_px):
    """
    Respect explicit line breaks for RTL text.
    Each line separated by \n is treated as its own logical line.
    Blank lines are preserved.
    """
    text = normalize_instruction_text(text)
    if not text:
        return []

    if rtl:
        raw_lines = text.split('\n')
        all_lines = []

        for line in raw_lines:
            if not line.strip():
                all_lines.append('')
                continue

            wrapped = wrap_paragraph(draw, line.strip(), font_obj, max_width_px, rtl=rtl)
            all_lines.extend(wrapped)

        return all_lines

    paragraphs = text.split('\n\n')
    all_lines = []

    for i, p in enumerate(paragraphs):
        lines = wrap_paragraph(draw, p, font_obj, max_width_px, rtl=rtl)
        all_lines.extend(lines)
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
    line_spacing_px=24,
    bg_color=(255, 255, 255, 0),
    text_color='black'
):
    rtl = str(language_code).lower() in RTL_LANGS

    # Use transparent RGBA background so no rectangle/border appears around text.
    image = Image.new('RGBA', (image_width, image_height), color=bg_color)
    draw = ImageDraw.Draw(image)
    font_obj = ImageFont.truetype(font_path, font_size)

    max_width_px = image_width - 2 * margin_px
    logical_lines = wrap_text_to_lines(text, rtl, draw, font_obj, max_width_px)

    display_lines = []
    line_heights = []

    for line in logical_lines:
        if line == '':
            display_lines.append('')
            line_heights.append(font_size // 2)
            continue
        display_line = visual_line(line, rtl=rtl)
        _, h = measure_text_pil(draw, display_line, font_obj)
        display_lines.append(display_line)
        line_heights.append(h)

    total_height = 0
    for i, h in enumerate(line_heights):
        total_height += h
        if i < len(line_heights) - 1:
            total_height += line_spacing_px

    y = max(20, (image_height - total_height) // 2)

    for i, line in enumerate(display_lines):
        if line == '':
            y += line_heights[i] + line_spacing_px
            continue
        w, h = measure_text_pil(draw, line, font_obj)
        x = (image_width - w) // 2
        draw.text((x, y), line, font=font_obj, fill=text_color)
        y += h + line_spacing_px

    image.save(out_path)
    return out_path


def show_text_screen(
    win,
    text,
    language_code,
    font_name,
    font_path,
    output_dir,
    image_name,
    height=0.05,
    image_width=1800,
    image_height=1100,
    rtl_font_size_large=52,
    rtl_font_size_small=42
):
    """
    RTL languages: render welcome/instruction/done as Pillow image
    LTR languages: keep original PsychoPy TextStim style
    """
    if str(language_code).lower() in RTL_LANGS:
        img_path = Path(output_dir) / image_name
        render_text_screen_to_image(
            text=text,
            language_code=language_code,
            font_path=font_path,
            out_path=str(img_path),
            image_width=image_width,
            image_height=image_height,
            font_size=rtl_font_size_large if height >= 0.05 else rtl_font_size_small,
            line_spacing_px=20
        )
        stim = visual.ImageStim(
            win=win,
            image=str(img_path),
            pos=(0, 0),
            size=(1.8, 1.5),
            units='norm',
            interpolate=True
        )
    else:
        stim = visual.TextStim(
            win=win,
            text=clean_ltr_text(text),
            alignText='center',
            anchorHoriz='center',
            anchorVert='center',
            font=font_name if font_name else "Arial",
            pos=(0, 0),
            height=height,
            wrapWidth=1.3,
            ori=0.0,
            color='black',
            colorSpace='rgb',
            opacity=None,
            languageStyle='LTR',
            depth=0.0
        )

    stim.draw()
    win.flip()
    event.clearEvents(eventType='keyboard')

    while True:
        keys = event.waitKeys(keyList=['space', 'escape'])
        if 'escape' in keys:
            win.close()
            core.quit()
        if 'space' in keys:
            break


def render_question_option_block_to_image(
    question,
    options,
    language_code,
    font_path,
    out_path,
    image_width=1600,
    image_height=700,
    question_font_size=36,
    option_font_size=32,
    margin_px=80,
    line_spacing_px=18,
    block_gap_px=10,
    bg_color=(255, 255, 255, 0),
    text_color='black'
):
    """
    Render one full question+options block as a single image.
    Returns option bounding boxes in pixel coordinates for highlight rectangles.
    """
    rtl = str(language_code).lower() in RTL_LANGS

    image = Image.new('RGBA', (image_width, image_height), color=bg_color)
    draw = ImageDraw.Draw(image)
    q_font = ImageFont.truetype(font_path, question_font_size)
    o_font = ImageFont.truetype(font_path, option_font_size)

    max_width_px = image_width - 2 * margin_px

    q_lines = wrap_text_to_lines(question, rtl, draw, q_font, max_width_px)
    q_display_lines = [visual_line(line, rtl=rtl) if line else '' for line in q_lines]

    option_display_blocks = []
    for opt in options:
        opt_lines = wrap_text_to_lines(opt, rtl, draw, o_font, max_width_px)
        option_display_blocks.append([visual_line(line, rtl=rtl) if line else '' for line in opt_lines])

    total_height = 0
    q_line_heights = []
    for line in q_display_lines:
        _, h = measure_text_pil(draw, line if line else " ", q_font)
        q_line_heights.append(h)
        total_height += h + line_spacing_px

    total_height += block_gap_px

    option_heights = []
    for block in option_display_blocks:
        block_h = 0
        block_line_heights = []
        for line in block:
            _, h = measure_text_pil(draw, line if line else " ", o_font)
            block_line_heights.append(h)
            block_h += h + line_spacing_px
        block_h = max(1, block_h - line_spacing_px)
        option_heights.append(block_line_heights)
        total_height += block_h + block_gap_px

    y = max(20, (image_height - total_height) // 2)

    for i, line in enumerate(q_display_lines):
        w, h = measure_text_pil(draw, line if line else " ", q_font)
        x = (image_width - w) // 2
        draw.text((x, y), line, font=q_font, fill=text_color)
        y += h + line_spacing_px

    y += block_gap_px

    option_boxes = []

    for block_idx, block in enumerate(option_display_blocks):
        block_top = y
        block_width = 0
        block_height = 0
        line_sizes = []

        for line in block:
            w, h = measure_text_pil(draw, line if line else " ", o_font)
            line_sizes.append((w, h))
            block_width = max(block_width, w)
            block_height += h + line_spacing_px

        block_height = max(1, block_height - line_spacing_px)

        for line_idx, line in enumerate(block):
            w, h = line_sizes[line_idx]
            x = (image_width - w) // 2
            draw.text((x, y), line, font=o_font, fill=text_color)
            y += h + line_spacing_px

        block_left = (image_width - block_width) // 2
        option_boxes.append((block_left, block_top, block_left + block_width, block_top + block_height))
        y += block_gap_px

    image.save(out_path)
    return out_path, option_boxes


def normalize_key_name(key_name):
    if key_name is None:
        return None

    if isinstance(key_name, (list, tuple)) and len(key_name) > 0:
        key_name = key_name[0]
    elif isinstance(key_name, str) and key_name.startswith('[') and key_name.endswith(']'):
        try:
            parsed = ast.literal_eval(key_name)
            if isinstance(parsed, (list, tuple)) and len(parsed) > 0:
                key_name = parsed[0]
        except (SyntaxError, ValueError):
            pass

    normalized = str(key_name).strip().lower().replace('-', '_')
    key_map = {
        'spacebar': 'space',
        'enter': 'return',
        'leftarrow': 'left',
        'rightarrow': 'right',
    }
    normalized = key_map.get(normalized, normalized)

    for prefix in ('num_', 'numpad_', 'kp_'):
        if normalized.startswith(prefix):
            suffix = normalized[len(prefix):]
            if len(suffix) == 1 and suffix.isdigit():
                return suffix
    return normalized


_key_backend_warning_shown = False
CONTINUE_KEYS = ['space', 'return']


def safe_event_get_keys(key_list=None):
    global _key_backend_warning_shown
    try:
        return event.getKeys(keyList=key_list)
    except Exception as exc:
        if not _key_backend_warning_shown:
            logging.info(f"event.getKeys failed on this backend: {exc}")
            _key_backend_warning_shown = True
        return []


def safe_keyboard_get_keys(keyboard_component, key_list=None, wait_release=False):
    global _key_backend_warning_shown
    try:
        return keyboard_component.getKeys(keyList=key_list, waitRelease=wait_release)
    except Exception as exc:
        if not _key_backend_warning_shown:
            logging.info(f"keyboard.getKeys failed on this backend: {exc}")
            _key_backend_warning_shown = True
        return []


def escape_pressed(default_keyboard):
    if safe_keyboard_get_keys(default_keyboard, ['escape']):
        return True
    return any(normalize_key_name(name) == 'escape' for name in safe_event_get_keys(['escape']))


def get_primary_screen_size(default=(1440, 900)):
    try:
        import pyglet
        screen = pyglet.canvas.get_display().get_default_screen()
        return [int(screen.width), int(screen.height)]
    except Exception:
        return list(default)

# ========================================= Metadata =========================================================

psychopyVersion = '2025.1.1'
expName = 'PLAB'

instructions_path = resolve_conditions_file(
    str(PROJECT_ROOT / 'languages' / language / 'instructions' / f'PLAB_instructions_{language.lower()}'),
    file_label='PLAB instructions file'
)
if instructions_path.endswith('.csv'):
    instructions_df = pd.read_csv(instructions_path, index_col='screen')
else:
    instructions_df = pd.read_excel(instructions_path, index_col='screen')

welcome_text = normalize_text(instructions_df.loc['Welcome_text', language])
done_text_str = normalize_text(instructions_df.loc['done_text', language])
Goodbyetext_str = normalize_text(instructions_df.loc['Goodbye_text', language])
PLAB_instructions_str = normalize_text(instructions_df.loc['PLAB_instructions', language])

task1_img = str(PROJECT_ROOT / 'languages' / language / 'PLAB' / f'Plab_part4_task1_{language.lower()}.png')
task2_img = str(PROJECT_ROOT / 'languages' / language / 'PLAB' / f'Plab_part4_task2_{language.lower()}.png')
PlabStim = resolve_conditions_file(
    str(PROJECT_ROOT / 'languages' / language / 'PLAB' / f'PlabStim_{language.lower()}'),
    file_label='PLAB stimulus file'
)

thisExp = data.ExperimentHandler(
    name='PLAB', version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename
)

logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.ERROR)

endExpNow = False

win = visual.Window(
    size=get_primary_screen_size(), fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='white', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height', checkTiming=False
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

expInfo['frameRate'] = None
defaultKeyboard = keyboard.Keyboard()
font_path = choose_font_path(language, font)
print(f"[PLAB] Question/options font path: {font_path}")

# ========================================= Basic components =========================================================

blank = visual.TextStim(
    win=win, name='blank',
    text='\n\n',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb',
    languageStyle='LTR'
)

fix_cross = visual.TextStim(
    win=win, name='fix_cross',
    text='+',
    font='Courier New',
    pos=(0, 0), height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb',
    languageStyle='LTR'
)

PLAB_task1_key = keyboard.Keyboard()
PLAB_task2_key = keyboard.Keyboard()
key_goodbye = keyboard.Keyboard()

# ========================================= Welcome / Instruction =========================================================

show_text_screen(
    win=win,
    text=welcome_text,
    language_code=language,
    font_name=font,
    font_path=font_path,
    output_dir=rendered_text_dir,
    image_name='welcome.png',
    height=0.05
)

show_text_screen(
    win=win,
    text=PLAB_instructions_str,
    language_code=language,
    font_name=font,
    font_path=font_path,
    output_dir=rendered_text_dir,
    image_name='instructions.png',
    height=0.03,
    image_width=1800,
    image_height=1500,
    rtl_font_size_small=42
)

# ========================================= Blank500 =========================================================

routineTimer = core.CountdownTimer(0.5)
while routineTimer.getTime() > 0:
    blank.draw()
    win.flip()
    if endExpNow or escape_pressed(defaultKeyboard):
        core.quit()

# ========================================= Trials =========================================================

full_trial_list = data.importConditions(PlabStim)
PLAB_task1_list = full_trial_list[:4]
PLAB_task2_list = full_trial_list[4:]

PLAB_pics_1 = visual.ImageStim(
    win=win, name='plab_task1',
    image=task1_img,
    pos=(0, 0.18),
    size=(1.5, 0.6),
    color=[1, 1, 1], colorSpace='rgb',
    ori=0.0,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=False
)

PLAB_pics_2 = visual.ImageStim(
    win=win, name='plab_task2',
    image=task2_img,
    pos=(0, 0.18),
    size=(1.5, 0.6),
    color=[1, 1, 1], colorSpace='rgb',
    ori=0.0,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=False
)


def run_plab_block(trials, task_name, task_image_stim, keyboard_component):
    global routineTimer

    for this_trial in trials:
        valid_answer = False
        chosen_key = None

        question_id = this_trial['question_id']
        question = sanitize_text(this_trial['question'])
        options = [
            sanitize_text(this_trial['option_a']),
            sanitize_text(this_trial['option_b']),
            sanitize_text(this_trial['option_c']),
            sanitize_text(this_trial['option_d']),
        ]
        correct_key = str(this_trial['correct_key'])

        block_img_path = rendered_text_dir / f"{task_name}_{question_id}_block.png"
        block_img_path, option_boxes_px = render_question_option_block_to_image(
            question=question,
            options=options,
            language_code=language,
            font_path=font_path,
            out_path=str(block_img_path),
            image_width=1600,
            image_height=700,
            question_font_size=42 if is_rtl else 44,
            option_font_size=42 if is_rtl else 44,
            margin_px=80,
            line_spacing_px=18,
            block_gap_px=10
        )

        block_stim = visual.ImageStim(
            win=win,
            image=str(block_img_path),
            pos=(0, -0.28),
            size=(1.15, 0.48),
            units='height',
            interpolate=True
        )

        rects_for_this_trial = []
        img_w_px = 1600
        img_h_px = 700
        stim_w_h = 1.15
        stim_h_h = 0.48

        for (x1, y1, x2, y2) in option_boxes_px:
            cx_px = (x1 + x2) / 2.0
            cy_px = (y1 + y2) / 2.0
            w_px = x2 - x1
            h_px = y2 - y1

            cx = ((cx_px / img_w_px) - 0.5) * stim_w_h
            cy = (0.5 - (cy_px / img_h_px)) * stim_h_h - 0.28
            rw = (w_px / img_w_px) * stim_w_h + 0.05
            rh = (h_px / img_h_px) * stim_h_h + 0.02

            rects_for_this_trial.append(
                visual.Rect(
                    win=win,
                    width=rw,
                    height=rh,
                    pos=(cx, cy),
                    lineColor='red',
                    lineWidth=2,
                    fillColor=None
                )
            )

        keyboard_component.keys = []
        keyboard_component.rt = []
        keyboard_component.clock.reset()
        keyboard_component.clearEvents()
        task_start_time = core.getTime()

        continueRoutine = True
        while continueRoutine:
            task_image_stim.draw()
            block_stim.draw()
            for rect in rects_for_this_trial:
                if rect.autoDraw:
                    rect.draw()

            theseKeys = safe_keyboard_get_keys(keyboard_component)
            fallback_keys = safe_event_get_keys()

            for key in theseKeys:
                key_name = normalize_key_name(key.name)

                if key_name in ['1', '2', '3', '4']:
                    valid_answer = True
                    chosen_key = key_name
                    selected_option_index = int(key_name) - 1
                    for i, rect in enumerate(rects_for_this_trial):
                        rect.setAutoDraw(i == selected_option_index)

                if key_name in ['space', 'return'] and valid_answer:
                    keyboard_component.keys = chosen_key
                    keyboard_component.rt = core.getTime() - task_start_time
                    for rect in rects_for_this_trial:
                        rect.setAutoDraw(False)
                    continueRoutine = False
                    break

                if key_name == 'escape':
                    core.quit()

            if continueRoutine:
                for key_name in fallback_keys:
                    normalized_key = normalize_key_name(key_name)

                    if normalized_key in ['1', '2', '3', '4']:
                        valid_answer = True
                        chosen_key = normalized_key
                        selected_option_index = int(normalized_key) - 1
                        for i, rect in enumerate(rects_for_this_trial):
                            rect.setAutoDraw(i == selected_option_index)

                    if normalized_key in ['space', 'return'] and valid_answer:
                        keyboard_component.keys = chosen_key
                        keyboard_component.rt = core.getTime() - task_start_time
                        for rect in rects_for_this_trial:
                            rect.setAutoDraw(False)
                        continueRoutine = False
                        break

                    if normalized_key == 'escape':
                        core.quit()

            if continueRoutine:
                win.flip()

        corr = int(str(keyboard_component.keys) == correct_key)

        thisExp.addData('task', task_name)
        thisExp.addData('question_id', question_id)
        thisExp.addData('chosen_key', keyboard_component.keys)
        thisExp.addData('correctness', corr)
        thisExp.addData('rt', keyboard_component.rt)
        thisExp.nextEntry()

        routineTimer = core.CountdownTimer(0.5)
        while routineTimer.getTime() > 0:
            fix_cross.draw()
            win.flip()
            if endExpNow or escape_pressed(defaultKeyboard):
                core.quit()


PLAB_task1_trials = data.TrialHandler(
    nReps=1.0, method='sequential',
    trialList=PLAB_task1_list,
    seed=random_seed, name='PLAB_task1_trials'
)
thisExp.addLoop(PLAB_task1_trials)
run_plab_block(PLAB_task1_trials, 'task1', PLAB_pics_1, PLAB_task1_key)

PLAB_task2_trials = data.TrialHandler(
    nReps=1.0, method='sequential',
    trialList=PLAB_task2_list,
    seed=random_seed, name='PLAB_task2_trials'
)
thisExp.addLoop(PLAB_task2_trials)
run_plab_block(PLAB_task2_trials, 'task2', PLAB_pics_2, PLAB_task2_key)

# ========================================= Done / Goodbye =========================================================

show_text_screen(
    win=win,
    text=done_text_str,
    language_code=language,
    font_name=font,
    font_path=font_path,
    output_dir=rendered_text_dir,
    image_name='done.png',
    height=0.035
)

if is_rtl:
    goodbye_img_path = rendered_text_dir / 'goodbye.png'
    render_text_screen_to_image(
        text=Goodbyetext_str,
        language_code=language,
        font_path=font_path,
        out_path=str(goodbye_img_path),
        font_size=52,
        line_spacing_px=24
    )
    goodbye_stim = visual.ImageStim(
        win=win,
        image=str(goodbye_img_path),
        pos=(0, 0),
        size=(1.8, 1.1),
        units='norm',
        interpolate=True
    )
else:
    goodbye_stim = visual.TextStim(
        win=win,
        text=clean_ltr_text(Goodbyetext_str),
        font=font if font else "Arial",
        pos=(0, 0),
        height=0.05,
        wrapWidth=1.3,
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

goodbye_stim.draw()
win.flip()

# clear old keypresses from the previous screen
event.clearEvents(eventType='keyboard')
core.wait(0.15)

# wait up to 10 seconds, or continue immediately on space/return
keys = event.waitKeys(maxWait=10.0, keyList=['space', 'return', 'escape'])
if keys and 'escape' in keys:
    win.close()
    core.quit()

win.flip()

thisExp.saveAsWideText(filename + '.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()

thisExp.abort()
win.close()
# core.quit()