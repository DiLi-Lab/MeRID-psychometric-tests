#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.2.3),
    on Sun Jan 16 16:49:37 2022
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

import pandas as pd
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import os  # handy system and path functions

from psychopy.hardware import keyboard
import yaml
from datetime import datetime

# # Ensure that relative paths start from the same directory as this script
# _thisDir = os.path.dirname(os.path.abspath(__file__))

date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Path to the YAML file contains the language and experiment configurations
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
font = config_data['font']

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

# Create folder name for the results
results_folder = f"{participant_id}_{language}_{country_code}_{lab_number}_PT{expInfo['session_id']}"

# Create folder for audio and csv data
output_path = f'data/psychometric_test_{language}_{country_code}_{lab_number}/Stroop_Flanker/{results_folder}/'
os.makedirs(output_path, exist_ok=True)
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = f"{output_path}" \
           f"{language}{country_code}{lab_number}" \
           f"_{participant_id}_PT{expInfo['session_id']}_{date}"

# Load the instruction CSV file
instructions_df = pd.read_excel(f'languages/{language}/instructions/Stroop_Flanker_instructions_{language.lower()}.xlsx', index_col='screen')
welcome_text = instructions_df.loc['Welcome_text', language]
welcome_text = welcome_text.replace('\\n', '\n')
stroop_instructions = instructions_df.loc['stroop_instructions', language]
stroop_instructions = stroop_instructions.replace('\\n', '\n')
flanker_instructions = instructions_df.loc['flanker_instructions', language]
flanker_instructions = flanker_instructions.replace('\\n', '\n')
done_text = instructions_df.loc['done_text', language]
done_text = done_text.replace('\\n', '\n')
start_warning_text = instructions_df.loc['start_warning_text', language]
start_warning_text = start_warning_text.replace('\\n', '\n')
Goodbyetext = instructions_df.loc['Goodbyetext', language]
Goodbyetext = Goodbyetext.replace('\\n', '\n')


# Function to get the correct_key for a given color
def get_correct_key_for_color(df, color):
    color_rows = df[df['color'] == color]
    if color_rows['correct_key'].nunique() == 1:
        return color_rows['correct_key'].iloc[0]
    else:
        raise ValueError(f"Not all 'correct_key' values are the same for color '{color}'.")

stroop_stimulus = pd.read_excel(f'languages/{language}/Stroop-Flanker/Stroop_practice_trials_{language.lower()}.xlsx')
stroop_blue_key = get_correct_key_for_color(stroop_stimulus, 'blue')
stroop_yellow_key = get_correct_key_for_color(stroop_stimulus, 'yellow')
stroop_red_key = get_correct_key_for_color(stroop_stimulus, 'red')

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name='Stroop_Flanker', version='',
    extraInfo=expInfo, runtimeInfo=None,
    # originPath='/Users/cui/Documents/uzh/PhD/Projects/MeRID/Psychometric_Tests/stroop-simon-german/CognControl_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1440, 900], fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
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

# Initialize components for Routine "WelcomeScreen"
WelcomeScreenClock = core.Clock()
Welcome_text = visual.TextStim(win=win, name='Welcome_text',
    text=welcome_text,
    font=font,
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=0.0);
Welcome_resp = keyboard.Keyboard()

# Initialize components for Routine "StroopInstructions"
StroopInstructionsClock = core.Clock()
stroop_instructions = visual.TextStim(win=win, name='stroop_instructions',
    text=stroop_instructions,
    font=font,
    pos=(0, 0), height=0.035, wrapWidth=1.5, ori=0.0,
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0,);
stroop_instruction_key = keyboard.Keyboard()

# Initialize components for Routine "Blank500"
Blank500Clock = core.Clock()
blank = visual.TextStim(win=win, name='blank',
    text='\n\n',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "FixationCross"
FixationCrossClock = core.Clock()
fix_cross = visual.TextStim(win=win, name='fix_cross',
    text='+',
    font='Courier New',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "StroopPractice"
StroopPracticeClock = core.Clock()
stroop_practice_word = visual.TextStim(win=win, name='stroop_practice_word',
    text='',
    font=font,
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
stroop_practice_key = keyboard.Keyboard()

# Initialize components for Routine "stroop_practice_feedback"
stroop_practice_feedbackClock = core.Clock()
stroop_feedback_text = visual.TextStim(win=win, name='stroop_feedback_text',
    text='',
    font='Arial Unicode MS',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "StartWarning"
StartWarningClock = core.Clock()
start_warning_text = visual.TextStim(win=win, name='start_warning_text',
    text=start_warning_text,
    font=font,
    pos=(0, 0), height=0.035, wrapWidth=1.5, ori=0.0,
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "StroopTrials"
StroopTrialsClock = core.Clock()
stroop_word = visual.TextStim(win=win, name='stroop_word',
    text='',
    font=font,
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
stroop_key = keyboard.Keyboard()

# Initialize components for Routine "Done"
DoneClock = core.Clock()
done_text = visual.TextStim(win=win, name='done_text',
    text=done_text,
    font=font,
    pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
done_key = keyboard.Keyboard()

# Initialize components for Routine "FlankerInstruction"
FlankerInstructionClock = core.Clock()
Flanker_instructions = visual.TextStim(win=win, name='Flanker_instructions',
    text=flanker_instructions,
    font=font,
    pos=(0, 0), height=0.035, wrapWidth=1.5, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
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
    languageStyle='LTR',
    depth=0.0);
Flanker_practice_key = keyboard.Keyboard()

# Initialize components for Routine "flanker_practice_feedback"
Flanker_practice_feedbackClock = core.Clock()
Flanker_feedback_text = visual.TextStim(win=win, name='flanker_feedback_text',
    text='',
    font='Arial Unicode MS',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
    color='white', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "FlankerTrials"
FlankerTrialsClock = core.Clock()
Flanker_arrows = visual.TextStim(win=win, name='Flanker_arrows',
    text='',
    font='Courier New',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
    color='white', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=0.0);
Flanker_key = keyboard.Keyboard()

# Initialize components for Routine "GoodbyeScreen"
GoodbyeScreenClock = core.Clock()
Goodbyetext = visual.TextStim(win=win, name='Goodbyetext',
    text=Goodbyetext,
    font=font,
    pos=(0, 0), height=0.05, wrapWidth=1.5, ori=0.0,
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_goodbye = keyboard.Keyboard()

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
    if Welcome_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Welcome_text.frameNStart = frameN  # exact frame index
        Welcome_text.tStart = t  # local t and not account for scr refresh
        Welcome_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Welcome_text, 'tStartRefresh')  # time at next scr refresh
        Welcome_text.setAutoDraw(True)
    
    # *Welcome_resp* updates
    waitOnFlip = False
    if Welcome_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
    if Welcome_resp.status == STARTED and not waitOnFlip:
        theseKeys = Welcome_resp.getKeys(keyList=['space'], waitRelease=False)
        _Welcome_resp_allKeys.extend(theseKeys)
        if len(_Welcome_resp_allKeys):
            Welcome_resp.keys = _Welcome_resp_allKeys[-1].name  # just the last key pressed
            Welcome_resp.rt = _Welcome_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
thisExp.addData('Welcome_resp.keys',Welcome_resp.keys)
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
    if stroop_instructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        stroop_instructions.frameNStart = frameN  # exact frame index
        stroop_instructions.tStart = t  # local t and not account for scr refresh
        stroop_instructions.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(stroop_instructions, 'tStartRefresh')  # time at next scr refresh
        stroop_instructions.setAutoDraw(True)
    
    # *stroop_instruction_key* updates
    waitOnFlip = False
    if stroop_instruction_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
    if stroop_instruction_key.status == STARTED and not waitOnFlip:
        theseKeys = stroop_instruction_key.getKeys(keyList=['space'], waitRelease=False)
        _stroop_instruction_key_allKeys.extend(theseKeys)
        if len(_stroop_instruction_key_allKeys):
            stroop_instruction_key.keys = _stroop_instruction_key_allKeys[-1].name  # just the last key pressed
            stroop_instruction_key.rt = _stroop_instruction_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
thisExp.addData('stroop_instruction_key.keys',stroop_instruction_key.keys)
if stroop_instruction_key.keys != None:  # we had a response
    thisExp.addData('stroop_instruction_key.rt', stroop_instruction_key.rt)
thisExp.addData('stroop_instruction_key.started', stroop_instruction_key.tStartRefresh)
thisExp.addData('stroop_instruction_key.stopped', stroop_instruction_key.tStopRefresh)
thisExp.nextEntry()
# the Routine "StroopInstructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Blank500"-------
continueRoutine = True
routineTimer.add(0.500000)
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
    if blank.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        blank.frameNStart = frameN  # exact frame index
        blank.tStart = t  # local t and not account for scr refresh
        blank.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(blank, 'tStartRefresh')  # time at next scr refresh
        blank.setAutoDraw(True)
    if blank.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > blank.tStartRefresh + .5-frameTolerance:
            # keep track of stop time/frame for later
            blank.tStop = t  # not accounting for scr refresh
            blank.frameNStop = frameN  # exact frame index
            win.timeOnFlip(blank, 'tStopRefresh')  # time at next scr refresh
            blank.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
  trialList=data.importConditions(f'languages/{language}/Stroop-Flanker/Stroop_practice_trials_{language.lower()}.xlsx'),
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
    routineTimer.add(0.350000)
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
        if fix_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix_cross.frameNStart = frameN  # exact frame index
            fix_cross.tStart = t  # local t and not account for scr refresh
            fix_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_cross, 'tStartRefresh')  # time at next scr refresh
            fix_cross.setAutoDraw(True)
        if fix_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix_cross.tStartRefresh + .35-frameTolerance:
                # keep track of stop time/frame for later
                fix_cross.tStop = t  # not accounting for scr refresh
                fix_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fix_cross, 'tStopRefresh')  # time at next scr refresh
                fix_cross.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
    stroop_practice_word.setText(word)
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
        if stroop_practice_word.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stroop_practice_word.frameNStart = frameN  # exact frame index
            stroop_practice_word.tStart = t  # local t and not account for scr refresh
            stroop_practice_word.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stroop_practice_word, 'tStartRefresh')  # time at next scr refresh
            stroop_practice_word.setAutoDraw(True)
        
        # *stroop_practice_key* updates
        waitOnFlip = False
        if stroop_practice_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
        if stroop_practice_key.status == STARTED and not waitOnFlip:
            theseKeys = stroop_practice_key.getKeys(keyList=[stroop_blue_key, stroop_red_key, stroop_yellow_key], waitRelease=False)
            _stroop_practice_key_allKeys.extend(theseKeys)
            if len(_stroop_practice_key_allKeys):
                stroop_practice_key.keys = _stroop_practice_key_allKeys[-1].name  # just the last key pressed
                stroop_practice_key.rt = _stroop_practice_key_allKeys[-1].rt
                # was this correct?
                if (stroop_practice_key.keys == str(correct_key)) or (stroop_practice_key.keys == correct_key):
                    stroop_practice_key.corr = 1
                else:
                    stroop_practice_key.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
    stroop_practice_trial.addData('stroop_practice_key.keys',stroop_practice_key.keys)
    stroop_practice_trial.addData('stroop_practice_key.corr', stroop_practice_key.corr)
    if stroop_practice_key.keys != None:  # we had a response
        stroop_practice_trial.addData('stroop_practice_key.rt', stroop_practice_key.rt)
    stroop_practice_trial.addData('stroop_practice_key.started', stroop_practice_key.tStartRefresh)
    stroop_practice_trial.addData('stroop_practice_key.stopped', stroop_practice_key.tStopRefresh)
    # the Routine "StroopPractice" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "stroop_practice_feedback"-------
    continueRoutine = True
    routineTimer.add(1.000000)
    # update component parameters for each repeat
    if(stroop_practice_key.corr == 1):
        feedback_text = "✓"
    elif(stroop_practice_key.corr == 0):
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
        if stroop_feedback_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stroop_feedback_text.frameNStart = frameN  # exact frame index
            stroop_feedback_text.tStart = t  # local t and not account for scr refresh
            stroop_feedback_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stroop_feedback_text, 'tStartRefresh')  # time at next scr refresh
            stroop_feedback_text.setAutoDraw(True)
        if stroop_feedback_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > stroop_feedback_text.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                stroop_feedback_text.tStop = t  # not accounting for scr refresh
                stroop_feedback_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(stroop_feedback_text, 'tStopRefresh')  # time at next scr refresh
                stroop_feedback_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
routineTimer.add(6.000000)
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
    if start_warning_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_warning_text.frameNStart = frameN  # exact frame index
        start_warning_text.tStart = t  # local t and not account for scr refresh
        start_warning_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_warning_text, 'tStartRefresh')  # time at next scr refresh
        start_warning_text.setAutoDraw(True)
    if start_warning_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > start_warning_text.tStartRefresh + 6.0-frameTolerance:
            # keep track of stop time/frame for later
            start_warning_text.tStop = t  # not accounting for scr refresh
            start_warning_text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(start_warning_text, 'tStopRefresh')  # time at next scr refresh
            start_warning_text.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
    trialList=data.importConditions(f'languages/{language}/Stroop-Flanker/StroopStim_{language.lower()}.xlsx'),
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
    routineTimer.add(0.350000)
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
        if fix_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix_cross.frameNStart = frameN  # exact frame index
            fix_cross.tStart = t  # local t and not account for scr refresh
            fix_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_cross, 'tStartRefresh')  # time at next scr refresh
            fix_cross.setAutoDraw(True)
        if fix_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix_cross.tStartRefresh + .35-frameTolerance:
                # keep track of stop time/frame for later
                fix_cross.tStop = t  # not accounting for scr refresh
                fix_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fix_cross, 'tStopRefresh')  # time at next scr refresh
                fix_cross.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
    stroop_word.setText(word)
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
        if stroop_word.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            stroop_word.frameNStart = frameN  # exact frame index
            stroop_word.tStart = t  # local t and not account for scr refresh
            stroop_word.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stroop_word, 'tStartRefresh')  # time at next scr refresh
            stroop_word.setAutoDraw(True)
        
        # *stroop_key* updates
        waitOnFlip = False
        if stroop_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
        if stroop_key.status == STARTED and not waitOnFlip:
            theseKeys = stroop_key.getKeys(keyList=[stroop_red_key, stroop_blue_key, stroop_yellow_key], waitRelease=False)
            _stroop_key_allKeys.extend(theseKeys)
            if len(_stroop_key_allKeys):
                stroop_key.keys = _stroop_key_allKeys[-1].name  # just the last key pressed
                stroop_key.rt = _stroop_key_allKeys[-1].rt
                # was this correct?
                if (stroop_key.keys == str(correct_key)) or (stroop_key.keys == correct_key):
                    stroop_key.corr = 1
                else:
                    stroop_key.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
    Stroop_trials.addData('stroop_key.keys',stroop_key.keys)
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
    if done_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        done_text.frameNStart = frameN  # exact frame index
        done_text.tStart = t  # local t and not account for scr refresh
        done_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(done_text, 'tStartRefresh')  # time at next scr refresh
        done_text.setAutoDraw(True)

    # *done_key* updates
    waitOnFlip = False
    if done_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
    if done_key.status == STARTED and not waitOnFlip:
        theseKeys = done_key.getKeys(keyList=['space'], waitRelease=False)
        _done_key_allKeys.extend(theseKeys)
        if len(_done_key_allKeys):
            done_key.keys = _done_key_allKeys[-1].name  # just the last key pressed
            done_key.rt = _done_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
thisExp.addData('done_key.keys',done_key.keys)
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
    if Flanker_instructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Flanker_instructions.frameNStart = frameN  # exact frame index
        Flanker_instructions.tStart = t  # local t and not account for scr refresh
        Flanker_instructions.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Flanker_instructions, 'tStartRefresh')  # time at next scr refresh
        Flanker_instructions.setAutoDraw(True)

    # *Flanker_instruction_key* updates
    waitOnFlip = False
    if Flanker_instruction_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
    if Flanker_instruction_key.status == STARTED and not waitOnFlip:
        theseKeys = Flanker_instruction_key.getKeys(keyList=['space'], waitRelease=False)
        _Flanker_instruction_key_allKeys.extend(theseKeys)
        if len(_Flanker_instruction_key_allKeys):
            Flanker_instruction_key.keys = _Flanker_instruction_key_allKeys[-1].name  # just the last key pressed
            Flanker_instruction_key.rt = _Flanker_instruction_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
thisExp.addData('Flanker_instruction_key.keys',Flanker_instruction_key.keys)
if Flanker_instruction_key.keys != None:  # we had a response
    thisExp.addData('Flanker_instruction_key.rt', Flanker_instruction_key.rt)
thisExp.addData('Flanker_instruction_key.started', Flanker_instruction_key.tStartRefresh)
thisExp.addData('Flanker_instruction_key.stopped', Flanker_instruction_key.tStopRefresh)
thisExp.nextEntry()
# the Routine "FlankerInstruction" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Blank500"-------
continueRoutine = True
routineTimer.add(0.500000)
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
    if blank.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        blank.frameNStart = frameN  # exact frame index
        blank.tStart = t  # local t and not account for scr refresh
        blank.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(blank, 'tStartRefresh')  # time at next scr refresh
        blank.setAutoDraw(True)
    if blank.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > blank.tStartRefresh + .5-frameTolerance:
            # keep track of stop time/frame for later
            blank.tStop = t  # not accounting for scr refresh
            blank.frameNStop = frameN  # exact frame index
            win.timeOnFlip(blank, 'tStopRefresh')  # time at next scr refresh
            blank.setAutoDraw(False)

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
    trialList=data.importConditions(f'languages/{language}/Stroop-Flanker/FlankerStim_{language.lower()}.xlsx'),
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
    routineTimer.add(0.350000)
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
        if fix_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix_cross.frameNStart = frameN  # exact frame index
            fix_cross.tStart = t  # local t and not account for scr refresh
            fix_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_cross, 'tStartRefresh')  # time at next scr refresh
            fix_cross.setAutoDraw(True)
        if fix_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix_cross.tStartRefresh + .35-frameTolerance:
                # keep track of stop time/frame for later
                fix_cross.tStop = t  # not accounting for scr refresh
                fix_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fix_cross, 'tStopRefresh')  # time at next scr refresh
                fix_cross.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
        if Flanker_practice_arrows.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Flanker_practice_arrows.frameNStart = frameN  # exact frame index
            Flanker_practice_arrows.tStart = t  # local t and not account for scr refresh
            Flanker_practice_arrows.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Flanker_practice_arrows, 'tStartRefresh')  # time at next scr refresh
            Flanker_practice_arrows.setAutoDraw(True)

        # *Flanker_practice_key* updates
        waitOnFlip = False
        if Flanker_practice_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
        if Flanker_practice_key.status == STARTED and not waitOnFlip:
            theseKeys = Flanker_practice_key.getKeys(keyList=['left', 'right'], waitRelease=False)
            _Flanker_practice_key_allKeys.extend(theseKeys)
            if len(_Flanker_practice_key_allKeys):
                Flanker_practice_key.keys = _Flanker_practice_key_allKeys[-1].name  # just the last key pressed
                Flanker_practice_key.rt = _Flanker_practice_key_allKeys[-1].rt
                # was this correct?
                if (Flanker_practice_key.keys == str(correct_key)) or (Flanker_practice_key.keys == correct_key):
                    Flanker_practice_key.corr = 1
                else:
                    Flanker_practice_key.corr = 0
                # a response ends the routine
                continueRoutine = False

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
    Flanker_practice_trials.addData('Flanker_practice_key.keys',Flanker_practice_key.keys)
    Flanker_practice_trials.addData('Flanker_practice_key.corr', Flanker_practice_key.corr)
    if Flanker_practice_key.keys != None:  # we had a response
        Flanker_practice_trials.addData('Flanker_practice_key.rt', Flanker_practice_key.rt)
    Flanker_practice_trials.addData('Flanker_practice_key.started', Flanker_practice_key.tStartRefresh)
    Flanker_practice_trials.addData('Flanker_practice_key.stopped', Flanker_practice_key.tStopRefresh)
    # the Routine "FlankerPractice" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ------Prepare to start Routine "Flanker_practice_feedback"-------
    continueRoutine = True
    routineTimer.add(1.000000)
    # update component parameters for each repeat
    if(Flanker_practice_key.corr == 1):
        feedback_text2 = "✓"
    elif(Flanker_practice_key.corr == 0):
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
        if Flanker_feedback_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Flanker_feedback_text.frameNStart = frameN  # exact frame index
            Flanker_feedback_text.tStart = t  # local t and not account for scr refresh
            Flanker_feedback_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Flanker_feedback_text, 'tStartRefresh')  # time at next scr refresh
            Flanker_feedback_text.setAutoDraw(True)
        if Flanker_feedback_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Flanker_feedback_text.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                Flanker_feedback_text.tStop = t  # not accounting for scr refresh
                Flanker_feedback_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(Flanker_feedback_text, 'tStopRefresh')  # time at next scr refresh
                Flanker_feedback_text.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
routineTimer.add(6.000000)
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
    if start_warning_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_warning_text.frameNStart = frameN  # exact frame index
        start_warning_text.tStart = t  # local t and not account for scr refresh
        start_warning_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_warning_text, 'tStartRefresh')  # time at next scr refresh
        start_warning_text.setAutoDraw(True)
    if start_warning_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > start_warning_text.tStartRefresh + 6.0-frameTolerance:
            # keep track of stop time/frame for later
            start_warning_text.tStop = t  # not accounting for scr refresh
            start_warning_text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(start_warning_text, 'tStopRefresh')  # time at next scr refresh
            start_warning_text.setAutoDraw(False)

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
    trialList=data.importConditions(f'languages/{language}/Stroop-Flanker/FlankerStim_{language.lower()}.xlsx'),
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
    routineTimer.add(0.350000)
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
        if fix_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix_cross.frameNStart = frameN  # exact frame index
            fix_cross.tStart = t  # local t and not account for scr refresh
            fix_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_cross, 'tStartRefresh')  # time at next scr refresh
            fix_cross.setAutoDraw(True)
        if fix_cross.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix_cross.tStartRefresh + .35-frameTolerance:
                # keep track of stop time/frame for later
                fix_cross.tStop = t  # not accounting for scr refresh
                fix_cross.frameNStop = frameN  # exact frame index
                win.timeOnFlip(fix_cross, 'tStopRefresh')  # time at next scr refresh
                fix_cross.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
        if Flanker_arrows.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Flanker_arrows.frameNStart = frameN  # exact frame index
            Flanker_arrows.tStart = t  # local t and not account for scr refresh
            Flanker_arrows.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Flanker_arrows, 'tStartRefresh')  # time at next scr refresh
            Flanker_arrows.setAutoDraw(True)

        # *Flanker_key* updates
        waitOnFlip = False
        if Flanker_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
        if Flanker_key.status == STARTED and not waitOnFlip:
            theseKeys = Flanker_key.getKeys(keyList=['left', 'right'], waitRelease=False)
            _Flanker_key_allKeys.extend(theseKeys)
            if len(_Flanker_key_allKeys):
                Flanker_key.keys = _Flanker_key_allKeys[-1].name  # just the last key pressed
                Flanker_key.rt = _Flanker_key_allKeys[-1].rt
                # was this correct?
                if (Flanker_key.keys == str(correct_key)) or (Flanker_key.keys == correct_key):
                    Flanker_key.corr = 1
                else:
                    Flanker_key.corr = 0
                # a response ends the routine
                continueRoutine = False

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
    Flanker_trials.addData('Flanker_key.keys',Flanker_key.keys)
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
routineTimer.add(10.000000)
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
    if Goodbyetext.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Goodbyetext.frameNStart = frameN  # exact frame index
        Goodbyetext.tStart = t  # local t and not account for scr refresh
        Goodbyetext.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Goodbyetext, 'tStartRefresh')  # time at next scr refresh
        Goodbyetext.setAutoDraw(True)
    if Goodbyetext.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > Goodbyetext.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            Goodbyetext.tStop = t  # not accounting for scr refresh
            Goodbyetext.frameNStop = frameN  # exact frame index
            win.timeOnFlip(Goodbyetext, 'tStopRefresh')  # time at next scr refresh
            Goodbyetext.setAutoDraw(False)
    
    # *key_goodbye* updates
    waitOnFlip = False
    if key_goodbye.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
    if key_goodbye.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > key_goodbye.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            key_goodbye.tStop = t  # not accounting for scr refresh
            key_goodbye.frameNStop = frameN  # exact frame index
            win.timeOnFlip(key_goodbye, 'tStopRefresh')  # time at next scr refresh
            key_goodbye.status = FINISHED
    if key_goodbye.status == STARTED and not waitOnFlip:
        theseKeys = key_goodbye.getKeys(keyList=['space'], waitRelease=False)
        _key_goodbye_allKeys.extend(theseKeys)
        if len(_key_goodbye_allKeys):
            key_goodbye.keys = _key_goodbye_allKeys[-1].name  # just the last key pressed
            key_goodbye.rt = _key_goodbye_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
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
thisExp.addData('key_goodbye.keys',key_goodbye.keys)
if key_goodbye.keys != None:  # we had a response
    thisExp.addData('key_goodbye.rt', key_goodbye.rt)
thisExp.addData('key_goodbye.started', key_goodbye.tStartRefresh)
thisExp.addData('key_goodbye.stopped', key_goodbye.tStopRefresh)
thisExp.nextEntry()

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
