import re
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
import yaml
import pandas as pd
from datetime import datetime

from main import MyMainWindow


class MyWelcomeWindow(QMainWindow):
    def __init__(self):
        super(MyWelcomeWindow, self).__init__()
        self.initUI()
        self.showFullScreen()

    def initUI(self) -> None:
        self.setStyleSheet("background-color: rgb(221, 235, 255);")
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")

        # Define styles
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(26)  # Increase the font size for the main text
        font.setItalic(False)

        # Set up a vertical layout to center widgets
        layout = QtWidgets.QVBoxLayout(self.centralWidget)

        exp = self.get_exp_info()
        self.language = exp[0].lower()
        self.participant_id = exp[1]
        self.psychopyVersion = exp[2]
        self.expName = exp[3]
        self.filename = exp[4]
        self.output_path = exp[5]

        instructions_df = pd.read_excel(f'languages/{self.language.upper()}/instructions/WikiVocab_instructions_{self.language}.xlsx',
                                        index_col='screen')
        welcome_text = instructions_df.loc['Welcome_text', self.language.upper()]
        welcome_text = welcome_text.replace('\\n', '\n')
        WikiVocab_instructions = instructions_df.loc['WikiVocab_instructions', self.language.upper()]
        WikiVocab_instructions = WikiVocab_instructions.replace('\\n', '\n')
        self.welcome_instructions = welcome_text + WikiVocab_instructions
        self.start_text = instructions_df.loc['start_text', self.language.upper()]

        # Add main text
        self.mainText = QtWidgets.QLabel(self.centralWidget)
        self.mainText.setFont(font)
        self.mainText.setStyleSheet("color: rgb(0, 0, 0);")  # Set font color to black
        self.mainText.setAlignment(QtCore.Qt.AlignCenter)
        self.mainText.setObjectName("mainText")
        self.mainText.setText(self.welcome_instructions)
        layout.addWidget(self.mainText, alignment=QtCore.Qt.AlignCenter)

        # Define styles for other widgets
        widget_font = QtGui.QFont()
        widget_font.setFamily("Arial Unicode MS")
        widget_font.setPointSize(24)
        widget_font.setItalic(False)

        # Add the combo box
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setFont(widget_font)
        self.comboBox.setStyleSheet("color: rgb(0, 0, 0);")  # Set font color to black
        self.comboBox.setStyleSheet("""
                    color: rgb(0, 0, 0);  /* Font color */
                    padding: 10px;       /* Add padding */
                """)  # Add padding and set font color to black
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setMinimumSize(400, 60)
        items = self.get_languages()
        self.comboBox.addItems(items)
        self.comboBox.setCurrentText(self.language)
        layout.addWidget(self.comboBox, alignment=QtCore.Qt.AlignCenter)

        # Add the main button
        self.mainButton = QtWidgets.QPushButton(self.centralWidget)
        self.mainButton.setFont(widget_font)
        self.mainButton.setStyleSheet("""
            color: rgb(0, 0, 0);  /* Font color */
            padding: 10px;       /* Add padding */
        """)  # Add padding and set font color to black
        self.mainButton.setObjectName("mainButton")
        self.mainButton.setMinimumSize(400, 60)
        self.mainButton.clicked.connect(self.click_main_button)
        self.mainButton.setText(self.start_text)
        layout.addWidget(self.mainButton, alignment=QtCore.Qt.AlignCenter)

        self.setCentralWidget(self.centralWidget)

    def click_main_button(self) -> None:
        self.main_window = MyMainWindow(
            name=self.participant_id,
            language=self.comboBox.currentText(),
            result_folder=self.output_path,
            result_filename=self.filename
        )
        self.main_window.show()
        self.close()

    def get_languages(self) -> list:
        result = []
        template = re.compile(r'(.+)\.csv')
        for file in os.listdir("tasks/WikiVocab/data"):
            m = template.match(file)
            if m:
                result.append(m.group(1))
        return result

    def get_exp_info(self):
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
        expName = 'WikiVocab'  # from the Builder filename that created this script

        # Create folder name for the results
        results_folder = f"{participant_id}_{language}_{country_code}_{lab_number}_PT{expInfo['session_id']}"

        # Create folder for audio and csv data
        output_path = f'data/psychometric_test_{language}_{country_code}_{lab_number}/WikiVocab/{results_folder}/'
        os.makedirs(output_path, exist_ok=True)

        # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
        filename = f"{output_path}" \
                   f"{language}{country_code}{lab_number}" \
                   f"_{participant_id}_PT{expInfo['session_id']}_{date}"
        return language, participant_id, psychopyVersion, expName, filename, output_path
