#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
import pandas as pd
import argparse
import os
import re
import unicodedata
from pathlib import Path

from psychopy import prefs
prefs.hardware['audioLib'] = 'pygame'
prefs.hardware['keyboardBackend'] = 'event'
from psychopy import visual, core, event, sound, data, logging
import random
import yaml
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager

try:
    import arabic_reshaper
except Exception:
    arabic_reshaper = None

try:
    from bidi.algorithm import get_display
except Exception:
    get_display = None

date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

parser = argparse.ArgumentParser(description="Run the WCST test.")
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
random_seed = config_data['random_seed']
font = config_data['font']
rtl_langs = {'fa', 'fas', 'ar', 'ara', 'he', 'heb', 'ur', 'urd'}
is_rtl = str(language).strip().lower() in rtl_langs
text_language_style = 'Arabic' if is_rtl else 'LTR'

if experiment_config_path.exists():
    # Load the experiment configuration if the file exists
    with experiment_config_path.open('r', encoding='utf-8') as file:
        expInfo = yaml.safe_load(file)
        participant_id_str = str(expInfo['participant_id'])
        while len(participant_id_str) < 3:
            participant_id_str = "0" + participant_id_str
        participant_id = participant_id_str
else:
    # Set default values if the file does not exist
    expInfo = {'participant_id': 999, 'session_id': 2}
    participant_id = "999"

# Store info about the experiment session
psychopyVersion = '2023.2.3'
expName = 'WCST'  # from the Builder filename that created this script


# Create folder for task output data
output_path = PROJECT_ROOT / 'data' / results_folder / 'WCST'
output_path.mkdir(parents=True, exist_ok=True)

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = str(
    output_path / (
        f"{language}{country_code}{lab_number}"
        f"_{participant_id}_PT{expInfo['session_id']}_{date}"
    )
)
game_data = []
rendered_text_dir = output_path / f'rendered_text_{date}'
rendered_text_dir.mkdir(parents=True, exist_ok=True)

def resolve_table_file(base_path_without_ext, file_label='input file'):
    candidate_extensions = ('.xlsx', '.csv')
    base_path = Path(base_path_without_ext)
    for extension in candidate_extensions:
        candidate_path = base_path.with_suffix(extension)
        if candidate_path.exists():
            return candidate_path

    tried_paths = ", ".join(str(base_path.with_suffix(ext)) for ext in candidate_extensions)
    raise FileNotFoundError(f"Could not find {file_label}. Tried: {tried_paths}")


instructions_path = resolve_table_file(
    PROJECT_ROOT / 'languages' / language / 'instructions' / f'WCST_instructions_{language.lower()}',
    file_label='WCST instructions file'
)
if instructions_path.suffix.lower() == '.csv':
    instructions_df = pd.read_csv(instructions_path, index_col='screen')
else:
    instructions_df = pd.read_excel(instructions_path, index_col='screen')

def get_instruction_text(df, screen_key, language_code, default=''):
    try:
        value = df.loc[screen_key, language_code]
    except Exception:
        return default
    if pd.isna(value):
        return default
    text = str(value)
    text = text.replace('\\in', '\\n')
    text = text.replace('\\n', '\n')
    return text


welcome_text = get_instruction_text(instructions_df, 'Welcome_text', language, default='Welcome')
success_text = get_instruction_text(instructions_df, 'success_text', language, default='Correct')
fail_text = get_instruction_text(instructions_df, 'fail_text', language, default='Incorrect')
instructions = get_instruction_text(instructions_df, 'WCST_instructions', language, default='')
summary_text = get_instruction_text(instructions_df, 'summary_text', language, default='')
summary_text_list = [line.strip() for line in summary_text.split('\n') if str(line).strip()]
done_text = get_instruction_text(instructions_df, 'done_text', language, default='')
Goodbyetext = get_instruction_text(instructions_df, 'Goodbye_text', language, default='Goodbye')

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.ERROR)  # reduce non-critical runtime warnings on console

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame


# CLASSES
class Card:
    """
    A card class that creates playing card objects.
    Attributes:
    -----------
    number : int
        The number associated with the card
    shape : str
        The shape of the card (e.g., "circle", "square").
    color : str
        The color of the card

    Methods:
    --------
    get_card_property(prop) -> str:
        Returns the requested property of the card. `prop` can be "number", "shape", or "color".

    get_filename() -> str:
        Returns the filename of the image associated with the card.
        _CAUTION_
        Sett window before initialzing any cards.
        Dependent on correct image_path: Sett inside the class. 
        As of now, only works if you actually have png files at the image_path, that are named following the format: number_shape_color.png
        
    get_psychopy(position) -> obj
        Creates a PsychoPy ImageStim object representing the card.
    """
    
    #The directory path where card images are stored and card_size.
    image_path = str(PROJECT_ROOT / 'tasks' / 'WCST' / 'cards')
    card_size = (128,176)
    _pos = None
    window = None
    
    @classmethod
    def set_window(cls,window):
        cls.window = window
    
    def __init__(self,number,shape,color):
        self.number = number
        self.shape = shape
        self.color = color
        self.psypy = self.create_psychopy()
     
        
    def get_card_property(self, prop):
        """
        Function returns one of the properties of the card.
        prop is one of "number", "shape" or "color"
        """
        if prop=="number":
            return self.number
        elif prop=="shape":
            return self.shape
        elif prop=="color":
            return self.color
        else:
            raise AttributeError("Unknown atttribute")
    
    def __repr__(self):
        """
        Returns the string representation of the card object
        str: Card(number,shape,color)
        """
        return "{num},{shape},{color}".format(num=self.number,shape=self.shape, color=self.color)
    
    def get_filename(self): # property possibility
        """Return filename of the image file for that card"""
        fname = os.path.join(self.image_path, "%i_%s_%s.png"%(self.number, self.shape, self.color))
        return fname
    
    def create_psychopy(self, position=(0,0), **kwargs):
        """
        Creates a PsychoPy ImageStim object representing the card.
    
        Parameters:
        -----------
        position : tuple of int, optional
            The (x, y) coordinates for the position of the image in the window.
            Defaults to (0, 0).
    
        Returns:
        --------
        A PsychoPy ImageStim object with the card's image set at the specified position.
        """
        if not Card.window:
            raise ValueError("The window attribute for Card is not set. Use Card.set_window() and give the class a valid psychopy window configuration.")
        ppy_repr = visual.ImageStim(Card.window,image=self.get_filename(),size=(self.card_size),pos=(position), **kwargs)
        return ppy_repr
        
    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, value):
        self._pos = value
        self.psypy.pos = value

        
    def render(self):
        self.psypy.draw()
        
    @property
    def rect(self):
        """A method that gives the cordinates of the card: Used when looking for mouse clicks"""
        width, height = self.card_size
        xpos, ypos = self.psypy.pos
        left = xpos - width / 2
        right = xpos + width / 2
        top = ypos + height / 2
        bottom = ypos - height / 2

        return [left, top, right, bottom]
        

class Stack():
    
    """
    A class that simulates a stack, akin to a deck of cards.
    
    Attributes:
    -----------
    list_of_cards : list[Card1,Card2,Card3]
        A list containing objects of the Card class.
        
    Methods:
    --------
    add(new_card: Card) -> None:
        Adds the given card to the top of the stack.
    
    pop() -> Card:
        Removes and returns the card from the top of the stack.
    
        _CAUTION_
        THe end of the list is conceptualized as the top of the stack
    
    render()
        A function that takes the card at the top of the stack and renders it on screen as psychopy image.
        Also, updates the card with a position argument corresponding to its stack.
    """

    
    def __init__(self,list_of_cards):
        self.list_of_cards = list_of_cards
        
    def __repr__(self):
        return repr(self.list_of_cards)
    
    def __len__(self):
        return len(self.list_of_cards)
    
    def add(self,new_card):
        self.list_of_cards.append(new_card)
    
    def pop(self):
        return self.list_of_cards.pop()
    
    def render(self):
        if self.list_of_cards:
            card = self.list_of_cards[-1]
            card.pos = (self.xpos, self.ypos)
            card.render()


class MainStack(Stack):
    """
    This is the player deck. Its a subclass of the stack class.
    Compiles a a list of card objects and gives it a cordinate position.
    
    Contains data:
        Contains lists of card attributes.
        -numbers-list[int]
        -shapes -list[str]
        -colors -list[str]
        -xpos   -int
        -ypos   -int
    """
    
    xpos = 0
    ypos = -350
    numbers = [1,2,3,4]
    shapes = ["circle","square","triangle","star"]
    colors = ["blue","green","red","yellow"]
    
    def __init__(self):
        self.list_of_cards = []
        for i in self.numbers:
            for y in self.shapes:
                for x in self.colors:
                    card = Card(i,y,x)
                    self.list_of_cards.append(card)
        random.shuffle(self.list_of_cards)
        
    

class DiscardStack(Stack):
    """
    This is a multistack. Its a subclass of the stack class.
    A representation of the stimulus cards and their corresponding discard piles.
    Compiles the stimulus decks and gives them the presett card, rendering cordinates and a clickbox.
    Contains data:
        -xpos_stimcard   -int
        -ypos_discard   -int
        -stimdesign    -dict : contains text information for psychoppy textStim object : Can be changed in class for visual customization.
    Method
    ------
    render()
    Contains a custom renderingg method, specific for this multistack.
    It will always draw the stimulus card, and if there are cards present in the discard stack, the top card will be rendered.
    Additionally, it will draw a psychopy text object on top of the stimulus card, indicating keybord input for choosing that stimulus card.
    """
    
    ypos_stimcard = 300
    ypos_discard = 110
    
    stimdesign  = {
    'font': font,
    'height': 42,
    'color': 'white',
    'bold': True
    }
    
    def __init__(self, num):
        self.list_of_cards=[]
        self.stimulus_card=None
        if num==1:
            self.xpos = -300
            self.stimulus_card=Card(1, "triangle", "red")

        elif num==2:
            self.xpos = -100
            self.stimulus_card=Card(2, "star", "green")
           
        elif num==3:
            self.xpos =  100
            self.stimulus_card=Card(3, "square", "yellow")
          
        elif num==4:
            self.xpos =  300
            self.stimulus_card=Card(4, "circle", "blue")
            
        self.stimulus_card.pos = (self.xpos, self.ypos_stimcard)
        
    def __repr__(self):
        if len(self.list_of_cards)>0:
            card=self.list_of_cards[-1]
        else:
            card="<empty>"
        return "DiscardStack(%s, %s)"%(self.stimulus_card, card)
        
    def render(self):
        # render the stimulus card
        self.stimulus_card.pos = (self.xpos, self.ypos_stimcard)
        self.stimulus_card.render()
        # if there are cards in the discard stack render the top card
        if self.list_of_cards:
            card=self.list_of_cards[-1]
            card.pos = (self.xpos, self.ypos_discard)
            card.render()
        # render the number on top of the stack
        add = {
        'text': self.stimulus_card.number,
        'pos': (self.xpos, self.ypos_stimcard + 110)
        }
        design = DiscardStack.stimdesign.copy()
        design.update(add)
        stim_text = visual.TextStim(win, **design)
        stim_text.draw()




    
# FUNCTIONS

def track(data_point, trial):
    trial.append(data_point)
    return trial

def matched_category(rules,choice,card,stim_card):
    """" parameters: 
        a function that takes in, a list of matching categories 'aka' rules, and two card objects
        returns: a list of strings that contain the categories on which the cards are matched """
    matched = []
    for rule in rules:
        if card.get_card_property(rule) == stim_card.get_card_property(rule):
            matched.append(rule)
    return matched
    

def random_key(key_length):
    """A function that makes a random string of letters and numbers
    Parameters: lenght of string as int
    Returns: -> str
    """
    key = []
    alpha = "abcdefghijklmnopqrstuvwxyz"
    num = "123456789"
    for i in range(key_length):
        l = random.choice(alpha)
        n = random.choice(num)
        if int(n) % 2 == 0:
            l = l.capitalize()
        key.append(l + n)
    return ''.join(key)

    
    
def save_results(data, filename):
    index = ["rt", "card", "chosen card", "success", "matched on categories", "active rule", "win streak"]
    game_data_dicts = []

    for trial_data in data:
        trial_dict = {}
        for i, field in enumerate(index):
            trial_dict[field] = trial_data[i]
        game_data_dicts.append(trial_dict)

    df = pd.DataFrame(game_data_dicts)
    output_filename = f"{filename}.csv"
    df.to_csv(output_filename, index=False)

    

def results(data):
    holder = "blank"
    preservative_error = 0
    index = ["rt", "card","chosen card", "success", "matched on categories", "active rule",  "win streak"]
    # procent_correct
    win_list = [item[3] for item in data]
    total_correct = sum(win_list)
    total_number = len(win_list)
    procent_correct = total_correct /total_number * 100
    
    # Categories completed
    win_streak = [item[6]for item in data]
    completed = [item[6] for item in data if item[6] == 5]
    completed_categories = len(completed)
    
    # Error type
    active_rule = [item[5] for item in data]
    matched_categories = [item[4] for item in data]
    
    for index, (win, rule, matched, streak) in enumerate(zip(win_list, active_rule, matched_categories, win_streak)):
        if streak == 5:
            holder = rule
        if win == False and holder in matched:
            preservative_error += 1
    
    return procent_correct, completed_categories, preservative_error
    
# Build a robust summary message even when the translation has fewer lines.
def build_summary_text(template_lines, percent_correct, categories_completed, preservative_errors):
    defaults = [
        "Correct answers:",
        "Categories completed:",
        "Perseverative errors:",
    ]
    labels = list(template_lines[:3])
    while len(labels) < 3:
        labels.append(defaults[len(labels)])
    return f"{labels[0]} {percent_correct}% \n {labels[1]} {categories_completed} \n {labels[2]} {preservative_errors}"


def get_primary_screen_size(default=(1440, 900)):
    try:
        import pyglet
        screen = pyglet.canvas.get_display().get_default_screen()
        return [int(screen.width), int(screen.height)]
    except Exception:
        return list(default)


def sanitize_text(value):
    if value is None:
        return ''
    text = str(value).replace('\r\n', '\n').replace('\r', '\n')
    text = unicodedata.normalize('NFC', text)
    cleaned = []
    for char in text:
        category = unicodedata.category(char)
        if category in {'Cs', 'Co', 'Cn'}:
            continue
        if category == 'Cc' and char not in ('\n', '\t'):
            continue
        cleaned.append(char)
    return ''.join(cleaned)


def normalize_instruction_text(text):
    text = sanitize_text(text).strip()
    if not text:
        return ''
    if is_rtl:
        lines = text.split('\n')
        cleaned = [re.sub(r'[ \t]+', ' ', line).strip() for line in lines]
        return '\n'.join(cleaned)
    paragraphs = re.split(r'\n\s*\n+', text)
    normalized = []
    for paragraph in paragraphs:
        paragraph = re.sub(r'[\n\t]+', ' ', paragraph)
        paragraph = re.sub(r'\s+', ' ', paragraph).strip()
        if paragraph:
            normalized.append(paragraph)
    return '\n\n'.join(normalized)


def shape_rtl_line(line):
    if arabic_reshaper is None or get_display is None:
        return line
    return get_display(arabic_reshaper.reshape(line))


def prepare_display_text(text):
    language_code = str(language).lower()
    arabic_script_langs = {'ar', 'fa', 'fas', 'ur', 'ug'}
    rtl_non_joining_langs = {'he', 'yi'}
    prepared = sanitize_text(text)
    if language_code in arabic_script_langs and arabic_reshaper is not None and get_display is not None:
        prepared = arabic_reshaper.reshape(prepared)
        prepared = get_display(prepared)
    elif language_code in rtl_non_joining_langs and get_display is not None:
        prepared = get_display(prepared)
    return prepared


def visual_line(line):
    cleaned = sanitize_text(line)
    return prepare_display_text(cleaned) if is_rtl else cleaned


def _get_installed_font_families():
    return {font_item.name for font_item in font_manager.fontManager.ttflist}


def _pick_first_installed(candidates):
    installed = _get_installed_font_families()
    for font_name in candidates:
        if font_name in installed:
            return font_name
    return 'DejaVu Sans'


def get_textstim_font_for_language(language_code, preferred_font):
    code = str(language_code).lower()
    if code in {'ar', 'fa', 'fas', 'ur', 'ug'}:
        return _pick_first_installed(['Noto Naskh Arabic', 'Noto Sans Arabic', 'Arial Unicode MS', 'DejaVu Sans'])
    if code in {'he', 'yi'}:
        return _pick_first_installed(['Noto Sans Hebrew', 'Arial Hebrew', 'Arial Unicode MS', 'DejaVu Sans'])
    if preferred_font:
        return _pick_first_installed([preferred_font, 'Arial Unicode MS', 'Arial', 'Helvetica Neue', 'DejaVu Sans'])
    return _pick_first_installed(['Arial Unicode MS', 'Arial', 'Helvetica Neue', 'DejaVu Sans'])


def resolve_font_path(preferred_font_name):
    try:
        found = font_manager.findfont(preferred_font_name, fallback_to_default=False)
        if found and Path(found).exists():
            return found
    except Exception:
        pass
    fallback = font_manager.findfont('DejaVu Sans')
    if fallback and Path(fallback).exists():
        return fallback
    raise FileNotFoundError(f"Could not resolve a font path for '{preferred_font_name}'.")


def choose_font_path():
    if is_rtl:
        return resolve_font_path('DejaVu Sans')
    return resolve_font_path(font if font else 'Arial')


def measure_text_pil(draw, text, font_obj):
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text_to_lines(text, draw, font_obj, max_width_px):
    normalized = normalize_instruction_text(text)
    if not normalized:
        return []
    paragraphs = normalized.split('\n') if is_rtl else normalized.split('\n\n')
    all_lines = []
    for idx, paragraph in enumerate(paragraphs):
        if not paragraph:
            all_lines.append('')
            continue
        words = paragraph.split()
        current = []
        for word in words:
            candidate_logical = ' '.join(current + [word])
            candidate_visual = visual_line(candidate_logical)
            width, _ = measure_text_pil(draw, candidate_visual, font_obj)
            if width <= max_width_px or not current:
                current.append(word)
            else:
                all_lines.append(' '.join(current))
                current = [word]
        if current:
            all_lines.append(' '.join(current))
        if not is_rtl and idx < len(paragraphs) - 1:
            all_lines.append('')
    return all_lines


def render_text_screen_to_image(text, out_path, font_path, image_width=1800, image_height=1100, font_size=56, margin_px=150):
    image = Image.new('RGBA', (image_width, image_height), color=(255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    font_obj = ImageFont.truetype(font_path, font_size)
    max_width_px = image_width - 2 * margin_px
    logical_lines = wrap_text_to_lines(text, draw, font_obj, max_width_px)
    display_lines = [visual_line(line) if line else '' for line in logical_lines]

    line_spacing_px = max(16, font_size // 3)
    line_heights = []
    for line in display_lines:
        _, line_height = measure_text_pil(draw, line if line else ' ', font_obj)
        line_heights.append(line_height if line else font_size // 2)

    total_height = 0
    for i, height in enumerate(line_heights):
        total_height += height
        if i < len(line_heights) - 1:
            total_height += line_spacing_px
    y = max(20, (image_height - total_height) // 2)

    for i, line in enumerate(display_lines):
        if line == '':
            y += line_heights[i] + line_spacing_px
            continue
        width, height = measure_text_pil(draw, line, font_obj)
        x = (image_width - width) // 2
        draw.text((x, y), line, font=font_obj, fill='black')
        y += height + line_spacing_px

    image.save(out_path)
    return out_path


def show_text_screen(win, text, image_name, font_name, font_path, height=30, wait_keys=('space', 'escape'), auto_wait=None):
    # Ensure no previous frame content leaks into this screen.
    try:
        win.clearBuffer()
    except Exception:
        win.flip(clearBuffer=True)

    if is_rtl:
        image_path = rendered_text_dir / image_name
        render_text_screen_to_image(text=text, out_path=str(image_path), font_path=font_path, font_size=60 if height >= 36 else 50)
        screen_stim = visual.ImageStim(
            win=win,
            image=str(image_path),
            pos=(0, 0),
            size=(1800, 1100),
            units='pix',
            interpolate=True
        )
    else:
        screen_stim = visual.TextStim(
            win=win,
            text=text,
            font=font_name,
            pos=(0, 0),
            height=height,
            wrapWidth=1000,
            color='black',
            colorSpace='rgb',
            languageStyle=text_language_style,
            alignText='center',
            anchorHoriz='center',
            anchorVert='center'
        )

    screen_stim.draw()
    win.flip()
    event.clearEvents(eventType='keyboard')

    if auto_wait is not None:
        core.wait(auto_wait)
        return

    while True:
        keys = event.waitKeys(keyList=list(wait_keys))
        if keys and 'escape' in keys:
            win.close()
            core.quit()
        if keys and 'space' in keys:
            return


_mouse_backend_warning_shown = False
feedback_font = get_textstim_font_for_language(language, font)


def safe_mouse_left_pressed(mouse_obj):
    global _mouse_backend_warning_shown
    try:
        return bool(mouse_obj.getPressed()[0])
    except Exception as exc:
        if not _mouse_backend_warning_shown:
            logging.info(f"mouse.getPressed failed on this backend: {exc}. Falling back to keyboard-only response mode.")
            _mouse_backend_warning_shown = True
        return False


def safe_mouse_pos(mouse_obj):
    global _mouse_backend_warning_shown
    try:
        return mouse_obj.getPos()
    except Exception as exc:
        if not _mouse_backend_warning_shown:
            logging.info(f"mouse.getPos failed on this backend: {exc}. Falling back to keyboard-only response mode.")
            _mouse_backend_warning_shown = True
        return None


success = {
    'text': visual_line(success_text),
    'font': feedback_font,
    'height': 42,
    'color': 'green',
    'bold': True,
    'italic': False,
    'pos': (0, -100),
    'languageStyle': 'LTR',
    'alignText': 'center',
    'anchorHoriz': 'center',
    'anchorVert': 'center'
}

fail = {
    'text': visual_line(fail_text),
    'font': feedback_font,
    'height': 42,
    'color': 'red',
    'bold': True,
    'italic': False,
    'pos': (0, -50),
    'languageStyle': 'LTR',
    'alignText': 'center',
    'anchorHoriz': 'center',
    'anchorVert': 'center'
}


# GAME_SETUP

# Window settings
win = visual.Window(
    size=get_primary_screen_size(), fullscr=True, screen=0,
    # winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, units="pix", checkTiming=False)
ui_font_path = choose_font_path()

Card.set_window(win) # Pass in the window for the card class


# Create stacks of cards
mainstack = MainStack()
dstacks = {i:DiscardStack(i) for i in range(1,5)}

# initialize
rules = ["shape", "color", "number"]
active_rule = random.choice(rules)
win_streak=0
# text_input = visual.TextBox2(win=window, text='Write your username: ')

#SOUNDS
# Create a sound object from an audio file, but keep WCST runnable when audio backend is unavailable.
sound_file = PROJECT_ROOT / 'tasks' / 'WCST' / 'sounds' / 'win.wav'
win_music = None
try:
    win_music = sound.Sound(str(sound_file))
except Exception as exc:
    logging.info(f"Could not initialize WCST feedback sound: {exc}. Continuing without sound feedback.")

#LOGO
# logo = visual.ImageStim(window,image="../logo/logo.png",pos=(0,300),size=(300,300))

# GAME


# Start screen
keys_clock = core.Clock()

show_text_screen(
    win=win,
    text=welcome_text,
    image_name='welcome.png',
    font_name=font,
    font_path=ui_font_path,
    height=36
)

    
## instructions
show_text_screen(
    win=win,
    text=instructions,
    image_name='instructions.png',
    font_name=font,
    font_path=ui_font_path,
    height=30
)
        
mouse = event.Mouse()

#Main loop
while len(mainstack):
    
    trial = [] # initialize a trial data list

    # Render the top card of the stack
    mainstack.render()
    
    # Render top card of discard stack and the corresponding stimcards
    for stack in dstacks.values():
        stack.render()
          

    # Update window
    win.flip()
    
    choice = None
    keys_clock.reset()
    while choice is None:
        # Check for mouse click first
        if safe_mouse_left_pressed(mouse):  # [0] corresponds to the left mouse button
            mouse_pos = safe_mouse_pos(mouse)
            if mouse_pos is None:
                continue
            for i, dstack in dstacks.items():
                rect = dstack.stimulus_card.rect
                if (rect[0] <= mouse_pos[0] <= rect[2] and rect[1] >= mouse_pos[1] >= rect[3]): #left,top,right,bottom
                    choice = i
                    break
        else:
            # If no mouse click, wait for keyboard input
            keys = event.getKeys(keyList=['1','2','3','4', 'escape'], timeStamped=keys_clock)
            for key, rt in keys:
                if key == 'escape':
                    win.close()
                    core.quit()
                elif key in ['1', '2', '3', '4']:
                    choice = int(key)
                    track(rt, trial)

    # Pop the top card from the mainstack and put it in the right discard pile
    card = mainstack.pop()
    track(card.__repr__(),trial)
    
    dstacks[choice].add(card)
    track(dstacks[choice].stimulus_card.__repr__(),trial)
    

    
    # Feedback
    chosen_card=dstacks[choice].stimulus_card
    correct = card.get_card_property(active_rule)==chosen_card.get_card_property(active_rule)
    track(correct,trial)
    
    if correct:
        if win_music is not None:
            win_music.stop()
            win_music.play()
        win_streak += 1 
        text = visual.TextStim(win, **success)
        text.draw()
    else:
        win_streak = 0
        text = visual.TextStim(win, **fail)
        text.draw()
        
    # Logg results
    match = matched_category(rules, choice, card, chosen_card)
    track(match,trial)
    track(active_rule,trial)
    track(win_streak,trial)
    # Change rule if streak is more than 5   
    if win_streak >= 5:
        active_rule=random.choice(list(set(rules).difference([active_rule])))
        win_streak = 0
    
    game_data.append(trial)
    # print(game_data)

# Data analysis for end screen
p, c, e = results(game_data)
pro = int(p)
log_message = f"You got a total of {pro}% correct. You completed a total of {c} categories. Preservative errors: {e}"
logging.log(level=logging.DATA, msg=log_message)

save_results(game_data, filename)

# show_text_screen(
#     win=win,
#     text=build_summary_text(summary_text_list, pro, c, e),
#     image_name='summary.png',
#     font_name=font,
#     font_path=ui_font_path,
#     height=30,
#     auto_wait=8
# )

if done_text.strip():
    show_text_screen(
        win=win,
        text=done_text,
        image_name='done.png',
        font_name=font,
        font_path=ui_font_path,
        height=30
    )

# End of task message
show_text_screen(
    win=win,
    text=Goodbyetext,
    image_name='goodbye.png',
    font_name=font,
    font_path=ui_font_path,
    height=30
)
win.close()

# core.quit()
