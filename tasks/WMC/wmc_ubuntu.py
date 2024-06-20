#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2020.2.10),
    on Thu 03 Nov 2022 09:55:04 PM CET
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
prefs.hardware['audioLib'] = 'pygame'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
import os  # handy system and path functions
import sys  # to get file system encoding
import yaml
from psychopy.hardware import keyboard
from datetime import datetime

date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # add a simple timestamp

# Path to the YAML file contains the language and experiment configurations
config_path = f'configs/config.yaml'
experiment_config_path = f'configs/experiment.yaml'

# Load the YAML file
with open(config_path, 'r', encoding="utf-8") as file:
    config_data = yaml.safe_load(file)
language = config_data['language']
country_code = config_data['country_code']
lab_number = config_data['lab_number']
random_seed = config_data['random_seed']

if os.path.exists(experiment_config_path):
    # Load the experiment configuration if the file exists
    with open(experiment_config_path, 'r', encoding="utf-8") as file:
        expInfo = yaml.safe_load(file)
        participant_id_str = str(expInfo['participant_id'])
        while len(participant_id_str) < 3:
            participant_id_str = "0" + participant_id_str
        participant_id = participant_id_str
else:
    # Set default values if the file does not exist
    expInfo = {'participant_id': 999, 'session_id': 2}

psychopyVersion = '2023.2.3'
expName = 'WMC'

dlg = gui.Dlg(title=expName)
dlg.addText('Please choose the tasks you want to run; we recommend running all tasks.')
dlg.addField('Memory Update', True)
dlg.addField('Operation Span', True)
dlg.addField('Sentence Span', True)
dlg.addField('Spatial Short Term Memory', True)

ok_data = dlg.show()
if dlg.OK:  # The user pressed OK
    user_entered = dlg.data
    field_names = ['Memory Update', 'Operation Span', 'Sentence Span',
                   'Spatial Short Term Memory', 'Random Seed']
    wmcInfo = dict(zip(field_names, user_entered))
    expInfo.update(wmcInfo)
    print("User entered:", wmcInfo)
else:
    core.quit()

# Create folder name for the results
results_folder = f"{participant_id}_{language}_{country_code}_{lab_number}_PT{expInfo['session_id']}"

# Create folder for audio and csv data
output_path = f'data/psychometric_test_{language}_{country_code}_{lab_number}/WMC/{results_folder}/'
os.makedirs(output_path, exist_ok=True)

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = f"{output_path}" \
           f"{language}{country_code}{lab_number}" \
           f"_{participant_id}_PT{expInfo['session_id']}_{date}"

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name='WMC', version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\danie\\Documents\\workspace\\wmc-battery\\wmc_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1440, 900], fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=True,
    monitor='testMonitor', color='white', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Setup eyetracking
ioDevice = ioConfig = ioSession = ioServer = eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "base_init"
base_initClock = core.Clock()
import os

from psychopy.hardware.keyboard import Keyboard
from common.config import WMCConfig
from common.experiment_messages import ExperimentMessages
from common.instructions import Instructions

# for catching experiment quit key
experiment_keyboard = Keyboard()

thisExp.extraInfo['datetime'] = datetime.today()

subject_id = thisExp.extraInfo['participant_id']
assert subject_id is not None, 'Please specify a participant id'
assert subject_id != '', 'Please specify a participant id'

language = thisExp.extraInfo['language']

config = WMCConfig(language=language)
expmsgs = ExperimentMessages(language=language,
                             encoding=config.experiment_messages.encoding)
instructions = Instructions(language)

do_mu_task = thisExp.extraInfo['Memory Update']
do_os_task = thisExp.extraInfo['Operation Span']
do_ss_task = thisExp.extraInfo['Sentence Span']
do_sstm_task = thisExp.extraInfo['Spatial Short Term Memory']

if random_seed is None or random_seed == '':
    random_seed = subject_id

# set text wrap width to 90% of screen width (in height units)
text_wrap_width = win.size[0] / win.size[1] * 0.9


# Initialize components for Routine "base_instruction"
base_instructionClock = core.Clock()
base_image_instruction = visual.ImageStim(
    win=win,
    name='base_image_instruction', units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=1.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
base_key_resp_instruction = keyboard.Keyboard()
base_aperture_instruction = visual.Aperture(
    win=win, name='base_aperture_instruction',
    units='height', size=10, pos=(0, 0))
base_aperture_instruction.disable()  # disable until its actually used

# Initialize components for Routine "mu_init"
mu_initClock = core.Clock()

# Initialize components for Routine "base_instruction"
base_instructionClock = core.Clock()
base_image_instruction = visual.ImageStim(
    win=win,
    name='base_image_instruction', units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=1.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
base_key_resp_instruction = keyboard.Keyboard()
base_aperture_instruction = visual.Aperture(
    win=win, name='base_aperture_instruction',
    units='height', size=10, pos=(0, 0))
base_aperture_instruction.disable()  # disable until its actually used

# Initialize components for Routine "base_init_task"
base_init_taskClock = core.Clock()
base_text_begin_task = visual.TextStim(win=win, name='base_text_begin_task',
    text='default text',
    font=config.experiment_messages.font,
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_key_resp_task_begin = keyboard.Keyboard()

# Initialize components for Routine "base_init_trial"
base_init_trialClock = core.Clock()

# Initialize components for Routine "mu_init_trial"
mu_init_trialClock = core.Clock()
mu_text_blank = visual.TextStim(win=win, name='mu_text_blank',
    text=None,
    font='Arial',
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "mu_display_digit"
mu_display_digitClock = core.Clock()
mu_text_digit = visual.TextStim(win=win, name='mu_text_digit',
    text='default text',
    font=config.memory_update.text.font,
    units='height', pos=[0,0], height=config.memory_update.text.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "mu_empty_cells"
mu_empty_cellsClock = core.Clock()
mu_text_blank_2 = visual.TextStim(win=win, name='mu_text_blank_2',
    text=None,
    font=config.memory_update.text.font,
    units='height', pos=(0, 0), height=config.memory_update.text.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "mu_display_operation"
mu_display_operationClock = core.Clock()
mu_text_operation = visual.TextStim(win=win, name='mu_text_operation',
    text='default text',
    font=config.memory_update.text.font,
    units='height', pos=[0,0], height=config.memory_update.text.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "mu_empty_cells"
mu_empty_cellsClock = core.Clock()
mu_text_blank_2 = visual.TextStim(win=win, name='mu_text_blank_2',
    text=None,
    font=config.memory_update.text.font,
    units='height', pos=(0, 0), height=config.memory_update.text.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "mu_recall"
mu_recallClock = core.Clock()
mu_text_question_mark = visual.TextStim(win=win, name='mu_text_question_mark',
    text='?',
    font=config.memory_update.text.font,
    units='height', pos=[0,0], height=config.memory_update.text.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
mu_key_resp_recall = keyboard.Keyboard()

# Initialize components for Routine "mu_display_recall"
mu_display_recallClock = core.Clock()
mu_text_recall = visual.TextStim(win=win, name='mu_text_recall',
    text='default text',
    font=config.memory_update.text.font,
    pos=[0,0], height=config.memory_update.text.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "base_next_trial"
base_next_trialClock = core.Clock()
base_text_next_trial = visual.TextStim(win=win, name='base_text_next_trial',
    text='default text',
    font=config.experiment_messages.font,
    pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_next_trial_key_resp = keyboard.Keyboard()

# Initialize components for Routine "base_intertrial"
base_intertrialClock = core.Clock()
base_text_intertrial = visual.TextStim(win=win, name='base_text_intertrial',
    text=None,
    font='Arial',
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "base_task_end"
base_task_endClock = core.Clock()
base_text_task_end = visual.TextStim(win=win, name='base_text_task_end',
    text='default text',
    font=config.experiment_messages.font,
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_key_resp_task_end = keyboard.Keyboard()

# Initialize components for Routine "os_init"
os_initClock = core.Clock()

# Initialize components for Routine "base_instruction"
base_instructionClock = core.Clock()
base_image_instruction = visual.ImageStim(
    win=win,
    name='base_image_instruction', units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=1.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
base_key_resp_instruction = keyboard.Keyboard()
base_aperture_instruction = visual.Aperture(
    win=win, name='base_aperture_instruction',
    units='height', size=10, pos=(0, 0))
base_aperture_instruction.disable()  # disable until its actually used

# Initialize components for Routine "base_init_task"
base_init_taskClock = core.Clock()
base_text_begin_task = visual.TextStim(win=win, name='base_text_begin_task',
    text='default text',
    font=config.experiment_messages.font,
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_key_resp_task_begin = keyboard.Keyboard()

# Initialize components for Routine "base_init_trial"
base_init_trialClock = core.Clock()

# Initialize components for Routine "os_init_trial"
os_init_trialClock = core.Clock()
os_text_fixation_cross = visual.TextStim(win=win, name='os_text_fixation_cross',
    text='+',
    font=config.operation_span.text.fixation_cross.font,
    units='height', pos=(0, 0), height=config.operation_span.text.fixation_cross.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "os_equation"
os_equationClock = core.Clock()
os_text_equation = visual.TextStim(win=win, name='os_text_equation',
    text='default text',
    font=config.operation_span.text.letters.font,
    units='height', pos=(0, 0), height=config.operation_span.text.equations.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
os_key_resp_equation = keyboard.Keyboard()

# Initialize components for Routine "os_letter"
os_letterClock = core.Clock()
os_text_letter = visual.TextStim(win=win, name='os_text_letter',
    text='default text',
    font=config.operation_span.text.letters.font,
    units='height', pos=(0, 0), height=config.operation_span.text.letters.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "os_blank"
os_blankClock = core.Clock()
os_text_blank = visual.TextStim(win=win, name='os_text_blank',
    text=None,
    font='Arial',
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "os_recall"
os_recallClock = core.Clock()
os_text_question_mark = visual.TextStim(win=win, name='os_text_question_mark',
    text='?',
    font=config.operation_span.text.letters.font,
    units='height', pos=(0, 0), height=config.operation_span.text.letters.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
os_key_resp_recall = keyboard.Keyboard()

# Initialize components for Routine "os_display_recall"
os_display_recallClock = core.Clock()
os_text_recall = visual.TextStim(win=win, name='os_text_recall',
    text='default text',
    font=config.operation_span.text.letters.font,
    units='height', pos=(0.075, 0), height=config.operation_span.text.letters.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "base_intertrial"
base_intertrialClock = core.Clock()
base_text_intertrial = visual.TextStim(win=win, name='base_text_intertrial',
    text=None,
    font='Arial',
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "base_self_paced_break"
base_self_paced_breakClock = core.Clock()
base_text_self_paced_break = visual.TextStim(win=win, name='base_text_self_paced_break',
    text='default text',
    font=config.experiment_messages.font,
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_key_resp_self_paced_break = keyboard.Keyboard()

# Initialize components for Routine "base_after_break_pause"
base_after_break_pauseClock = core.Clock()
base_text_pause_after_break = visual.TextStim(win=win, name='base_text_pause_after_break',
    text=None,
    font='Arial',
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "base_task_end"
base_task_endClock = core.Clock()
base_text_task_end = visual.TextStim(win=win, name='base_text_task_end',
    text='default text',
    font=config.experiment_messages.font,
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_key_resp_task_end = keyboard.Keyboard()

# Initialize components for Routine "ss_init"
ss_initClock = core.Clock()

# Initialize components for Routine "base_instruction"
base_instructionClock = core.Clock()
base_image_instruction = visual.ImageStim(
    win=win,
    name='base_image_instruction', units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=1.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
base_key_resp_instruction = keyboard.Keyboard()
base_aperture_instruction = visual.Aperture(
    win=win, name='base_aperture_instruction',
    units='height', size=10, pos=(0, 0))
base_aperture_instruction.disable()  # disable until its actually used

# Initialize components for Routine "base_init_task"
base_init_taskClock = core.Clock()
base_text_begin_task = visual.TextStim(win=win, name='base_text_begin_task',
    text='default text',
    font=config.experiment_messages.font,
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_key_resp_task_begin = keyboard.Keyboard()

# Initialize components for Routine "base_init_trial"
base_init_trialClock = core.Clock()

# Initialize components for Routine "ss_init_trial"
ss_init_trialClock = core.Clock()
ss_text_fixation_cross = visual.TextStim(win=win, name='ss_text_fixation_cross',
    text='+',
    font=config.sentence_span.text.fixation_cross.font,
    units='height', pos=(0, 0), height=config.sentence_span.text.fixation_cross.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "ss_sentence"
ss_sentenceClock = core.Clock()
ss_text_sentence = visual.TextStim(win=win, name='ss_text_sentence',
    text='default text',
    font=config.sentence_span.text.sentences.font,
    units='height', pos=(0, 0), height=config.sentence_span.text.sentences.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
ss_key_resp_sentence = keyboard.Keyboard()

# Initialize components for Routine "ss_letter"
ss_letterClock = core.Clock()
ss_text_letter = visual.TextStim(win=win, name='ss_text_letter',
    text='default text',
    font=config.sentence_span.text.letters.font,
    units='height', pos=(0, 0), height=config.sentence_span.text.letters.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "ss_blank"
ss_blankClock = core.Clock()
ss_text_blank = visual.TextStim(win=win, name='ss_text_blank',
    text=None,
    font='Arial',
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "ss_recall"
ss_recallClock = core.Clock()
ss_text_question_mark = visual.TextStim(win=win, name='ss_text_question_mark',
    text='?',
    font=config.sentence_span.text.letters.font,
    units='height', pos=(0, 0), height=config.sentence_span.text.letters.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
ss_key_resp_recall = keyboard.Keyboard()

# Initialize components for Routine "ss_display_recall"
ss_display_recallClock = core.Clock()
ss_text_display_recall = visual.TextStim(win=win, name='ss_text_display_recall',
    text='default text',
    font=config.sentence_span.text.letters.font,
    units='height', pos=(0.075, 0), height=config.sentence_span.text.letters.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "base_intertrial"
base_intertrialClock = core.Clock()
base_text_intertrial = visual.TextStim(win=win, name='base_text_intertrial',
    text=None,
    font='Arial',
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "base_self_paced_break"
base_self_paced_breakClock = core.Clock()
base_text_self_paced_break = visual.TextStim(win=win, name='base_text_self_paced_break',
    text='default text',
    font=config.experiment_messages.font,
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_key_resp_self_paced_break = keyboard.Keyboard()

# Initialize components for Routine "base_after_break_pause"
base_after_break_pauseClock = core.Clock()
base_text_pause_after_break = visual.TextStim(win=win, name='base_text_pause_after_break',
    text=None,
    font='Arial',
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "base_task_end"
base_task_endClock = core.Clock()
base_text_task_end = visual.TextStim(win=win, name='base_text_task_end',
    text='default text',
    font=config.experiment_messages.font,
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_key_resp_task_end = keyboard.Keyboard()

# Initialize components for Routine "sstm_init"
sstm_initClock = core.Clock()

# Initialize components for Routine "base_instruction"
base_instructionClock = core.Clock()
base_image_instruction = visual.ImageStim(
    win=win,
    name='base_image_instruction', units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=1.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
base_key_resp_instruction = keyboard.Keyboard()
base_aperture_instruction = visual.Aperture(
    win=win, name='base_aperture_instruction',
    units='height', size=10, pos=(0, 0))
base_aperture_instruction.disable()  # disable until its actually used

# Initialize components for Routine "base_init_task"
base_init_taskClock = core.Clock()
base_text_begin_task = visual.TextStim(win=win, name='base_text_begin_task',
    text='default text',
    font=config.experiment_messages.font,
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_key_resp_task_begin = keyboard.Keyboard()

# Initialize components for Routine "base_init_trial"
base_init_trialClock = core.Clock()

# Initialize components for Routine "sstm_init_trial"
sstm_init_trialClock = core.Clock()
sstm_text_fixation_cross = visual.TextStim(win=win, name='sstm_text_fixation_cross',
    text='+',
    font=config.spatial_short_term_memory.text.fixation_cross.font,
    units='height', pos=(0, 0), height=config.spatial_short_term_memory.text.fixation_cross.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "sstm_empty_grid"
sstm_empty_gridClock = core.Clock()
sstm_text_blank = visual.TextStim(win=win, name='sstm_text_blank',
    text=None,
    font='Arial',
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "sstm_display_dot"
sstm_display_dotClock = core.Clock()
sstm_polygon_display_dot = visual.Polygon(
    win=win, name='sstm_polygon_display_dot',units='height', 
    edges=128, size=[1.0, 1.0],
    ori=0, pos=[0,0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='black', fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)

# Initialize components for Routine "sstm_after_display_dot"
sstm_after_display_dotClock = core.Clock()
sstm_text_after_display_dot = visual.TextStim(win=win, name='sstm_text_after_display_dot',
    text=None,
    font='Arial',
    units='height', pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "sstm_draw_request"
sstm_draw_requestClock = core.Clock()
text_sstm_draw_dots = visual.TextStim(win=win, name='text_sstm_draw_dots',
    text='default text',
    font=config.spatial_short_term_memory.text.draw_text.font,
    units='height', pos=(0, -0.075), height=config.spatial_short_term_memory.text.draw_text.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
text_sstm_presentation_end = visual.TextStim(win=win, name='text_sstm_presentation_end',
    text='default text',
    font=config.spatial_short_term_memory.text.end_text.font,
    pos=(0, 0.075), height=config.spatial_short_term_memory.text.end_text.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);

# Initialize components for Routine "sstm_recall"
sstm_recallClock = core.Clock()
sstm_text_next = visual.TextStim(win=win, name='sstm_text_next',
    text='default text',
    font=config.spatial_short_term_memory.text.next_button.font,
    units='height', pos=(10, 10), height=config.spatial_short_term_memory.text.next_button.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
sstm_mouse = event.Mouse(win=win)
x, y = [None, None]
sstm_mouse.mouseClock = core.Clock()

# Initialize components for Routine "base_next_trial"
base_next_trialClock = core.Clock()
base_text_next_trial = visual.TextStim(win=win, name='base_text_next_trial',
    text='default text',
    font=config.experiment_messages.font,
    pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_next_trial_key_resp = keyboard.Keyboard()

# Initialize components for Routine "base_intertrial"
base_intertrialClock = core.Clock()
base_text_intertrial = visual.TextStim(win=win, name='base_text_intertrial',
    text=None,
    font='Arial',
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "sstm_task_end"
sstm_task_endClock = core.Clock()
text_sstm_task_end = visual.TextStim(win=win, name='text_sstm_task_end',
    text=expmsgs.task_over,
    font=config.experiment_messages.font,
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
sstm_key_resp_task_end = keyboard.Keyboard()

# Initialize components for Routine "base_end"
base_endClock = core.Clock()
base_text_end = visual.TextStim(win=win, name='base_text_end',
    text='default text',
    font=config.experiment_messages.font,
    units='height', pos=(0, 0), height=config.experiment_messages.size, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
base_key_resp_end = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "base_init"-------
continueRoutine = True
# update component parameters for each repeat
instruction_filepaths = instructions.get_instructions('init')
win.mouseVisible = False
sstm_mouse.setVisible(False)


# task initialization is done at the experiment beginning
# to circumvent lag when generating dots
if do_sstm_task:
    from tasks.spatial_short_term_memory import SpatialShortTermMemoryTask
    sstm_task = SpatialShortTermMemoryTask(window=win, seed=random_seed, experiment_data=thisExp, config=config.spatial_short_term_memory)

# keep track of which components have finished
base_initComponents = []
for thisComponent in base_initComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
base_initClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "base_init"-------
while continueRoutine:
    # get current time
    t = base_initClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=base_initClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in base_initComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "base_init"-------
for thisComponent in base_initComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "base_init" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "base_instruction"-------
continueRoutine = True
# update component parameters for each repeat
instruction_filepath = instruction_filepaths.pop(0)

# the following is just needed because of a bug in psychopy
# where images will get a grey border. a workaround is
# setting up an aperture to hide these borders.

from PIL import Image
instr_img_size = Image.open(instruction_filepath).size

# set aperture parameters from image size in pixels
aperture_padding = 4
aperture_width = instr_img_size[0] - aperture_padding
aperture_height = instr_img_size[1] - aperture_padding

# height scaling only scales by screen height to keep aspect ratio
aperture_right = aperture_width / 2 / win.size[1]
aperture_top = aperture_height / 2 / win.size[1]

# setup rectangle vertices
aperture_vertices = [
    [aperture_right, aperture_top],
    [aperture_right, -aperture_top],
    [-aperture_right, -aperture_top],
    [-aperture_right, aperture_top],
]

aperture_instruction = visual.Aperture(win, size=1, shape='square', units='height')

base_image_instruction.setSize(instr_img_size)
base_image_instruction.setImage(instruction_filepath)
base_key_resp_instruction.keys = []
base_key_resp_instruction.rt = []
_base_key_resp_instruction_allKeys = []
# keep track of which components have finished
base_instructionComponents = [base_image_instruction, base_key_resp_instruction, base_aperture_instruction]
for thisComponent in base_instructionComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
base_instructionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "base_instruction"-------
while continueRoutine:
    # get current time
    t = base_instructionClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=base_instructionClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
        core.quit()
    
    # *base_image_instruction* updates
    if base_image_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        base_image_instruction.frameNStart = frameN  # exact frame index
        base_image_instruction.tStart = t  # local t and not account for scr refresh
        base_image_instruction.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(base_image_instruction, 'tStartRefresh')  # time at next scr refresh
        base_image_instruction.setAutoDraw(True)
    
    # *base_key_resp_instruction* updates
    waitOnFlip = False
    if base_key_resp_instruction.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        base_key_resp_instruction.frameNStart = frameN  # exact frame index
        base_key_resp_instruction.tStart = t  # local t and not account for scr refresh
        base_key_resp_instruction.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(base_key_resp_instruction, 'tStartRefresh')  # time at next scr refresh
        base_key_resp_instruction.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(base_key_resp_instruction.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(base_key_resp_instruction.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if base_key_resp_instruction.status == STARTED and not waitOnFlip:
        theseKeys = base_key_resp_instruction.getKeys(keyList=None, waitRelease=False)
        _base_key_resp_instruction_allKeys.extend(theseKeys)
        if len(_base_key_resp_instruction_allKeys):
            base_key_resp_instruction.keys = _base_key_resp_instruction_allKeys[-1].name  # just the last key pressed
            base_key_resp_instruction.rt = _base_key_resp_instruction_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *base_aperture_instruction* updates
    if base_aperture_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        base_aperture_instruction.frameNStart = frameN  # exact frame index
        base_aperture_instruction.tStart = t  # local t and not account for scr refresh
        base_aperture_instruction.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(base_aperture_instruction, 'tStartRefresh')  # time at next scr refresh
        base_aperture_instruction.enabled = True
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in base_instructionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "base_instruction"-------
for thisComponent in base_instructionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
del aperture_instruction
thisExp.addData('base_image_instruction.started', base_image_instruction.tStartRefresh)
thisExp.addData('base_image_instruction.stopped', base_image_instruction.tStopRefresh)
# check responses
if base_key_resp_instruction.keys in ['', [], None]:  # No response was made
    base_key_resp_instruction.keys = None
thisExp.addData('base_key_resp_instruction.keys',base_key_resp_instruction.keys)
if base_key_resp_instruction.keys != None:  # we had a response
    thisExp.addData('base_key_resp_instruction.rt', base_key_resp_instruction.rt)
thisExp.addData('base_key_resp_instruction.started', base_key_resp_instruction.tStartRefresh)
thisExp.addData('base_key_resp_instruction.stopped', base_key_resp_instruction.tStopRefresh)
thisExp.nextEntry()
base_aperture_instruction.enabled = False  # just in case it was left enabled
thisExp.addData('base_aperture_instruction.started', base_aperture_instruction.tStartRefresh)
thisExp.addData('base_aperture_instruction.stopped', base_aperture_instruction.tStopRefresh)
# the Routine "base_instruction" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
do_memory_update_dummy = data.TrialHandler(nReps=do_mu_task, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='do_memory_update_dummy')
thisExp.addLoop(do_memory_update_dummy)  # add the loop to the experiment
thisDo_memory_update_dummy = do_memory_update_dummy.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisDo_memory_update_dummy.rgb)
if thisDo_memory_update_dummy != None:
    for paramName in thisDo_memory_update_dummy:
        exec('{} = thisDo_memory_update_dummy[paramName]'.format(paramName))

for thisDo_memory_update_dummy in do_memory_update_dummy:
    currentLoop = do_memory_update_dummy
    # abbreviate parameter names if possible (e.g. rgb = thisDo_memory_update_dummy.rgb)
    if thisDo_memory_update_dummy != None:
        for paramName in thisDo_memory_update_dummy:
            exec('{} = thisDo_memory_update_dummy[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "mu_init"-------
    continueRoutine = True
    # update component parameters for each repeat
    from tasks.memory_update import MemoryUpdateTask
    current_task = MemoryUpdateTask(window=win, seed=random_seed, config=config.memory_update)
    
    instruction_filepaths = instructions.get_instructions('mu')
    n_instruction_pages = instructions.get_instruction_page_count('mu')
    # keep track of which components have finished
    mu_initComponents = []
    for thisComponent in mu_initComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    mu_initClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "mu_init"-------
    while continueRoutine:
        # get current time
        t = mu_initClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=mu_initClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in mu_initComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "mu_init"-------
    for thisComponent in mu_initComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "mu_init" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    mu_instruction_pages = data.TrialHandler(nReps=n_instruction_pages, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='mu_instruction_pages')
    thisExp.addLoop(mu_instruction_pages)  # add the loop to the experiment
    thisMu_instruction_page = mu_instruction_pages.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisMu_instruction_page.rgb)
    if thisMu_instruction_page != None:
        for paramName in thisMu_instruction_page:
            exec('{} = thisMu_instruction_page[paramName]'.format(paramName))
    
    for thisMu_instruction_page in mu_instruction_pages:
        currentLoop = mu_instruction_pages
        # abbreviate parameter names if possible (e.g. rgb = thisMu_instruction_page.rgb)
        if thisMu_instruction_page != None:
            for paramName in thisMu_instruction_page:
                exec('{} = thisMu_instruction_page[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "base_instruction"-------
        continueRoutine = True
        # update component parameters for each repeat
        instruction_filepath = instruction_filepaths.pop(0)
        
        # the following is just needed because of a bug in psychopy
        # where images will get a grey border. a workaround is
        # setting up an aperture to hide these borders.
        
        from PIL import Image
        instr_img_size = Image.open(instruction_filepath).size
        
        # set aperture parameters from image size in pixels
        aperture_padding = 4
        aperture_width = instr_img_size[0] - aperture_padding
        aperture_height = instr_img_size[1] - aperture_padding
        
        # height scaling only scales by screen height to keep aspect ratio
        aperture_right = aperture_width / 2 / win.size[1]
        aperture_top = aperture_height / 2 / win.size[1]
        
        # setup rectangle vertices
        aperture_vertices = [
            [aperture_right, aperture_top],
            [aperture_right, -aperture_top],
            [-aperture_right, -aperture_top],
            [-aperture_right, aperture_top],
        ]
        
        aperture_instruction = visual.Aperture(win, size=1, shape='square', units='height')
        
        base_image_instruction.setSize(instr_img_size)
        base_image_instruction.setImage(instruction_filepath)
        base_key_resp_instruction.keys = []
        base_key_resp_instruction.rt = []
        _base_key_resp_instruction_allKeys = []
        # keep track of which components have finished
        base_instructionComponents = [base_image_instruction, base_key_resp_instruction, base_aperture_instruction]
        for thisComponent in base_instructionComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        base_instructionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "base_instruction"-------
        while continueRoutine:
            # get current time
            t = base_instructionClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=base_instructionClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                core.quit()
            
            # *base_image_instruction* updates
            if base_image_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_image_instruction.frameNStart = frameN  # exact frame index
                base_image_instruction.tStart = t  # local t and not account for scr refresh
                base_image_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_image_instruction, 'tStartRefresh')  # time at next scr refresh
                base_image_instruction.setAutoDraw(True)
            
            # *base_key_resp_instruction* updates
            waitOnFlip = False
            if base_key_resp_instruction.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                base_key_resp_instruction.frameNStart = frameN  # exact frame index
                base_key_resp_instruction.tStart = t  # local t and not account for scr refresh
                base_key_resp_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_key_resp_instruction, 'tStartRefresh')  # time at next scr refresh
                base_key_resp_instruction.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(base_key_resp_instruction.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(base_key_resp_instruction.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if base_key_resp_instruction.status == STARTED and not waitOnFlip:
                theseKeys = base_key_resp_instruction.getKeys(keyList=None, waitRelease=False)
                _base_key_resp_instruction_allKeys.extend(theseKeys)
                if len(_base_key_resp_instruction_allKeys):
                    base_key_resp_instruction.keys = _base_key_resp_instruction_allKeys[-1].name  # just the last key pressed
                    base_key_resp_instruction.rt = _base_key_resp_instruction_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # *base_aperture_instruction* updates
            if base_aperture_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_aperture_instruction.frameNStart = frameN  # exact frame index
                base_aperture_instruction.tStart = t  # local t and not account for scr refresh
                base_aperture_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_aperture_instruction, 'tStartRefresh')  # time at next scr refresh
                base_aperture_instruction.enabled = True
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in base_instructionComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "base_instruction"-------
        for thisComponent in base_instructionComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        del aperture_instruction
        mu_instruction_pages.addData('base_image_instruction.started', base_image_instruction.tStartRefresh)
        mu_instruction_pages.addData('base_image_instruction.stopped', base_image_instruction.tStopRefresh)
        # check responses
        if base_key_resp_instruction.keys in ['', [], None]:  # No response was made
            base_key_resp_instruction.keys = None
        mu_instruction_pages.addData('base_key_resp_instruction.keys',base_key_resp_instruction.keys)
        if base_key_resp_instruction.keys != None:  # we had a response
            mu_instruction_pages.addData('base_key_resp_instruction.rt', base_key_resp_instruction.rt)
        mu_instruction_pages.addData('base_key_resp_instruction.started', base_key_resp_instruction.tStartRefresh)
        mu_instruction_pages.addData('base_key_resp_instruction.stopped', base_key_resp_instruction.tStopRefresh)
        base_aperture_instruction.enabled = False  # just in case it was left enabled
        mu_instruction_pages.addData('base_aperture_instruction.started', base_aperture_instruction.tStartRefresh)
        mu_instruction_pages.addData('base_aperture_instruction.stopped', base_aperture_instruction.tStopRefresh)
        # the Routine "base_instruction" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed n_instruction_pages repeats of 'mu_instruction_pages'
    
    
    # set up handler to look after randomisation of conditions etc
    mu_practice_dummy = data.TrialHandler(nReps=2, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='mu_practice_dummy')
    thisExp.addLoop(mu_practice_dummy)  # add the loop to the experiment
    thisMu_practice_dummy = mu_practice_dummy.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisMu_practice_dummy.rgb)
    if thisMu_practice_dummy != None:
        for paramName in thisMu_practice_dummy:
            exec('{} = thisMu_practice_dummy[paramName]'.format(paramName))
    
    for thisMu_practice_dummy in mu_practice_dummy:
        currentLoop = mu_practice_dummy
        # abbreviate parameter names if possible (e.g. rgb = thisMu_practice_dummy.rgb)
        if thisMu_practice_dummy != None:
            for paramName in thisMu_practice_dummy:
                exec('{} = thisMu_practice_dummy[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "base_init_task"-------
        continueRoutine = True
        # update component parameters for each repeat
        # set begin task message depending on practice
        if current_task.do_practice:
            msg_task_begin = expmsgs.begin_practice
        else:
            msg_task_begin = expmsgs.begin_task
        
        n_trials = current_task.get_trial_count()
        base_text_begin_task.setText(msg_task_begin)
        base_key_resp_task_begin.keys = []
        base_key_resp_task_begin.rt = []
        _base_key_resp_task_begin_allKeys = []
        # keep track of which components have finished
        base_init_taskComponents = [base_text_begin_task, base_key_resp_task_begin]
        for thisComponent in base_init_taskComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        base_init_taskClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "base_init_task"-------
        while continueRoutine:
            # get current time
            t = base_init_taskClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=base_init_taskClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                core.quit()
            
            # *base_text_begin_task* updates
            if base_text_begin_task.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_text_begin_task.frameNStart = frameN  # exact frame index
                base_text_begin_task.tStart = t  # local t and not account for scr refresh
                base_text_begin_task.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_text_begin_task, 'tStartRefresh')  # time at next scr refresh
                base_text_begin_task.setAutoDraw(True)
            
            # *base_key_resp_task_begin* updates
            waitOnFlip = False
            if base_key_resp_task_begin.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                base_key_resp_task_begin.frameNStart = frameN  # exact frame index
                base_key_resp_task_begin.tStart = t  # local t and not account for scr refresh
                base_key_resp_task_begin.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_key_resp_task_begin, 'tStartRefresh')  # time at next scr refresh
                base_key_resp_task_begin.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(base_key_resp_task_begin.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(base_key_resp_task_begin.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if base_key_resp_task_begin.status == STARTED and not waitOnFlip:
                theseKeys = base_key_resp_task_begin.getKeys(keyList=['space'], waitRelease=False)
                _base_key_resp_task_begin_allKeys.extend(theseKeys)
                if len(_base_key_resp_task_begin_allKeys):
                    base_key_resp_task_begin.keys = _base_key_resp_task_begin_allKeys[-1].name  # just the last key pressed
                    base_key_resp_task_begin.rt = _base_key_resp_task_begin_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in base_init_taskComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "base_init_task"-------
        for thisComponent in base_init_taskComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        mu_practice_dummy.addData('base_text_begin_task.started', base_text_begin_task.tStartRefresh)
        mu_practice_dummy.addData('base_text_begin_task.stopped', base_text_begin_task.tStopRefresh)
        # check responses
        if base_key_resp_task_begin.keys in ['', [], None]:  # No response was made
            base_key_resp_task_begin.keys = None
        mu_practice_dummy.addData('base_key_resp_task_begin.keys',base_key_resp_task_begin.keys)
        if base_key_resp_task_begin.keys != None:  # we had a response
            mu_practice_dummy.addData('base_key_resp_task_begin.rt', base_key_resp_task_begin.rt)
        mu_practice_dummy.addData('base_key_resp_task_begin.started', base_key_resp_task_begin.tStartRefresh)
        mu_practice_dummy.addData('base_key_resp_task_begin.stopped', base_key_resp_task_begin.tStopRefresh)
        # the Routine "base_init_task" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        mu_trials = data.TrialHandler(nReps=n_trials, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='mu_trials')
        thisExp.addLoop(mu_trials)  # add the loop to the experiment
        thisMu_trial = mu_trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisMu_trial.rgb)
        if thisMu_trial != None:
            for paramName in thisMu_trial:
                exec('{} = thisMu_trial[paramName]'.format(paramName))
        
        for thisMu_trial in mu_trials:
            currentLoop = mu_trials
            # abbreviate parameter names if possible (e.g. rgb = thisMu_trial.rgb)
            if thisMu_trial != None:
                for paramName in thisMu_trial:
                    exec('{} = thisMu_trial[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "base_init_trial"-------
            continueRoutine = True
            # update component parameters for each repeat
            current_trial = current_task.start_new_trial()
            do_break = current_task.has_pause()
            # keep track of which components have finished
            base_init_trialComponents = []
            for thisComponent in base_init_trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            base_init_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "base_init_trial"-------
            while continueRoutine:
                # get current time
                t = base_init_trialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=base_init_trialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in base_init_trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "base_init_trial"-------
            for thisComponent in base_init_trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "base_init_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "mu_init_trial"-------
            continueRoutine = True
            # update component parameters for each repeat
            n_digits = current_trial.get_n_digits()
            n_operations = current_trial.get_n_operations()
            # keep track of which components have finished
            mu_init_trialComponents = [mu_text_blank]
            for thisComponent in mu_init_trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            mu_init_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "mu_init_trial"-------
            while continueRoutine:
                # get current time
                t = mu_init_trialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=mu_init_trialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # *mu_text_blank* updates
                if mu_text_blank.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    mu_text_blank.frameNStart = frameN  # exact frame index
                    mu_text_blank.tStart = t  # local t and not account for scr refresh
                    mu_text_blank.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mu_text_blank, 'tStartRefresh')  # time at next scr refresh
                    mu_text_blank.setAutoDraw(True)
                if mu_text_blank.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > mu_text_blank.tStartRefresh + current_task.config.timing.init_trial-frameTolerance:
                        # keep track of stop time/frame for later
                        mu_text_blank.tStop = t  # not accounting for scr refresh
                        mu_text_blank.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(mu_text_blank, 'tStopRefresh')  # time at next scr refresh
                        mu_text_blank.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in mu_init_trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "mu_init_trial"-------
            for thisComponent in mu_init_trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            mu_trials.addData('mu_text_blank.started', mu_text_blank.tStartRefresh)
            mu_trials.addData('mu_text_blank.stopped', mu_text_blank.tStopRefresh)
            # the Routine "mu_init_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # set up handler to look after randomisation of conditions etc
            mu_presentations = data.TrialHandler(nReps=n_digits, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='mu_presentations')
            thisExp.addLoop(mu_presentations)  # add the loop to the experiment
            thisMu_presentation = mu_presentations.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisMu_presentation.rgb)
            if thisMu_presentation != None:
                for paramName in thisMu_presentation:
                    exec('{} = thisMu_presentation[paramName]'.format(paramName))
            
            for thisMu_presentation in mu_presentations:
                currentLoop = mu_presentations
                # abbreviate parameter names if possible (e.g. rgb = thisMu_presentation.rgb)
                if thisMu_presentation != None:
                    for paramName in thisMu_presentation:
                        exec('{} = thisMu_presentation[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "mu_display_digit"-------
                continueRoutine = True
                # update component parameters for each repeat
                current_digit, current_digit_position = current_trial.get_next_digit()
                mu_text_digit.setPos(current_digit_position)
                mu_text_digit.setText(current_digit)
                # keep track of which components have finished
                mu_display_digitComponents = [mu_text_digit]
                for thisComponent in mu_display_digitComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                mu_display_digitClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "mu_display_digit"-------
                while continueRoutine:
                    # get current time
                    t = mu_display_digitClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=mu_display_digitClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *mu_text_digit* updates
                    if mu_text_digit.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        mu_text_digit.frameNStart = frameN  # exact frame index
                        mu_text_digit.tStart = t  # local t and not account for scr refresh
                        mu_text_digit.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(mu_text_digit, 'tStartRefresh')  # time at next scr refresh
                        mu_text_digit.setAutoDraw(True)
                    if mu_text_digit.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > mu_text_digit.tStartRefresh + current_task.config.timing.digit-frameTolerance:
                            # keep track of stop time/frame for later
                            mu_text_digit.tStop = t  # not accounting for scr refresh
                            mu_text_digit.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(mu_text_digit, 'tStopRefresh')  # time at next scr refresh
                            mu_text_digit.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in mu_display_digitComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "mu_display_digit"-------
                for thisComponent in mu_display_digitComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                mu_presentations.addData('mu_text_digit.started', mu_text_digit.tStartRefresh)
                mu_presentations.addData('mu_text_digit.stopped', mu_text_digit.tStopRefresh)
                # the Routine "mu_display_digit" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "mu_empty_cells"-------
                continueRoutine = True
                # update component parameters for each repeat
                # keep track of which components have finished
                mu_empty_cellsComponents = [mu_text_blank_2]
                for thisComponent in mu_empty_cellsComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                mu_empty_cellsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "mu_empty_cells"-------
                while continueRoutine:
                    # get current time
                    t = mu_empty_cellsClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=mu_empty_cellsClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *mu_text_blank_2* updates
                    if mu_text_blank_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        mu_text_blank_2.frameNStart = frameN  # exact frame index
                        mu_text_blank_2.tStart = t  # local t and not account for scr refresh
                        mu_text_blank_2.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(mu_text_blank_2, 'tStartRefresh')  # time at next scr refresh
                        mu_text_blank_2.setAutoDraw(True)
                    if mu_text_blank_2.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > mu_text_blank_2.tStartRefresh + current_task.config.timing.inter_item-frameTolerance:
                            # keep track of stop time/frame for later
                            mu_text_blank_2.tStop = t  # not accounting for scr refresh
                            mu_text_blank_2.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(mu_text_blank_2, 'tStopRefresh')  # time at next scr refresh
                            mu_text_blank_2.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in mu_empty_cellsComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "mu_empty_cells"-------
                for thisComponent in mu_empty_cellsComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                mu_presentations.addData('mu_text_blank_2.started', mu_text_blank_2.tStartRefresh)
                mu_presentations.addData('mu_text_blank_2.stopped', mu_text_blank_2.tStopRefresh)
                # the Routine "mu_empty_cells" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed n_digits repeats of 'mu_presentations'
            
            
            # set up handler to look after randomisation of conditions etc
            mu_operations = data.TrialHandler(nReps=n_operations, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='mu_operations')
            thisExp.addLoop(mu_operations)  # add the loop to the experiment
            thisMu_operation = mu_operations.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisMu_operation.rgb)
            if thisMu_operation != None:
                for paramName in thisMu_operation:
                    exec('{} = thisMu_operation[paramName]'.format(paramName))
            
            for thisMu_operation in mu_operations:
                currentLoop = mu_operations
                # abbreviate parameter names if possible (e.g. rgb = thisMu_operation.rgb)
                if thisMu_operation != None:
                    for paramName in thisMu_operation:
                        exec('{} = thisMu_operation[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "mu_display_operation"-------
                continueRoutine = True
                # update component parameters for each repeat
                current_operation, current_operation_position = current_trial.get_next_operation()
                mu_text_operation.setPos(current_operation_position)
                mu_text_operation.setText(current_operation)
                # keep track of which components have finished
                mu_display_operationComponents = [mu_text_operation]
                for thisComponent in mu_display_operationComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                mu_display_operationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "mu_display_operation"-------
                while continueRoutine:
                    # get current time
                    t = mu_display_operationClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=mu_display_operationClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *mu_text_operation* updates
                    if mu_text_operation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        mu_text_operation.frameNStart = frameN  # exact frame index
                        mu_text_operation.tStart = t  # local t and not account for scr refresh
                        mu_text_operation.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(mu_text_operation, 'tStartRefresh')  # time at next scr refresh
                        mu_text_operation.setAutoDraw(True)
                    if mu_text_operation.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > mu_text_operation.tStartRefresh + current_task.config.timing.operation-frameTolerance:
                            # keep track of stop time/frame for later
                            mu_text_operation.tStop = t  # not accounting for scr refresh
                            mu_text_operation.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(mu_text_operation, 'tStopRefresh')  # time at next scr refresh
                            mu_text_operation.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in mu_display_operationComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "mu_display_operation"-------
                for thisComponent in mu_display_operationComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                mu_operations.addData('mu_text_operation.started', mu_text_operation.tStartRefresh)
                mu_operations.addData('mu_text_operation.stopped', mu_text_operation.tStopRefresh)
                # the Routine "mu_display_operation" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "mu_empty_cells"-------
                continueRoutine = True
                # update component parameters for each repeat
                # keep track of which components have finished
                mu_empty_cellsComponents = [mu_text_blank_2]
                for thisComponent in mu_empty_cellsComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                mu_empty_cellsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "mu_empty_cells"-------
                while continueRoutine:
                    # get current time
                    t = mu_empty_cellsClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=mu_empty_cellsClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *mu_text_blank_2* updates
                    if mu_text_blank_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        mu_text_blank_2.frameNStart = frameN  # exact frame index
                        mu_text_blank_2.tStart = t  # local t and not account for scr refresh
                        mu_text_blank_2.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(mu_text_blank_2, 'tStartRefresh')  # time at next scr refresh
                        mu_text_blank_2.setAutoDraw(True)
                    if mu_text_blank_2.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > mu_text_blank_2.tStartRefresh + current_task.config.timing.inter_item-frameTolerance:
                            # keep track of stop time/frame for later
                            mu_text_blank_2.tStop = t  # not accounting for scr refresh
                            mu_text_blank_2.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(mu_text_blank_2, 'tStopRefresh')  # time at next scr refresh
                            mu_text_blank_2.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in mu_empty_cellsComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "mu_empty_cells"-------
                for thisComponent in mu_empty_cellsComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                mu_operations.addData('mu_text_blank_2.started', mu_text_blank_2.tStartRefresh)
                mu_operations.addData('mu_text_blank_2.stopped', mu_text_blank_2.tStopRefresh)
                # the Routine "mu_empty_cells" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed n_operations repeats of 'mu_operations'
            
            
            # set up handler to look after randomisation of conditions etc
            mu_recalls = data.TrialHandler(nReps=n_digits, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='mu_recalls')
            thisExp.addLoop(mu_recalls)  # add the loop to the experiment
            thisMu_recall = mu_recalls.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisMu_recall.rgb)
            if thisMu_recall != None:
                for paramName in thisMu_recall:
                    exec('{} = thisMu_recall[paramName]'.format(paramName))
            
            for thisMu_recall in mu_recalls:
                currentLoop = mu_recalls
                # abbreviate parameter names if possible (e.g. rgb = thisMu_recall.rgb)
                if thisMu_recall != None:
                    for paramName in thisMu_recall:
                        exec('{} = thisMu_recall[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "mu_recall"-------
                continueRoutine = True
                # update component parameters for each repeat
                current_recall = current_trial.get_next_recall()
                recall_position = current_recall['position']
                
                correct_answer_digit = str(current_recall['result'])
                correct_answer = [correct_answer_digit, f'num_{correct_answer_digit}']
                
                thisExp.addData('is_practice', current_task.do_practice)
                thisExp.addData('mu_key_resp_recall.correct_answer', current_recall['result'])
                thisExp.addData('mu_key_resp_recall.position', current_recall['position'])
                thisExp.addData('mu_key_resp_recall.position_id', current_recall['position_id'])
                thisExp.addData('mu_key_resp_recall.operation_sequence', current_recall['operation_sequence'])
                mu_text_question_mark.setPos(recall_position)
                mu_key_resp_recall.keys = []
                mu_key_resp_recall.rt = []
                _mu_key_resp_recall_allKeys = []
                # keep track of which components have finished
                mu_recallComponents = [mu_text_question_mark, mu_key_resp_recall]
                for thisComponent in mu_recallComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                mu_recallClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "mu_recall"-------
                while continueRoutine:
                    # get current time
                    t = mu_recallClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=mu_recallClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *mu_text_question_mark* updates
                    if mu_text_question_mark.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        mu_text_question_mark.frameNStart = frameN  # exact frame index
                        mu_text_question_mark.tStart = t  # local t and not account for scr refresh
                        mu_text_question_mark.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(mu_text_question_mark, 'tStartRefresh')  # time at next scr refresh
                        mu_text_question_mark.setAutoDraw(True)
                    
                    # *mu_key_resp_recall* updates
                    waitOnFlip = False
                    if mu_key_resp_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        mu_key_resp_recall.frameNStart = frameN  # exact frame index
                        mu_key_resp_recall.tStart = t  # local t and not account for scr refresh
                        mu_key_resp_recall.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(mu_key_resp_recall, 'tStartRefresh')  # time at next scr refresh
                        mu_key_resp_recall.status = STARTED
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(mu_key_resp_recall.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(mu_key_resp_recall.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if mu_key_resp_recall.status == STARTED and not waitOnFlip:
                        theseKeys = mu_key_resp_recall.getKeys(keyList=None, waitRelease=False)
                        _mu_key_resp_recall_allKeys.extend(theseKeys)
                        if len(_mu_key_resp_recall_allKeys):
                            mu_key_resp_recall.keys = _mu_key_resp_recall_allKeys[-1].name  # just the last key pressed
                            mu_key_resp_recall.rt = _mu_key_resp_recall_allKeys[-1].rt
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in mu_recallComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "mu_recall"-------
                for thisComponent in mu_recallComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                keyboard_response = mu_key_resp_recall.keys.replace('num_', '')
                is_correct = keyboard_response == str(current_recall['result'])
                
                thisExp.addData('mu_key_resp_recall.response', keyboard_response)
                thisExp.addData('mu_key_resp_recall.is_correct', is_correct)
                
                mu_recalls.addData('mu_text_question_mark.started', mu_text_question_mark.tStartRefresh)
                mu_recalls.addData('mu_text_question_mark.stopped', mu_text_question_mark.tStopRefresh)
                # check responses
                if mu_key_resp_recall.keys in ['', [], None]:  # No response was made
                    mu_key_resp_recall.keys = None
                mu_recalls.addData('mu_key_resp_recall.keys',mu_key_resp_recall.keys)
                if mu_key_resp_recall.keys != None:  # we had a response
                    mu_recalls.addData('mu_key_resp_recall.rt', mu_key_resp_recall.rt)
                mu_recalls.addData('mu_key_resp_recall.started', mu_key_resp_recall.tStartRefresh)
                mu_recalls.addData('mu_key_resp_recall.stopped', mu_key_resp_recall.tStopRefresh)
                # the Routine "mu_recall" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "mu_display_recall"-------
                continueRoutine = True
                # update component parameters for each repeat
                keyboard_response = mu_key_resp_recall.keys.replace('num_', '')
                if keyboard_response.isspace():
                    keyboard_response = '.'
                if len(keyboard_response) > 1:
                    keyboard_response = '.'
                keyboard_response = keyboard_response.upper()
                current_trial.save_response(keyboard_response)
                mu_text_recall.setPos(recall_position)
                mu_text_recall.setText(keyboard_response)
                # keep track of which components have finished
                mu_display_recallComponents = [mu_text_recall]
                for thisComponent in mu_display_recallComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                mu_display_recallClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "mu_display_recall"-------
                while continueRoutine:
                    # get current time
                    t = mu_display_recallClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=mu_display_recallClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *mu_text_recall* updates
                    if mu_text_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        mu_text_recall.frameNStart = frameN  # exact frame index
                        mu_text_recall.tStart = t  # local t and not account for scr refresh
                        mu_text_recall.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(mu_text_recall, 'tStartRefresh')  # time at next scr refresh
                        mu_text_recall.setAutoDraw(True)
                    if mu_text_recall.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > mu_text_recall.tStartRefresh + current_task.config.timing.recall-frameTolerance:
                            # keep track of stop time/frame for later
                            mu_text_recall.tStop = t  # not accounting for scr refresh
                            mu_text_recall.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(mu_text_recall, 'tStopRefresh')  # time at next scr refresh
                            mu_text_recall.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in mu_display_recallComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "mu_display_recall"-------
                for thisComponent in mu_display_recallComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                if current_trial.get_left_recalls() == 0:
                    current_task.hide_frames()
                mu_recalls.addData('mu_text_recall.started', mu_text_recall.tStartRefresh)
                mu_recalls.addData('mu_text_recall.stopped', mu_text_recall.tStopRefresh)
                # the Routine "mu_display_recall" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed n_digits repeats of 'mu_recalls'
            
            
            # set up handler to look after randomisation of conditions etc
            mu_base_next_trial_dummy = data.TrialHandler(nReps=current_task.get_left_trials() > 0, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='mu_base_next_trial_dummy')
            thisExp.addLoop(mu_base_next_trial_dummy)  # add the loop to the experiment
            thisMu_base_next_trial_dummy = mu_base_next_trial_dummy.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisMu_base_next_trial_dummy.rgb)
            if thisMu_base_next_trial_dummy != None:
                for paramName in thisMu_base_next_trial_dummy:
                    exec('{} = thisMu_base_next_trial_dummy[paramName]'.format(paramName))
            
            for thisMu_base_next_trial_dummy in mu_base_next_trial_dummy:
                currentLoop = mu_base_next_trial_dummy
                # abbreviate parameter names if possible (e.g. rgb = thisMu_base_next_trial_dummy.rgb)
                if thisMu_base_next_trial_dummy != None:
                    for paramName in thisMu_base_next_trial_dummy:
                        exec('{} = thisMu_base_next_trial_dummy[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "base_next_trial"-------
                continueRoutine = True
                # update component parameters for each repeat
                base_text_next_trial.setText(expmsgs.next_trial)
                base_next_trial_key_resp.keys = []
                base_next_trial_key_resp.rt = []
                _base_next_trial_key_resp_allKeys = []
                # keep track of which components have finished
                base_next_trialComponents = [base_text_next_trial, base_next_trial_key_resp]
                for thisComponent in base_next_trialComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                base_next_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "base_next_trial"-------
                while continueRoutine:
                    # get current time
                    t = base_next_trialClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=base_next_trialClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *base_text_next_trial* updates
                    if base_text_next_trial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        base_text_next_trial.frameNStart = frameN  # exact frame index
                        base_text_next_trial.tStart = t  # local t and not account for scr refresh
                        base_text_next_trial.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(base_text_next_trial, 'tStartRefresh')  # time at next scr refresh
                        base_text_next_trial.setAutoDraw(True)
                    
                    # *base_next_trial_key_resp* updates
                    waitOnFlip = False
                    if base_next_trial_key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        base_next_trial_key_resp.frameNStart = frameN  # exact frame index
                        base_next_trial_key_resp.tStart = t  # local t and not account for scr refresh
                        base_next_trial_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(base_next_trial_key_resp, 'tStartRefresh')  # time at next scr refresh
                        base_next_trial_key_resp.status = STARTED
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(base_next_trial_key_resp.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(base_next_trial_key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if base_next_trial_key_resp.status == STARTED and not waitOnFlip:
                        theseKeys = base_next_trial_key_resp.getKeys(keyList=['space'], waitRelease=False)
                        _base_next_trial_key_resp_allKeys.extend(theseKeys)
                        if len(_base_next_trial_key_resp_allKeys):
                            base_next_trial_key_resp.keys = _base_next_trial_key_resp_allKeys[-1].name  # just the last key pressed
                            base_next_trial_key_resp.rt = _base_next_trial_key_resp_allKeys[-1].rt
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in base_next_trialComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "base_next_trial"-------
                for thisComponent in base_next_trialComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                mu_base_next_trial_dummy.addData('base_text_next_trial.started', base_text_next_trial.tStartRefresh)
                mu_base_next_trial_dummy.addData('base_text_next_trial.stopped', base_text_next_trial.tStopRefresh)
                # check responses
                if base_next_trial_key_resp.keys in ['', [], None]:  # No response was made
                    base_next_trial_key_resp.keys = None
                mu_base_next_trial_dummy.addData('base_next_trial_key_resp.keys',base_next_trial_key_resp.keys)
                if base_next_trial_key_resp.keys != None:  # we had a response
                    mu_base_next_trial_dummy.addData('base_next_trial_key_resp.rt', base_next_trial_key_resp.rt)
                mu_base_next_trial_dummy.addData('base_next_trial_key_resp.started', base_next_trial_key_resp.tStartRefresh)
                mu_base_next_trial_dummy.addData('base_next_trial_key_resp.stopped', base_next_trial_key_resp.tStopRefresh)
                # the Routine "base_next_trial" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed current_task.get_left_trials() > 0 repeats of 'mu_base_next_trial_dummy'
            
            
            # ------Prepare to start Routine "base_intertrial"-------
            continueRoutine = True
            # update component parameters for each repeat
            current_task.finish_trial()
            # keep track of which components have finished
            base_intertrialComponents = [base_text_intertrial]
            for thisComponent in base_intertrialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            base_intertrialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "base_intertrial"-------
            while continueRoutine:
                # get current time
                t = base_intertrialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=base_intertrialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # *base_text_intertrial* updates
                if base_text_intertrial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    base_text_intertrial.frameNStart = frameN  # exact frame index
                    base_text_intertrial.tStart = t  # local t and not account for scr refresh
                    base_text_intertrial.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(base_text_intertrial, 'tStartRefresh')  # time at next scr refresh
                    base_text_intertrial.setAutoDraw(True)
                if base_text_intertrial.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > base_text_intertrial.tStartRefresh + current_task.config.timing.inter_trial-frameTolerance:
                        # keep track of stop time/frame for later
                        base_text_intertrial.tStop = t  # not accounting for scr refresh
                        base_text_intertrial.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(base_text_intertrial, 'tStopRefresh')  # time at next scr refresh
                        base_text_intertrial.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in base_intertrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "base_intertrial"-------
            for thisComponent in base_intertrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            mu_trials.addData('base_text_intertrial.started', base_text_intertrial.tStartRefresh)
            mu_trials.addData('base_text_intertrial.stopped', base_text_intertrial.tStopRefresh)
            # the Routine "base_intertrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed n_trials repeats of 'mu_trials'
        
        thisExp.nextEntry()
        
    # completed 2 repeats of 'mu_practice_dummy'
    
    
    # ------Prepare to start Routine "base_task_end"-------
    continueRoutine = True
    # update component parameters for each repeat
    output_filepath = os.path.join(output_path, f'{current_task.name}-{subject_id}.dat')
    current_task.write_results(output_filepath)
    base_text_task_end.setText(expmsgs.task_over)
    base_key_resp_task_end.keys = []
    base_key_resp_task_end.rt = []
    _base_key_resp_task_end_allKeys = []
    # keep track of which components have finished
    base_task_endComponents = [base_text_task_end, base_key_resp_task_end]
    for thisComponent in base_task_endComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    base_task_endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "base_task_end"-------
    while continueRoutine:
        # get current time
        t = base_task_endClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=base_task_endClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
            core.quit()
        
        # *base_text_task_end* updates
        if base_text_task_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            base_text_task_end.frameNStart = frameN  # exact frame index
            base_text_task_end.tStart = t  # local t and not account for scr refresh
            base_text_task_end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(base_text_task_end, 'tStartRefresh')  # time at next scr refresh
            base_text_task_end.setAutoDraw(True)
        
        # *base_key_resp_task_end* updates
        waitOnFlip = False
        if base_key_resp_task_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            base_key_resp_task_end.frameNStart = frameN  # exact frame index
            base_key_resp_task_end.tStart = t  # local t and not account for scr refresh
            base_key_resp_task_end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(base_key_resp_task_end, 'tStartRefresh')  # time at next scr refresh
            base_key_resp_task_end.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(base_key_resp_task_end.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(base_key_resp_task_end.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if base_key_resp_task_end.status == STARTED and not waitOnFlip:
            theseKeys = base_key_resp_task_end.getKeys(keyList=['space'], waitRelease=False)
            _base_key_resp_task_end_allKeys.extend(theseKeys)
            if len(_base_key_resp_task_end_allKeys):
                base_key_resp_task_end.keys = _base_key_resp_task_end_allKeys[-1].name  # just the last key pressed
                base_key_resp_task_end.rt = _base_key_resp_task_end_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in base_task_endComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "base_task_end"-------
    for thisComponent in base_task_endComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    do_memory_update_dummy.addData('base_text_task_end.started', base_text_task_end.tStartRefresh)
    do_memory_update_dummy.addData('base_text_task_end.stopped', base_text_task_end.tStopRefresh)
    # check responses
    if base_key_resp_task_end.keys in ['', [], None]:  # No response was made
        base_key_resp_task_end.keys = None
    do_memory_update_dummy.addData('base_key_resp_task_end.keys',base_key_resp_task_end.keys)
    if base_key_resp_task_end.keys != None:  # we had a response
        do_memory_update_dummy.addData('base_key_resp_task_end.rt', base_key_resp_task_end.rt)
    do_memory_update_dummy.addData('base_key_resp_task_end.started', base_key_resp_task_end.tStartRefresh)
    do_memory_update_dummy.addData('base_key_resp_task_end.stopped', base_key_resp_task_end.tStopRefresh)
    # the Routine "base_task_end" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed do_mu_task repeats of 'do_memory_update_dummy'


# set up handler to look after randomisation of conditions etc
do_operation_span_dummy = data.TrialHandler(nReps=do_os_task, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='do_operation_span_dummy')
thisExp.addLoop(do_operation_span_dummy)  # add the loop to the experiment
thisDo_operation_span_dummy = do_operation_span_dummy.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisDo_operation_span_dummy.rgb)
if thisDo_operation_span_dummy != None:
    for paramName in thisDo_operation_span_dummy:
        exec('{} = thisDo_operation_span_dummy[paramName]'.format(paramName))

for thisDo_operation_span_dummy in do_operation_span_dummy:
    currentLoop = do_operation_span_dummy
    # abbreviate parameter names if possible (e.g. rgb = thisDo_operation_span_dummy.rgb)
    if thisDo_operation_span_dummy != None:
        for paramName in thisDo_operation_span_dummy:
            exec('{} = thisDo_operation_span_dummy[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "os_init"-------
    continueRoutine = True
    # update component parameters for each repeat
    from tasks.operation_span import OperationSpanTask
    
    current_task = OperationSpanTask(random_seed, config.operation_span)
    equation_keys = current_task.get_equation_keys()
    
    instruction_filepaths = instructions.get_instructions('os')
    n_instruction_pages = instructions.get_instruction_page_count('os')
    # keep track of which components have finished
    os_initComponents = []
    for thisComponent in os_initComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    os_initClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "os_init"-------
    while continueRoutine:
        # get current time
        t = os_initClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=os_initClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in os_initComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "os_init"-------
    for thisComponent in os_initComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "os_init" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    os_instruction_pages = data.TrialHandler(nReps=n_instruction_pages, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='os_instruction_pages')
    thisExp.addLoop(os_instruction_pages)  # add the loop to the experiment
    thisOs_instruction_page = os_instruction_pages.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisOs_instruction_page.rgb)
    if thisOs_instruction_page != None:
        for paramName in thisOs_instruction_page:
            exec('{} = thisOs_instruction_page[paramName]'.format(paramName))
    
    for thisOs_instruction_page in os_instruction_pages:
        currentLoop = os_instruction_pages
        # abbreviate parameter names if possible (e.g. rgb = thisOs_instruction_page.rgb)
        if thisOs_instruction_page != None:
            for paramName in thisOs_instruction_page:
                exec('{} = thisOs_instruction_page[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "base_instruction"-------
        continueRoutine = True
        # update component parameters for each repeat
        instruction_filepath = instruction_filepaths.pop(0)
        
        # the following is just needed because of a bug in psychopy
        # where images will get a grey border. a workaround is
        # setting up an aperture to hide these borders.
        
        from PIL import Image
        instr_img_size = Image.open(instruction_filepath).size
        
        # set aperture parameters from image size in pixels
        aperture_padding = 4
        aperture_width = instr_img_size[0] - aperture_padding
        aperture_height = instr_img_size[1] - aperture_padding
        
        # height scaling only scales by screen height to keep aspect ratio
        aperture_right = aperture_width / 2 / win.size[1]
        aperture_top = aperture_height / 2 / win.size[1]
        
        # setup rectangle vertices
        aperture_vertices = [
            [aperture_right, aperture_top],
            [aperture_right, -aperture_top],
            [-aperture_right, -aperture_top],
            [-aperture_right, aperture_top],
        ]
        
        aperture_instruction = visual.Aperture(win, size=1, shape='square', units='height')
        
        base_image_instruction.setSize(instr_img_size)
        base_image_instruction.setImage(instruction_filepath)
        base_key_resp_instruction.keys = []
        base_key_resp_instruction.rt = []
        _base_key_resp_instruction_allKeys = []
        # keep track of which components have finished
        base_instructionComponents = [base_image_instruction, base_key_resp_instruction, base_aperture_instruction]
        for thisComponent in base_instructionComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        base_instructionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "base_instruction"-------
        while continueRoutine:
            # get current time
            t = base_instructionClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=base_instructionClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                core.quit()
            
            # *base_image_instruction* updates
            if base_image_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_image_instruction.frameNStart = frameN  # exact frame index
                base_image_instruction.tStart = t  # local t and not account for scr refresh
                base_image_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_image_instruction, 'tStartRefresh')  # time at next scr refresh
                base_image_instruction.setAutoDraw(True)
            
            # *base_key_resp_instruction* updates
            waitOnFlip = False
            if base_key_resp_instruction.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                base_key_resp_instruction.frameNStart = frameN  # exact frame index
                base_key_resp_instruction.tStart = t  # local t and not account for scr refresh
                base_key_resp_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_key_resp_instruction, 'tStartRefresh')  # time at next scr refresh
                base_key_resp_instruction.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(base_key_resp_instruction.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(base_key_resp_instruction.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if base_key_resp_instruction.status == STARTED and not waitOnFlip:
                theseKeys = base_key_resp_instruction.getKeys(keyList=None, waitRelease=False)
                _base_key_resp_instruction_allKeys.extend(theseKeys)
                if len(_base_key_resp_instruction_allKeys):
                    base_key_resp_instruction.keys = _base_key_resp_instruction_allKeys[-1].name  # just the last key pressed
                    base_key_resp_instruction.rt = _base_key_resp_instruction_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # *base_aperture_instruction* updates
            if base_aperture_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_aperture_instruction.frameNStart = frameN  # exact frame index
                base_aperture_instruction.tStart = t  # local t and not account for scr refresh
                base_aperture_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_aperture_instruction, 'tStartRefresh')  # time at next scr refresh
                base_aperture_instruction.enabled = True
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in base_instructionComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "base_instruction"-------
        for thisComponent in base_instructionComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        del aperture_instruction
        os_instruction_pages.addData('base_image_instruction.started', base_image_instruction.tStartRefresh)
        os_instruction_pages.addData('base_image_instruction.stopped', base_image_instruction.tStopRefresh)
        # check responses
        if base_key_resp_instruction.keys in ['', [], None]:  # No response was made
            base_key_resp_instruction.keys = None
        os_instruction_pages.addData('base_key_resp_instruction.keys',base_key_resp_instruction.keys)
        if base_key_resp_instruction.keys != None:  # we had a response
            os_instruction_pages.addData('base_key_resp_instruction.rt', base_key_resp_instruction.rt)
        os_instruction_pages.addData('base_key_resp_instruction.started', base_key_resp_instruction.tStartRefresh)
        os_instruction_pages.addData('base_key_resp_instruction.stopped', base_key_resp_instruction.tStopRefresh)
        base_aperture_instruction.enabled = False  # just in case it was left enabled
        os_instruction_pages.addData('base_aperture_instruction.started', base_aperture_instruction.tStartRefresh)
        os_instruction_pages.addData('base_aperture_instruction.stopped', base_aperture_instruction.tStopRefresh)
        # the Routine "base_instruction" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed n_instruction_pages repeats of 'os_instruction_pages'
    
    
    # set up handler to look after randomisation of conditions etc
    os_practice_dummy = data.TrialHandler(nReps=2, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='os_practice_dummy')
    thisExp.addLoop(os_practice_dummy)  # add the loop to the experiment
    thisOs_practice_dummy = os_practice_dummy.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisOs_practice_dummy.rgb)
    if thisOs_practice_dummy != None:
        for paramName in thisOs_practice_dummy:
            exec('{} = thisOs_practice_dummy[paramName]'.format(paramName))
    
    for thisOs_practice_dummy in os_practice_dummy:
        currentLoop = os_practice_dummy
        # abbreviate parameter names if possible (e.g. rgb = thisOs_practice_dummy.rgb)
        if thisOs_practice_dummy != None:
            for paramName in thisOs_practice_dummy:
                exec('{} = thisOs_practice_dummy[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "base_init_task"-------
        continueRoutine = True
        # update component parameters for each repeat
        # set begin task message depending on practice
        if current_task.do_practice:
            msg_task_begin = expmsgs.begin_practice
        else:
            msg_task_begin = expmsgs.begin_task
        
        n_trials = current_task.get_trial_count()
        base_text_begin_task.setText(msg_task_begin)
        base_key_resp_task_begin.keys = []
        base_key_resp_task_begin.rt = []
        _base_key_resp_task_begin_allKeys = []
        # keep track of which components have finished
        base_init_taskComponents = [base_text_begin_task, base_key_resp_task_begin]
        for thisComponent in base_init_taskComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        base_init_taskClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "base_init_task"-------
        while continueRoutine:
            # get current time
            t = base_init_taskClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=base_init_taskClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                core.quit()
            
            # *base_text_begin_task* updates
            if base_text_begin_task.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_text_begin_task.frameNStart = frameN  # exact frame index
                base_text_begin_task.tStart = t  # local t and not account for scr refresh
                base_text_begin_task.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_text_begin_task, 'tStartRefresh')  # time at next scr refresh
                base_text_begin_task.setAutoDraw(True)
            
            # *base_key_resp_task_begin* updates
            waitOnFlip = False
            if base_key_resp_task_begin.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                base_key_resp_task_begin.frameNStart = frameN  # exact frame index
                base_key_resp_task_begin.tStart = t  # local t and not account for scr refresh
                base_key_resp_task_begin.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_key_resp_task_begin, 'tStartRefresh')  # time at next scr refresh
                base_key_resp_task_begin.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(base_key_resp_task_begin.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(base_key_resp_task_begin.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if base_key_resp_task_begin.status == STARTED and not waitOnFlip:
                theseKeys = base_key_resp_task_begin.getKeys(keyList=['space'], waitRelease=False)
                _base_key_resp_task_begin_allKeys.extend(theseKeys)
                if len(_base_key_resp_task_begin_allKeys):
                    base_key_resp_task_begin.keys = _base_key_resp_task_begin_allKeys[-1].name  # just the last key pressed
                    base_key_resp_task_begin.rt = _base_key_resp_task_begin_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in base_init_taskComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "base_init_task"-------
        for thisComponent in base_init_taskComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        os_practice_dummy.addData('base_text_begin_task.started', base_text_begin_task.tStartRefresh)
        os_practice_dummy.addData('base_text_begin_task.stopped', base_text_begin_task.tStopRefresh)
        # check responses
        if base_key_resp_task_begin.keys in ['', [], None]:  # No response was made
            base_key_resp_task_begin.keys = None
        os_practice_dummy.addData('base_key_resp_task_begin.keys',base_key_resp_task_begin.keys)
        if base_key_resp_task_begin.keys != None:  # we had a response
            os_practice_dummy.addData('base_key_resp_task_begin.rt', base_key_resp_task_begin.rt)
        os_practice_dummy.addData('base_key_resp_task_begin.started', base_key_resp_task_begin.tStartRefresh)
        os_practice_dummy.addData('base_key_resp_task_begin.stopped', base_key_resp_task_begin.tStopRefresh)
        # the Routine "base_init_task" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        os_trials = data.TrialHandler(nReps=n_trials, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='os_trials')
        thisExp.addLoop(os_trials)  # add the loop to the experiment
        thisOs_trial = os_trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisOs_trial.rgb)
        if thisOs_trial != None:
            for paramName in thisOs_trial:
                exec('{} = thisOs_trial[paramName]'.format(paramName))
        
        for thisOs_trial in os_trials:
            currentLoop = os_trials
            # abbreviate parameter names if possible (e.g. rgb = thisOs_trial.rgb)
            if thisOs_trial != None:
                for paramName in thisOs_trial:
                    exec('{} = thisOs_trial[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "base_init_trial"-------
            continueRoutine = True
            # update component parameters for each repeat
            current_trial = current_task.start_new_trial()
            do_break = current_task.has_pause()
            # keep track of which components have finished
            base_init_trialComponents = []
            for thisComponent in base_init_trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            base_init_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "base_init_trial"-------
            while continueRoutine:
                # get current time
                t = base_init_trialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=base_init_trialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in base_init_trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "base_init_trial"-------
            for thisComponent in base_init_trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "base_init_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "os_init_trial"-------
            continueRoutine = True
            # update component parameters for each repeat
            n_presentations = current_trial.get_presentation_count()
            # keep track of which components have finished
            os_init_trialComponents = [os_text_fixation_cross]
            for thisComponent in os_init_trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            os_init_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "os_init_trial"-------
            while continueRoutine:
                # get current time
                t = os_init_trialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=os_init_trialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # *os_text_fixation_cross* updates
                if os_text_fixation_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    os_text_fixation_cross.frameNStart = frameN  # exact frame index
                    os_text_fixation_cross.tStart = t  # local t and not account for scr refresh
                    os_text_fixation_cross.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(os_text_fixation_cross, 'tStartRefresh')  # time at next scr refresh
                    os_text_fixation_cross.setAutoDraw(True)
                if os_text_fixation_cross.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > os_text_fixation_cross.tStartRefresh + current_task.config.timing.init_trial-frameTolerance:
                        # keep track of stop time/frame for later
                        os_text_fixation_cross.tStop = t  # not accounting for scr refresh
                        os_text_fixation_cross.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(os_text_fixation_cross, 'tStopRefresh')  # time at next scr refresh
                        os_text_fixation_cross.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in os_init_trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "os_init_trial"-------
            for thisComponent in os_init_trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            os_trials.addData('os_text_fixation_cross.started', os_text_fixation_cross.tStartRefresh)
            os_trials.addData('os_text_fixation_cross.stopped', os_text_fixation_cross.tStopRefresh)
            # the Routine "os_init_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # set up handler to look after randomisation of conditions etc
            os_presentations = data.TrialHandler(nReps=n_presentations, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='os_presentations')
            thisExp.addLoop(os_presentations)  # add the loop to the experiment
            thisOs_presentation = os_presentations.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisOs_presentation.rgb)
            if thisOs_presentation != None:
                for paramName in thisOs_presentation:
                    exec('{} = thisOs_presentation[paramName]'.format(paramName))
            
            for thisOs_presentation in os_presentations:
                currentLoop = os_presentations
                # abbreviate parameter names if possible (e.g. rgb = thisOs_presentation.rgb)
                if thisOs_presentation != None:
                    for paramName in thisOs_presentation:
                        exec('{} = thisOs_presentation[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "os_equation"-------
                continueRoutine = True
                # update component parameters for each repeat
                equation = current_trial.get_next_equation()
                equation_string = str(equation)
                correct_key = current_task.key_map[equation.correct]
                
                thisExp.addData('is_practice', current_task.do_practice)
                thisExp.addData('os_key_resp_equation.equation_string', equation_string)
                thisExp.addData('os_key_resp_equation.equation_correct', equation.correct)
                thisExp.addData('os_key_resp_equation.correct_answer', correct_key)
                
                os_text_equation.setText(equation_string)
                os_key_resp_equation.keys = []
                os_key_resp_equation.rt = []
                _os_key_resp_equation_allKeys = []
                # keep track of which components have finished
                os_equationComponents = [os_text_equation, os_key_resp_equation]
                for thisComponent in os_equationComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                os_equationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "os_equation"-------
                while continueRoutine:
                    # get current time
                    t = os_equationClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=os_equationClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *os_text_equation* updates
                    if os_text_equation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        os_text_equation.frameNStart = frameN  # exact frame index
                        os_text_equation.tStart = t  # local t and not account for scr refresh
                        os_text_equation.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(os_text_equation, 'tStartRefresh')  # time at next scr refresh
                        os_text_equation.setAutoDraw(True)
                    if os_text_equation.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > os_text_equation.tStartRefresh + current_task.config.timing.equation-frameTolerance:
                            # keep track of stop time/frame for later
                            os_text_equation.tStop = t  # not accounting for scr refresh
                            os_text_equation.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(os_text_equation, 'tStopRefresh')  # time at next scr refresh
                            os_text_equation.setAutoDraw(False)
                    
                    # *os_key_resp_equation* updates
                    waitOnFlip = False
                    if os_key_resp_equation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        os_key_resp_equation.frameNStart = frameN  # exact frame index
                        os_key_resp_equation.tStart = t  # local t and not account for scr refresh
                        os_key_resp_equation.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(os_key_resp_equation, 'tStartRefresh')  # time at next scr refresh
                        os_key_resp_equation.status = STARTED
                        # AllowedKeys looks like a variable named `equation_keys`
                        if not type(equation_keys) in [list, tuple, np.ndarray]:
                            if not isinstance(equation_keys, str):
                                logging.error('AllowedKeys variable `equation_keys` is not string- or list-like.')
                                core.quit()
                            elif not ',' in equation_keys:
                                equation_keys = (equation_keys,)
                            else:
                                equation_keys = eval(equation_keys)
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(os_key_resp_equation.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(os_key_resp_equation.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if os_key_resp_equation.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > os_key_resp_equation.tStartRefresh + current_task.config.timing.equation-frameTolerance:
                            # keep track of stop time/frame for later
                            os_key_resp_equation.tStop = t  # not accounting for scr refresh
                            os_key_resp_equation.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(os_key_resp_equation, 'tStopRefresh')  # time at next scr refresh
                            os_key_resp_equation.status = FINISHED
                    if os_key_resp_equation.status == STARTED and not waitOnFlip:
                        theseKeys = os_key_resp_equation.getKeys(keyList=list(equation_keys), waitRelease=False)
                        _os_key_resp_equation_allKeys.extend(theseKeys)
                        if len(_os_key_resp_equation_allKeys):
                            os_key_resp_equation.keys = _os_key_resp_equation_allKeys[-1].name  # just the last key pressed
                            os_key_resp_equation.rt = _os_key_resp_equation_allKeys[-1].rt
                            # was this correct?
                            if (os_key_resp_equation.keys == str(correct_key)) or (os_key_resp_equation.keys == correct_key):
                                os_key_resp_equation.corr = 1
                            else:
                                os_key_resp_equation.corr = 0
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in os_equationComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "os_equation"-------
                for thisComponent in os_equationComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                keyboard_response = os_key_resp_equation.keys
                
                try:
                    equation_response = current_task.inv_key_map[keyboard_response]
                except TypeError:
                    equation_response = -1
                
                equation_rt = os_key_resp_equation.rt
                if equation_rt == []:
                    equation_rt = 3.0
                
                current_trial.save_equation_response(equation_response, equation_rt)
                os_presentations.addData('os_text_equation.started', os_text_equation.tStartRefresh)
                os_presentations.addData('os_text_equation.stopped', os_text_equation.tStopRefresh)
                # check responses
                if os_key_resp_equation.keys in ['', [], None]:  # No response was made
                    os_key_resp_equation.keys = None
                    # was no response the correct answer?!
                    if str(correct_key).lower() == 'none':
                       os_key_resp_equation.corr = 1;  # correct non-response
                    else:
                       os_key_resp_equation.corr = 0;  # failed to respond (incorrectly)
                # store data for os_presentations (TrialHandler)
                os_presentations.addData('os_key_resp_equation.keys',os_key_resp_equation.keys)
                os_presentations.addData('os_key_resp_equation.corr', os_key_resp_equation.corr)
                if os_key_resp_equation.keys != None:  # we had a response
                    os_presentations.addData('os_key_resp_equation.rt', os_key_resp_equation.rt)
                os_presentations.addData('os_key_resp_equation.started', os_key_resp_equation.tStartRefresh)
                os_presentations.addData('os_key_resp_equation.stopped', os_key_resp_equation.tStopRefresh)
                # the Routine "os_equation" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "os_letter"-------
                continueRoutine = True
                # update component parameters for each repeat
                letter = current_trial.get_next_letter().upper()
                os_text_letter.setText(letter)
                # keep track of which components have finished
                os_letterComponents = [os_text_letter]
                for thisComponent in os_letterComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                os_letterClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "os_letter"-------
                while continueRoutine:
                    # get current time
                    t = os_letterClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=os_letterClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *os_text_letter* updates
                    if os_text_letter.status == NOT_STARTED and tThisFlip >= 0.-frameTolerance:
                        # keep track of start time/frame for later
                        os_text_letter.frameNStart = frameN  # exact frame index
                        os_text_letter.tStart = t  # local t and not account for scr refresh
                        os_text_letter.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(os_text_letter, 'tStartRefresh')  # time at next scr refresh
                        os_text_letter.setAutoDraw(True)
                    if os_text_letter.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > os_text_letter.tStartRefresh + current_task.config.timing.letter-frameTolerance:
                            # keep track of stop time/frame for later
                            os_text_letter.tStop = t  # not accounting for scr refresh
                            os_text_letter.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(os_text_letter, 'tStopRefresh')  # time at next scr refresh
                            os_text_letter.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in os_letterComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "os_letter"-------
                for thisComponent in os_letterComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                os_presentations.addData('os_text_letter.started', os_text_letter.tStartRefresh)
                os_presentations.addData('os_text_letter.stopped', os_text_letter.tStopRefresh)
                # the Routine "os_letter" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "os_blank"-------
                continueRoutine = True
                # update component parameters for each repeat
                # keep track of which components have finished
                os_blankComponents = [os_text_blank]
                for thisComponent in os_blankComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                os_blankClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "os_blank"-------
                while continueRoutine:
                    # get current time
                    t = os_blankClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=os_blankClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *os_text_blank* updates
                    if os_text_blank.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        os_text_blank.frameNStart = frameN  # exact frame index
                        os_text_blank.tStart = t  # local t and not account for scr refresh
                        os_text_blank.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(os_text_blank, 'tStartRefresh')  # time at next scr refresh
                        os_text_blank.setAutoDraw(True)
                    if os_text_blank.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > os_text_blank.tStartRefresh + current_task.config.timing.inter_item-frameTolerance:
                            # keep track of stop time/frame for later
                            os_text_blank.tStop = t  # not accounting for scr refresh
                            os_text_blank.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(os_text_blank, 'tStopRefresh')  # time at next scr refresh
                            os_text_blank.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in os_blankComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "os_blank"-------
                for thisComponent in os_blankComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                os_presentations.addData('os_text_blank.started', os_text_blank.tStartRefresh)
                os_presentations.addData('os_text_blank.stopped', os_text_blank.tStopRefresh)
                # the Routine "os_blank" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed n_presentations repeats of 'os_presentations'
            
            
            # set up handler to look after randomisation of conditions etc
            os_recalls = data.TrialHandler(nReps=n_presentations, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='os_recalls')
            thisExp.addLoop(os_recalls)  # add the loop to the experiment
            thisOs_recall = os_recalls.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisOs_recall.rgb)
            if thisOs_recall != None:
                for paramName in thisOs_recall:
                    exec('{} = thisOs_recall[paramName]'.format(paramName))
            
            for thisOs_recall in os_recalls:
                currentLoop = os_recalls
                # abbreviate parameter names if possible (e.g. rgb = thisOs_recall.rgb)
                if thisOs_recall != None:
                    for paramName in thisOs_recall:
                        exec('{} = thisOs_recall[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "os_recall"-------
                continueRoutine = True
                # update component parameters for each repeat
                correct_letter = current_trial.get_next_recall_letter()
                
                thisExp.addData('is_practice', current_task.do_practice)
                thisExp.addData('os_key_resp_recall.correct_letter', correct_letter)
                
                os_allowed_keys = current_task.config.allowed_keys
                os_key_resp_recall.keys = []
                os_key_resp_recall.rt = []
                _os_key_resp_recall_allKeys = []
                # keep track of which components have finished
                os_recallComponents = [os_text_question_mark, os_key_resp_recall]
                for thisComponent in os_recallComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                os_recallClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "os_recall"-------
                while continueRoutine:
                    # get current time
                    t = os_recallClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=os_recallClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *os_text_question_mark* updates
                    if os_text_question_mark.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        os_text_question_mark.frameNStart = frameN  # exact frame index
                        os_text_question_mark.tStart = t  # local t and not account for scr refresh
                        os_text_question_mark.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(os_text_question_mark, 'tStartRefresh')  # time at next scr refresh
                        os_text_question_mark.setAutoDraw(True)
                    
                    # *os_key_resp_recall* updates
                    waitOnFlip = False
                    if os_key_resp_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        os_key_resp_recall.frameNStart = frameN  # exact frame index
                        os_key_resp_recall.tStart = t  # local t and not account for scr refresh
                        os_key_resp_recall.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(os_key_resp_recall, 'tStartRefresh')  # time at next scr refresh
                        os_key_resp_recall.status = STARTED
                        # AllowedKeys looks like a variable named `os_allowed_keys`
                        if not type(os_allowed_keys) in [list, tuple, np.ndarray]:
                            if not isinstance(os_allowed_keys, str):
                                logging.error('AllowedKeys variable `os_allowed_keys` is not string- or list-like.')
                                core.quit()
                            elif not ',' in os_allowed_keys:
                                os_allowed_keys = (os_allowed_keys,)
                            else:
                                os_allowed_keys = eval(os_allowed_keys)
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(os_key_resp_recall.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(os_key_resp_recall.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if os_key_resp_recall.status == STARTED and not waitOnFlip:
                        theseKeys = os_key_resp_recall.getKeys(keyList=list(os_allowed_keys), waitRelease=False)
                        _os_key_resp_recall_allKeys.extend(theseKeys)
                        if len(_os_key_resp_recall_allKeys):
                            os_key_resp_recall.keys = _os_key_resp_recall_allKeys[-1].name  # just the last key pressed
                            os_key_resp_recall.rt = _os_key_resp_recall_allKeys[-1].rt
                            # was this correct?
                            if (os_key_resp_recall.keys == str(correct_letter)) or (os_key_resp_recall.keys == correct_letter):
                                os_key_resp_recall.corr = 1
                            else:
                                os_key_resp_recall.corr = 0
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in os_recallComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "os_recall"-------
                for thisComponent in os_recallComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                os_recalls.addData('os_text_question_mark.started', os_text_question_mark.tStartRefresh)
                os_recalls.addData('os_text_question_mark.stopped', os_text_question_mark.tStopRefresh)
                # check responses
                if os_key_resp_recall.keys in ['', [], None]:  # No response was made
                    os_key_resp_recall.keys = None
                    # was no response the correct answer?!
                    if str(correct_letter).lower() == 'none':
                       os_key_resp_recall.corr = 1;  # correct non-response
                    else:
                       os_key_resp_recall.corr = 0;  # failed to respond (incorrectly)
                # store data for os_recalls (TrialHandler)
                os_recalls.addData('os_key_resp_recall.keys',os_key_resp_recall.keys)
                os_recalls.addData('os_key_resp_recall.corr', os_key_resp_recall.corr)
                if os_key_resp_recall.keys != None:  # we had a response
                    os_recalls.addData('os_key_resp_recall.rt', os_key_resp_recall.rt)
                os_recalls.addData('os_key_resp_recall.started', os_key_resp_recall.tStartRefresh)
                os_recalls.addData('os_key_resp_recall.stopped', os_key_resp_recall.tStopRefresh)
                # the Routine "os_recall" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "os_display_recall"-------
                continueRoutine = True
                # update component parameters for each repeat
                letter_response = os_key_resp_recall.keys
                letter_rt = os_key_resp_recall.rt
                current_trial.save_letter_response(letter_response, letter_rt)
                
                os_text_recall.setText(letter_response.upper())
                # keep track of which components have finished
                os_display_recallComponents = [os_text_recall]
                for thisComponent in os_display_recallComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                os_display_recallClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "os_display_recall"-------
                while continueRoutine:
                    # get current time
                    t = os_display_recallClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=os_display_recallClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *os_text_recall* updates
                    if os_text_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        os_text_recall.frameNStart = frameN  # exact frame index
                        os_text_recall.tStart = t  # local t and not account for scr refresh
                        os_text_recall.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(os_text_recall, 'tStartRefresh')  # time at next scr refresh
                        os_text_recall.setAutoDraw(True)
                    if os_text_recall.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > os_text_recall.tStartRefresh + current_task.config.timing.recall-frameTolerance:
                            # keep track of stop time/frame for later
                            os_text_recall.tStop = t  # not accounting for scr refresh
                            os_text_recall.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(os_text_recall, 'tStopRefresh')  # time at next scr refresh
                            os_text_recall.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in os_display_recallComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "os_display_recall"-------
                for thisComponent in os_display_recallComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                os_recalls.addData('os_text_recall.started', os_text_recall.tStartRefresh)
                os_recalls.addData('os_text_recall.stopped', os_text_recall.tStopRefresh)
                # the Routine "os_display_recall" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed n_presentations repeats of 'os_recalls'
            
            
            # ------Prepare to start Routine "base_intertrial"-------
            continueRoutine = True
            # update component parameters for each repeat
            current_task.finish_trial()
            # keep track of which components have finished
            base_intertrialComponents = [base_text_intertrial]
            for thisComponent in base_intertrialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            base_intertrialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "base_intertrial"-------
            while continueRoutine:
                # get current time
                t = base_intertrialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=base_intertrialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # *base_text_intertrial* updates
                if base_text_intertrial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    base_text_intertrial.frameNStart = frameN  # exact frame index
                    base_text_intertrial.tStart = t  # local t and not account for scr refresh
                    base_text_intertrial.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(base_text_intertrial, 'tStartRefresh')  # time at next scr refresh
                    base_text_intertrial.setAutoDraw(True)
                if base_text_intertrial.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > base_text_intertrial.tStartRefresh + current_task.config.timing.inter_trial-frameTolerance:
                        # keep track of stop time/frame for later
                        base_text_intertrial.tStop = t  # not accounting for scr refresh
                        base_text_intertrial.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(base_text_intertrial, 'tStopRefresh')  # time at next scr refresh
                        base_text_intertrial.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in base_intertrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "base_intertrial"-------
            for thisComponent in base_intertrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            os_trials.addData('base_text_intertrial.started', base_text_intertrial.tStartRefresh)
            os_trials.addData('base_text_intertrial.stopped', base_text_intertrial.tStopRefresh)
            # the Routine "base_intertrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # set up handler to look after randomisation of conditions etc
            os_break_dummy = data.TrialHandler(nReps=do_break, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='os_break_dummy')
            thisExp.addLoop(os_break_dummy)  # add the loop to the experiment
            thisOs_break_dummy = os_break_dummy.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisOs_break_dummy.rgb)
            if thisOs_break_dummy != None:
                for paramName in thisOs_break_dummy:
                    exec('{} = thisOs_break_dummy[paramName]'.format(paramName))
            
            for thisOs_break_dummy in os_break_dummy:
                currentLoop = os_break_dummy
                # abbreviate parameter names if possible (e.g. rgb = thisOs_break_dummy.rgb)
                if thisOs_break_dummy != None:
                    for paramName in thisOs_break_dummy:
                        exec('{} = thisOs_break_dummy[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "base_self_paced_break"-------
                continueRoutine = True
                # update component parameters for each repeat
                base_text_self_paced_break.setText(expmsgs.self_paced_break)
                base_key_resp_self_paced_break.keys = []
                base_key_resp_self_paced_break.rt = []
                _base_key_resp_self_paced_break_allKeys = []
                # keep track of which components have finished
                base_self_paced_breakComponents = [base_text_self_paced_break, base_key_resp_self_paced_break]
                for thisComponent in base_self_paced_breakComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                base_self_paced_breakClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "base_self_paced_break"-------
                while continueRoutine:
                    # get current time
                    t = base_self_paced_breakClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=base_self_paced_breakClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *base_text_self_paced_break* updates
                    if base_text_self_paced_break.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        base_text_self_paced_break.frameNStart = frameN  # exact frame index
                        base_text_self_paced_break.tStart = t  # local t and not account for scr refresh
                        base_text_self_paced_break.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(base_text_self_paced_break, 'tStartRefresh')  # time at next scr refresh
                        base_text_self_paced_break.setAutoDraw(True)
                    
                    # *base_key_resp_self_paced_break* updates
                    waitOnFlip = False
                    if base_key_resp_self_paced_break.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                        # keep track of start time/frame for later
                        base_key_resp_self_paced_break.frameNStart = frameN  # exact frame index
                        base_key_resp_self_paced_break.tStart = t  # local t and not account for scr refresh
                        base_key_resp_self_paced_break.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(base_key_resp_self_paced_break, 'tStartRefresh')  # time at next scr refresh
                        base_key_resp_self_paced_break.status = STARTED
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(base_key_resp_self_paced_break.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(base_key_resp_self_paced_break.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if base_key_resp_self_paced_break.status == STARTED and not waitOnFlip:
                        theseKeys = base_key_resp_self_paced_break.getKeys(keyList=['space'], waitRelease=False)
                        _base_key_resp_self_paced_break_allKeys.extend(theseKeys)
                        if len(_base_key_resp_self_paced_break_allKeys):
                            base_key_resp_self_paced_break.keys = _base_key_resp_self_paced_break_allKeys[-1].name  # just the last key pressed
                            base_key_resp_self_paced_break.rt = _base_key_resp_self_paced_break_allKeys[-1].rt
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in base_self_paced_breakComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "base_self_paced_break"-------
                for thisComponent in base_self_paced_breakComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                os_break_dummy.addData('base_text_self_paced_break.started', base_text_self_paced_break.tStartRefresh)
                os_break_dummy.addData('base_text_self_paced_break.stopped', base_text_self_paced_break.tStopRefresh)
                # check responses
                if base_key_resp_self_paced_break.keys in ['', [], None]:  # No response was made
                    base_key_resp_self_paced_break.keys = None
                os_break_dummy.addData('base_key_resp_self_paced_break.keys',base_key_resp_self_paced_break.keys)
                if base_key_resp_self_paced_break.keys != None:  # we had a response
                    os_break_dummy.addData('base_key_resp_self_paced_break.rt', base_key_resp_self_paced_break.rt)
                os_break_dummy.addData('base_key_resp_self_paced_break.started', base_key_resp_self_paced_break.tStartRefresh)
                os_break_dummy.addData('base_key_resp_self_paced_break.stopped', base_key_resp_self_paced_break.tStopRefresh)
                # the Routine "base_self_paced_break" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "base_after_break_pause"-------
                continueRoutine = True
                # update component parameters for each repeat
                # keep track of which components have finished
                base_after_break_pauseComponents = [base_text_pause_after_break]
                for thisComponent in base_after_break_pauseComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                base_after_break_pauseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "base_after_break_pause"-------
                while continueRoutine:
                    # get current time
                    t = base_after_break_pauseClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=base_after_break_pauseClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *base_text_pause_after_break* updates
                    if base_text_pause_after_break.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        base_text_pause_after_break.frameNStart = frameN  # exact frame index
                        base_text_pause_after_break.tStart = t  # local t and not account for scr refresh
                        base_text_pause_after_break.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(base_text_pause_after_break, 'tStartRefresh')  # time at next scr refresh
                        base_text_pause_after_break.setAutoDraw(True)
                    if base_text_pause_after_break.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > base_text_pause_after_break.tStartRefresh + current_task.config.timing.after_break-frameTolerance:
                            # keep track of stop time/frame for later
                            base_text_pause_after_break.tStop = t  # not accounting for scr refresh
                            base_text_pause_after_break.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(base_text_pause_after_break, 'tStopRefresh')  # time at next scr refresh
                            base_text_pause_after_break.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in base_after_break_pauseComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "base_after_break_pause"-------
                for thisComponent in base_after_break_pauseComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                os_break_dummy.addData('base_text_pause_after_break.started', base_text_pause_after_break.tStartRefresh)
                os_break_dummy.addData('base_text_pause_after_break.stopped', base_text_pause_after_break.tStopRefresh)
                # the Routine "base_after_break_pause" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed do_break repeats of 'os_break_dummy'
            
            thisExp.nextEntry()
            
        # completed n_trials repeats of 'os_trials'
        
        thisExp.nextEntry()
        
    # completed 2 repeats of 'os_practice_dummy'
    
    
    # ------Prepare to start Routine "base_task_end"-------
    continueRoutine = True
    # update component parameters for each repeat
    output_filepath = os.path.join(output_path, f'{current_task.name}-{subject_id}.dat')
    current_task.write_results(output_filepath)
    base_text_task_end.setText(expmsgs.task_over)
    base_key_resp_task_end.keys = []
    base_key_resp_task_end.rt = []
    _base_key_resp_task_end_allKeys = []
    # keep track of which components have finished
    base_task_endComponents = [base_text_task_end, base_key_resp_task_end]
    for thisComponent in base_task_endComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    base_task_endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "base_task_end"-------
    while continueRoutine:
        # get current time
        t = base_task_endClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=base_task_endClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
            core.quit()
        
        # *base_text_task_end* updates
        if base_text_task_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            base_text_task_end.frameNStart = frameN  # exact frame index
            base_text_task_end.tStart = t  # local t and not account for scr refresh
            base_text_task_end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(base_text_task_end, 'tStartRefresh')  # time at next scr refresh
            base_text_task_end.setAutoDraw(True)
        
        # *base_key_resp_task_end* updates
        waitOnFlip = False
        if base_key_resp_task_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            base_key_resp_task_end.frameNStart = frameN  # exact frame index
            base_key_resp_task_end.tStart = t  # local t and not account for scr refresh
            base_key_resp_task_end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(base_key_resp_task_end, 'tStartRefresh')  # time at next scr refresh
            base_key_resp_task_end.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(base_key_resp_task_end.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(base_key_resp_task_end.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if base_key_resp_task_end.status == STARTED and not waitOnFlip:
            theseKeys = base_key_resp_task_end.getKeys(keyList=['space'], waitRelease=False)
            _base_key_resp_task_end_allKeys.extend(theseKeys)
            if len(_base_key_resp_task_end_allKeys):
                base_key_resp_task_end.keys = _base_key_resp_task_end_allKeys[-1].name  # just the last key pressed
                base_key_resp_task_end.rt = _base_key_resp_task_end_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in base_task_endComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "base_task_end"-------
    for thisComponent in base_task_endComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    do_operation_span_dummy.addData('base_text_task_end.started', base_text_task_end.tStartRefresh)
    do_operation_span_dummy.addData('base_text_task_end.stopped', base_text_task_end.tStopRefresh)
    # check responses
    if base_key_resp_task_end.keys in ['', [], None]:  # No response was made
        base_key_resp_task_end.keys = None
    do_operation_span_dummy.addData('base_key_resp_task_end.keys',base_key_resp_task_end.keys)
    if base_key_resp_task_end.keys != None:  # we had a response
        do_operation_span_dummy.addData('base_key_resp_task_end.rt', base_key_resp_task_end.rt)
    do_operation_span_dummy.addData('base_key_resp_task_end.started', base_key_resp_task_end.tStartRefresh)
    do_operation_span_dummy.addData('base_key_resp_task_end.stopped', base_key_resp_task_end.tStopRefresh)
    # the Routine "base_task_end" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed do_os_task repeats of 'do_operation_span_dummy'


# set up handler to look after randomisation of conditions etc
do_sentence_span_dummy = data.TrialHandler(nReps=do_ss_task, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='do_sentence_span_dummy')
thisExp.addLoop(do_sentence_span_dummy)  # add the loop to the experiment
thisDo_sentence_span_dummy = do_sentence_span_dummy.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisDo_sentence_span_dummy.rgb)
if thisDo_sentence_span_dummy != None:
    for paramName in thisDo_sentence_span_dummy:
        exec('{} = thisDo_sentence_span_dummy[paramName]'.format(paramName))

for thisDo_sentence_span_dummy in do_sentence_span_dummy:
    currentLoop = do_sentence_span_dummy
    # abbreviate parameter names if possible (e.g. rgb = thisDo_sentence_span_dummy.rgb)
    if thisDo_sentence_span_dummy != None:
        for paramName in thisDo_sentence_span_dummy:
            exec('{} = thisDo_sentence_span_dummy[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "ss_init"-------
    continueRoutine = True
    # update component parameters for each repeat
    from tasks.sentence_span import SentenceSpanTask
    
    current_task = SentenceSpanTask(language=language, seed=random_seed, config=config.sentence_span)
    sentence_keys = current_task.get_sentence_keys()
    
    instruction_filepaths = instructions.get_instructions('ss')
    n_instruction_pages = instructions.get_instruction_page_count('ss')
    # keep track of which components have finished
    ss_initComponents = []
    for thisComponent in ss_initComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    ss_initClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "ss_init"-------
    while continueRoutine:
        # get current time
        t = ss_initClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=ss_initClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ss_initComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "ss_init"-------
    for thisComponent in ss_initComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "ss_init" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    ss_instruction_pages = data.TrialHandler(nReps=n_instruction_pages, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='ss_instruction_pages')
    thisExp.addLoop(ss_instruction_pages)  # add the loop to the experiment
    thisSs_instruction_page = ss_instruction_pages.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisSs_instruction_page.rgb)
    if thisSs_instruction_page != None:
        for paramName in thisSs_instruction_page:
            exec('{} = thisSs_instruction_page[paramName]'.format(paramName))
    
    for thisSs_instruction_page in ss_instruction_pages:
        currentLoop = ss_instruction_pages
        # abbreviate parameter names if possible (e.g. rgb = thisSs_instruction_page.rgb)
        if thisSs_instruction_page != None:
            for paramName in thisSs_instruction_page:
                exec('{} = thisSs_instruction_page[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "base_instruction"-------
        continueRoutine = True
        # update component parameters for each repeat
        instruction_filepath = instruction_filepaths.pop(0)
        
        # the following is just needed because of a bug in psychopy
        # where images will get a grey border. a workaround is
        # setting up an aperture to hide these borders.
        
        from PIL import Image
        instr_img_size = Image.open(instruction_filepath).size
        
        # set aperture parameters from image size in pixels
        aperture_padding = 4
        aperture_width = instr_img_size[0] - aperture_padding
        aperture_height = instr_img_size[1] - aperture_padding
        
        # height scaling only scales by screen height to keep aspect ratio
        aperture_right = aperture_width / 2 / win.size[1]
        aperture_top = aperture_height / 2 / win.size[1]
        
        # setup rectangle vertices
        aperture_vertices = [
            [aperture_right, aperture_top],
            [aperture_right, -aperture_top],
            [-aperture_right, -aperture_top],
            [-aperture_right, aperture_top],
        ]
        
        aperture_instruction = visual.Aperture(win, size=1, shape='square', units='height')
        
        base_image_instruction.setSize(instr_img_size)
        base_image_instruction.setImage(instruction_filepath)
        base_key_resp_instruction.keys = []
        base_key_resp_instruction.rt = []
        _base_key_resp_instruction_allKeys = []
        # keep track of which components have finished
        base_instructionComponents = [base_image_instruction, base_key_resp_instruction, base_aperture_instruction]
        for thisComponent in base_instructionComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        base_instructionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "base_instruction"-------
        while continueRoutine:
            # get current time
            t = base_instructionClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=base_instructionClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                core.quit()
            
            # *base_image_instruction* updates
            if base_image_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_image_instruction.frameNStart = frameN  # exact frame index
                base_image_instruction.tStart = t  # local t and not account for scr refresh
                base_image_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_image_instruction, 'tStartRefresh')  # time at next scr refresh
                base_image_instruction.setAutoDraw(True)
            
            # *base_key_resp_instruction* updates
            waitOnFlip = False
            if base_key_resp_instruction.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                base_key_resp_instruction.frameNStart = frameN  # exact frame index
                base_key_resp_instruction.tStart = t  # local t and not account for scr refresh
                base_key_resp_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_key_resp_instruction, 'tStartRefresh')  # time at next scr refresh
                base_key_resp_instruction.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(base_key_resp_instruction.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(base_key_resp_instruction.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if base_key_resp_instruction.status == STARTED and not waitOnFlip:
                theseKeys = base_key_resp_instruction.getKeys(keyList=None, waitRelease=False)
                _base_key_resp_instruction_allKeys.extend(theseKeys)
                if len(_base_key_resp_instruction_allKeys):
                    base_key_resp_instruction.keys = _base_key_resp_instruction_allKeys[-1].name  # just the last key pressed
                    base_key_resp_instruction.rt = _base_key_resp_instruction_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # *base_aperture_instruction* updates
            if base_aperture_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_aperture_instruction.frameNStart = frameN  # exact frame index
                base_aperture_instruction.tStart = t  # local t and not account for scr refresh
                base_aperture_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_aperture_instruction, 'tStartRefresh')  # time at next scr refresh
                base_aperture_instruction.enabled = True
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in base_instructionComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "base_instruction"-------
        for thisComponent in base_instructionComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        del aperture_instruction
        ss_instruction_pages.addData('base_image_instruction.started', base_image_instruction.tStartRefresh)
        ss_instruction_pages.addData('base_image_instruction.stopped', base_image_instruction.tStopRefresh)
        # check responses
        if base_key_resp_instruction.keys in ['', [], None]:  # No response was made
            base_key_resp_instruction.keys = None
        ss_instruction_pages.addData('base_key_resp_instruction.keys',base_key_resp_instruction.keys)
        if base_key_resp_instruction.keys != None:  # we had a response
            ss_instruction_pages.addData('base_key_resp_instruction.rt', base_key_resp_instruction.rt)
        ss_instruction_pages.addData('base_key_resp_instruction.started', base_key_resp_instruction.tStartRefresh)
        ss_instruction_pages.addData('base_key_resp_instruction.stopped', base_key_resp_instruction.tStopRefresh)
        base_aperture_instruction.enabled = False  # just in case it was left enabled
        ss_instruction_pages.addData('base_aperture_instruction.started', base_aperture_instruction.tStartRefresh)
        ss_instruction_pages.addData('base_aperture_instruction.stopped', base_aperture_instruction.tStopRefresh)
        # the Routine "base_instruction" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed n_instruction_pages repeats of 'ss_instruction_pages'
    
    
    # set up handler to look after randomisation of conditions etc
    ss_practice_dummy = data.TrialHandler(nReps=2, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='ss_practice_dummy')
    thisExp.addLoop(ss_practice_dummy)  # add the loop to the experiment
    thisSs_practice_dummy = ss_practice_dummy.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisSs_practice_dummy.rgb)
    if thisSs_practice_dummy != None:
        for paramName in thisSs_practice_dummy:
            exec('{} = thisSs_practice_dummy[paramName]'.format(paramName))
    
    for thisSs_practice_dummy in ss_practice_dummy:
        currentLoop = ss_practice_dummy
        # abbreviate parameter names if possible (e.g. rgb = thisSs_practice_dummy.rgb)
        if thisSs_practice_dummy != None:
            for paramName in thisSs_practice_dummy:
                exec('{} = thisSs_practice_dummy[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "base_init_task"-------
        continueRoutine = True
        # update component parameters for each repeat
        # set begin task message depending on practice
        if current_task.do_practice:
            msg_task_begin = expmsgs.begin_practice
        else:
            msg_task_begin = expmsgs.begin_task
        
        n_trials = current_task.get_trial_count()
        base_text_begin_task.setText(msg_task_begin)
        base_key_resp_task_begin.keys = []
        base_key_resp_task_begin.rt = []
        _base_key_resp_task_begin_allKeys = []
        # keep track of which components have finished
        base_init_taskComponents = [base_text_begin_task, base_key_resp_task_begin]
        for thisComponent in base_init_taskComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        base_init_taskClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "base_init_task"-------
        while continueRoutine:
            # get current time
            t = base_init_taskClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=base_init_taskClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                core.quit()
            
            # *base_text_begin_task* updates
            if base_text_begin_task.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_text_begin_task.frameNStart = frameN  # exact frame index
                base_text_begin_task.tStart = t  # local t and not account for scr refresh
                base_text_begin_task.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_text_begin_task, 'tStartRefresh')  # time at next scr refresh
                base_text_begin_task.setAutoDraw(True)
            
            # *base_key_resp_task_begin* updates
            waitOnFlip = False
            if base_key_resp_task_begin.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                base_key_resp_task_begin.frameNStart = frameN  # exact frame index
                base_key_resp_task_begin.tStart = t  # local t and not account for scr refresh
                base_key_resp_task_begin.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_key_resp_task_begin, 'tStartRefresh')  # time at next scr refresh
                base_key_resp_task_begin.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(base_key_resp_task_begin.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(base_key_resp_task_begin.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if base_key_resp_task_begin.status == STARTED and not waitOnFlip:
                theseKeys = base_key_resp_task_begin.getKeys(keyList=['space'], waitRelease=False)
                _base_key_resp_task_begin_allKeys.extend(theseKeys)
                if len(_base_key_resp_task_begin_allKeys):
                    base_key_resp_task_begin.keys = _base_key_resp_task_begin_allKeys[-1].name  # just the last key pressed
                    base_key_resp_task_begin.rt = _base_key_resp_task_begin_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in base_init_taskComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "base_init_task"-------
        for thisComponent in base_init_taskComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        ss_practice_dummy.addData('base_text_begin_task.started', base_text_begin_task.tStartRefresh)
        ss_practice_dummy.addData('base_text_begin_task.stopped', base_text_begin_task.tStopRefresh)
        # check responses
        if base_key_resp_task_begin.keys in ['', [], None]:  # No response was made
            base_key_resp_task_begin.keys = None
        ss_practice_dummy.addData('base_key_resp_task_begin.keys',base_key_resp_task_begin.keys)
        if base_key_resp_task_begin.keys != None:  # we had a response
            ss_practice_dummy.addData('base_key_resp_task_begin.rt', base_key_resp_task_begin.rt)
        ss_practice_dummy.addData('base_key_resp_task_begin.started', base_key_resp_task_begin.tStartRefresh)
        ss_practice_dummy.addData('base_key_resp_task_begin.stopped', base_key_resp_task_begin.tStopRefresh)
        # the Routine "base_init_task" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        ss_trials = data.TrialHandler(nReps=n_trials, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='ss_trials')
        thisExp.addLoop(ss_trials)  # add the loop to the experiment
        thisSs_trial = ss_trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSs_trial.rgb)
        if thisSs_trial != None:
            for paramName in thisSs_trial:
                exec('{} = thisSs_trial[paramName]'.format(paramName))
        
        for thisSs_trial in ss_trials:
            currentLoop = ss_trials
            # abbreviate parameter names if possible (e.g. rgb = thisSs_trial.rgb)
            if thisSs_trial != None:
                for paramName in thisSs_trial:
                    exec('{} = thisSs_trial[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "base_init_trial"-------
            continueRoutine = True
            # update component parameters for each repeat
            current_trial = current_task.start_new_trial()
            do_break = current_task.has_pause()
            # keep track of which components have finished
            base_init_trialComponents = []
            for thisComponent in base_init_trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            base_init_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "base_init_trial"-------
            while continueRoutine:
                # get current time
                t = base_init_trialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=base_init_trialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in base_init_trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "base_init_trial"-------
            for thisComponent in base_init_trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "base_init_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "ss_init_trial"-------
            continueRoutine = True
            # update component parameters for each repeat
            n_presentations = current_trial.get_presentation_count()
            # keep track of which components have finished
            ss_init_trialComponents = [ss_text_fixation_cross]
            for thisComponent in ss_init_trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            ss_init_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "ss_init_trial"-------
            while continueRoutine:
                # get current time
                t = ss_init_trialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=ss_init_trialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # *ss_text_fixation_cross* updates
                if ss_text_fixation_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    ss_text_fixation_cross.frameNStart = frameN  # exact frame index
                    ss_text_fixation_cross.tStart = t  # local t and not account for scr refresh
                    ss_text_fixation_cross.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ss_text_fixation_cross, 'tStartRefresh')  # time at next scr refresh
                    ss_text_fixation_cross.setAutoDraw(True)
                if ss_text_fixation_cross.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > ss_text_fixation_cross.tStartRefresh + current_task.config.timing.init_trial-frameTolerance:
                        # keep track of stop time/frame for later
                        ss_text_fixation_cross.tStop = t  # not accounting for scr refresh
                        ss_text_fixation_cross.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(ss_text_fixation_cross, 'tStopRefresh')  # time at next scr refresh
                        ss_text_fixation_cross.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in ss_init_trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "ss_init_trial"-------
            for thisComponent in ss_init_trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            ss_trials.addData('ss_text_fixation_cross.started', ss_text_fixation_cross.tStartRefresh)
            ss_trials.addData('ss_text_fixation_cross.stopped', ss_text_fixation_cross.tStopRefresh)
            # the Routine "ss_init_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # set up handler to look after randomisation of conditions etc
            ss_presentations = data.TrialHandler(nReps=n_presentations, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='ss_presentations')
            thisExp.addLoop(ss_presentations)  # add the loop to the experiment
            thisSs_presentation = ss_presentations.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisSs_presentation.rgb)
            if thisSs_presentation != None:
                for paramName in thisSs_presentation:
                    exec('{} = thisSs_presentation[paramName]'.format(paramName))
            
            for thisSs_presentation in ss_presentations:
                currentLoop = ss_presentations
                # abbreviate parameter names if possible (e.g. rgb = thisSs_presentation.rgb)
                if thisSs_presentation != None:
                    for paramName in thisSs_presentation:
                        exec('{} = thisSs_presentation[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "ss_sentence"-------
                continueRoutine = True
                # update component parameters for each repeat
                sentence = current_trial.get_next_sentence()
                sentence_string = str(sentence)
                correct_key = current_task.key_map[sentence.correct]
                
                thisExp.addData('is_practice', current_task.do_practice)
                thisExp.addData('ss_key_resp_sentence.sentence_string', sentence_string)
                thisExp.addData('ss_key_resp_sentence.sentence_correct', sentence.correct)
                thisExp.addData('ss_key_resp_sentence.correct_answer', correct_key)
                
                ss_text_sentence.setText(sentence_string)
                ss_key_resp_sentence.keys = []
                ss_key_resp_sentence.rt = []
                _ss_key_resp_sentence_allKeys = []
                # keep track of which components have finished
                ss_sentenceComponents = [ss_text_sentence, ss_key_resp_sentence]
                for thisComponent in ss_sentenceComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                ss_sentenceClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "ss_sentence"-------
                while continueRoutine:
                    # get current time
                    t = ss_sentenceClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=ss_sentenceClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *ss_text_sentence* updates
                    if ss_text_sentence.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        ss_text_sentence.frameNStart = frameN  # exact frame index
                        ss_text_sentence.tStart = t  # local t and not account for scr refresh
                        ss_text_sentence.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(ss_text_sentence, 'tStartRefresh')  # time at next scr refresh
                        ss_text_sentence.setAutoDraw(True)
                    if ss_text_sentence.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > ss_text_sentence.tStartRefresh + current_task.config.timing.sentence-frameTolerance:
                            # keep track of stop time/frame for later
                            ss_text_sentence.tStop = t  # not accounting for scr refresh
                            ss_text_sentence.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(ss_text_sentence, 'tStopRefresh')  # time at next scr refresh
                            ss_text_sentence.setAutoDraw(False)
                    
                    # *ss_key_resp_sentence* updates
                    waitOnFlip = False
                    if ss_key_resp_sentence.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        ss_key_resp_sentence.frameNStart = frameN  # exact frame index
                        ss_key_resp_sentence.tStart = t  # local t and not account for scr refresh
                        ss_key_resp_sentence.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(ss_key_resp_sentence, 'tStartRefresh')  # time at next scr refresh
                        ss_key_resp_sentence.status = STARTED
                        # AllowedKeys looks like a variable named `sentence_keys`
                        if not type(sentence_keys) in [list, tuple, np.ndarray]:
                            if not isinstance(sentence_keys, str):
                                logging.error('AllowedKeys variable `sentence_keys` is not string- or list-like.')
                                core.quit()
                            elif not ',' in sentence_keys:
                                sentence_keys = (sentence_keys,)
                            else:
                                sentence_keys = eval(sentence_keys)
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(ss_key_resp_sentence.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(ss_key_resp_sentence.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if ss_key_resp_sentence.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > ss_key_resp_sentence.tStartRefresh + current_task.config.timing.sentence-frameTolerance:
                            # keep track of stop time/frame for later
                            ss_key_resp_sentence.tStop = t  # not accounting for scr refresh
                            ss_key_resp_sentence.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(ss_key_resp_sentence, 'tStopRefresh')  # time at next scr refresh
                            ss_key_resp_sentence.status = FINISHED
                    if ss_key_resp_sentence.status == STARTED and not waitOnFlip:
                        theseKeys = ss_key_resp_sentence.getKeys(keyList=list(sentence_keys), waitRelease=False)
                        _ss_key_resp_sentence_allKeys.extend(theseKeys)
                        if len(_ss_key_resp_sentence_allKeys):
                            ss_key_resp_sentence.keys = _ss_key_resp_sentence_allKeys[-1].name  # just the last key pressed
                            ss_key_resp_sentence.rt = _ss_key_resp_sentence_allKeys[-1].rt
                            # was this correct?
                            if (ss_key_resp_sentence.keys == str(correct_key)) or (ss_key_resp_sentence.keys == correct_key):
                                ss_key_resp_sentence.corr = 1
                            else:
                                ss_key_resp_sentence.corr = 0
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in ss_sentenceComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "ss_sentence"-------
                for thisComponent in ss_sentenceComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                keyboard_response = ss_key_resp_sentence.keys
                
                try:
                    sentence_response = current_task.inv_key_map[keyboard_response]
                except TypeError:
                    sentence_response = -1
                
                sentence_rt = ss_key_resp_sentence.rt
                if sentence_rt == []:
                    sentence_rt = 3.0
                
                current_trial.save_sentence_response(sentence_response, sentence_rt)
                ss_presentations.addData('ss_text_sentence.started', ss_text_sentence.tStartRefresh)
                ss_presentations.addData('ss_text_sentence.stopped', ss_text_sentence.tStopRefresh)
                # check responses
                if ss_key_resp_sentence.keys in ['', [], None]:  # No response was made
                    ss_key_resp_sentence.keys = None
                    # was no response the correct answer?!
                    if str(correct_key).lower() == 'none':
                       ss_key_resp_sentence.corr = 1;  # correct non-response
                    else:
                       ss_key_resp_sentence.corr = 0;  # failed to respond (incorrectly)
                # store data for ss_presentations (TrialHandler)
                ss_presentations.addData('ss_key_resp_sentence.keys',ss_key_resp_sentence.keys)
                ss_presentations.addData('ss_key_resp_sentence.corr', ss_key_resp_sentence.corr)
                if ss_key_resp_sentence.keys != None:  # we had a response
                    ss_presentations.addData('ss_key_resp_sentence.rt', ss_key_resp_sentence.rt)
                ss_presentations.addData('ss_key_resp_sentence.started', ss_key_resp_sentence.tStartRefresh)
                ss_presentations.addData('ss_key_resp_sentence.stopped', ss_key_resp_sentence.tStopRefresh)
                # the Routine "ss_sentence" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "ss_letter"-------
                continueRoutine = True
                # update component parameters for each repeat
                letter = current_trial.get_next_letter().upper()
                ss_text_letter.setText(letter)
                # keep track of which components have finished
                ss_letterComponents = [ss_text_letter]
                for thisComponent in ss_letterComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                ss_letterClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "ss_letter"-------
                while continueRoutine:
                    # get current time
                    t = ss_letterClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=ss_letterClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *ss_text_letter* updates
                    if ss_text_letter.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        ss_text_letter.frameNStart = frameN  # exact frame index
                        ss_text_letter.tStart = t  # local t and not account for scr refresh
                        ss_text_letter.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(ss_text_letter, 'tStartRefresh')  # time at next scr refresh
                        ss_text_letter.setAutoDraw(True)
                    if ss_text_letter.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > ss_text_letter.tStartRefresh + current_task.config.timing.letter-frameTolerance:
                            # keep track of stop time/frame for later
                            ss_text_letter.tStop = t  # not accounting for scr refresh
                            ss_text_letter.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(ss_text_letter, 'tStopRefresh')  # time at next scr refresh
                            ss_text_letter.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in ss_letterComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "ss_letter"-------
                for thisComponent in ss_letterComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                ss_presentations.addData('ss_text_letter.started', ss_text_letter.tStartRefresh)
                ss_presentations.addData('ss_text_letter.stopped', ss_text_letter.tStopRefresh)
                # the Routine "ss_letter" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "ss_blank"-------
                continueRoutine = True
                # update component parameters for each repeat
                # keep track of which components have finished
                ss_blankComponents = [ss_text_blank]
                for thisComponent in ss_blankComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                ss_blankClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "ss_blank"-------
                while continueRoutine:
                    # get current time
                    t = ss_blankClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=ss_blankClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *ss_text_blank* updates
                    if ss_text_blank.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        ss_text_blank.frameNStart = frameN  # exact frame index
                        ss_text_blank.tStart = t  # local t and not account for scr refresh
                        ss_text_blank.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(ss_text_blank, 'tStartRefresh')  # time at next scr refresh
                        ss_text_blank.setAutoDraw(True)
                    if ss_text_blank.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > ss_text_blank.tStartRefresh + current_task.config.timing.inter_item-frameTolerance:
                            # keep track of stop time/frame for later
                            ss_text_blank.tStop = t  # not accounting for scr refresh
                            ss_text_blank.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(ss_text_blank, 'tStopRefresh')  # time at next scr refresh
                            ss_text_blank.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in ss_blankComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "ss_blank"-------
                for thisComponent in ss_blankComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                ss_presentations.addData('ss_text_blank.started', ss_text_blank.tStartRefresh)
                ss_presentations.addData('ss_text_blank.stopped', ss_text_blank.tStopRefresh)
                # the Routine "ss_blank" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed n_presentations repeats of 'ss_presentations'
            
            
            # set up handler to look after randomisation of conditions etc
            ss_recalls = data.TrialHandler(nReps=n_presentations, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='ss_recalls')
            thisExp.addLoop(ss_recalls)  # add the loop to the experiment
            thisSs_recall = ss_recalls.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisSs_recall.rgb)
            if thisSs_recall != None:
                for paramName in thisSs_recall:
                    exec('{} = thisSs_recall[paramName]'.format(paramName))
            
            for thisSs_recall in ss_recalls:
                currentLoop = ss_recalls
                # abbreviate parameter names if possible (e.g. rgb = thisSs_recall.rgb)
                if thisSs_recall != None:
                    for paramName in thisSs_recall:
                        exec('{} = thisSs_recall[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "ss_recall"-------
                continueRoutine = True
                # update component parameters for each repeat
                correct_letter = current_trial.get_next_recall_letter()
                
                thisExp.addData('is_practice', current_task.do_practice)
                thisExp.addData('ss_key_resp_recall.correct_letter', correct_letter)
                
                ss_allowed_keys = current_task.config.allowed_keys
                ss_key_resp_recall.keys = []
                ss_key_resp_recall.rt = []
                _ss_key_resp_recall_allKeys = []
                # keep track of which components have finished
                ss_recallComponents = [ss_text_question_mark, ss_key_resp_recall]
                for thisComponent in ss_recallComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                ss_recallClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "ss_recall"-------
                while continueRoutine:
                    # get current time
                    t = ss_recallClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=ss_recallClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *ss_text_question_mark* updates
                    if ss_text_question_mark.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        ss_text_question_mark.frameNStart = frameN  # exact frame index
                        ss_text_question_mark.tStart = t  # local t and not account for scr refresh
                        ss_text_question_mark.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(ss_text_question_mark, 'tStartRefresh')  # time at next scr refresh
                        ss_text_question_mark.setAutoDraw(True)
                    
                    # *ss_key_resp_recall* updates
                    waitOnFlip = False
                    if ss_key_resp_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        ss_key_resp_recall.frameNStart = frameN  # exact frame index
                        ss_key_resp_recall.tStart = t  # local t and not account for scr refresh
                        ss_key_resp_recall.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(ss_key_resp_recall, 'tStartRefresh')  # time at next scr refresh
                        ss_key_resp_recall.status = STARTED
                        # AllowedKeys looks like a variable named `ss_allowed_keys`
                        if not type(ss_allowed_keys) in [list, tuple, np.ndarray]:
                            if not isinstance(ss_allowed_keys, str):
                                logging.error('AllowedKeys variable `ss_allowed_keys` is not string- or list-like.')
                                core.quit()
                            elif not ',' in ss_allowed_keys:
                                ss_allowed_keys = (ss_allowed_keys,)
                            else:
                                ss_allowed_keys = eval(ss_allowed_keys)
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(ss_key_resp_recall.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(ss_key_resp_recall.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if ss_key_resp_recall.status == STARTED and not waitOnFlip:
                        theseKeys = ss_key_resp_recall.getKeys(keyList=list(ss_allowed_keys), waitRelease=False)
                        _ss_key_resp_recall_allKeys.extend(theseKeys)
                        if len(_ss_key_resp_recall_allKeys):
                            ss_key_resp_recall.keys = _ss_key_resp_recall_allKeys[-1].name  # just the last key pressed
                            ss_key_resp_recall.rt = _ss_key_resp_recall_allKeys[-1].rt
                            # was this correct?
                            if (ss_key_resp_recall.keys == str(correct_letter)) or (ss_key_resp_recall.keys == correct_letter):
                                ss_key_resp_recall.corr = 1
                            else:
                                ss_key_resp_recall.corr = 0
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in ss_recallComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "ss_recall"-------
                for thisComponent in ss_recallComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                ss_recalls.addData('ss_text_question_mark.started', ss_text_question_mark.tStartRefresh)
                ss_recalls.addData('ss_text_question_mark.stopped', ss_text_question_mark.tStopRefresh)
                # check responses
                if ss_key_resp_recall.keys in ['', [], None]:  # No response was made
                    ss_key_resp_recall.keys = None
                    # was no response the correct answer?!
                    if str(correct_letter).lower() == 'none':
                       ss_key_resp_recall.corr = 1;  # correct non-response
                    else:
                       ss_key_resp_recall.corr = 0;  # failed to respond (incorrectly)
                # store data for ss_recalls (TrialHandler)
                ss_recalls.addData('ss_key_resp_recall.keys',ss_key_resp_recall.keys)
                ss_recalls.addData('ss_key_resp_recall.corr', ss_key_resp_recall.corr)
                if ss_key_resp_recall.keys != None:  # we had a response
                    ss_recalls.addData('ss_key_resp_recall.rt', ss_key_resp_recall.rt)
                ss_recalls.addData('ss_key_resp_recall.started', ss_key_resp_recall.tStartRefresh)
                ss_recalls.addData('ss_key_resp_recall.stopped', ss_key_resp_recall.tStopRefresh)
                # the Routine "ss_recall" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "ss_display_recall"-------
                continueRoutine = True
                # update component parameters for each repeat
                letter_response = ss_key_resp_recall.keys
                letter_rt = ss_key_resp_recall.rt
                current_trial.save_letter_response(letter_response, letter_rt)
                
                ss_text_display_recall.setText(letter_response.upper())
                # keep track of which components have finished
                ss_display_recallComponents = [ss_text_display_recall]
                for thisComponent in ss_display_recallComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                ss_display_recallClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "ss_display_recall"-------
                while continueRoutine:
                    # get current time
                    t = ss_display_recallClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=ss_display_recallClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *ss_text_display_recall* updates
                    if ss_text_display_recall.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        ss_text_display_recall.frameNStart = frameN  # exact frame index
                        ss_text_display_recall.tStart = t  # local t and not account for scr refresh
                        ss_text_display_recall.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(ss_text_display_recall, 'tStartRefresh')  # time at next scr refresh
                        ss_text_display_recall.setAutoDraw(True)
                    if ss_text_display_recall.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > ss_text_display_recall.tStartRefresh + current_task.config.timing.recall-frameTolerance:
                            # keep track of stop time/frame for later
                            ss_text_display_recall.tStop = t  # not accounting for scr refresh
                            ss_text_display_recall.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(ss_text_display_recall, 'tStopRefresh')  # time at next scr refresh
                            ss_text_display_recall.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in ss_display_recallComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "ss_display_recall"-------
                for thisComponent in ss_display_recallComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                ss_recalls.addData('ss_text_display_recall.started', ss_text_display_recall.tStartRefresh)
                ss_recalls.addData('ss_text_display_recall.stopped', ss_text_display_recall.tStopRefresh)
                # the Routine "ss_display_recall" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed n_presentations repeats of 'ss_recalls'
            
            
            # ------Prepare to start Routine "base_intertrial"-------
            continueRoutine = True
            # update component parameters for each repeat
            current_task.finish_trial()
            # keep track of which components have finished
            base_intertrialComponents = [base_text_intertrial]
            for thisComponent in base_intertrialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            base_intertrialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "base_intertrial"-------
            while continueRoutine:
                # get current time
                t = base_intertrialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=base_intertrialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # *base_text_intertrial* updates
                if base_text_intertrial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    base_text_intertrial.frameNStart = frameN  # exact frame index
                    base_text_intertrial.tStart = t  # local t and not account for scr refresh
                    base_text_intertrial.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(base_text_intertrial, 'tStartRefresh')  # time at next scr refresh
                    base_text_intertrial.setAutoDraw(True)
                if base_text_intertrial.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > base_text_intertrial.tStartRefresh + current_task.config.timing.inter_trial-frameTolerance:
                        # keep track of stop time/frame for later
                        base_text_intertrial.tStop = t  # not accounting for scr refresh
                        base_text_intertrial.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(base_text_intertrial, 'tStopRefresh')  # time at next scr refresh
                        base_text_intertrial.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in base_intertrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "base_intertrial"-------
            for thisComponent in base_intertrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            ss_trials.addData('base_text_intertrial.started', base_text_intertrial.tStartRefresh)
            ss_trials.addData('base_text_intertrial.stopped', base_text_intertrial.tStopRefresh)
            # the Routine "base_intertrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # set up handler to look after randomisation of conditions etc
            ss_break_dummy = data.TrialHandler(nReps=do_break, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='ss_break_dummy')
            thisExp.addLoop(ss_break_dummy)  # add the loop to the experiment
            thisSs_break_dummy = ss_break_dummy.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisSs_break_dummy.rgb)
            if thisSs_break_dummy != None:
                for paramName in thisSs_break_dummy:
                    exec('{} = thisSs_break_dummy[paramName]'.format(paramName))
            
            for thisSs_break_dummy in ss_break_dummy:
                currentLoop = ss_break_dummy
                # abbreviate parameter names if possible (e.g. rgb = thisSs_break_dummy.rgb)
                if thisSs_break_dummy != None:
                    for paramName in thisSs_break_dummy:
                        exec('{} = thisSs_break_dummy[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "base_self_paced_break"-------
                continueRoutine = True
                # update component parameters for each repeat
                base_text_self_paced_break.setText(expmsgs.self_paced_break)
                base_key_resp_self_paced_break.keys = []
                base_key_resp_self_paced_break.rt = []
                _base_key_resp_self_paced_break_allKeys = []
                # keep track of which components have finished
                base_self_paced_breakComponents = [base_text_self_paced_break, base_key_resp_self_paced_break]
                for thisComponent in base_self_paced_breakComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                base_self_paced_breakClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "base_self_paced_break"-------
                while continueRoutine:
                    # get current time
                    t = base_self_paced_breakClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=base_self_paced_breakClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *base_text_self_paced_break* updates
                    if base_text_self_paced_break.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        base_text_self_paced_break.frameNStart = frameN  # exact frame index
                        base_text_self_paced_break.tStart = t  # local t and not account for scr refresh
                        base_text_self_paced_break.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(base_text_self_paced_break, 'tStartRefresh')  # time at next scr refresh
                        base_text_self_paced_break.setAutoDraw(True)
                    
                    # *base_key_resp_self_paced_break* updates
                    waitOnFlip = False
                    if base_key_resp_self_paced_break.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                        # keep track of start time/frame for later
                        base_key_resp_self_paced_break.frameNStart = frameN  # exact frame index
                        base_key_resp_self_paced_break.tStart = t  # local t and not account for scr refresh
                        base_key_resp_self_paced_break.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(base_key_resp_self_paced_break, 'tStartRefresh')  # time at next scr refresh
                        base_key_resp_self_paced_break.status = STARTED
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(base_key_resp_self_paced_break.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(base_key_resp_self_paced_break.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if base_key_resp_self_paced_break.status == STARTED and not waitOnFlip:
                        theseKeys = base_key_resp_self_paced_break.getKeys(keyList=['space'], waitRelease=False)
                        _base_key_resp_self_paced_break_allKeys.extend(theseKeys)
                        if len(_base_key_resp_self_paced_break_allKeys):
                            base_key_resp_self_paced_break.keys = _base_key_resp_self_paced_break_allKeys[-1].name  # just the last key pressed
                            base_key_resp_self_paced_break.rt = _base_key_resp_self_paced_break_allKeys[-1].rt
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in base_self_paced_breakComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "base_self_paced_break"-------
                for thisComponent in base_self_paced_breakComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                ss_break_dummy.addData('base_text_self_paced_break.started', base_text_self_paced_break.tStartRefresh)
                ss_break_dummy.addData('base_text_self_paced_break.stopped', base_text_self_paced_break.tStopRefresh)
                # check responses
                if base_key_resp_self_paced_break.keys in ['', [], None]:  # No response was made
                    base_key_resp_self_paced_break.keys = None
                ss_break_dummy.addData('base_key_resp_self_paced_break.keys',base_key_resp_self_paced_break.keys)
                if base_key_resp_self_paced_break.keys != None:  # we had a response
                    ss_break_dummy.addData('base_key_resp_self_paced_break.rt', base_key_resp_self_paced_break.rt)
                ss_break_dummy.addData('base_key_resp_self_paced_break.started', base_key_resp_self_paced_break.tStartRefresh)
                ss_break_dummy.addData('base_key_resp_self_paced_break.stopped', base_key_resp_self_paced_break.tStopRefresh)
                # the Routine "base_self_paced_break" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "base_after_break_pause"-------
                continueRoutine = True
                # update component parameters for each repeat
                # keep track of which components have finished
                base_after_break_pauseComponents = [base_text_pause_after_break]
                for thisComponent in base_after_break_pauseComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                base_after_break_pauseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "base_after_break_pause"-------
                while continueRoutine:
                    # get current time
                    t = base_after_break_pauseClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=base_after_break_pauseClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *base_text_pause_after_break* updates
                    if base_text_pause_after_break.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        base_text_pause_after_break.frameNStart = frameN  # exact frame index
                        base_text_pause_after_break.tStart = t  # local t and not account for scr refresh
                        base_text_pause_after_break.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(base_text_pause_after_break, 'tStartRefresh')  # time at next scr refresh
                        base_text_pause_after_break.setAutoDraw(True)
                    if base_text_pause_after_break.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > base_text_pause_after_break.tStartRefresh + current_task.config.timing.after_break-frameTolerance:
                            # keep track of stop time/frame for later
                            base_text_pause_after_break.tStop = t  # not accounting for scr refresh
                            base_text_pause_after_break.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(base_text_pause_after_break, 'tStopRefresh')  # time at next scr refresh
                            base_text_pause_after_break.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in base_after_break_pauseComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "base_after_break_pause"-------
                for thisComponent in base_after_break_pauseComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                ss_break_dummy.addData('base_text_pause_after_break.started', base_text_pause_after_break.tStartRefresh)
                ss_break_dummy.addData('base_text_pause_after_break.stopped', base_text_pause_after_break.tStopRefresh)
                # the Routine "base_after_break_pause" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed do_break repeats of 'ss_break_dummy'
            
            thisExp.nextEntry()
            
        # completed n_trials repeats of 'ss_trials'
        
        thisExp.nextEntry()
        
    # completed 2 repeats of 'ss_practice_dummy'
    
    
    # ------Prepare to start Routine "base_task_end"-------
    continueRoutine = True
    # update component parameters for each repeat
    output_filepath = os.path.join(output_path, f'{current_task.name}-{subject_id}.dat')
    current_task.write_results(output_filepath)
    base_text_task_end.setText(expmsgs.task_over)
    base_key_resp_task_end.keys = []
    base_key_resp_task_end.rt = []
    _base_key_resp_task_end_allKeys = []
    # keep track of which components have finished
    base_task_endComponents = [base_text_task_end, base_key_resp_task_end]
    for thisComponent in base_task_endComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    base_task_endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "base_task_end"-------
    while continueRoutine:
        # get current time
        t = base_task_endClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=base_task_endClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
            core.quit()
        
        # *base_text_task_end* updates
        if base_text_task_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            base_text_task_end.frameNStart = frameN  # exact frame index
            base_text_task_end.tStart = t  # local t and not account for scr refresh
            base_text_task_end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(base_text_task_end, 'tStartRefresh')  # time at next scr refresh
            base_text_task_end.setAutoDraw(True)
        
        # *base_key_resp_task_end* updates
        waitOnFlip = False
        if base_key_resp_task_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            base_key_resp_task_end.frameNStart = frameN  # exact frame index
            base_key_resp_task_end.tStart = t  # local t and not account for scr refresh
            base_key_resp_task_end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(base_key_resp_task_end, 'tStartRefresh')  # time at next scr refresh
            base_key_resp_task_end.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(base_key_resp_task_end.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(base_key_resp_task_end.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if base_key_resp_task_end.status == STARTED and not waitOnFlip:
            theseKeys = base_key_resp_task_end.getKeys(keyList=['space'], waitRelease=False)
            _base_key_resp_task_end_allKeys.extend(theseKeys)
            if len(_base_key_resp_task_end_allKeys):
                base_key_resp_task_end.keys = _base_key_resp_task_end_allKeys[-1].name  # just the last key pressed
                base_key_resp_task_end.rt = _base_key_resp_task_end_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in base_task_endComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "base_task_end"-------
    for thisComponent in base_task_endComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    do_sentence_span_dummy.addData('base_text_task_end.started', base_text_task_end.tStartRefresh)
    do_sentence_span_dummy.addData('base_text_task_end.stopped', base_text_task_end.tStopRefresh)
    # check responses
    if base_key_resp_task_end.keys in ['', [], None]:  # No response was made
        base_key_resp_task_end.keys = None
    do_sentence_span_dummy.addData('base_key_resp_task_end.keys',base_key_resp_task_end.keys)
    if base_key_resp_task_end.keys != None:  # we had a response
        do_sentence_span_dummy.addData('base_key_resp_task_end.rt', base_key_resp_task_end.rt)
    do_sentence_span_dummy.addData('base_key_resp_task_end.started', base_key_resp_task_end.tStartRefresh)
    do_sentence_span_dummy.addData('base_key_resp_task_end.stopped', base_key_resp_task_end.tStopRefresh)
    # the Routine "base_task_end" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed do_ss_task repeats of 'do_sentence_span_dummy'


# set up handler to look after randomisation of conditions etc
do_spatial_short_term_memory_dummy = data.TrialHandler(nReps=do_sstm_task, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='do_spatial_short_term_memory_dummy')
thisExp.addLoop(do_spatial_short_term_memory_dummy)  # add the loop to the experiment
thisDo_spatial_short_term_memory_dummy = do_spatial_short_term_memory_dummy.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisDo_spatial_short_term_memory_dummy.rgb)
if thisDo_spatial_short_term_memory_dummy != None:
    for paramName in thisDo_spatial_short_term_memory_dummy:
        exec('{} = thisDo_spatial_short_term_memory_dummy[paramName]'.format(paramName))

for thisDo_spatial_short_term_memory_dummy in do_spatial_short_term_memory_dummy:
    currentLoop = do_spatial_short_term_memory_dummy
    # abbreviate parameter names if possible (e.g. rgb = thisDo_spatial_short_term_memory_dummy.rgb)
    if thisDo_spatial_short_term_memory_dummy != None:
        for paramName in thisDo_spatial_short_term_memory_dummy:
            exec('{} = thisDo_spatial_short_term_memory_dummy[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "sstm_init"-------
    continueRoutine = True
    # update component parameters for each repeat
    # task initialization is done at the experiment beginning
    # to circumvent lag when generating dots
    current_task = sstm_task
    
    instruction_filepaths = instructions.get_instructions('sstm')
    n_instruction_pages = instructions.get_instruction_page_count('sstm')
    # keep track of which components have finished
    sstm_initComponents = []
    for thisComponent in sstm_initComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    sstm_initClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "sstm_init"-------
    while continueRoutine:
        # get current time
        t = sstm_initClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=sstm_initClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in sstm_initComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "sstm_init"-------
    for thisComponent in sstm_initComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "sstm_init" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    sstm_instruction_pages = data.TrialHandler(nReps=n_instruction_pages, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='sstm_instruction_pages')
    thisExp.addLoop(sstm_instruction_pages)  # add the loop to the experiment
    thisSstm_instruction_page = sstm_instruction_pages.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisSstm_instruction_page.rgb)
    if thisSstm_instruction_page != None:
        for paramName in thisSstm_instruction_page:
            exec('{} = thisSstm_instruction_page[paramName]'.format(paramName))
    
    for thisSstm_instruction_page in sstm_instruction_pages:
        currentLoop = sstm_instruction_pages
        # abbreviate parameter names if possible (e.g. rgb = thisSstm_instruction_page.rgb)
        if thisSstm_instruction_page != None:
            for paramName in thisSstm_instruction_page:
                exec('{} = thisSstm_instruction_page[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "base_instruction"-------
        continueRoutine = True
        # update component parameters for each repeat
        instruction_filepath = instruction_filepaths.pop(0)
        
        # the following is just needed because of a bug in psychopy
        # where images will get a grey border. a workaround is
        # setting up an aperture to hide these borders.
        
        from PIL import Image
        instr_img_size = Image.open(instruction_filepath).size
        
        # set aperture parameters from image size in pixels
        aperture_padding = 4
        aperture_width = instr_img_size[0] - aperture_padding
        aperture_height = instr_img_size[1] - aperture_padding
        
        # height scaling only scales by screen height to keep aspect ratio
        aperture_right = aperture_width / 2 / win.size[1]
        aperture_top = aperture_height / 2 / win.size[1]
        
        # setup rectangle vertices
        aperture_vertices = [
            [aperture_right, aperture_top],
            [aperture_right, -aperture_top],
            [-aperture_right, -aperture_top],
            [-aperture_right, aperture_top],
        ]
        
        aperture_instruction = visual.Aperture(win, size=1, shape='square', units='height')
        
        base_image_instruction.setSize(instr_img_size)
        base_image_instruction.setImage(instruction_filepath)
        base_key_resp_instruction.keys = []
        base_key_resp_instruction.rt = []
        _base_key_resp_instruction_allKeys = []
        # keep track of which components have finished
        base_instructionComponents = [base_image_instruction, base_key_resp_instruction, base_aperture_instruction]
        for thisComponent in base_instructionComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        base_instructionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "base_instruction"-------
        while continueRoutine:
            # get current time
            t = base_instructionClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=base_instructionClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                core.quit()
            
            # *base_image_instruction* updates
            if base_image_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_image_instruction.frameNStart = frameN  # exact frame index
                base_image_instruction.tStart = t  # local t and not account for scr refresh
                base_image_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_image_instruction, 'tStartRefresh')  # time at next scr refresh
                base_image_instruction.setAutoDraw(True)
            
            # *base_key_resp_instruction* updates
            waitOnFlip = False
            if base_key_resp_instruction.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                base_key_resp_instruction.frameNStart = frameN  # exact frame index
                base_key_resp_instruction.tStart = t  # local t and not account for scr refresh
                base_key_resp_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_key_resp_instruction, 'tStartRefresh')  # time at next scr refresh
                base_key_resp_instruction.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(base_key_resp_instruction.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(base_key_resp_instruction.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if base_key_resp_instruction.status == STARTED and not waitOnFlip:
                theseKeys = base_key_resp_instruction.getKeys(keyList=None, waitRelease=False)
                _base_key_resp_instruction_allKeys.extend(theseKeys)
                if len(_base_key_resp_instruction_allKeys):
                    base_key_resp_instruction.keys = _base_key_resp_instruction_allKeys[-1].name  # just the last key pressed
                    base_key_resp_instruction.rt = _base_key_resp_instruction_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # *base_aperture_instruction* updates
            if base_aperture_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_aperture_instruction.frameNStart = frameN  # exact frame index
                base_aperture_instruction.tStart = t  # local t and not account for scr refresh
                base_aperture_instruction.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_aperture_instruction, 'tStartRefresh')  # time at next scr refresh
                base_aperture_instruction.enabled = True
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in base_instructionComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "base_instruction"-------
        for thisComponent in base_instructionComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        del aperture_instruction
        sstm_instruction_pages.addData('base_image_instruction.started', base_image_instruction.tStartRefresh)
        sstm_instruction_pages.addData('base_image_instruction.stopped', base_image_instruction.tStopRefresh)
        # check responses
        if base_key_resp_instruction.keys in ['', [], None]:  # No response was made
            base_key_resp_instruction.keys = None
        sstm_instruction_pages.addData('base_key_resp_instruction.keys',base_key_resp_instruction.keys)
        if base_key_resp_instruction.keys != None:  # we had a response
            sstm_instruction_pages.addData('base_key_resp_instruction.rt', base_key_resp_instruction.rt)
        sstm_instruction_pages.addData('base_key_resp_instruction.started', base_key_resp_instruction.tStartRefresh)
        sstm_instruction_pages.addData('base_key_resp_instruction.stopped', base_key_resp_instruction.tStopRefresh)
        base_aperture_instruction.enabled = False  # just in case it was left enabled
        sstm_instruction_pages.addData('base_aperture_instruction.started', base_aperture_instruction.tStartRefresh)
        sstm_instruction_pages.addData('base_aperture_instruction.stopped', base_aperture_instruction.tStopRefresh)
        # the Routine "base_instruction" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed n_instruction_pages repeats of 'sstm_instruction_pages'
    
    
    # set up handler to look after randomisation of conditions etc
    sstm_practice_dummy = data.TrialHandler(nReps=2, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='sstm_practice_dummy')
    thisExp.addLoop(sstm_practice_dummy)  # add the loop to the experiment
    thisSstm_practice_dummy = sstm_practice_dummy.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisSstm_practice_dummy.rgb)
    if thisSstm_practice_dummy != None:
        for paramName in thisSstm_practice_dummy:
            exec('{} = thisSstm_practice_dummy[paramName]'.format(paramName))
    
    for thisSstm_practice_dummy in sstm_practice_dummy:
        currentLoop = sstm_practice_dummy
        # abbreviate parameter names if possible (e.g. rgb = thisSstm_practice_dummy.rgb)
        if thisSstm_practice_dummy != None:
            for paramName in thisSstm_practice_dummy:
                exec('{} = thisSstm_practice_dummy[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "base_init_task"-------
        continueRoutine = True
        # update component parameters for each repeat
        # set begin task message depending on practice
        if current_task.do_practice:
            msg_task_begin = expmsgs.begin_practice
        else:
            msg_task_begin = expmsgs.begin_task
        
        n_trials = current_task.get_trial_count()
        base_text_begin_task.setText(msg_task_begin)
        base_key_resp_task_begin.keys = []
        base_key_resp_task_begin.rt = []
        _base_key_resp_task_begin_allKeys = []
        # keep track of which components have finished
        base_init_taskComponents = [base_text_begin_task, base_key_resp_task_begin]
        for thisComponent in base_init_taskComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        base_init_taskClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "base_init_task"-------
        while continueRoutine:
            # get current time
            t = base_init_taskClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=base_init_taskClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                core.quit()
            
            # *base_text_begin_task* updates
            if base_text_begin_task.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                base_text_begin_task.frameNStart = frameN  # exact frame index
                base_text_begin_task.tStart = t  # local t and not account for scr refresh
                base_text_begin_task.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_text_begin_task, 'tStartRefresh')  # time at next scr refresh
                base_text_begin_task.setAutoDraw(True)
            
            # *base_key_resp_task_begin* updates
            waitOnFlip = False
            if base_key_resp_task_begin.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                base_key_resp_task_begin.frameNStart = frameN  # exact frame index
                base_key_resp_task_begin.tStart = t  # local t and not account for scr refresh
                base_key_resp_task_begin.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(base_key_resp_task_begin, 'tStartRefresh')  # time at next scr refresh
                base_key_resp_task_begin.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(base_key_resp_task_begin.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(base_key_resp_task_begin.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if base_key_resp_task_begin.status == STARTED and not waitOnFlip:
                theseKeys = base_key_resp_task_begin.getKeys(keyList=['space'], waitRelease=False)
                _base_key_resp_task_begin_allKeys.extend(theseKeys)
                if len(_base_key_resp_task_begin_allKeys):
                    base_key_resp_task_begin.keys = _base_key_resp_task_begin_allKeys[-1].name  # just the last key pressed
                    base_key_resp_task_begin.rt = _base_key_resp_task_begin_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in base_init_taskComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "base_init_task"-------
        for thisComponent in base_init_taskComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        sstm_practice_dummy.addData('base_text_begin_task.started', base_text_begin_task.tStartRefresh)
        sstm_practice_dummy.addData('base_text_begin_task.stopped', base_text_begin_task.tStopRefresh)
        # check responses
        if base_key_resp_task_begin.keys in ['', [], None]:  # No response was made
            base_key_resp_task_begin.keys = None
        sstm_practice_dummy.addData('base_key_resp_task_begin.keys',base_key_resp_task_begin.keys)
        if base_key_resp_task_begin.keys != None:  # we had a response
            sstm_practice_dummy.addData('base_key_resp_task_begin.rt', base_key_resp_task_begin.rt)
        sstm_practice_dummy.addData('base_key_resp_task_begin.started', base_key_resp_task_begin.tStartRefresh)
        sstm_practice_dummy.addData('base_key_resp_task_begin.stopped', base_key_resp_task_begin.tStopRefresh)
        # the Routine "base_init_task" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        sstm_trials = data.TrialHandler(nReps=n_trials, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='sstm_trials')
        thisExp.addLoop(sstm_trials)  # add the loop to the experiment
        thisSstm_trial = sstm_trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSstm_trial.rgb)
        if thisSstm_trial != None:
            for paramName in thisSstm_trial:
                exec('{} = thisSstm_trial[paramName]'.format(paramName))
        
        for thisSstm_trial in sstm_trials:
            currentLoop = sstm_trials
            # abbreviate parameter names if possible (e.g. rgb = thisSstm_trial.rgb)
            if thisSstm_trial != None:
                for paramName in thisSstm_trial:
                    exec('{} = thisSstm_trial[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "base_init_trial"-------
            continueRoutine = True
            # update component parameters for each repeat
            current_trial = current_task.start_new_trial()
            do_break = current_task.has_pause()
            # keep track of which components have finished
            base_init_trialComponents = []
            for thisComponent in base_init_trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            base_init_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "base_init_trial"-------
            while continueRoutine:
                # get current time
                t = base_init_trialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=base_init_trialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in base_init_trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "base_init_trial"-------
            for thisComponent in base_init_trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "base_init_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "sstm_init_trial"-------
            continueRoutine = True
            # update component parameters for each repeat
            n_presentations = current_trial.get_presentation_count()
            
            # keep track of which components have finished
            sstm_init_trialComponents = [sstm_text_fixation_cross]
            for thisComponent in sstm_init_trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            sstm_init_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "sstm_init_trial"-------
            while continueRoutine:
                # get current time
                t = sstm_init_trialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=sstm_init_trialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # *sstm_text_fixation_cross* updates
                if sstm_text_fixation_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    sstm_text_fixation_cross.frameNStart = frameN  # exact frame index
                    sstm_text_fixation_cross.tStart = t  # local t and not account for scr refresh
                    sstm_text_fixation_cross.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(sstm_text_fixation_cross, 'tStartRefresh')  # time at next scr refresh
                    sstm_text_fixation_cross.setAutoDraw(True)
                if sstm_text_fixation_cross.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > sstm_text_fixation_cross.tStartRefresh + current_task.config.timing.fixation_cross-frameTolerance:
                        # keep track of stop time/frame for later
                        sstm_text_fixation_cross.tStop = t  # not accounting for scr refresh
                        sstm_text_fixation_cross.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(sstm_text_fixation_cross, 'tStopRefresh')  # time at next scr refresh
                        sstm_text_fixation_cross.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in sstm_init_trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "sstm_init_trial"-------
            for thisComponent in sstm_init_trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            sstm_trials.addData('sstm_text_fixation_cross.started', sstm_text_fixation_cross.tStartRefresh)
            sstm_trials.addData('sstm_text_fixation_cross.stopped', sstm_text_fixation_cross.tStopRefresh)
            # the Routine "sstm_init_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "sstm_empty_grid"-------
            continueRoutine = True
            # update component parameters for each repeat
            current_trial.grid.show(True)
            # keep track of which components have finished
            sstm_empty_gridComponents = [sstm_text_blank]
            for thisComponent in sstm_empty_gridComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            sstm_empty_gridClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "sstm_empty_grid"-------
            while continueRoutine:
                # get current time
                t = sstm_empty_gridClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=sstm_empty_gridClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # *sstm_text_blank* updates
                if sstm_text_blank.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    sstm_text_blank.frameNStart = frameN  # exact frame index
                    sstm_text_blank.tStart = t  # local t and not account for scr refresh
                    sstm_text_blank.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(sstm_text_blank, 'tStartRefresh')  # time at next scr refresh
                    sstm_text_blank.setAutoDraw(True)
                if sstm_text_blank.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > sstm_text_blank.tStartRefresh + current_task.config.timing.init_trial-frameTolerance:
                        # keep track of stop time/frame for later
                        sstm_text_blank.tStop = t  # not accounting for scr refresh
                        sstm_text_blank.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(sstm_text_blank, 'tStopRefresh')  # time at next scr refresh
                        sstm_text_blank.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in sstm_empty_gridComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "sstm_empty_grid"-------
            for thisComponent in sstm_empty_gridComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            sstm_trials.addData('sstm_text_blank.started', sstm_text_blank.tStartRefresh)
            sstm_trials.addData('sstm_text_blank.stopped', sstm_text_blank.tStopRefresh)
            # the Routine "sstm_empty_grid" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # set up handler to look after randomisation of conditions etc
            sstm_presentations = data.TrialHandler(nReps=n_presentations, method='sequential', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='sstm_presentations')
            thisExp.addLoop(sstm_presentations)  # add the loop to the experiment
            thisSstm_presentation = sstm_presentations.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisSstm_presentation.rgb)
            if thisSstm_presentation != None:
                for paramName in thisSstm_presentation:
                    exec('{} = thisSstm_presentation[paramName]'.format(paramName))
            
            for thisSstm_presentation in sstm_presentations:
                currentLoop = sstm_presentations
                # abbreviate parameter names if possible (e.g. rgb = thisSstm_presentation.rgb)
                if thisSstm_presentation != None:
                    for paramName in thisSstm_presentation:
                        exec('{} = thisSstm_presentation[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "sstm_display_dot"-------
                continueRoutine = True
                # update component parameters for each repeat
                current_dot = current_trial.get_next_presentation()
                sstm_polygon_display_dot.setPos(current_dot)
                sstm_polygon_display_dot.setSize((current_task.config.dots.size, current_task.config.dots.size))
                # keep track of which components have finished
                sstm_display_dotComponents = [sstm_polygon_display_dot]
                for thisComponent in sstm_display_dotComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                sstm_display_dotClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "sstm_display_dot"-------
                while continueRoutine:
                    # get current time
                    t = sstm_display_dotClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=sstm_display_dotClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *sstm_polygon_display_dot* updates
                    if sstm_polygon_display_dot.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        sstm_polygon_display_dot.frameNStart = frameN  # exact frame index
                        sstm_polygon_display_dot.tStart = t  # local t and not account for scr refresh
                        sstm_polygon_display_dot.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(sstm_polygon_display_dot, 'tStartRefresh')  # time at next scr refresh
                        sstm_polygon_display_dot.setAutoDraw(True)
                    if sstm_polygon_display_dot.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > sstm_polygon_display_dot.tStartRefresh + current_task.config.timing.dot-frameTolerance:
                            # keep track of stop time/frame for later
                            sstm_polygon_display_dot.tStop = t  # not accounting for scr refresh
                            sstm_polygon_display_dot.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(sstm_polygon_display_dot, 'tStopRefresh')  # time at next scr refresh
                            sstm_polygon_display_dot.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in sstm_display_dotComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "sstm_display_dot"-------
                for thisComponent in sstm_display_dotComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                sstm_presentations.addData('sstm_polygon_display_dot.started', sstm_polygon_display_dot.tStartRefresh)
                sstm_presentations.addData('sstm_polygon_display_dot.stopped', sstm_polygon_display_dot.tStopRefresh)
                # the Routine "sstm_display_dot" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                
                # ------Prepare to start Routine "sstm_after_display_dot"-------
                continueRoutine = True
                # update component parameters for each repeat
                # keep track of which components have finished
                sstm_after_display_dotComponents = [sstm_text_after_display_dot]
                for thisComponent in sstm_after_display_dotComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                sstm_after_display_dotClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "sstm_after_display_dot"-------
                while continueRoutine:
                    # get current time
                    t = sstm_after_display_dotClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=sstm_after_display_dotClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *sstm_text_after_display_dot* updates
                    if sstm_text_after_display_dot.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        sstm_text_after_display_dot.frameNStart = frameN  # exact frame index
                        sstm_text_after_display_dot.tStart = t  # local t and not account for scr refresh
                        sstm_text_after_display_dot.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(sstm_text_after_display_dot, 'tStartRefresh')  # time at next scr refresh
                        sstm_text_after_display_dot.setAutoDraw(True)
                    if sstm_text_after_display_dot.status == STARTED:
                        # is it time to stop? (based on global clock, using actual start)
                        if tThisFlipGlobal > sstm_text_after_display_dot.tStartRefresh + current_task.config.timing.inter_item-frameTolerance:
                            # keep track of stop time/frame for later
                            sstm_text_after_display_dot.tStop = t  # not accounting for scr refresh
                            sstm_text_after_display_dot.frameNStop = frameN  # exact frame index
                            win.timeOnFlip(sstm_text_after_display_dot, 'tStopRefresh')  # time at next scr refresh
                            sstm_text_after_display_dot.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in sstm_after_display_dotComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "sstm_after_display_dot"-------
                for thisComponent in sstm_after_display_dotComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                sstm_presentations.addData('sstm_text_after_display_dot.started', sstm_text_after_display_dot.tStartRefresh)
                sstm_presentations.addData('sstm_text_after_display_dot.stopped', sstm_text_after_display_dot.tStopRefresh)
                # the Routine "sstm_after_display_dot" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed n_presentations repeats of 'sstm_presentations'
            
            
            # ------Prepare to start Routine "sstm_draw_request"-------
            continueRoutine = True
            # update component parameters for each repeat
            current_trial.grid.show(False)
            text_sstm_draw_dots.setText(expmsgs.draw_dots)
            text_sstm_presentation_end.setText(expmsgs.word_end)
            # keep track of which components have finished
            sstm_draw_requestComponents = [text_sstm_draw_dots, text_sstm_presentation_end]
            for thisComponent in sstm_draw_requestComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            sstm_draw_requestClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "sstm_draw_request"-------
            while continueRoutine:
                # get current time
                t = sstm_draw_requestClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=sstm_draw_requestClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # *text_sstm_draw_dots* updates
                if text_sstm_draw_dots.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text_sstm_draw_dots.frameNStart = frameN  # exact frame index
                    text_sstm_draw_dots.tStart = t  # local t and not account for scr refresh
                    text_sstm_draw_dots.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_sstm_draw_dots, 'tStartRefresh')  # time at next scr refresh
                    text_sstm_draw_dots.setAutoDraw(True)
                if text_sstm_draw_dots.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > text_sstm_draw_dots.tStartRefresh + current_task.config.timing.draw_request-frameTolerance:
                        # keep track of stop time/frame for later
                        text_sstm_draw_dots.tStop = t  # not accounting for scr refresh
                        text_sstm_draw_dots.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(text_sstm_draw_dots, 'tStopRefresh')  # time at next scr refresh
                        text_sstm_draw_dots.setAutoDraw(False)
                
                # *text_sstm_presentation_end* updates
                if text_sstm_presentation_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text_sstm_presentation_end.frameNStart = frameN  # exact frame index
                    text_sstm_presentation_end.tStart = t  # local t and not account for scr refresh
                    text_sstm_presentation_end.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_sstm_presentation_end, 'tStartRefresh')  # time at next scr refresh
                    text_sstm_presentation_end.setAutoDraw(True)
                if text_sstm_presentation_end.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > text_sstm_presentation_end.tStartRefresh + current_task.config.timing.draw_request-frameTolerance:
                        # keep track of stop time/frame for later
                        text_sstm_presentation_end.tStop = t  # not accounting for scr refresh
                        text_sstm_presentation_end.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(text_sstm_presentation_end, 'tStopRefresh')  # time at next scr refresh
                        text_sstm_presentation_end.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in sstm_draw_requestComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "sstm_draw_request"-------
            for thisComponent in sstm_draw_requestComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            sstm_trials.addData('text_sstm_draw_dots.started', text_sstm_draw_dots.tStartRefresh)
            sstm_trials.addData('text_sstm_draw_dots.stopped', text_sstm_draw_dots.tStopRefresh)
            sstm_trials.addData('text_sstm_presentation_end.started', text_sstm_presentation_end.tStartRefresh)
            sstm_trials.addData('text_sstm_presentation_end.stopped', text_sstm_presentation_end.tStopRefresh)
            # the Routine "sstm_draw_request" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "sstm_recall"-------
            continueRoutine = True
            # update component parameters for each repeat
            current_trial.grid.show(True)
            win.mouseVisible = True
            sstm_mouse.setVisible(True)
            sstm_text_next.setText(expmsgs.word_next)
            # setup some python lists for storing info about the sstm_mouse
            sstm_mouse.x = []
            sstm_mouse.y = []
            sstm_mouse.leftButton = []
            sstm_mouse.midButton = []
            sstm_mouse.rightButton = []
            sstm_mouse.time = []
            sstm_mouse.clicked_name = []
            gotValidClick = False  # until a click is received
            sstm_mouse.mouseClock.reset()
            # keep track of which components have finished
            sstm_recallComponents = [sstm_text_next, sstm_mouse]
            for thisComponent in sstm_recallComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            sstm_recallClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "sstm_recall"-------
            while continueRoutine:
                # get current time
                t = sstm_recallClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=sstm_recallClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                    
                current_trial.process_mouse_event(sstm_mouse)
                
                active_position = config.spatial_short_term_memory.text.next_button.position
                if current_trial.selected_required_count():
                    sstm_text_next.pos = active_position
                else:
                    sstm_text_next.pos = (10, 10)
                
                # *sstm_text_next* updates
                if sstm_text_next.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    sstm_text_next.frameNStart = frameN  # exact frame index
                    sstm_text_next.tStart = t  # local t and not account for scr refresh
                    sstm_text_next.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(sstm_text_next, 'tStartRefresh')  # time at next scr refresh
                    sstm_text_next.setAutoDraw(True)
                # *sstm_mouse* updates
                if sstm_mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    sstm_mouse.frameNStart = frameN  # exact frame index
                    sstm_mouse.tStart = t  # local t and not account for scr refresh
                    sstm_mouse.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(sstm_mouse, 'tStartRefresh')  # time at next scr refresh
                    sstm_mouse.status = STARTED
                    prevButtonState = sstm_mouse.getPressed()  # if button is down already this ISN'T a new click
                if sstm_mouse.status == STARTED:  # only update if started and not finished!
                    buttons = sstm_mouse.getPressed()
                    if buttons != prevButtonState:  # button state changed?
                        prevButtonState = buttons
                        if sum(buttons) > 0:  # state changed to a new click
                            # check if the mouse was inside our 'clickable' objects
                            gotValidClick = False
                            for obj in [sstm_text_next]:
                                if obj.contains(sstm_mouse):
                                    gotValidClick = True
                                    sstm_mouse.clicked_name.append(obj.name)
                            x, y = sstm_mouse.getPos()
                            sstm_mouse.x.append(x)
                            sstm_mouse.y.append(y)
                            buttons = sstm_mouse.getPressed()
                            sstm_mouse.leftButton.append(buttons[0])
                            sstm_mouse.midButton.append(buttons[1])
                            sstm_mouse.rightButton.append(buttons[2])
                            sstm_mouse.time.append(sstm_mouse.mouseClock.getTime())
                            if gotValidClick:  # abort routine on response
                                continueRoutine = False
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in sstm_recallComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "sstm_recall"-------
            for thisComponent in sstm_recallComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            win.mouseVisible = False
            sstm_mouse.setVisible(False)
            
            sstm_trial_rt = sstm_mouse.time[-1]
            current_trial.save_response(sstm_trial_rt)
            
            current_trial.show(False)
            
            thisExp.addData('is_practice', current_task.do_practice)
            thisExp.addData('sstm_recall.correct_dots', current_trial.sequence)
            thisExp.addData('sstm_recall.response_dots', current_trial.response_dots)
            thisExp.addData('sstm_recall.response_time', current_trial.response_time)
            sstm_trials.addData('sstm_text_next.started', sstm_text_next.tStartRefresh)
            sstm_trials.addData('sstm_text_next.stopped', sstm_text_next.tStopRefresh)
            # store data for sstm_trials (TrialHandler)
            if len(sstm_mouse.x): sstm_trials.addData('sstm_mouse.x', sstm_mouse.x[0])
            if len(sstm_mouse.y): sstm_trials.addData('sstm_mouse.y', sstm_mouse.y[0])
            if len(sstm_mouse.leftButton): sstm_trials.addData('sstm_mouse.leftButton', sstm_mouse.leftButton[0])
            if len(sstm_mouse.midButton): sstm_trials.addData('sstm_mouse.midButton', sstm_mouse.midButton[0])
            if len(sstm_mouse.rightButton): sstm_trials.addData('sstm_mouse.rightButton', sstm_mouse.rightButton[0])
            if len(sstm_mouse.time): sstm_trials.addData('sstm_mouse.time', sstm_mouse.time[0])
            if len(sstm_mouse.clicked_name): sstm_trials.addData('sstm_mouse.clicked_name', sstm_mouse.clicked_name[0])
            sstm_trials.addData('sstm_mouse.started', sstm_mouse.tStart)
            sstm_trials.addData('sstm_mouse.stopped', sstm_mouse.tStop)
            # the Routine "sstm_recall" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # set up handler to look after randomisation of conditions etc
            sstm_next_trial_dummy = data.TrialHandler(nReps=current_task.get_left_trials() > 0, method='random', 
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='sstm_next_trial_dummy')
            thisExp.addLoop(sstm_next_trial_dummy)  # add the loop to the experiment
            thisSstm_next_trial_dummy = sstm_next_trial_dummy.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisSstm_next_trial_dummy.rgb)
            if thisSstm_next_trial_dummy != None:
                for paramName in thisSstm_next_trial_dummy:
                    exec('{} = thisSstm_next_trial_dummy[paramName]'.format(paramName))
            
            for thisSstm_next_trial_dummy in sstm_next_trial_dummy:
                currentLoop = sstm_next_trial_dummy
                # abbreviate parameter names if possible (e.g. rgb = thisSstm_next_trial_dummy.rgb)
                if thisSstm_next_trial_dummy != None:
                    for paramName in thisSstm_next_trial_dummy:
                        exec('{} = thisSstm_next_trial_dummy[paramName]'.format(paramName))
                
                # ------Prepare to start Routine "base_next_trial"-------
                continueRoutine = True
                # update component parameters for each repeat
                base_text_next_trial.setText(expmsgs.next_trial)
                base_next_trial_key_resp.keys = []
                base_next_trial_key_resp.rt = []
                _base_next_trial_key_resp_allKeys = []
                # keep track of which components have finished
                base_next_trialComponents = [base_text_next_trial, base_next_trial_key_resp]
                for thisComponent in base_next_trialComponents:
                    thisComponent.tStart = None
                    thisComponent.tStop = None
                    thisComponent.tStartRefresh = None
                    thisComponent.tStopRefresh = None
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                # reset timers
                t = 0
                _timeToFirstFrame = win.getFutureFlipTime(clock="now")
                base_next_trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
                frameN = -1
                
                # -------Run Routine "base_next_trial"-------
                while continueRoutine:
                    # get current time
                    t = base_next_trialClock.getTime()
                    tThisFlip = win.getFutureFlipTime(clock=base_next_trialClock)
                    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                        core.quit()
                    
                    # *base_text_next_trial* updates
                    if base_text_next_trial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        base_text_next_trial.frameNStart = frameN  # exact frame index
                        base_text_next_trial.tStart = t  # local t and not account for scr refresh
                        base_text_next_trial.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(base_text_next_trial, 'tStartRefresh')  # time at next scr refresh
                        base_text_next_trial.setAutoDraw(True)
                    
                    # *base_next_trial_key_resp* updates
                    waitOnFlip = False
                    if base_next_trial_key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                        # keep track of start time/frame for later
                        base_next_trial_key_resp.frameNStart = frameN  # exact frame index
                        base_next_trial_key_resp.tStart = t  # local t and not account for scr refresh
                        base_next_trial_key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(base_next_trial_key_resp, 'tStartRefresh')  # time at next scr refresh
                        base_next_trial_key_resp.status = STARTED
                        # keyboard checking is just starting
                        waitOnFlip = True
                        win.callOnFlip(base_next_trial_key_resp.clock.reset)  # t=0 on next screen flip
                        win.callOnFlip(base_next_trial_key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                    if base_next_trial_key_resp.status == STARTED and not waitOnFlip:
                        theseKeys = base_next_trial_key_resp.getKeys(keyList=['space'], waitRelease=False)
                        _base_next_trial_key_resp_allKeys.extend(theseKeys)
                        if len(_base_next_trial_key_resp_allKeys):
                            base_next_trial_key_resp.keys = _base_next_trial_key_resp_allKeys[-1].name  # just the last key pressed
                            base_next_trial_key_resp.rt = _base_next_trial_key_resp_allKeys[-1].rt
                            # a response ends the routine
                            continueRoutine = False
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in base_next_trialComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "base_next_trial"-------
                for thisComponent in base_next_trialComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                sstm_next_trial_dummy.addData('base_text_next_trial.started', base_text_next_trial.tStartRefresh)
                sstm_next_trial_dummy.addData('base_text_next_trial.stopped', base_text_next_trial.tStopRefresh)
                # check responses
                if base_next_trial_key_resp.keys in ['', [], None]:  # No response was made
                    base_next_trial_key_resp.keys = None
                sstm_next_trial_dummy.addData('base_next_trial_key_resp.keys',base_next_trial_key_resp.keys)
                if base_next_trial_key_resp.keys != None:  # we had a response
                    sstm_next_trial_dummy.addData('base_next_trial_key_resp.rt', base_next_trial_key_resp.rt)
                sstm_next_trial_dummy.addData('base_next_trial_key_resp.started', base_next_trial_key_resp.tStartRefresh)
                sstm_next_trial_dummy.addData('base_next_trial_key_resp.stopped', base_next_trial_key_resp.tStopRefresh)
                # the Routine "base_next_trial" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()
                thisExp.nextEntry()
                
            # completed current_task.get_left_trials() > 0 repeats of 'sstm_next_trial_dummy'
            
            
            # ------Prepare to start Routine "base_intertrial"-------
            continueRoutine = True
            # update component parameters for each repeat
            current_task.finish_trial()
            # keep track of which components have finished
            base_intertrialComponents = [base_text_intertrial]
            for thisComponent in base_intertrialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            base_intertrialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "base_intertrial"-------
            while continueRoutine:
                # get current time
                t = base_intertrialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=base_intertrialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
                    core.quit()
                
                # *base_text_intertrial* updates
                if base_text_intertrial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    base_text_intertrial.frameNStart = frameN  # exact frame index
                    base_text_intertrial.tStart = t  # local t and not account for scr refresh
                    base_text_intertrial.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(base_text_intertrial, 'tStartRefresh')  # time at next scr refresh
                    base_text_intertrial.setAutoDraw(True)
                if base_text_intertrial.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > base_text_intertrial.tStartRefresh + current_task.config.timing.inter_trial-frameTolerance:
                        # keep track of stop time/frame for later
                        base_text_intertrial.tStop = t  # not accounting for scr refresh
                        base_text_intertrial.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(base_text_intertrial, 'tStopRefresh')  # time at next scr refresh
                        base_text_intertrial.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in base_intertrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "base_intertrial"-------
            for thisComponent in base_intertrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            sstm_trials.addData('base_text_intertrial.started', base_text_intertrial.tStartRefresh)
            sstm_trials.addData('base_text_intertrial.stopped', base_text_intertrial.tStopRefresh)
            # the Routine "base_intertrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed n_trials repeats of 'sstm_trials'
        
        thisExp.nextEntry()
        
    # completed 2 repeats of 'sstm_practice_dummy'
    
    
    # ------Prepare to start Routine "sstm_task_end"-------
    continueRoutine = True
    # update component parameters for each repeat
    detailed_output_filepath = os.path.join(output_path, 'sstm_detailed', f'{current_task.name}-{subject_id}.dat')
    current_task.write_results(detailed_output_filepath)
    
    overall_output_filepath = os.path.join(output_path, f'{current_task.name}-{subject_id}.dat')
    current_task.write_overall_results(overall_output_filepath)
    sstm_key_resp_task_end.keys = []
    sstm_key_resp_task_end.rt = []
    _sstm_key_resp_task_end_allKeys = []
    # keep track of which components have finished
    sstm_task_endComponents = [text_sstm_task_end, sstm_key_resp_task_end]
    for thisComponent in sstm_task_endComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    sstm_task_endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "sstm_task_end"-------
    while continueRoutine:
        # get current time
        t = sstm_task_endClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=sstm_task_endClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
            core.quit()
        
        # *text_sstm_task_end* updates
        if text_sstm_task_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_sstm_task_end.frameNStart = frameN  # exact frame index
            text_sstm_task_end.tStart = t  # local t and not account for scr refresh
            text_sstm_task_end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_sstm_task_end, 'tStartRefresh')  # time at next scr refresh
            text_sstm_task_end.setAutoDraw(True)
        
        # *sstm_key_resp_task_end* updates
        waitOnFlip = False
        if sstm_key_resp_task_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sstm_key_resp_task_end.frameNStart = frameN  # exact frame index
            sstm_key_resp_task_end.tStart = t  # local t and not account for scr refresh
            sstm_key_resp_task_end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(sstm_key_resp_task_end, 'tStartRefresh')  # time at next scr refresh
            sstm_key_resp_task_end.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(sstm_key_resp_task_end.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(sstm_key_resp_task_end.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if sstm_key_resp_task_end.status == STARTED and not waitOnFlip:
            theseKeys = sstm_key_resp_task_end.getKeys(keyList=['space'], waitRelease=False)
            _sstm_key_resp_task_end_allKeys.extend(theseKeys)
            if len(_sstm_key_resp_task_end_allKeys):
                sstm_key_resp_task_end.keys = _sstm_key_resp_task_end_allKeys[-1].name  # just the last key pressed
                sstm_key_resp_task_end.rt = _sstm_key_resp_task_end_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in sstm_task_endComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "sstm_task_end"-------
    for thisComponent in sstm_task_endComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    do_spatial_short_term_memory_dummy.addData('text_sstm_task_end.started', text_sstm_task_end.tStartRefresh)
    do_spatial_short_term_memory_dummy.addData('text_sstm_task_end.stopped', text_sstm_task_end.tStopRefresh)
    # check responses
    if sstm_key_resp_task_end.keys in ['', [], None]:  # No response was made
        sstm_key_resp_task_end.keys = None
    do_spatial_short_term_memory_dummy.addData('sstm_key_resp_task_end.keys',sstm_key_resp_task_end.keys)
    if sstm_key_resp_task_end.keys != None:  # we had a response
        do_spatial_short_term_memory_dummy.addData('sstm_key_resp_task_end.rt', sstm_key_resp_task_end.rt)
    do_spatial_short_term_memory_dummy.addData('sstm_key_resp_task_end.started', sstm_key_resp_task_end.tStartRefresh)
    do_spatial_short_term_memory_dummy.addData('sstm_key_resp_task_end.stopped', sstm_key_resp_task_end.tStopRefresh)
    # the Routine "sstm_task_end" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed do_sstm_task repeats of 'do_spatial_short_term_memory_dummy'


# ------Prepare to start Routine "base_end"-------
continueRoutine = True
# update component parameters for each repeat
base_text_end.setText(expmsgs.experiment_over)
base_key_resp_end.keys = []
base_key_resp_end.rt = []
_base_key_resp_end_allKeys = []
# keep track of which components have finished
base_endComponents = [base_text_end, base_key_resp_end]
for thisComponent in base_endComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
base_endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "base_end"-------
while continueRoutine:
    # get current time
    t = base_endClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=base_endClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
        core.quit()
    
    # *base_text_end* updates
    if base_text_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        base_text_end.frameNStart = frameN  # exact frame index
        base_text_end.tStart = t  # local t and not account for scr refresh
        base_text_end.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(base_text_end, 'tStartRefresh')  # time at next scr refresh
        base_text_end.setAutoDraw(True)
    if base_text_end.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > base_text_end.tStartRefresh + 7-frameTolerance:
            # keep track of stop time/frame for later
            base_text_end.tStop = t  # not accounting for scr refresh
            base_text_end.frameNStop = frameN  # exact frame index
            win.timeOnFlip(base_text_end, 'tStopRefresh')  # time at next scr refresh
            base_text_end.setAutoDraw(False)
    
    # *base_key_resp_end* updates
    waitOnFlip = False
    if base_key_resp_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        base_key_resp_end.frameNStart = frameN  # exact frame index
        base_key_resp_end.tStart = t  # local t and not account for scr refresh
        base_key_resp_end.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(base_key_resp_end, 'tStartRefresh')  # time at next scr refresh
        base_key_resp_end.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(base_key_resp_end.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(base_key_resp_end.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if base_key_resp_end.status == STARTED and not waitOnFlip:
        theseKeys = base_key_resp_end.getKeys(keyList=None, waitRelease=False)
        _base_key_resp_end_allKeys.extend(theseKeys)
        if len(_base_key_resp_end_allKeys):
            base_key_resp_end.keys = _base_key_resp_end_allKeys[-1].name  # just the last key pressed
            base_key_resp_end.rt = _base_key_resp_end_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in base_endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "base_end"-------
for thisComponent in base_endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('base_text_end.started', base_text_end.tStartRefresh)
thisExp.addData('base_text_end.stopped', base_text_end.tStopRefresh)
# check responses
if base_key_resp_end.keys in ['', [], None]:  # No response was made
    base_key_resp_end.keys = None
thisExp.addData('base_key_resp_end.keys',base_key_resp_end.keys)
if base_key_resp_end.keys != None:  # we had a response
    thisExp.addData('base_key_resp_end.rt', base_key_resp_end.rt)
thisExp.addData('base_key_resp_end.started', base_key_resp_end.tStartRefresh)
thisExp.addData('base_key_resp_end.stopped', base_key_resp_end.tStopRefresh)
thisExp.nextEntry()
# the Routine "base_end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
# core.quit()
