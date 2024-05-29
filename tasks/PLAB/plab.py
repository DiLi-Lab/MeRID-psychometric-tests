from __future__ import absolute_import, division
import pandas as pd
from psychopy import gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, FINISHED)
import os

from psychopy.hardware import keyboard
import yaml
from datetime import datetime

date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

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

# Store info about the experiment session
psychopyVersion = '2023.2.3'
expName = 'PLAB'  # from the Builder filename that created this script


# Create folder name for the results
results_folder = f"{participant_id}_{language}_{country_code}_{lab_number}_S{expInfo['session_id']}"

# Create folder for audio and csv data
output_path = f'data/psychometric_test_{language}_{country_code}_{lab_number}/PLAB/{results_folder}/'
os.makedirs(output_path, exist_ok=True)

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = f"{output_path}" \
           f"{language}{country_code}{lab_number}" \
           f"_{participant_id}_S{expInfo['session_id']}_{date}"

instructions_df = pd.read_excel(f'languages/{language}/instructions/PLAB_instructions_{language.lower()}.xlsx', index_col='screen')
welcome_text = instructions_df.loc['Welcome_text', language]
welcome_text = welcome_text.replace('\\n', '\n')
done_text = instructions_df.loc['done_text', language]
done_text = done_text.replace('\\n', '\n')
# start_warning_text = instructions_df.loc['start_warning_text', language]
# start_warning_text = start_warning_text.replace('\\n', '\n')
Goodbyetext = instructions_df.loc['Goodbye_text', language]
Goodbyetext = Goodbyetext.replace('\\n', '\n')
PLAB_instructions = instructions_df.loc['PLAB_instructions', language]
PLAB_instructions = PLAB_instructions.replace('\\n', '\n')

task1_img = f'languages/{language}/PLAB/Plab_part4_task1_{language.lower()}.png'
task2_img = f'languages/{language}/PLAB/Plab_part4_task2_{language.lower()}.png'
PlabStim = f'languages/{language}/PLAB/PlabStim_{language.lower()}.xlsx'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name='PLAB', version='',
    extraInfo=expInfo, runtimeInfo=None,
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


# Initialize components for Routine "Blank500"
Blank500Clock = core.Clock()
blank = visual.TextStim(win=win, name='blank',
    text='\n\n',
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "FixationCross"
FixationCrossClock = core.Clock()
fix_cross = visual.TextStim(win=win, name='fix_cross',
    text='+',
    font='Courier New',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=0.0);

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

# Initialize components for Routine "PLABInstruction"
PLABInstructionClock = core.Clock()
PLAB_instructions = visual.TextStim(win=win, name='PLAB_instructions',
    text= PLAB_instructions,
    font=font,
    pos=(0, 0), height=0.03, wrapWidth=1.3, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=0.0);
PLAB_instruction_key = keyboard.Keyboard()

# Initialize components for Routine "PLAB Task1 Trials"
PLABTask1Clock = core.Clock()
PLAB_pics_1 = visual.ImageStim(
        win=win,
        name='plab_task1',
        image=task1_img,
        pos=(0, 0.18), # 0.18 is the vertical position of the image from the center
        size=(1.5, 0.6), # 1.5 is the width of the image, 0.6 is the height of the image
        color=[1, 1, 1], colorSpace='rgb',
        ori=0.0,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=False
    )
PLAB_task1 = visual.TextStim(win=win, name='PLAB_task1',
    text='',
    font=font,
    pos=(0, -0.28), height=0.035, wrapWidth=None, ori=0.0, # -0.28 is the vertical position of the text from the center
    color='black', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=0.0);
PLAB_task1_key = keyboard.Keyboard()

# Rectangles for highlighting options
highlight_rects = []
option_positions = [(0, -0.26), (0, -0.31), (0, -0.35), (0, -0.40)]
for pos in option_positions:
    rect = visual.Rect(
        win=win,
        width=0.8, height=0.035,
        pos=pos,
        lineColor='red',
        lineWidth=2,
        fillColor=None
    )
    highlight_rects.append(rect)


# Initialize components for Routine "PLAB Task2 Trials"
PLABTask2Clock = core.Clock()
PLAB_pics_2 = visual.ImageStim(
        win=win,
        name='plab_task2',
        image=task2_img,
        pos=(0, 0.18),
        size=(1.5, 0.6),
        color=[1, 1, 1], colorSpace='rgb',
        ori=0.0,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=False
    )
PLAB_task2 = visual.TextStim(win=win, name='PLAB_task2',
    text='',
    font=font,
    pos=(0, -0.28), height=0.035, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=0.0);
PLAB_task2_key = keyboard.Keyboard()


# Initialize components for Routine "GoodbyeScreen"
GoodbyeScreenClock = core.Clock()
Goodbyetext = visual.TextStim(win=win, name='Goodbyetext',
    text=Goodbyetext,
    font=font,
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0,
    color='black', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=0.0);
key_goodbye = keyboard.Keyboard()


# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# Display welcome message
welcome_text = visual.TextStim(win, text=welcome_text, alignHoriz='center', alignVert='center',
                                 font=font, pos=(0, 0), height=0.05, ori=0.0,
                                    color='black', colorSpace='rgb', opacity=None, languageStyle='LTR', depth=0.0);
welcome_text.draw()
win.flip()
event.waitKeys()


# ------Prepare to start Routine "PLABInstruction"-------
continueRoutine = True
# update component parameters for each repeat
PLAB_instruction_key.keys = []
PLAB_instruction_key.rt = []
_PLAB_instruction_key_allKeys = []
# keep track of which components have finished
PLABInstructionComponents = [PLAB_instructions, PLAB_instruction_key]
for thisComponent in PLABInstructionComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
PLABInstructionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "PLABInstruction"-------
while continueRoutine:
    # get current time
    t = PLABInstructionClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=PLABInstructionClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *PLAB_instructions* updates
    if PLAB_instructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        PLAB_instructions.frameNStart = frameN  # exact frame index
        PLAB_instructions.tStart = t  # local t and not account for scr refresh
        PLAB_instructions.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(PLAB_instructions, 'tStartRefresh')  # time at next scr refresh
        PLAB_instructions.setAutoDraw(True)

    # *PLAB_instruction_key* updates
    waitOnFlip = False
    if PLAB_instruction_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        PLAB_instruction_key.frameNStart = frameN  # exact frame index
        PLAB_instruction_key.tStart = t  # local t and not account for scr refresh
        PLAB_instruction_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(PLAB_instruction_key, 'tStartRefresh')  # time at next scr refresh
        PLAB_instruction_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(PLAB_instruction_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(PLAB_instruction_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if PLAB_instruction_key.status == STARTED and not waitOnFlip:
        theseKeys = PLAB_instruction_key.getKeys(keyList=['space'], waitRelease=False)
        _PLAB_instruction_key_allKeys.extend(theseKeys)
        if len(_PLAB_instruction_key_allKeys):
            PLAB_instruction_key.keys = _PLAB_instruction_key_allKeys[-1].name  # just the last key pressed
            PLAB_instruction_key.rt = _PLAB_instruction_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in PLABInstructionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "PLABInstruction"-------
for thisComponent in PLABInstructionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('PLAB_instructions.started', PLAB_instructions.tStartRefresh)
thisExp.addData('PLAB_instructions.stopped', PLAB_instructions.tStopRefresh)
# check responses
if PLAB_instruction_key.keys in ['', [], None]:  # No response was made
    PLAB_instruction_key.keys = None
thisExp.addData('PLAB_instruction_key.keys',PLAB_instruction_key.keys)
if PLAB_instruction_key.keys != None:  # we had a response
    thisExp.addData('PLAB_instruction_key.rt', PLAB_instruction_key.rt)
thisExp.addData('PLAB_instruction_key.started', PLAB_instruction_key.tStartRefresh)
thisExp.addData('PLAB_instruction_key.stopped', PLAB_instruction_key.tStopRefresh)
thisExp.nextEntry()
# the Routine "PLABInstruction" was not non-slip safe, so reset the non-slip timer
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

full_trial_list = data.importConditions(PlabStim)
# task1 contains the first 4 rows of the trial list
PLAB_task1_list = full_trial_list[:4]
# task2 contains the rest rows of the trial list
PLAB_task2_list = full_trial_list[4:]
# set up handler to look after randomisation of conditions etc
PLAB_task1_trials = data.TrialHandler(nReps=1.0, method='sequential',
    trialList=PLAB_task1_list,
    seed=None, name='PLAB_task1_trials')
thisExp.addLoop(PLAB_task1_trials)  # add the loop to the experiment

mouse = event.Mouse(win=win)
continueRoutine = True
routineTimer = core.CountdownTimer()

for thisPLAB_task1_trial in PLAB_task1_trials:
    valid_answer = False
    currentLoop = PLAB_task1_trials
    question_id = thisPLAB_task1_trial['question_id']
    question = thisPLAB_task1_trial['question']
    options = (thisPLAB_task1_trial['option_a'], thisPLAB_task1_trial['option_b'],
               thisPLAB_task1_trial['option_c'], thisPLAB_task1_trial['option_d'])
    correct_key = thisPLAB_task1_trial['correct_key']
    display_text = f"{question}\n\n {options[0]}\n {options[1]}\n {options[2]}\n {options[3]}"

    # ------Prepare to start Routine "PLAB Task1 Trials"-------
    continueRoutine = True
    # update component parameters for each repeat
    PLAB_task1.setText(display_text)
    PLAB_task1_Components = [PLAB_task1] + highlight_rects  # Add rectangles to the components list
    # Reset keyboard
    PLAB_task1_key.keys = []
    PLAB_task1_key.rt = []
    _PLAB_task1_key_allKeys = []
    task_start_time = globalClock.getTime()

    # -------Run Routine "PLAB Task1 Trials"-------
    while continueRoutine:
        PLAB_pics_1.draw()
        PLAB_task1.draw()

        # *PLAB_practice_key* updates
        theseKeys = PLAB_task1_key.getKeys(keyList=['1', '2', '3', '4', 'space', 'escape'], waitRelease=False)
        for key in theseKeys:
            if key.name in ['1', '2', '3', '4']:
                valid_answer = True
                chosen_key = key.name
                # Highlight the selected option
                selected_option_index = int(key.name) - 1
                for i, rect in enumerate(highlight_rects):
                    if i == selected_option_index:
                        rect.setAutoDraw(True)  # Draw the selected rectangle
                    else:
                        rect.setAutoDraw(False)  # Hide other rectangles

            if key.name == 'space' and valid_answer:
                # A valid key was pressed, store the key name and reaction time
                PLAB_task1_key.keys = chosen_key
                PLAB_task1_key.rt = key.rt - task_start_time
                # Clear all components
                PLAB_task1.setAutoDraw(False)
                for rect in highlight_rects:
                    rect.setAutoDraw(False)
                continueRoutine = False  # End the routine after the space key is pressed
                break  # Exit the loop after handling the valid response

            if key.name == 'escape':
                core.quit()  # Exit the experiment if the escape key was pressed

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in PLAB_task1_Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "PLAB Task1 Trials"-------
    # check responses
    if PLAB_task1_key.keys in ['', [], None]:  # No response was made
        PLAB_task1_key.keys = None
        PLAB_task1_key.corr = int(str(correct_key).lower() == 'none')
    else:  # we had a response
        PLAB_task1_key.corr = int(PLAB_task1_key.keys == str(correct_key))

    # Save trial data
    thisExp.addData('chosen_key', PLAB_task1_key.keys)
    # thisExp.addData('correct_key', correct_key)
    thisExp.addData('correctness', PLAB_task1_key.corr)
    thisExp.addData('rt', PLAB_task1_key.rt)

    routineTimer.reset()
    thisExp.nextEntry()

    # Add a fixation screen between trials
    continueRoutine = True
    fix_cross.tStart = None
    fix_cross.tStop = None
    fix_cross.tStartRefresh = None
    fix_cross.tStopRefresh = None
    routineTimer.reset()
    routineTimer.add(0.5)  # display fixation cross for 500 ms

    while continueRoutine and routineTimer.getTime() > 0:
        fix_cross.draw()
        win.flip()
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
# completed 'PLAB task 1 trials'

# set up handler to look after randomisation of conditions etc
PLAB_task2_trials = data.TrialHandler(nReps=1.0, method='sequential',
                                      trialList=PLAB_task2_list,
                                      seed=None, name='PLAB_task2_trials')
thisExp.addLoop(PLAB_task2_trials)  # add the loop to the experiment

for thisPLAB_task2_trial in PLAB_task2_trials:
    valid_answer = False
    currentLoop = PLAB_task2_trials
    question_id = thisPLAB_task2_trial['question_id']
    question = thisPLAB_task2_trial['question']
    options = (thisPLAB_task2_trial['option_a'], thisPLAB_task2_trial['option_b'],
               thisPLAB_task2_trial['option_c'], thisPLAB_task2_trial['option_d'])
    correct_key = thisPLAB_task2_trial['correct_key']
    display_text = f"{question}\n\n {options[0]}\n {options[1]}\n {options[2]}\n {options[3]}"

    # ------Prepare to start Routine "PLAB Task2 Trials"-------
    continueRoutine = True
    # update component parameters for each repeat
    PLAB_task2.setText(display_text)
    PLAB_task2_Components = [PLAB_task1]
    # Reset keyboard
    PLAB_task2_key.keys = []
    PLAB_task2_key.rt = []
    _PLAB_task2_key_allKeys = []
    task_start_time = globalClock.getTime()

    # -------Run Routine "PLAB Task2 Trials"-------
    while continueRoutine:
        PLAB_pics_2.draw()
        PLAB_task2.draw()

        # *PLAB_practice_key* updates
        theseKeys = PLAB_task2_key.getKeys(keyList=['1', '2', '3', '4', 'space', 'escape'], waitRelease=False)
        for key in theseKeys:
            if key.name in ['1', '2', '3', '4']:
                valid_answer = True
                chosen_key = key.name
                # Highlight the selected option
                selected_option_index = int(key.name) - 1
                for i, rect in enumerate(highlight_rects):
                    if i == selected_option_index:
                        rect.setAutoDraw(True)  # Draw the selected rectangle
                    else:
                        rect.setAutoDraw(False)  # Hide other rectangles
            if key.name == 'space' and valid_answer:
                # A valid key was pressed, store the key name and reaction time
                PLAB_task2_key.keys = chosen_key
                PLAB_task2_key.rt = key.rt - task_start_time
                # Clear all components
                PLAB_task2.setAutoDraw(False)
                for rect in highlight_rects:
                    rect.setAutoDraw(False)
                continueRoutine = False  # End the routine after the space key is pressed
                break  # Exit the loop after handling the valid response

            if key.name == 'escape':
                core.quit()  # Exit the experiment if the escape key was pressed

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in PLAB_task2_Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "PLAB Task2 Trials"-------
    # check responses
    if PLAB_task2_key.keys in ['', [], None]:  # No response was made
        PLAB_task2_key.keys = None
        PLAB_task2_key.corr = int(str(correct_key).lower() == 'none')
    else:  # we had a response
        PLAB_task2_key.corr = int(PLAB_task2_key.keys == str(correct_key))

    # Save trial data
    thisExp.addData('chosen_key', PLAB_task2_key.keys)
    # thisExp.addData('correct_key', correct_key)
    thisExp.addData('correctness', PLAB_task2_key.corr)
    thisExp.addData('rt', PLAB_task2_key.rt)

    routineTimer.reset()
    thisExp.nextEntry()

    # Add a fixation screen between trials
    continueRoutine = True
    fix_cross.tStart = None
    fix_cross.tStop = None
    fix_cross.tStartRefresh = None
    fix_cross.tStopRefresh = None
    routineTimer.reset()
    routineTimer.add(0.5)  # display fixation cross for 500 ms

    while continueRoutine and routineTimer.getTime() > 0:
        fix_cross.draw()
        win.flip()
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

# completed 'PLAB Task2 trials'

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
