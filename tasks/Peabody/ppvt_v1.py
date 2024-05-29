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
from psychopy import  gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import os

from psychopy.hardware import keyboard
from psychopy import sound


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
language = 'de'  # 'en' or 'de' for English or German

# Store info about the experiment session
psychopyVersion = '2021.2.3'
expName = 'PPVT'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'results/ppvt/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

instructions_df = pd.read_excel('stroop_flanker_instructions.xlsx', index_col='screen')
welcome_text = instructions_df.loc['Welcome_text', language]
welcome_text = welcome_text.replace('\\n', '\n')
done_text = instructions_df.loc['done_text', language]
done_text = done_text.replace('\\n', '\n')
start_warning_text = instructions_df.loc['start_warning_text', language]
start_warning_text = start_warning_text.replace('\\n', '\n')
Goodbyetext = instructions_df.loc['Goodbyetext', language]
Goodbyetext = Goodbyetext.replace('\\n', '\n')
PPVT_instructions = instructions_df.loc['PPVT_instructions', language]
PPVT_instructions = PPVT_instructions.replace('\\n', '\n')

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/cui/Documents/uzh/PhD/Projects/MeRID/Psychometric_Tests/Stroop-Flanker-PPVT/pptv.py',
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

# Initialize the audio icon as a visual stimulus
audio_icon = visual.ImageStim(win=win, image="/Users/cui/Documents/uzh/PhD/Projects/MeRID/Psychometric_Tests/Stroop-Flanker-PPVT/languages/de/ppvt/audios/audio_icon.png", pos=(0, 0), size=(0.1, 0.1))

# # Initialize the audio stimulus (assuming sound.Sound() is already imported)
# audio_stim = sound.Sound(value='A', secs=-1)  # Placeholder, will set the actual sound file later

# Initialize components for Routine "WelcomeScreen"
WelcomeScreenClock = core.Clock()
Welcome_text = visual.TextStim(win=win, name='Welcome_text',
    text=welcome_text,
    font='Courier New',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=0.0);
Welcome_resp = keyboard.Keyboard()

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

# Initialize components for Routine "StartWarning"
StartWarningClock = core.Clock()
start_warning_text = visual.TextStim(win=win, name='start_warning_text',
    text=start_warning_text,
    font='Courier New',
    pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Done"
DoneClock = core.Clock()
done_text = visual.TextStim(win=win, name='done_text',
    text=done_text,
    font='Courier New',
    pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
done_key = keyboard.Keyboard()

# Initialize components for Routine "PPVTInstruction"
PPVTInstructionClock = core.Clock()
PPVT_instructions = visual.TextStim(win=win, name='PPVT_instructions',
    text= PPVT_instructions,
    font='Courier New',
    pos=(0, 0), height=0.035, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
PPVT_instruction_key = keyboard.Keyboard()

# Positions for the images: top-left, top-right, bottom-left, bottom-right
positions = [(-0.25, 0.25), (0.25, 0.25), (-0.25, -0.25), (0.25, -0.25)]
# Assuming all images are the same size and the path to the images are specified correctly
practice_images = [
    'languages/de/ppvt/images/set_0/1_1.png',
    'languages/de/ppvt/images/set_0/1_2.png',
    'languages/de/ppvt/images/set_0/1_3.png',
    'languages/de/ppvt/images/set_0/1_4.png'
]

# Initialize components for Routine "PPVTPractice"
PPVTPracticeClock = core.Clock()
# Create a list to hold the ImageStim objects for the four images
PPVT_practice_pics = [
    visual.ImageStim(
        win=win,
        name=f'PPVT_practice_pic_{i}',
        image=practice_images[i],
        pos=positions[i],
        size=(0.35, 0.35),  # Adjust the size as needed
        color=[1, 1, 1], colorSpace='rgb',
        ori=0.0,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True
    ) for i in range(4)
]
PPVT_practice_key = keyboard.Keyboard()

# Initialize components for Routine "PPVT_practice_feedback"
PPVT_practice_feedbackClock = core.Clock()
PPVT_feedback_text = visual.TextStim(win=win, name='PPVT_feedback_text',
    text='',
    font='Courier New',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
    color='white', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "PPVTTrials"
PPVTTrialsClock = core.Clock()
PPVT_pics = [
    visual.ImageStim(
        win=win,
        name=f'PPVT_pic_{i}',
        image=None,
        pos=positions[i],
        size=(0.35, 0.35),
        color=[1, 1, 1], colorSpace='rgb',
        ori=0.0,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True
    ) for i in range(4)
]
PPVT_key = keyboard.Keyboard()

# Initialize components for Routine "GoodbyeScreen"
GoodbyeScreenClock = core.Clock()
Goodbyetext = visual.TextStim(win=win, name='Goodbyetext',
    text=Goodbyetext,
    font='Courier New',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0,
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

# ------Prepare to start Routine "PPVTInstruction"-------
continueRoutine = True
# update component parameters for each repeat
PPVT_instruction_key.keys = []
PPVT_instruction_key.rt = []
_PPVT_instruction_key_allKeys = []
# keep track of which components have finished
PPVTInstructionComponents = [PPVT_instructions, PPVT_instruction_key]
for thisComponent in PPVTInstructionComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
PPVTInstructionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "PPVTInstruction"-------
while continueRoutine:
    # get current time
    t = PPVTInstructionClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=PPVTInstructionClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *PPVT_instructions* updates
    if PPVT_instructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        PPVT_instructions.frameNStart = frameN  # exact frame index
        PPVT_instructions.tStart = t  # local t and not account for scr refresh
        PPVT_instructions.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(PPVT_instructions, 'tStartRefresh')  # time at next scr refresh
        PPVT_instructions.setAutoDraw(True)

    # *PPVT_instruction_key* updates
    waitOnFlip = False
    if PPVT_instruction_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        PPVT_instruction_key.frameNStart = frameN  # exact frame index
        PPVT_instruction_key.tStart = t  # local t and not account for scr refresh
        PPVT_instruction_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(PPVT_instruction_key, 'tStartRefresh')  # time at next scr refresh
        PPVT_instruction_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(PPVT_instruction_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(PPVT_instruction_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if PPVT_instruction_key.status == STARTED and not waitOnFlip:
        theseKeys = PPVT_instruction_key.getKeys(keyList=['space'], waitRelease=False)
        _PPVT_instruction_key_allKeys.extend(theseKeys)
        if len(_PPVT_instruction_key_allKeys):
            PPVT_instruction_key.keys = _PPVT_instruction_key_allKeys[-1].name  # just the last key pressed
            PPVT_instruction_key.rt = _PPVT_instruction_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in PPVTInstructionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "PPVTInstruction"-------
for thisComponent in PPVTInstructionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('PPVT_instructions.started', PPVT_instructions.tStartRefresh)
thisExp.addData('PPVT_instructions.stopped', PPVT_instructions.tStopRefresh)
# check responses
if PPVT_instruction_key.keys in ['', [], None]:  # No response was made
    PPVT_instruction_key.keys = None
thisExp.addData('PPVT_instruction_key.keys',PPVT_instruction_key.keys)
if PPVT_instruction_key.keys != None:  # we had a response
    thisExp.addData('PPVT_instruction_key.rt', PPVT_instruction_key.rt)
thisExp.addData('PPVT_instruction_key.started', PPVT_instruction_key.tStartRefresh)
thisExp.addData('PPVT_instruction_key.stopped', PPVT_instruction_key.tStopRefresh)
thisExp.nextEntry()
# the Routine "PPVTInstruction" was not non-slip safe, so reset the non-slip timer
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
PPVT_practice_trials = data.TrialHandler(nReps=1.0, method='sequential',
    trialList=data.importConditions('languages/de/ppvt/ppvt_practice.csv'),
    seed=None, name='PPVT_practice_trials')
thisExp.addLoop(PPVT_practice_trials)  # add the loop to the experiment

mouse = event.Mouse(win=win)
continueRoutine = True
routineTimer = core.CountdownTimer()

for thisPPVT_practice_trial in PPVT_practice_trials:
    currentLoop = PPVT_practice_trials
    set_id = thisPPVT_practice_trial['set_id']
    correct_key = thisPPVT_practice_trial['correct_key']
    print(f"Set ID: {set_id}, Correct Key: {correct_key}")

    audio_path = thisPPVT_practice_trial['audios_path']
    audio_stim = sound.Sound(value=audio_path)
    audio_played = False

    # ------Prepare to start Routine "FixationCross"-------
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
    PPVT_practice_trials.addData('fix_cross.started', fix_cross.tStartRefresh)
    PPVT_practice_trials.addData('fix_cross.stopped', fix_cross.tStopRefresh)

    # ------Prepare to start Routine "PPVTPractice"-------
    continueRoutine = True
    # Update images for each repeat (if necessary)
    for pic, pos, img in zip(PPVT_practice_pics, positions, practice_images):
        pic.setPos(pos)
        pic.setImage(img)
    # Reset keyboard
    PPVT_practice_key.keys = []
    PPVT_practice_key.rt = []
    _PPVT_practice_key_allKeys = []

    # -------Run Routine "PPVTPractice"-------
    while continueRoutine:
        # Draw each practice image
        for pic in PPVT_practice_pics:
            pic.draw()

        audio_icon.draw()
        # Check for initial audio playback after lag
        if not audio_played and routineTimer.getTime() < 0:
            audio_stim.play()
            audio_played = True

        # *PPVT_practice_key* updates
        theseKeys = PPVT_practice_key.getKeys(keyList=['1', '2', '3', '4', 'escape', 'r'], waitRelease=False)
        for key in theseKeys:
            if key.name in ['1', '2', '3', '4']:
                # A valid key was pressed, store the key name and reaction time
                PPVT_practice_key.keys = key.name
                PPVT_practice_key.rt = key.rt
                continueRoutine = False  # End the routine after the first valid response
                break  # Exit the loop after handling the valid response
            elif key.name == 'escape':
                # The escape key was pressed, exit the experiment
                core.quit()
            elif key.name == 'r':
                audio_stim.stop()  # Stop any current playback
                audio_stim.play()

        # Check for mouse click on the audio icon or ‘r’ key press to replay audio
        if mouse.isPressedIn(audio_icon):
            audio_stim.stop()  # Stop any current playback
            audio_stim.play()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "PPVTPractice"-------
    # Disable autoDraw for all images
    for pic in PPVT_practice_pics:
        if hasattr(pic, "setAutoDraw"):
            pic.setAutoDraw(False)
    # Check responses
    if PPVT_practice_key.keys in ['', [], None]:  # No response was made
        PPVT_practice_key.keys = None
        PPVT_practice_key.corr = int(
            str(correct_key).lower() == 'none')  # correct non-response if 'none' is the correct key
    else:
        # Check if the pressed key is correct
        PPVT_practice_key.corr = int(PPVT_practice_key.keys == str(correct_key))

    # Store data for PPVT_practice_trials (TrialHandler)
    PPVT_practice_trials.addData('PPVT_practice_key.keys', PPVT_practice_key.keys)
    PPVT_practice_trials.addData('PPVT_practice_key.corr', PPVT_practice_key.corr)
    if PPVT_practice_key.keys is not None:  # We had a response
        PPVT_practice_trials.addData('PPVT_practice_key.rt', PPVT_practice_key.rt)

    # Reset the routine timer for the next routine
    routineTimer.reset()

    # ------Prepare to start Routine "PPVT_practice_feedback"-------
    continueRoutine = True
    routineTimer.add(1.000000)
    # update component parameters for each repeat
    if(PPVT_practice_key.corr == 1):
        feedback_text2 = "✓"
    elif(PPVT_practice_key.corr == 0):
        feedback_text2 = "✗"
    PPVT_feedback_text.setText(feedback_text2)
    # keep track of which components have finished
    PPVT_practice_feedbackComponents = [PPVT_feedback_text]
    for thisComponent in PPVT_practice_feedbackComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    PPVT_practice_feedbackClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "PPVT_practice_feedback"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = PPVT_practice_feedbackClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=PPVT_practice_feedbackClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *PPVT_feedback_text* updates
        if PPVT_feedback_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            PPVT_feedback_text.frameNStart = frameN  # exact frame index
            PPVT_feedback_text.tStart = t  # local t and not account for scr refresh
            PPVT_feedback_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(PPVT_feedback_text, 'tStartRefresh')  # time at next scr refresh
            PPVT_feedback_text.setAutoDraw(True)
        if PPVT_feedback_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > PPVT_feedback_text.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                PPVT_feedback_text.tStop = t  # not accounting for scr refresh
                PPVT_feedback_text.frameNStop = frameN  # exact frame index
                win.timeOnFlip(PPVT_feedback_text, 'tStopRefresh')  # time at next scr refresh
                PPVT_feedback_text.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in PPVT_practice_feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "PPVT_practice_feedback"-------
    for thisComponent in PPVT_practice_feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    PPVT_practice_trials.addData('PPVT_feedback_text.started', PPVT_feedback_text.tStartRefresh)
    PPVT_practice_trials.addData('PPVT_feedback_text.stopped', PPVT_feedback_text.tStopRefresh)
    thisExp.nextEntry()
    
# completed 'PPVT_practice_trials'


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


current_set = 11  # Starting set number
sum_m = 0  # Initialize sum_m, will be reset for each set
total_mistakes = 0  # Initialize total_mistakes, will be reset for each set
floor_set = None
ceiling_set = None
sets_tested = []

full_df = pd.read_csv('./languages/de/ppvt/ppvt_vocab.csv')

# Main experiment loop
while current_set >= 1 and current_set <= 19:
    print("current_set: ", current_set)
    sum_m = 0
    current_set_df = full_df[full_df['set_id'] == current_set]
    current_set_trials = current_set_df.to_dict('records')
    # set up handler to look after randomisation of conditions etc
    PPVT_trials = data.TrialHandler(nReps=1.0, method='sequential',
        trialList=current_set_trials,
        seed=None, name='PPVT_trials')
    thisExp.addLoop(PPVT_trials)  # add the loop to the experiment

    mouse = event.Mouse(win=win)
    continueRoutine = True
    routineTimer = core.CountdownTimer()

    for thisPPVT_trial in PPVT_trials:
        currentLoop = PPVT_trials
        set_id = thisPPVT_trial['set_id']
        correct_key = thisPPVT_trial['correct_key']
        print(f"Set ID: {set_id}, Correct Key: {correct_key}")
        images_path = [thisPPVT_trial['images_path_1'],
                  thisPPVT_trial['images_path_2'],
                  thisPPVT_trial['images_path_3'],
                  thisPPVT_trial['images_path_4']]
        # for i, img_path in enumerate(images_path):
        #     PPVT_pics[i].image = img_path

        audio_path = thisPPVT_trial['audios_path']
        audio_stim = sound.Sound(value=audio_path)
        audio_played = False

        # ------Prepare to start Routine "FixationCross"-------
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
        PPVT_trials.addData('fix_cross.started', fix_cross.tStartRefresh)
        PPVT_trials.addData('fix_cross.stopped', fix_cross.tStopRefresh)

        # ------Prepare to start Routine "PPVTTrials"-------
        continueRoutine = True
        # update component parameters for each repeat
        for pic, pos, img in zip(PPVT_pics, positions, images_path):
            pic.setPos(pos)
            pic.setImage(img)
        PPVT_key.keys = []
        PPVT_key.rt = []
        _PPVT_key_allKeys = []

        # -------Run Routine "PPVTTrials"-------
        while continueRoutine:
            # get current time
            for pic in PPVT_pics:
                pic.draw()

            audio_icon.draw()
            # Check for initial audio playback after lag
            if not audio_played and routineTimer.getTime() < 0:
                audio_stim.play()
                audio_played = True

            # *PPVT_practice_key* updates
            theseKeys = PPVT_key.getKeys(keyList=['1', '2', '3', '4', 'escape', 'r'], waitRelease=False)
            for key in theseKeys:
                if key.name in ['1', '2', '3', '4']:
                    # A valid key was pressed, store the key name and reaction time
                    PPVT_key.keys = key.name
                    PPVT_key.rt = key.rt
                    continueRoutine = False  # End the routine after the first valid response
                    break  # Exit the loop after handling the valid response
                elif key.name == 'escape':
                    # The escape key was pressed, exit the experiment
                    core.quit()
                elif key.name == 'r':
                    audio_stim.stop()  # Stop any current playback
                    audio_stim.play()

            # Check for mouse click on the audio icon or ‘r’ key press to replay audio
            if mouse.isPressedIn(audio_icon):
                audio_stim.stop()  # Stop any current playback
                audio_stim.play()

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "PPVTTrials"-------
        for thisComponent in PPVT_pics:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        # check responses
        print("key pressed: ", PPVT_key.keys)
        PPVT_key.corr = int(PPVT_key.keys == str(correct_key).strip())
        if PPVT_key.corr == 0:
            sum_m += 1
            total_mistakes += 1
            print("wrong!", sum_m)
        # store data for PPVT_trials (TrialHandler)
        PPVT_trials.addData('PPVT_key.keys',PPVT_key.keys)
        PPVT_trials.addData('PPVT_key.corr', PPVT_key.corr)
        PPVT_trials.addData('PPVT_key.mistakes', sum_m)
        if PPVT_key.keys != None:  # we had a response
            PPVT_trials.addData('PPVT_key.rt', PPVT_key.rt)
        # the Routine "PPVTTrials" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()

    sets_tested.append(current_set)
    if sum_m <= 1:
        if not floor_set:
            floor_set = current_set
            print("floor_set: ", floor_set)
            if ceiling_set: break
        if current_set == 19:
            ceiling_set = 19
            break
        current_set = max(sets_tested) + 1  # Continue testing the next set
    elif sum_m >= 8:
        if not ceiling_set:
            ceiling_set = current_set  # Current set could potentially be the ceiling set
            print("ceiling_set: ", ceiling_set)
            if floor_set: break
        if current_set == 1:
            floor_set = 'untestable'
            break
        current_set = min(sets_tested) - 1
    else:
        if current_set == 1:
            floor_set = 1
            print("floor_set: ", 1)
            current_set = max(sets_tested) + 1
        elif current_set == 19:
            ceiling_set = 19
            print("ceiling_set: ", 19)
            break
        else:
            if floor_set:
                current_set = max(sets_tested) + 1
            else:
                current_set = min(sets_tested) - 1

log_stats = (f"Floor set: {floor_set}, Ceiling set: {ceiling_set}\n"
               f"Total mistakes: {total_mistakes}, Raw Values: {12 * int(ceiling_set) - total_mistakes}")

# Print the message to the console
print(log_stats)

# Write the message to the log file
logging.log(level=logging.DATA, msg=log_stats)

# completed 'PPVT_trials'

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
core.quit()
