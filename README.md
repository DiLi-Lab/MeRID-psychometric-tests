# MeRID: Psychometric Tests

## Introduction

### What are the Psychometric Tests covered in this project?

Psychometric tests are a standard and scientific method used to measure individuals' mental capabilities and behavioural style. They identify the extent to which candidates' personality and cognitive abilities match those required to perform the role. Employers use the information collected from the psychometric test to identify the hidden aspects of candidates that are difficult to extract from a face-to-face interview.

In this repository, we will cover the following psychometric tests:

1. **Lewandowsky WMC battery** : Working Memory Capacity (WMC) is a measure of the amount of information that can be held in mind and processed at one time. It is a key component of cognitive control and is strongly related to general intelligence. The Lewandowsky WMC battery is a set of tasks that measure WMC. The battery consists of four tasks: Memory Update, Operation Span, Sentence Span, and Spatial Short-Term Memory.
2. **RAN task**: The Rapid Automatized Naming (RAN) task is a test of the speed and efficiency of naming digits. It is used to assess the speed of processing and the ability to quickly retrieve information from memory.
3. **Stroop**: The Stroop test is a test of cognitive control that measures the ability to inhibit automatic responses. The test consists of three parts: a color naming task, a word reading task, and a color-word naming task.
4. **Flanker**: The Flanker test is a test of cognitive control that measures the ability to inhibit irrelevant information. The test consists of a series of trials in which participants must respond to a central target while ignoring flanking distractors.
5. **PLAB test**: The PLAB test is Pimsleur Language Aptitude Battery test. It is a test of language aptitude that is designed to measure an individual's ability to learn a foreign language.
6. **WikiVocab**: The WikiVocab test is a test of vocabulary knowledge that is based on the Wikipedia corpus. It is designed to measure the breadth of an individual's vocabulary knowledge.
7. **Peabody Picture Vocabulary Test (PPVT)**: The PPVT is a test of receptive vocabulary that is designed to measure an individual's ability to understand and use words. It is widely used in clinical and educational settings to assess language development and cognitive abilities.
8. **Berg Card Sorting Test (BCST)**: The BCST is a test of cognitive flexibility that is designed to measure an individual's ability to adapt to changing rules and conditions. It is widely used in clinical and research settings to assess executive function and cognitive control.
## Quick Start

### Clone the repository

```bash
git clone git@github.com:DiLi-Lab/MeRID-psychometric-tests.git
```
or
```bash
git clone https://github.com/DiLi-Lab/MeRID-psychometric-tests.git
```

### Create an environment, e.g with [miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/).

**Note**: Please first check whether you have installed miniconda or anaconda on your computer. If not, please install miniconda or anaconda first. For more information, please refer to the [miniconda documentation](https://docs.anaconda.com/free/miniconda/). If it is installed, please skip installing.
**Note**: The steps of creating an environment is similar to the steps in the MultiplEYE wg1-experiment-implementation repository. For details, please refer to the guidelines in the [wg1-experiment-implementation repository](http://...)

1. In the root directory of the repository, create a new environment with the following command:
```bash
conda create --name psychopy python=3.9
```

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

### Run the tests in English

By default, the tests are in English. First, you need to download the language data for English in the [MultiplEYE data repository](http://...). After downloading the data, unzip the data folder and put the folder `languages/EN` in the root directory of the repository.
To run the tests in English, run the following command:
```bash
python run_merid_psychometric_tests.py
```
With this command, the tests will be run in the following settings which are defined in the `config.yaml` file: 
```yaml
language: EN
full_language: English
country_code: X
lab_number: 1
random_seed: 123
font: Arial Unicode MS
```  
It will run Lewandowsky WMC battery, RAN task, Stroop, Flanker, PLAB task, WikiVocab (under developing), Peabody, WCST sequentially, which are also defined in the `config.yaml` file as `True`:
```yaml
wmc: True
ran: True
stroop_flanker: True
plab: True
peabody: True
wcst: True
```
The Lewandowsky WMC battery consists of four tasks: Memory Update, Operation Span, Sentence Span, and Spatial Short-Term Memory. By default, it will run all 4 tasks.

**Note**:
- Depends on your computer system, you may need to enable the audio input and output for the RAN task. If you encounter any issues with the audio input and output, please refer to the [PsychoPy documentation](https://www.psychopy.org/).
  - For Mac users, you may need to go to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Microphone` and enable your terminal or IDE to access the microphone.
  - For Windows users, you may need to go to `Settings` -> `Privacy` -> `Microphone` and enable your terminal or IDE to access the microphone.
  - For Linux users, you may need to go to `Settings` -> `Privacy` -> `Microphone` and enable your terminal or IDE to access the microphone.
- Depends on your computer system, you may need to enable the keyboard input. If you encounter any issues with the keyboard input, please refer to the [PsychoPy documentation](https://www.psychopy.org/).
  - For Mac users, you may need to go to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Input Monitoring` and add your terminal or IDE to the list.
  - For Windows users, you may need to go to `Settings` -> `Privacy` -> `Keyboard` and add your terminal or IDE to the list.
  - For Linux users, you may need to go to `Settings` -> `Privacy` -> `Keyboard` and add your terminal or IDE to the list.
### Run the tests in other languages

**Note**: For more detailed instructions on what and how to translate, please refer to Section 6 in [MultiplEYE Data Collection Guidelines](https://docs.google.com/document/d/1l8vkXlji2mng73q0wR-I_XMprPbiQT5JlQwvK4pZkA4/edit?usp=sharing). It contains the most up-to-date and official guideline for translating the tests.

1. To run the tests in other languages, first go to the `languages/EN` folder. Copy the `EN` folder and paste it in the `languages` folder. Rename the copied folder to the desired language code, e.g. `DE` for German.
2. Translate all the instructions and stimuli in the copied folder to the desired language.
- In the `instructions/` folder, for the xlsx instruction files, add a new column with the desired language code, e.g. `DE`, and translate the instructions from the `EN` column to the desired language.
- Specifically, after translating the PLAB instruction, we suggestion you copy the texts in a slide or doc file and screenshot them since PLAB tasks take the form of images as some of its inputs. You can follow the screenshotting in the `EN/PLAB/` folder.
- In the `instructions/` folder, for the WMC instruction which is a doc file, you need to translate the whole file and then screenshot the instruction according to the English version and put them in the `DE/WMC/instructions` folder as png files. Name them exactly the same as the English version.
- You need to translate the stimuli for WMC tasks in the `WMC/` folder, which are yaml files.
- You don't need to translate anything for RAN tasks. This is why `RAN` folder is empty.
- You have to translate the xlsx stimuli for Stroop and Flanker tasks in the `Stroop-Flanker/` folders, respectively.
- You need to translate the xlsx stimuli for PLAB tasks in the `PLAB/` folder. 
- If you are using Peabody test in your language, you need to have the audio stimuli, image stimuli and instruction audios in the `Peabody/` folder, under subfolders `audios_xx`, `images_xx` and `Peabody_instructions_audios_xx`, respectively. You also need to change the items and paths accordingly in `ppvt_practice.csv` and `ppvt_vocab.csv` files.
- If you want a different language from English to be used in the GUI, you need to translate the `english.json` file in the `ui_data` folder, and save it as `language_name.json`, e.g. `german.json`. Please make sure that the language name you are using matches the language full name in the `config.yaml` file, but in lowercase.
3. Rename the files in the copied folder to the desired language code so that instead of ending with `en`, they end with the desired language code, e.g. `de`.
4. In the `config.yaml` file, change the `language` and `full_language` to the desired language code and the full language name, respectively. Also change the `country_code` and the `lab_number` to the desired values. For example, for German data collected in University of Zurich at DiLi lab, which is the 2nd lab collecting MultipLEYE data in Switzerland, the settings would be:
```yaml
language: DE
full_language: German
country_code: CH
lab_number: 2
random_seed: 123
font: Arial Unicode MS
```
5. If you want to run only some of the tests, change the corresponding values to `False` in the `config.yaml` file. For example, if you only want to run the WMC battery and the PLAB test, the settings would be:
```yaml
wmc: True
ran: False
stroop_flanker: False
plab: True
peabody: False
wcst: False
wiki_vocab: False
```
6. Run the tests with the following command as for English:
```bash
python run_merid_psychometric_tests.py
```
7. A GUI will pop up with the instructions for you to enter the Participant ID and Session ID. All the other information in the GUI will be automatically filled in based on the settings in the `config.yaml` file. You should double-check that they are correct and consistent. If everything is correct, click the `Start` button to start the tests.
8. If run WMC battery, a second GUI will pop up asking you to select the sub-tasks to run. By default, all 4 tasks are selected. You can deselect the tasks that you don't want to run. Click the `Start` button to start the selected tasks. 
9. After the tests are completed, the results will be saved in the `data` folder in the root directory of the repository. There will be two folders in it. For example, for the above settings:
- The `psychometric_tests_DE_CH_2` folder contains the data for the tests, under separate subfolders for each test. In each test subfolder, there will be a separate folder for each participant, named with the Participant ID, language code, country code, lab number and Session ID. The data is saved in csv files and the logs are saved in log files. For RAN task, there is a folder storing the recorded audios.
- The `participant_configs_DE_CH_2` folder contains the participant configurations, which are saved in yaml files.

## Data Collection
1. When collecting data from each participant, please follow the [MultiplEYE Experimenter Script - Eye-Tracking Session](https://docs.google.com/document/d/1fMb3Z75wRkeidi3hn0jgWMaKC0HgYfhXXQRg45ioiRI/edit?usp=sharing) and [MultiplEYE Experimenter Script - Psychometric Tests Session](https://docs.google.com/document/d/118Yh66S1nBySV-3_YwkUKOUjEEyQjcby5hgcwVnn4Go/edit?usp=sharing) and please always check the Participant ID and Session ID before starting the tests.
2. Upload the whole data folder as a zip file to the MeRID and MultipLEYE data repository for the corresponding lab.

## Repository Structure
```
├── .github                   <- Github Actions workflows
│
├── configs                <- Main configs
│   ├── config             <- Default config, should be fixed for each lab collecting each language data
│   └── experiment         <- experiment caches
│
├── data                   <- Psychometric tests results
│
├── languages              <- Instructions and stimuli for different languages
│
├── tasks                  <- Source code for the psychometric tests
│   ├── PLAB                     <- PLAB scripts
│   ├── RAN                      <- RAN scripts
│   ├── Stroop-Flanker           <- Stroop and Flanker scripts
│   ├── WikiVocab                <- WikiVocab scripts
│   ├── WMC                      <- WMC scripts
│   ├── Peabody                  <- Peabody scripts
│   └── WCST                     <- WCST scripts
│
├── run_merid_psychometric_tests.py     <- Main script for running the psychometric tests
│
├── .gitignore                <- List of files ignored by git
├── .project-root             <- File for inferring the position of project root directory
├── requirements.txt          <- File for installing python dependencies
└── README.md
```
## Contact
Please contact [multipleye@cl.uzh.ch](mailto:multipleye@cl.uzh.ch) for more information.