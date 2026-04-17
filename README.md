# MeRID: Psychometric Tests

## Introduction

### What are the Psychometric Tests covered in this project?

Psychometric tests are a standard and scientific method used to measure individuals' mental capabilities and behavioural style. They identify the extent to which candidates' personality and cognitive abilities match those required to perform the role. Employers use the information collected from the psychometric test to identify the hidden aspects of candidates that are difficult to extract from a face-to-face interview.

In this repository, we cover the following psychometric tests. In the MeRID protocol, tests are run in two sessions: in session 1 (after the reading experiment), we run the first 7 tests listed below; in session 2 (after the reading part), we run the last test (Lewandowsky WMC battery).

1. **RAN task**: The Rapid Automatized Naming (RAN) task is a test of the speed and efficiency of naming digits. It is used to assess the speed of processing and the ability to quickly retrieve information from memory.
2. **Stroop**: The Stroop test is a test of cognitive control that measures the ability to inhibit automatic responses. The test consists of a series of trials in which participants must respond to the color of words while ignoring the color words themselves.
3. **Flanker**: The Flanker test is a test of cognitive control that measures the ability to inhibit irrelevant information. The test consists of a series of trials in which participants must respond to a central target while ignoring flanking distractors.
4. **PLAB**: The PLAB test is Pimsleur Language Aptitude Battery test. It is a test of language aptitude that is designed to measure an individual's ability to learn a foreign language.
5. **WikiVocab**: The WikiVocab test is a test of vocabulary knowledge that is based on the Wikipedia corpus. It is designed to measure the breadth of an individual's vocabulary knowledge. For English, German, Dutch, Mandarin and Cantonese Chinese, Portuguese and Estonian, the LexTALE test items are used instead because they are available in the LexTALE dataset and have been validated in each language.
6. **Peabody Picture Vocabulary Test (PPVT)**: The PPVT is a test of receptive vocabulary that is designed to measure an individual's ability to understand and use words. In the current MeRID implementation, Peabody is available only for German.
7. **Card Sorting Test (WCST)**: The WCST is a test of cognitive flexibility that is designed to measure an individual's ability to adapt to changing rules and conditions. It is widely used to assess executive function and cognitive control.
8. **Lewandowsky WMC battery** : Working Memory Capacity (WMC) is a measure of the amount of information that can be held in mind and processed at one time. It is a key component of cognitive control and is strongly related to general intelligence. The Lewandowsky WMC battery is a set of tasks that measure WMC. The battery consists of four tasks: Memory Update, Operation Span, Sentence Span, and Spatial Short-Term Memory.

## Quick Start

### Clone the repository

```bash
git clone git@github.com:DiLi-Lab/MeRID-psychometric-tests.git
```
or
```bash
git clone https://github.com/DiLi-Lab/MeRID-psychometric-tests.git
```

You can also download the repository as a zip file and unzip it to your desired location from the [GitHub repository](https://github.com/DiLi-Lab/MeRID-psychometric-tests) by clicking the `Code` button and then `Download ZIP`.

### Create an environment, e.g with [miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/).

**Note**: Please first check whether you have installed miniconda or anaconda on your computer. If not, please install miniconda or anaconda first. For more information, please refer to the [miniconda documentation](https://docs.anaconda.com/free/miniconda/). If it is installed, please skip installing.
**Note**: The steps of creating an environment are similar to the steps in the MultiplEYE wg1-experiment-implementation repository. For details, please refer to the guidelines in the [wg1-experiment-implementation repository](https://github.com/MultiplEYE-COST/wg1-experiment-implementation).

1. In the root directory of the repository, create a new environment with the following command:
```bash
conda create --name psychopy python=3.10
```

**Note**: The environment name is `psychopy`. You can change it to your desired name. For example, if you want to create an environment named `psytest3.10`, run:
```bash
conda create --name psytest3.10 python=3.10
```
Then change the environment name accordingly in the following steps.

2. Activate the environment:
```bash
conda activate psychopy
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

**Note**:
Mac user may encounter error saying "subprocess-exited-with-error" and "Could not find a local HDF5 installation". If you encounter this error, please run the following command first to install the HDF5 package before running the above command to install the required packages:
```bash
conda install -c anaconda hdf5
```
Then you can simply rerun the above command to install the required packages.

**Note**:
Windows users may encounter `ERROR: Microsoft Visual C++ 14.0 or greater is required`. If so, install the Microsoft C++ Build Tools from the link in the error message, then rerun `pip install -r requirements.txt`. You can find step-by-step instructions in this [Stack Overflow post](https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst).

Additional environment-related issues and fixes are documented in [HANDLING_ERRORS.md](https://github.com/MultiplEYE-COST/wg1-experiment-implementation/blob/main/guidelines/markdown/HANDLING_ERRORS.md).

### Run the tests in English

By default, the tests are in English. First, download the English language data from the [MultiplEYE SwitchDrive data repository](https://drive.switch.ch/index.php/s/i9ecUhd8ygcRDMg?path=%2FPsychometric%20tests%2Flanguages%2FEN) if you have access, or from the [MultiplEYE PsychArchives data repository](https://pasa.psycharchives.org/reviewonly/c46cc0928e2a20454cd5ad101f5b7c0e22ddb34085691e419743538f0e02327b). After downloading, unzip the data and place `languages/EN` in the repository root.

Run the launcher from the repository root:
```bash
python run_merid_psychometric_tests.py
```
The launcher opens a GUI where you confirm participant and lab metadata (participant ID, session ID, language, country code, lab number, and year).

With this command, the tests will be run in the following settings which are defined in the `config.yaml` file: 
```yaml
language: EN
full_language: English
country_code: X
year: 2025
lab_number: 1
random_seed: 123
font: Segoe UI
```  
It will run all tasks set to `True` in `config.yaml`. In the current MeRID protocol, you should run tests in two sessions:
- Session 1: RAN, Stroop-Flanker, PLAB, WikiVocab, Peabody (German only), WCST
- Session 2: Lewandowsky WMC battery

The available task toggles in `config.yaml` are:
```yaml
ran: True
stroop_flanker: True
plab: True
wiki_vocab: True
peabody: True
wcst: True
wmc: True
```
The Lewandowsky WMC battery consists of four tasks: Memory Update, Operation Span, Sentence Span, and Spatial Short-Term Memory. By default, it will run all 4 tasks.
To follow the MeRID two-session protocol, set `wmc: False` for session 1 and set the other tasks to `False` for session 2.
- Tasks set to `True` are shown in the GUI and can be deselected for a specific participant.
- Tasks set to `False` are hidden and cannot be selected at runtime.
- After clicking `Start`, selected tasks run sequentially.
- If WMC is enabled, a second WMC window appears to select WMC subtasks.
- Outputs are saved under `data/MultiplEYE_<LANG>_<COUNTRY>_<LAB>_<YEAR>/<PARTICIPANT>_<LANG>_<COUNTRY>_<LAB>_PT<SESSION>/`.

**Note**:
- Depends on your computer system (Mac, Windows, Linux) and the language you are going to run (e.g., English, Chinese, Persian, etc.), you may need to choose a suitable font for the experiment. The default font is `Segoe UI`, which supports most Latin and Cyrillic languages. If you are running Chinese in a Windows machine, you may need to choose a Chinese font like `Microsoft YaHei` or `SimSun`. We suggest you first try `Segoe UI` or `Arial Unicode MS` to see whether it can display all the characters correctly, and then try other fonts if you encounter any issues.
- Depends on your computer system, you may need to enable the audio input and output for the RAN task. If you encounter any issues with the audio input and output, please refer to the [PsychoPy documentation](https://www.psychopy.org/).
  - For Mac users, you may need to go to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Microphone` and enable your terminal or IDE to access the microphone.
  - For Windows users, you may need to go to `Settings` -> `Privacy` -> `Microphone` and enable your terminal or IDE to access the microphone.
  - For Linux users, you may need to go to `Settings` -> `Privacy` -> `Microphone` and enable your terminal or IDE to access the microphone.
- Depends on your computer system, you may need to enable the keyboard input. If you encounter any issues with the keyboard input, please refer to the [PsychoPy documentation](https://www.psychopy.org/).
  - For Mac users, you may need to go to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Input Monitoring` and add your terminal or IDE to the list.
  - For Windows users, you may need to go to `Settings` -> `Privacy` -> `Keyboard` and add your terminal or IDE to the list.
  - For Linux users, you may need to go to `Settings` -> `Privacy` -> `Keyboard` and add your terminal or IDE to the list.
- WMC currently supports macOS and Windows; Linux is not supported for WMC.
### Run the tests in other languages

**Note**: The current release (April 2026) includes 25 language versions, namely Albanian, Arabic, Basque, Cantonese, Catalan, Croatian, Czech, Danish, English, Estonian, Farsi, Finnish, German, Hebrew, Italian, Kalaallisut, Latvian, Mandarin, Portuguese, Romansh, Russian, Serbian, Slovenian, Swedish, and Turkish, spanning multiple writing systems and typological language families.

For more detailed instructions on what and how to prepare and translate the materials, please refer to Section 6 in the [MultiplEYE Data Collection Guidelines](https://multipleye.eu/wp-content/uploads/MultiplEYE-Data-Collection-Guidelines.pdf). It contains the most up-to-date and official guideline.

1. To run the tests in other languages, first go to the `languages/EN` folder. Copy the `EN` folder and paste it in the `languages` folder. Rename the copied folder to the desired language code, e.g. `DE` for German.
2. Translate all the instructions and stimuli in the copied folder to the desired language.
- In the `instructions/` folder, for the instruction files (supported formats: `.xlsx` or `.csv`), add a new column with the desired language code (e.g., `DE`) and translate the instructions from the `EN` column.
- Specifically, after translating the PLAB instruction, we suggestion you copy the texts in a slide or doc file and screenshot them since PLAB tasks take the form of images as some of its inputs. You can follow the screenshotting in the `EN/PLAB/` folder.
- In the `instructions/` folder, for the WMC instruction which is a doc file, you need to translate the whole file and then screenshot the instruction according to the English version and put them in the `DE/WMC/instructions` folder as png files. Name them exactly the same as the English version.
- You need to translate the stimuli for WMC tasks in the `WMC/` folder, which are yaml files.
- You don't need to translate anything for RAN tasks. This is why `RAN` folder is empty. Feel free to delete the empty `RAN` folder or keep it.
- You have to translate the xlsx/csv stimuli for Stroop and Flanker tasks in the `Stroop-Flanker/` folders, respectively.
- You need to translate the xlsx/csv stimuli for PLAB tasks in the `PLAB/` folder. 
- Peabody is currently configured only for German in MeRID. If you are using Peabody in another language, you need to provide the language-specific audio stimuli, image stimuli and instruction audios in the `Peabody/` folder, under subfolders `audios_xx`, `images_xx` and `Peabody_instructions_audios_xx`, respectively, and update `ppvt_practice.csv` and `ppvt_vocab.csv` accordingly. Otherwise, this test will be disabled no matter what you set `peabody: True` or `peabody: False`.
- If you want a different language from English to be used in the GUI, you need to translate the `english.json` file in the `ui_data` folder, and save it as `language_name.json`, e.g. `german.json`. Please make sure that the language name you are using matches the language full name in the `config.yaml` file, but in lowercase.
3. Rename the files in the copied folder to the desired language code so that instead of ending with `en`, they end with the desired language code, e.g. `de`.
4. In the `config.yaml` file, change the `language` and `full_language` to the desired language code and the full language name, respectively. Also change the `country_code`, `year`, and `lab_number` to the desired values. For example, for German data collected in University of Zurich at DiLi lab, which is the 2nd lab collecting MultipLEYE data in Switzerland, the settings would be:
```yaml
language: DE
full_language: German
country_code: CH
year: 2025
lab_number: 2
random_seed: 123
font: Segoe UI
```
5. If you want to run only some of the tests, change the corresponding values to `False` in the `config.yaml` file. For example, if you only want to run the WMC battery and the PLAB test throughout the whole experiment, the settings would be:
```yaml
ran: False
stroop_flanker: False
plab: True
peabody: False
wcst: False
wiki_vocab: False
wmc: True
```
6. Run the tests with the following command as for English:
```bash
python run_merid_psychometric_tests.py
```
7. In the GUI, enter or confirm participant metadata (`participant-id`, session ID, language, country code, lab number, and year), then click `Start`.
8. Task visibility is controlled by `configs/config.yaml`:
- Tasks set to `True` are shown and can be deselected for an individual participant.
- Tasks set to `False` are hidden and cannot be selected at runtime.
9. If WMC is enabled, a second WMC window appears to select WMC subtasks.
10. Results are saved in:
```text
data/MultiplEYE_<LANG>_<COUNTRY>_<LAB>_<YEAR>/<PARTICIPANT>_<LANG>_<COUNTRY>_<LAB>_PT<SESSION>/
```
The participant-specific YAML config is also saved in the participant folder.

## Data Collection
1. When collecting data from each participant, please follow the [MultiplEYE Experimenter Script - Eye-Tracking Session](https://multipleye.eu/wp-content/uploads/MultiplEYE-Experimenter-Script-Eye-Tracking-Session.pdf) and [MultiplEYE Experimenter Script - Psychometric Tests Session](https://multipleye.eu/wp-content/uploads/MultiplEYE-Experimenter-Script-Psychometric-Tests-Session.pdf), and always check the Participant ID and Session ID before starting the tests.
2. Upload the whole data folder as a zip/rar file to the MeRID and MultiplEYE data repository for the corresponding lab.

## Repository Structure
```
├── .github                   <- Github Actions workflows
│
├── configs                   <- Configuration files
│   ├── config.yaml           <- Lab-level defaults (language, lab metadata, random seed, task toggles)
│   └── experiment.yaml       <- Runtime cache of arguments from the latest launcher run
│
├── data                      <- Runtime output folder (participant folders, task outputs, logs, configs)
│
├── languages                 <- Language-specific instructions, stimuli, and GUI translations
│
├── tasks                     <- Task implementations
│   ├── PLAB                  <- PLAB scripts and assets
│   ├── RAN                   <- RAN scripts and audio handling
│   ├── Stroop-Flanker        <- Stroop and Flanker scripts and stimuli readers
│   ├── WikiVocab             <- WikiVocab scripts (and LexTALE for supported languages)
│   ├── WMC                   <- WMC launcher/task scripts (OS-specific entry points)
│   ├── Peabody               <- Peabody (PPVT) scripts and materials
│   ├── WCST                  <- WCST scripts and assets
│   └── __init__.py
│
├── run_merid_psychometric_tests.py <- Main launcher (GUI, participant folder setup, sequential task execution)
│
├── .gitignore                <- Git ignore rules
├── .project-root             <- Marker file used to infer repository root
├── LICENSE                   <- Project license (GPL-2.0)
├── NOTICE                    <- Third-party attribution notices
├── requirements.txt          <- Python dependencies
└── README.md                 <- Project setup and usage documentation
```

### Directory guide

- `configs/`: edit before data collection; `config.yaml` should stay stable within a lab/language study.
- `languages/`: translation workspace. Each language folder mirrors the task structure and includes UI text resources.
- `tasks/`: code for each psychometric task. Update when changing task logic, stimuli loading, or task-specific outputs.
- `run_merid_psychometric_tests.py`: entrypoint used by experimenters; handles GUI input, task selection, and run order.
- `data/`: generated during execution. Keep participant outputs for upload/archiving, but avoid committing raw data to Git.

### Task folder guide

- `tasks/WMC/`: Lewandowsky WMC battery (Memory Update, Operation Span, Sentence Span, Spatial Short-Term Memory), with OS-specific launch scripts for macOS and Windows plus shared task/common modules.
- `tasks/RAN/`: Rapid Automatized Naming task, including task flow and audio recording handling.
- `tasks/Stroop-Flanker/`: Stroop and Flanker implementations, including trial generation/loading and response logging.
- `tasks/PLAB/`: PLAB task implementation and scoring/output logic used during test execution.
- `tasks/WikiVocab/`: WikiVocab/LexTALE app-style flow (welcome, item/table loading, result handling).
- `tasks/Peabody/`: PPVT task implementation and stimuli handling (currently configured for German in MeRID).
- `tasks/WCST/`: Wisconsin card sorting task implementation and assets.
## Contact
Please contact [multipleye.project@gmail.com](mailto:multipleye.project@gmail.com) for more information.