#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
from pathlib import Path
import platform
import subprocess
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors

from gooey import Gooey, GooeyParser

import yaml
import sys


PARENT_FOLDER = Path(__file__).parent

# Path to the YAML file contains the language and experiment configurations
config_path = f'{PARENT_FOLDER}/configs/config.yaml'
experiment_config_path = f'{PARENT_FOLDER}/configs/experiment.yaml'

# Load the YAML file
with open(config_path, 'r', encoding="utf-8") as file:
    config_data = yaml.safe_load(file)
language = config_data['language']
full_language = config_data['full_language']
country_code = config_data['country_code']
lab_number = config_data['lab_number']
random_seed = config_data['random_seed']
wmc = config_data['wmc']
ran = config_data['ran']
stroop_flanker = config_data['stroop_flanker']
plab = config_data['plab']
peabody = config_data['peabody']
wiki_vocab = config_data['wiki_vocab']
wcst = config_data['wcst']

LANG_DIR = f'{PARENT_FOLDER}/languages/{language}/ui_data/interface_language/'
IMAGE_DIR = f'{PARENT_FOLDER}/languages/{language}/ui_data/interface_icons/'
if not os.path.exists(f'{LANG_DIR}/experiment_interface_{language.lower()}.json'):
    GUI_LANG = 'experiment_interface_en'
else:
    GUI_LANG = f'experiment_interface_{language.lower()}'

with open(f'{LANG_DIR}/{GUI_LANG}.json', 'r', encoding='utf-8') as translation_file:
    translations = json.load(translation_file)

@Gooey(
    language=GUI_LANG,
    program_name=translations['program_name'],
    program_description=translations['program_description'],
    image_dir=str(IMAGE_DIR),
    default_size=(900, 800),
    language_dir=str(LANG_DIR),
    show_preview_warning=False,
)
def parse_args():
    parser = GooeyParser(
        description=translations['parser_description'],
    )

    lab_settings = parser.add_argument_group(
        'Lab Settings',
        description=f'At the moment you will run the experiment with the language settings below. '
                    f'Review and modify the language settings below if they differ from your pre-registration form.',
        gooey_options={
            'show_underline': False,
        },
    )
    lab_settings.add_argument(
        '--language',
        widget='TextField',
        metavar='Language',
        help='Enter the 2-letter ISO-639-1 language code (e.g., EN, DE).',
        default=language,
        required=True,
        gooey_options={'visible': True},
    )
    lab_settings.add_argument(
        '--full_language',
        widget='TextField',
        help='Enter the full name of the language (e.g., English, German).',
        metavar='Full language',
        default=full_language,
        required=True,
        gooey_options={'visible': True},
    )
    lab_settings.add_argument(
        '--country_code',
        help='Enter the 2-letter ISO-3166-1 country code (e.g., US, DE).',
        metavar='Country code',
        widget='TextField',
        default=country_code,
        required=True,
        gooey_options={'visible': True},
    )
    lab_settings.add_argument(
        '--lab_number',
        metavar='Lab number',
        help='Enter your lab number as in the pre-registration form.',
        widget='TextField',
        default=1,
        type=int,
        required=True,
        gooey_options={'visible': True}
    )
    participants = parser.add_argument_group('Participant Information')
    participants.add_argument(
        '--participant-id',
        metavar='Participant ID',
        # default=1,
        type=int,
        widget='TextField',
        help='Enter the participant ID (1-999).',
        required=True,
        gooey_options={'visible': True}
    )
    participants.add_argument(
        '--session-id',
        metavar='Session ID',
        default=1,
        type=int,
        widget='TextField',
        help='Enter the session ID (1-9).',
        required=True,
        gooey_options={'visible': True}
    )
    participants.add_argument(
        '--random_seed',
        metavar='Random Seed',
        default=random_seed,
        type=int,
        widget='TextField',
        help='Random seed has to be a number between 1 and 9999.'
             'It is used to reproduce the same random sequence and numbers for the WMC and RAN experiments.'
             'If you want to change the random seed, please edit the config.yaml file in the configs folder.',
        required=True,
        gooey_options={'visible': True}
    )
    # add an argument for each test. Tests are WMC, Peabody, PLAB, RAN, StroopFlanker
    tests = parser.add_argument_group('Psychometric Tests',
                                      description='If you want to change the tests that you want to run, please edit the config.yaml file in the configs folder.')
    parser.set_defaults(ran=ran)
    parser.set_defaults(stroop_flanker=stroop_flanker)
    parser.set_defaults(plab=plab)
    # Main tests checkbox
    tests.add_argument(
        '--wmc',
        metavar=translations['wmc'],
        help=translations['wmc_help'],
        default=wmc,
        required=False,
        action='store_true',
        gooey_options={'visible': wmc}
    )

    tests.add_argument(
        '--ran',
        metavar=translations['ran'],
        help=translations['ran_help'],
        default=ran,
        required=False,
        action='store_true',
        gooey_options={'visible': ran}
    )

    tests.add_argument(
        '--stroop_flanker',
        metavar=translations['stroop_flanker'],
        help=translations['stroop_flanker_help'],
        default=stroop_flanker,
        required=False,
        action='store_true',
        gooey_options={'visible': stroop_flanker}
    )
    tests.add_argument(
        '--plab',
        metavar=translations['plab'],
        help=translations['plab_help'],
        default=plab,
        required=False,
        action='store_true',
        gooey_options={'visible': plab}
    )
    tests.add_argument(
        '--wiki_vocab',
        metavar=translations['wiki_vocab'],
        help=translations['wiki_vocab_help'],
        default=wiki_vocab,
        required=False,
        action='store_true',
        gooey_options={'visible': wiki_vocab}

    )
    tests.add_argument(
        '--ppvt',
        metavar=translations['ppvt'],
        help=translations['ppvt_help'],
        default=peabody,
        required=False,
        action='store_true',
        gooey_options={'visible': peabody}
    )
    tests.add_argument(
        '--wcst',
        metavar=translations['wcst'],
        help=translations['wcst_help'],
        default=wcst,
        required=False,
        action='store_true',
        gooey_options={'visible': wcst}
    )
    args = vars(parser.parse_args())
    print(args)
    return args


def run_script(script_path):
    try:
        result = subprocess.run(['python', script_path], check=True, text=True, capture_output=False)
        print("Output:", result.stdout)
        print("Errors:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        raise e

if __name__ == '__main__':
    system = platform.system()
    print(system)

    arguments = parse_args()
    arguments['system'] = system

    experiment_config_folder = f'{PARENT_FOLDER}/data/participant_configs_{language}_{country_code}_{lab_number}/'
    os.makedirs(experiment_config_folder, exist_ok=True)
    participant_config_path = f'{experiment_config_folder}/' \
                              f'{arguments["participant_id"]:03}_{arguments["language"]}_{arguments["country_code"]}' \
                              f'_{arguments["lab_number"]}_PT{arguments["session_id"]}.yaml'
    with open(experiment_config_path, 'w', encoding='utf-8') as file:  # cache the arguments
        yaml.dump(arguments, file)

    path_to_tasks = os.path.abspath('tasks/')
    sys.path.insert(0, path_to_tasks)  # Add tasks directory to Python path

    if arguments['wmc']:
        print("Running WMC")
        if system == 'Windows':
            print("Running WMC on Windows")
            run_script('tasks/WMC/wmc_windows.py')
        elif system == 'Linux':
            print("Running WMC on Linux")
            run_script('tasks/WMC/wmc_linux.py')
        else:
            print("Running WMC on Mac")
            run_script('tasks/WMC/wmc_mac.py')
        arguments['run_wmc'] = 'success'

    if arguments['ran']:
        print("Running RAN")
        run_script('tasks/RAN/ran_task.py')
        arguments['run_ran'] = 'success'

    if arguments['stroop_flanker']:
        print("Running Stroop Flanker")
        run_script('tasks/Stroop-Flanker/stroop_flanker.py')
        arguments['run_stroop_flanker'] = 'success'

    if arguments['plab']:
        print("Running PLAB")
        run_script('tasks/PLAB/plab.py')
        arguments['run_plab'] = 'success'

    if arguments['wiki_vocab']:
        print("Running WikiVocab")
        run_script('tasks/WikiVocab/app.py')
        arguments['run_wiki_vocab'] = 'success'

    if arguments['ppvt']:
        if Path(f"languages/{language}/instructions/Peabody_instructions_{language}.xlsx").exists():
            print("Running PPVT")
            run_script('tasks/Peabody/ppvt.py')
            arguments['run_ppvt'] = 'success'
        else:
            print("PPVT is not available for this language.")

    if arguments['wcst']:
        if Path(f"languages/{language}/instructions/WCST_instructions_{language}.xlsx").exists():
            print("Running WCST")
            run_script('tasks/WCST/wcst.py')
            arguments['run_wcst'] = 'success'
        else:
            print("WCST is not available for this language.")

    with open(participant_config_path, 'w') as file:
        yaml.dump(arguments, file)
    core.quit()