#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2020.2.10),
    on Thu 01 Jul 2021 05:44:25 PM CEST
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2020.2.10'
expName = 'test_language'  # from the Builder filename that created this script
expInfo = {'Language': ['English', 'English_easy', 'Deutsch', 'Chinese_simplified', 'Chinese_traditional']}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data' + os.sep + u'psychopy_data_' + data.getDateStr()

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/home/krakowczyk/workspace/wmc-battery/test_language_lastrun.py',
    savePickle=True, saveWideText=False,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1680, 1050], fullscr=True, screen=0, 
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

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "init"
initClock = core.Clock()
import datetime
import os

from common.config import WMCConfig
from common.experiment_messages import ExperimentMessages
from common.instructions import Instructions

# for catching experiment quit key
from psychopy.hardware.keyboard import Keyboard
experiment_keyboard = Keyboard()

thisExp.extraInfo['datetime'] = datetime.datetime.today()

language = thisExp.extraInfo['Language']

config = WMCConfig(language=language)
expmsgs = ExperimentMessages(language=language,
                             encoding=config.experiment_messages.encoding)

experiment_messages = list(expmsgs.items())
n_experiment_messages = len(experiment_messages)
print()
print("==================================================")
print(experiment_messages)
print("number of experiment messages:", n_experiment_messages)
print("==================================================")
print()


instructions = Instructions(language)
instruction_filepaths = (
    instructions.get_instructions('init') + 
    instructions.get_instructions('mu') + 
    instructions.get_instructions('os') + 
    instructions.get_instructions('ss') + 
    instructions.get_instructions('sstm')
)
n_instructions = len(instruction_filepaths)
print()
print("==================================================")
print(instruction_filepaths)
print("number of instructions:", n_instructions)
print("==================================================")

# set text wrap width to 90% of screen width (in height units)
text_wrap_width = win.size[0] / win.size[1] * 0.9

# Initialize components for Routine "experiment_message"
experiment_messageClock = core.Clock()
text_experiment_message_key = visual.TextStim(win=win, name='text_experiment_message_key',
    text='default text',
    font='Arial',
    pos=(0, 0.25), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
text_experiment_message = visual.TextStim(win=win, name='text_experiment_message',
    text='default text',
    font='Arial',
    pos=(0, 0), height=1.0, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
key_resp_experiment_message = keyboard.Keyboard()

# Initialize components for Routine "instruction"
instructionClock = core.Clock()
image_instruction = visual.ImageStim(
    win=win,
    name='image_instruction', units='pix', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=1.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
key_resp_instruction = keyboard.Keyboard()
aperture_dummy = visual.Aperture(
    win=win, name='aperture_dummy',
    units='norm', size=10, pos=(0, 0))
aperture_dummy.disable()  # disable until its actually used

# Initialize components for Routine "ss_sentence_summary"
ss_sentence_summaryClock = core.Clock()
text_ss_sentence_summary = visual.TextStim(win=win, name='text_ss_sentence_summary',
    text='default text',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
key_resp_ss_sentence_summary = keyboard.Keyboard()

# Initialize components for Routine "ss_sentence"
ss_sentenceClock = core.Clock()
text_ss_description = visual.TextStim(win=win, name='text_ss_description',
    text='default text',
    font='Arial',
    pos=(0, 0.25), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
text_ss_sentence = visual.TextStim(win=win, name='text_ss_sentence',
    text='default text',
    font='Arial',
    pos=(0, 0), height=1.0, wrapWidth=text_wrap_width, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
key_resp_ss_sentence = keyboard.Keyboard()

# Initialize components for Routine "end"
endClock = core.Clock()
text = visual.TextStim(win=win, name='text',
    text='Everything tested. Closing in 1 second.',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "init"-------
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
initComponents = []
for thisComponent in initComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
initClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "init"-------
while continueRoutine:
    # get current time
    t = initClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=initClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in initComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "init"-------
for thisComponent in initComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "init" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
experiment_message_loop = data.TrialHandler(nReps=n_experiment_messages, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='experiment_message_loop')
thisExp.addLoop(experiment_message_loop)  # add the loop to the experiment
thisExperiment_message_loop = experiment_message_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisExperiment_message_loop.rgb)
if thisExperiment_message_loop != None:
    for paramName in thisExperiment_message_loop:
        exec('{} = thisExperiment_message_loop[paramName]'.format(paramName))

for thisExperiment_message_loop in experiment_message_loop:
    currentLoop = experiment_message_loop
    # abbreviate parameter names if possible (e.g. rgb = thisExperiment_message_loop.rgb)
    if thisExperiment_message_loop != None:
        for paramName in thisExperiment_message_loop:
            exec('{} = thisExperiment_message_loop[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "experiment_message"-------
    continueRoutine = True
    # update component parameters for each repeat
    current_expmsg_key, current_expmsg_string = experiment_messages.pop(0)
    
    
    text_experiment_message_key.setText(current_expmsg_key)
    text_experiment_message.setText(current_expmsg_string)
    text_experiment_message.setFont(config.experiment_messages.font)
    text_experiment_message.setHeight(config.experiment_messages.size)
    key_resp_experiment_message.keys = []
    key_resp_experiment_message.rt = []
    _key_resp_experiment_message_allKeys = []
    # keep track of which components have finished
    experiment_messageComponents = [text_experiment_message_key, text_experiment_message, key_resp_experiment_message]
    for thisComponent in experiment_messageComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    experiment_messageClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "experiment_message"-------
    while continueRoutine:
        # get current time
        t = experiment_messageClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=experiment_messageClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
            core.quit()
        
        # *text_experiment_message_key* updates
        if text_experiment_message_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_experiment_message_key.frameNStart = frameN  # exact frame index
            text_experiment_message_key.tStart = t  # local t and not account for scr refresh
            text_experiment_message_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_experiment_message_key, 'tStartRefresh')  # time at next scr refresh
            text_experiment_message_key.setAutoDraw(True)
        
        # *text_experiment_message* updates
        if text_experiment_message.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_experiment_message.frameNStart = frameN  # exact frame index
            text_experiment_message.tStart = t  # local t and not account for scr refresh
            text_experiment_message.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_experiment_message, 'tStartRefresh')  # time at next scr refresh
            text_experiment_message.setAutoDraw(True)
        
        # *key_resp_experiment_message* updates
        waitOnFlip = False
        if key_resp_experiment_message.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_experiment_message.frameNStart = frameN  # exact frame index
            key_resp_experiment_message.tStart = t  # local t and not account for scr refresh
            key_resp_experiment_message.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_experiment_message, 'tStartRefresh')  # time at next scr refresh
            key_resp_experiment_message.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_experiment_message.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_experiment_message.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_experiment_message.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_experiment_message.getKeys(keyList=None, waitRelease=False)
            _key_resp_experiment_message_allKeys.extend(theseKeys)
            if len(_key_resp_experiment_message_allKeys):
                key_resp_experiment_message.keys = _key_resp_experiment_message_allKeys[-1].name  # just the last key pressed
                key_resp_experiment_message.rt = _key_resp_experiment_message_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in experiment_messageComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "experiment_message"-------
    for thisComponent in experiment_messageComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    experiment_message_loop.addData('text_experiment_message_key.started', text_experiment_message_key.tStartRefresh)
    experiment_message_loop.addData('text_experiment_message_key.stopped', text_experiment_message_key.tStopRefresh)
    experiment_message_loop.addData('text_experiment_message.started', text_experiment_message.tStartRefresh)
    experiment_message_loop.addData('text_experiment_message.stopped', text_experiment_message.tStopRefresh)
    # check responses
    if key_resp_experiment_message.keys in ['', [], None]:  # No response was made
        key_resp_experiment_message.keys = None
    experiment_message_loop.addData('key_resp_experiment_message.keys',key_resp_experiment_message.keys)
    if key_resp_experiment_message.keys != None:  # we had a response
        experiment_message_loop.addData('key_resp_experiment_message.rt', key_resp_experiment_message.rt)
    experiment_message_loop.addData('key_resp_experiment_message.started', key_resp_experiment_message.tStartRefresh)
    experiment_message_loop.addData('key_resp_experiment_message.stopped', key_resp_experiment_message.tStopRefresh)
    # the Routine "experiment_message" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed n_experiment_messages repeats of 'experiment_message_loop'


# set up handler to look after randomisation of conditions etc
instruction_loop = data.TrialHandler(nReps=n_instructions, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='instruction_loop')
thisExp.addLoop(instruction_loop)  # add the loop to the experiment
thisInstruction_loop = instruction_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisInstruction_loop.rgb)
if thisInstruction_loop != None:
    for paramName in thisInstruction_loop:
        exec('{} = thisInstruction_loop[paramName]'.format(paramName))

for thisInstruction_loop in instruction_loop:
    currentLoop = instruction_loop
    # abbreviate parameter names if possible (e.g. rgb = thisInstruction_loop.rgb)
    if thisInstruction_loop != None:
        for paramName in thisInstruction_loop:
            exec('{} = thisInstruction_loop[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "instruction"-------
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
    
    aperture_instruction = visual.Aperture(win, size=1, shape=aperture_vertices, units='height')
    
    image_instruction.setSize(instr_img_size)
    image_instruction.setImage(instruction_filepath)
    key_resp_instruction.keys = []
    key_resp_instruction.rt = []
    _key_resp_instruction_allKeys = []
    # keep track of which components have finished
    instructionComponents = [image_instruction, key_resp_instruction, aperture_dummy]
    for thisComponent in instructionComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    instructionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "instruction"-------
    while continueRoutine:
        # get current time
        t = instructionClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=instructionClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if experiment_keyboard.getKeys(keyList=[config.common.abort_key], clear=False):
            core.quit()
        
        # *image_instruction* updates
        if image_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            image_instruction.frameNStart = frameN  # exact frame index
            image_instruction.tStart = t  # local t and not account for scr refresh
            image_instruction.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(image_instruction, 'tStartRefresh')  # time at next scr refresh
            image_instruction.setAutoDraw(True)
        
        # *key_resp_instruction* updates
        waitOnFlip = False
        if key_resp_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_instruction.frameNStart = frameN  # exact frame index
            key_resp_instruction.tStart = t  # local t and not account for scr refresh
            key_resp_instruction.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_instruction, 'tStartRefresh')  # time at next scr refresh
            key_resp_instruction.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_instruction.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_instruction.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_instruction.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_instruction.getKeys(keyList=None, waitRelease=False)
            _key_resp_instruction_allKeys.extend(theseKeys)
            if len(_key_resp_instruction_allKeys):
                key_resp_instruction.keys = _key_resp_instruction_allKeys[-1].name  # just the last key pressed
                key_resp_instruction.rt = _key_resp_instruction_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # *aperture_dummy* updates
        if aperture_dummy.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            aperture_dummy.frameNStart = frameN  # exact frame index
            aperture_dummy.tStart = t  # local t and not account for scr refresh
            aperture_dummy.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(aperture_dummy, 'tStartRefresh')  # time at next scr refresh
            aperture_dummy.enabled = True
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructionComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "instruction"-------
    for thisComponent in instructionComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    del aperture_instruction
    instruction_loop.addData('image_instruction.started', image_instruction.tStartRefresh)
    instruction_loop.addData('image_instruction.stopped', image_instruction.tStopRefresh)
    # check responses
    if key_resp_instruction.keys in ['', [], None]:  # No response was made
        key_resp_instruction.keys = None
    instruction_loop.addData('key_resp_instruction.keys',key_resp_instruction.keys)
    if key_resp_instruction.keys != None:  # we had a response
        instruction_loop.addData('key_resp_instruction.rt', key_resp_instruction.rt)
    instruction_loop.addData('key_resp_instruction.started', key_resp_instruction.tStartRefresh)
    instruction_loop.addData('key_resp_instruction.stopped', key_resp_instruction.tStopRefresh)
    aperture_dummy.enabled = False  # just in case it was left enabled
    instruction_loop.addData('aperture_dummy.started', aperture_dummy.tStartRefresh)
    instruction_loop.addData('aperture_dummy.stopped', aperture_dummy.tStopRefresh)
    # the Routine "instruction" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed n_instructions repeats of 'instruction_loop'


# ------Prepare to start Routine "ss_sentence_summary"-------
continueRoutine = True
# update component parameters for each repeat
from tasks.sentence_span import SentenceSpanTask
ss_task = SentenceSpanTask(language=language, seed=0, config=config.sentence_span)

ss_sentences = (
    ss_task.sentences['practice'][True] +
    ss_task.sentences['practice'][False] + 
    ss_task.sentences['trials'][True] + 
    ss_task.sentences['trials'][False]
)
ss_descriptions = (
    [('practice', True) for _ in ss_task.sentences['practice'][True]] + 
    [('practice', False) for _ in ss_task.sentences['practice'][False]] + 
    [('trials', True) for _ in ss_task.sentences['trials'][True]] + 
    [('trials', False) for _ in ss_task.sentences['trials'][False]]
)

n_ss_sentences = len(ss_sentences)
n_ss_practice = (len(ss_task.sentences['practice'][True]) +
                 len(ss_task.sentences['practice'][False]))
n_ss_practice_t = len(ss_task.sentences['practice'][True])
n_ss_practice_f = len(ss_task.sentences['practice'][False])
n_ss_trials = (len(ss_task.sentences['trials'][True]) +
               len(ss_task.sentences['trials'][False]))
n_ss_trials_t = len(ss_task.sentences['trials'][True])
n_ss_trials_f = len(ss_task.sentences['trials'][False])


ss_summary = (
    f'sentence span summary: \n\n'
    f'total number of sentences: {n_ss_sentences}\n\n'
    f'total number of practice sentences: {n_ss_practice}\n'
    f'true: {n_ss_practice_t}, false: {n_ss_practice_f}\n\n'
    f'total number of trial sentences: {n_ss_trials}\n'
    f'true: {n_ss_trials_t}, false: {n_ss_trials_f}\n\n'
)

print()
print("==================================================")
print(ss_sentences)
print("number of ss sentences:", n_ss_sentences)
print("==================================================")
print()


text_ss_sentence_summary.setText(ss_summary)
key_resp_ss_sentence_summary.keys = []
key_resp_ss_sentence_summary.rt = []
_key_resp_ss_sentence_summary_allKeys = []
# keep track of which components have finished
ss_sentence_summaryComponents = [text_ss_sentence_summary, key_resp_ss_sentence_summary]
for thisComponent in ss_sentence_summaryComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
ss_sentence_summaryClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "ss_sentence_summary"-------
while continueRoutine:
    # get current time
    t = ss_sentence_summaryClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=ss_sentence_summaryClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_ss_sentence_summary* updates
    if text_ss_sentence_summary.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_ss_sentence_summary.frameNStart = frameN  # exact frame index
        text_ss_sentence_summary.tStart = t  # local t and not account for scr refresh
        text_ss_sentence_summary.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_ss_sentence_summary, 'tStartRefresh')  # time at next scr refresh
        text_ss_sentence_summary.setAutoDraw(True)
    
    # *key_resp_ss_sentence_summary* updates
    waitOnFlip = False
    if key_resp_ss_sentence_summary.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        key_resp_ss_sentence_summary.frameNStart = frameN  # exact frame index
        key_resp_ss_sentence_summary.tStart = t  # local t and not account for scr refresh
        key_resp_ss_sentence_summary.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_ss_sentence_summary, 'tStartRefresh')  # time at next scr refresh
        key_resp_ss_sentence_summary.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_ss_sentence_summary.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_ss_sentence_summary.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_ss_sentence_summary.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_ss_sentence_summary.getKeys(keyList=None, waitRelease=False)
        _key_resp_ss_sentence_summary_allKeys.extend(theseKeys)
        if len(_key_resp_ss_sentence_summary_allKeys):
            key_resp_ss_sentence_summary.keys = _key_resp_ss_sentence_summary_allKeys[-1].name  # just the last key pressed
            key_resp_ss_sentence_summary.rt = _key_resp_ss_sentence_summary_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in ss_sentence_summaryComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "ss_sentence_summary"-------
for thisComponent in ss_sentence_summaryComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('text_ss_sentence_summary.started', text_ss_sentence_summary.tStartRefresh)
thisExp.addData('text_ss_sentence_summary.stopped', text_ss_sentence_summary.tStopRefresh)
# check responses
if key_resp_ss_sentence_summary.keys in ['', [], None]:  # No response was made
    key_resp_ss_sentence_summary.keys = None
thisExp.addData('key_resp_ss_sentence_summary.keys',key_resp_ss_sentence_summary.keys)
if key_resp_ss_sentence_summary.keys != None:  # we had a response
    thisExp.addData('key_resp_ss_sentence_summary.rt', key_resp_ss_sentence_summary.rt)
thisExp.addData('key_resp_ss_sentence_summary.started', key_resp_ss_sentence_summary.tStartRefresh)
thisExp.addData('key_resp_ss_sentence_summary.stopped', key_resp_ss_sentence_summary.tStopRefresh)
thisExp.nextEntry()
# the Routine "ss_sentence_summary" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
ss_sentence_loop = data.TrialHandler(nReps=n_ss_sentences, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='ss_sentence_loop')
thisExp.addLoop(ss_sentence_loop)  # add the loop to the experiment
thisSs_sentence_loop = ss_sentence_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisSs_sentence_loop.rgb)
if thisSs_sentence_loop != None:
    for paramName in thisSs_sentence_loop:
        exec('{} = thisSs_sentence_loop[paramName]'.format(paramName))

for thisSs_sentence_loop in ss_sentence_loop:
    currentLoop = ss_sentence_loop
    # abbreviate parameter names if possible (e.g. rgb = thisSs_sentence_loop.rgb)
    if thisSs_sentence_loop != None:
        for paramName in thisSs_sentence_loop:
            exec('{} = thisSs_sentence_loop[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "ss_sentence"-------
    continueRoutine = True
    # update component parameters for each repeat
    current_ss_sentence = ss_sentences.pop(0)
    current_ss_description = ss_descriptions.pop(0)
    current_ss_description = (f'{current_ss_description[0]}, '
                              f'{current_ss_description[1]}')
    text_ss_description.setText(current_ss_description)
    text_ss_sentence.setText(current_ss_sentence)
    text_ss_sentence.setFont(config.sentence_span.text.sentences.font)
    text_ss_sentence.setHeight(config.sentence_span.text.sentences.size)
    key_resp_ss_sentence.keys = []
    key_resp_ss_sentence.rt = []
    _key_resp_ss_sentence_allKeys = []
    # keep track of which components have finished
    ss_sentenceComponents = [text_ss_description, text_ss_sentence, key_resp_ss_sentence]
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
        
        # *text_ss_description* updates
        if text_ss_description.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_ss_description.frameNStart = frameN  # exact frame index
            text_ss_description.tStart = t  # local t and not account for scr refresh
            text_ss_description.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_ss_description, 'tStartRefresh')  # time at next scr refresh
            text_ss_description.setAutoDraw(True)
        
        # *text_ss_sentence* updates
        if text_ss_sentence.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_ss_sentence.frameNStart = frameN  # exact frame index
            text_ss_sentence.tStart = t  # local t and not account for scr refresh
            text_ss_sentence.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_ss_sentence, 'tStartRefresh')  # time at next scr refresh
            text_ss_sentence.setAutoDraw(True)
        
        # *key_resp_ss_sentence* updates
        waitOnFlip = False
        if key_resp_ss_sentence.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_ss_sentence.frameNStart = frameN  # exact frame index
            key_resp_ss_sentence.tStart = t  # local t and not account for scr refresh
            key_resp_ss_sentence.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_ss_sentence, 'tStartRefresh')  # time at next scr refresh
            key_resp_ss_sentence.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_ss_sentence.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_ss_sentence.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_ss_sentence.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_ss_sentence.getKeys(keyList=None, waitRelease=False)
            _key_resp_ss_sentence_allKeys.extend(theseKeys)
            if len(_key_resp_ss_sentence_allKeys):
                key_resp_ss_sentence.keys = _key_resp_ss_sentence_allKeys[-1].name  # just the last key pressed
                key_resp_ss_sentence.rt = _key_resp_ss_sentence_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
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
    ss_sentence_loop.addData('text_ss_description.started', text_ss_description.tStartRefresh)
    ss_sentence_loop.addData('text_ss_description.stopped', text_ss_description.tStopRefresh)
    ss_sentence_loop.addData('text_ss_sentence.started', text_ss_sentence.tStartRefresh)
    ss_sentence_loop.addData('text_ss_sentence.stopped', text_ss_sentence.tStopRefresh)
    # check responses
    if key_resp_ss_sentence.keys in ['', [], None]:  # No response was made
        key_resp_ss_sentence.keys = None
    ss_sentence_loop.addData('key_resp_ss_sentence.keys',key_resp_ss_sentence.keys)
    if key_resp_ss_sentence.keys != None:  # we had a response
        ss_sentence_loop.addData('key_resp_ss_sentence.rt', key_resp_ss_sentence.rt)
    ss_sentence_loop.addData('key_resp_ss_sentence.started', key_resp_ss_sentence.tStartRefresh)
    ss_sentence_loop.addData('key_resp_ss_sentence.stopped', key_resp_ss_sentence.tStopRefresh)
    # the Routine "ss_sentence" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed n_ss_sentences repeats of 'ss_sentence_loop'


# ------Prepare to start Routine "end"-------
continueRoutine = True
routineTimer.add(1.000000)
# update component parameters for each repeat
# keep track of which components have finished
endComponents = [text]
for thisComponent in endComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "end"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = endClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=endClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text* updates
    if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text.frameNStart = frameN  # exact frame index
        text.tStart = t  # local t and not account for scr refresh
        text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
        text.setAutoDraw(True)
    if text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text.tStartRefresh + 1.0-frameTolerance:
            # keep track of stop time/frame for later
            text.tStop = t  # not accounting for scr refresh
            text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(text, 'tStopRefresh')  # time at next scr refresh
            text.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('text.started', text.tStartRefresh)
thisExp.addData('text.stopped', text.tStopRefresh)

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsPickle(filename)
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
