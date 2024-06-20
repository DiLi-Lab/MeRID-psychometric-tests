#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment runs the RAN digit test
"""

from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
import sounddevice as sd
import soundfile as sf
from datetime import datetime
import numpy as np
import os
import csv
import yaml
import pandas as pd


date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Path to the YAML file contains the language and experiment configurations
config_path = f'configs/config.yaml'
experiment_config_path = f'configs/experiment.yaml'
digits_path = f'tasks/RAN/digits.yaml'

# Load the YAML file
with open(config_path, 'r', encoding="utf-8") as file:
    config_data = yaml.safe_load(file)
language = config_data['language']
country_code = config_data['country_code']
lab_number = config_data['lab_number']
random_seed = config_data['random_seed']
font = config_data['font']

with open(digits_path, 'r', encoding="utf-8") as file:
    ran_data = yaml.safe_load(file)

# Extract and convert the numbers
digits = [
    [int(char) for line in block.strip().splitlines() for char in line.split() if char.isdigit()]
    for block in ran_data['items']['numbers']
]

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
output_path = f'data/psychometric_test_{language}_{country_code}_{lab_number}/RAN/{results_folder}/'
os.makedirs(output_path, exist_ok=True)
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = f"{output_path}" \
           f"{language}{country_code}{lab_number}" \
           f"_{participant_id}_PT{expInfo['session_id']}_{date}"

# Create folder for audio and csv data
save_audio_path = f"{output_path}/audio_{language}{country_code}{lab_number}" \
                  f"_{participant_id}_PT{expInfo['session_id']}_{date}/"
os.makedirs(save_audio_path, exist_ok=True)
save_csv_path = output_path

# ========================================= Main test =========================================================
# Initialize global variables for recording control
recording = []
recording_start_time = 0
# Configuration of the digit task
num_trials = 8


# Function to start recording audio asynchronously
def start_recording(samplerate=44100, channels=1, device_index=0, dtype='float32'):
    global recording, recording_start_time
    recording_start_time = core.getTime()
    recording = []  # Ensure recording is an empty list before starting
    def callback(indata, frames, time, status):
        recording.extend(indata.copy())
    stream = sd.InputStream(samplerate=samplerate, device=device_index, channels=channels, dtype=dtype, callback=callback)
    stream.start()
    return stream

# Function to stop the current recording and save it
def stop_and_save_recording(stream, filename, samplerate=44100):
    global recording
    stream.stop()
    stream.close()
    recording_stop_time = core.getTime()
    sf.write(filename, recording, samplerate)
    reading_time = recording_stop_time - recording_start_time
    recording.clear()  # Clear the recording list for the next trial
    return reading_time

# Print available devices
print(sd.query_devices())

# Load the instructions
instructions_df = pd.read_excel(f'languages/{language}/instructions/RAN_instructions_{language.lower()}.xlsx', index_col='screen')
welcome_text = instructions_df.loc['Welcome_text', language].replace('\\n', '\n')
instructions = instructions_df.loc['RAN_instructions', language].replace('\\n', '\n')
done_text = instructions_df.loc['done_text', language].replace('\\n', '\n')

# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Setup the Window
win = visual.Window(
    size=[1440, 900], fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='white', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='norm')

# Display welcome message
welcome_text = visual.TextStim(win, text=welcome_text, font=font, pos=(0, 0), height=0.12, wrapWidth=1.5, ori=0.0,
                                    color='black', colorSpace='rgb', opacity=None, languageStyle='LTR', depth=0.0);
welcome_text.draw()
win.flip()
event.waitKeys()

# Display instructions
instructions = visual.TextStim(win, text=instructions, font=font, pos=(0, 0), height=0.07, wrapWidth=1.5, ori=0.0,
                               color='black', colorSpace='rgb', opacity=None, languageStyle='LTR', depth=0.0);
instructions.draw()
win.flip()
event.waitKeys()

# Main experiment
results = []
for trial in range(num_trials):
    # Display fixation screen
    fixation = visual.TextStim(win=win, name='fix_cross', text='+', font='Courier New', pos=(0, 0), height=0.1,
                               wrapWidth=None, ori=0.0, color='black', colorSpace='rgb', opacity=None,
                               languageStyle='LTR', depth=0.0);
    fixation.draw()
    win.flip()
    core.wait(0.5)  # Show fixation for 1 second

    # # Generate and display the digits of 5 * 10 matrix
    # # matrix_content = np.random.choice(digits, size=(5 * 10), replace=True).reshape((5, 10))
    #
    # # Create a 5x9 matrix with each row containing a randomly ordered set of digits 1-9
    # matrix_content = np.array([np.random.permutation(digits) for _ in range(5)])
    # digits_matrix_str = '; '.join([' '.join(row) for row in matrix_content])

    # get the digits from the digits list, instead of generating them
    # print(digits)
    matrix = np.array(digits[trial]).reshape((5, 10))
    matrix_content = matrix.astype(str)
    digits_matrix_str = '; '.join([' '.join(row) for row in matrix_content])

    matrix_str = '\n\n'.join([' '.join(row) for row in matrix_content])
    matrix_display = visual.TextStim(win, text=matrix_str, pos=(0, 0), font='Courier New', height=0.15, wrapWidth=1.5, color='black', colorSpace='rgb')
    matrix_display.draw()
    win.flip()

    # Start audio recording
    audio_filename = f"{save_audio_path}{language}{country_code}{lab_number}_{expInfo['participant_id']}_S{expInfo['session_id']}_trial{trial + 1}.wav"
    stream = start_recording()

    # Wait for space key press to end recording
    # event.waitKeys(keyList=['space'])

    event.clearEvents()  # Clear the event buffer to avoid catching old key presses
    continue_trial = True
    while continue_trial:
        allKeys = event.getKeys()
        for thisKey in allKeys:
            if thisKey == 'space':
                continue_trial = False
                break
            elif thisKey == 'escape':
                win.close()
                core.quit()  # Ensure a clean shutdown

        if not continue_trial:
            break
    # Stop recording, save audio, and calculate reading time
    reading_time = stop_and_save_recording(stream, audio_filename)
    results.append([expInfo['participant_id'], expInfo['session_id'], trial + 1, reading_time, digits_matrix_str])

# Save results to a CSV file
csv_filename = f"{save_csv_path}{language}{country_code}{lab_number}_{expInfo['participant_id']}_S{expInfo['session_id']}_{date}.csv"

with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Participant_id', 'Session_id', 'Trial', 'Reading_Time', 'Digits_Matrix'])
    csvwriter.writerows(results)

# End of task message
end_text = visual.TextStim(win, text=done_text, font=font, pos=(0, 0), height=0.07, wrapWidth=1.5, ori=0.0,
                           color='black', colorSpace='rgb', opacity=None, languageStyle='LTR', depth=0.0)
end_text.draw()
win.flip()
keys = event.waitKeys(keyList=['space'])
win.close()

# core.quit()
