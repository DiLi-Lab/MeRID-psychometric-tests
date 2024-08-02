import os
import hashlib
from functools import partial
import time  # Add the time module

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QPixmap
from bidi import algorithm as bidialg
import arabic_reshaper
import matplotlib.pyplot as plt
import pandas as pd

from result import MyResultWindow

# Maximum number is 63
NUM_OF_WORDS = 63


def plot_text(text, file_path, font_name):
    # Calculate size based on text length
    text_length = len(text)
    width = 4 + (text_length / 10)
    # width = 5.5  # Adjust width dynamically
    height = 2  # Fixed height

    # Create a figure with calculated dimensions
    plt.figure(figsize=(width, height))  # Use calculated width
    plt.text(
        0.5,
        0.5,
        text,
        family=font_name,
        fontsize=34,
        weight='black',
        horizontalalignment='center',
        verticalalignment='center',
        transform=plt.gca().transAxes,
        clip_on=False
    )
    plt.axis('off')  # Turn off the axis
    plt.savefig(file_path, format='svg', bbox_inches='tight', pad_inches=0)  # Save the figure
    plt.close()


class MyMainWindow(QMainWindow):
    def __init__(self, name, language, result_folder, result_filename):
        super(MyMainWindow, self).__init__()
        self.name = name
        self.language = language
        self.result_folder = result_folder
        self.result_filename = result_filename
        self.data_df = None
        self.result_df = None
        self.current_index = -1
        self.stimulus_shown_time = None  # To capture the time when stimulus is shown
        instructions_df = pd.read_excel(f'languages/{self.language.upper()}/instructions/WikiVocab_instructions_{self.language}.xlsx',
                                        index_col='screen')
        key_instruction = instructions_df.loc['key_instruction', self.language.upper()]
        self.key_instruction = key_instruction.replace('\\n', '\n')
        self.real_text = instructions_df.loc['real_text', self.language.upper()]
        self.fake_text = instructions_df.loc['fake_text', self.language.upper()]

        self.initUI()

    def initUI(self) -> None:
        self.prepare_data()
        self.stimulies = self._get_stimuli()
        self.stimuli = next(self.stimulies)

        self.resize(900, 600)
        # self.showFullScreen()
        self.setStyleSheet("background-color: rgb(221, 235, 255);")
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")

        # Define styles
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(20)
        font.setItalic(False)  # Set italic to False

        # Use QSvgWidget to render SVGs
        # if Chinese, read png files from ch_items folder
        if self.language == 'zh':
            self.imageLabel = QtWidgets.QLabel(self.centralWidget)
            self.imageLabel.setGeometry(QtCore.QRect(350, 70, 471, 191))
        else:
            self.imageLabel = QSvgWidget(self.centralWidget)
            self.imageLabel.setGeometry(QtCore.QRect(210, 70, 471, 191))

        self.imageLabel.setObjectName("imageLabel")
        self.load_image()
        self.stimulus_shown_time = time.time()  # Capture the time when stimulus is shown

        self.real = QtWidgets.QPushButton(self.centralWidget)
        self.real.setGeometry(QtCore.QRect(700, 450, 101, 71))  # Align vertically
        self.real.setFont(font)
        self.real.setStyleSheet("color: rgb(0, 0, 0);")  # Set font color to black
        self.real.setObjectName("real")
        self.real.setText(self.real_text)
        self.real.clicked.connect(partial(self.process_action, "real"))

        self.fake = QtWidgets.QPushButton(self.centralWidget)
        self.fake.setGeometry(QtCore.QRect(100, 450, 101, 71))  # Align vertically
        self.fake.setFont(font)
        self.fake.setAutoFillBackground(False)
        self.fake.setStyleSheet("color: rgb(0, 0, 0);")  # Set font color to black
        self.fake.setObjectName("fake")
        self.fake.setText(self.fake_text)
        self.fake.clicked.connect(partial(self.process_action, "fake"))

        self.tips = QtWidgets.QLabel(self.centralWidget)
        self.tips.setGeometry(QtCore.QRect(90, 340, 720, 91))
        self.tips.setFont(font)
        self.tips.setStyleSheet("color: rgb(0, 0, 0);")  # Set font color to black
        self.tips.setAlignment(QtCore.Qt.AlignCenter)
        self.tips.setObjectName("tips")
        self.tips.setText(self.key_instruction)

        self.progressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.progressBar.setGeometry(QtCore.QRect(220, 470, 451, 23))  # Adjusted position
        self.progressBar.setStyleSheet("color: rgb(0, 0, 0);")  # Set font color to black
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.setCentralWidget(self.centralWidget)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            self.process_action("real")
        if event.key() == QtCore.Qt.Key_Left:
            self.process_action("fake")

    def load_image(self):
        if self.language == 'zh':
            # Use QPixmap for PNG images
            path = f"languages/{self.language.upper()}/WikiVocab/ch_items/LEXTALE_CH_{self.stimuli['hash']}.png"
            pixmap = QPixmap(path)
            self.imageLabel.setPixmap(pixmap)
        else:
            # For SVG images
            path = f"{self.get_result_folder()}/images/{self.stimuli['hash']}.svg"
            self.imageLabel.load(QtCore.QByteArray(open(path, 'rb').read()))

    def process_action(self, answer) -> None:
        key_press_time = time.time()  # Capture the time when key is pressed
        reaction_time = key_press_time - self.stimulus_shown_time  # Calculate reaction time
        result = 1 if answer == "real" else 0
        self.result_df.loc[self.current_index, "real_answer"] = result
        self.result_df.loc[self.current_index, "RT"] = reaction_time  # Store reaction time
        try:
            self.stimuli = next(self.stimulies)
        except StopIteration:
            self._close()
        # Load the new image
        self.load_image()
        self.stimulus_shown_time = time.time()  # Capture the time for the new stimulus

    def prepare_data(self) -> None:
        self.data_df = pd.read_csv(f"tasks/WikiVocab/vocab/{self.language}.csv", encoding="utf-8")
        self.data_df = self.data_df.sample(NUM_OF_WORDS, ignore_index=True, replace=False)

        self.result_df = pd.DataFrame(
            columns=(
                "hash", "stimuli", "correct_answer", "real_answer", "RT", "language"  # Added RT column
            )
        )
        if self.language in ['ar', 'fa', 'ug', 'ur']:
            font_name = 'Noto Sans Arabic'
        elif self.language == "got":
            font_name = 'Noto Sans Gothic'
        elif self.language in ['he', 'yi']:
            font_name = 'Noto Sans Hebrew'
        elif self.language in ['hi', 'mr', 'sa']:
            font_name = 'Noto Sans Devanagari'
        elif self.language in ["hy", "hyw"]:
            font_name = 'Noto Sans Armenian'
        elif self.language == 'ja':
            font_name = 'Noto Sans JP'
        elif self.language == 'ko':
            font_name = 'Noto Sans KR Black'
        elif self.language == 'ta':
            font_name = 'Noto Sans Tamil'
        elif self.language == 'te':
            font_name = 'Noto Sans Telugu'
        # elif self.language == 'zh':
        #     font_name = 'Noto Sans SC Black'
        else:
            font_name = 'Arial Unicode MS'

        if self.language == 'zh':
            for _, row in self.data_df.iterrows():
                text = row.stimulus
                # hash the text to get a unique filename
                hash = text
                res = {
                    "hash": hash,
                    "stimuli": text,
                    "correct_answer": 1 if row.correct_answer == "correct" else 0,
                    "real_answer": -1,  # to make sure that it has been answered in future
                    "RT": None,  # Initialize RT with None
                    "language": self.language
                }
                self.result_df = self.result_df._append(
                    res,
                    ignore_index=True
                )
        else:
            for _, row in self.data_df.iterrows():
                text = row.stimulus
                # hash the text to get a unique filename
                hash = hashlib.md5(text.encode('utf-8')).hexdigest()
                res = {
                    "hash": hash,
                    "stimuli": text,
                    "correct_answer": 1 if row.correct_answer == "correct" else 0,
                    "real_answer": -1,  # to make sure that it has been answered in future
                    "RT": None,  # Initialize RT with None
                    "language": self.language
                }
                self.result_df = self.result_df._append(
                    res,
                    ignore_index=True
                )
                img_dir = f'{self.get_result_folder()}/images'
                os.makedirs(img_dir, exist_ok=True)
                img_name = f'{img_dir}/{hash}.svg'
                if self.language == 'ar':
                    text = arabic_reshaper.reshape(text)
                plot_text(bidialg.get_display(text), img_name, font_name)


    def get_result_folder(self) -> str:
        return self.result_folder

    def _get_stimuli(self):
        for index, raw in self.result_df.iterrows():
            self.current_index = index
            if self.current_index > 0:
                percent = int(self.current_index / NUM_OF_WORDS * 100)
                self.progressBar.setProperty("value", percent)
            yield raw

    def save_results(self) -> None:
        csv_name = f"{self.result_filename}.csv"
        self.result_df.to_csv(
            csv_name, index=False, encoding="utf-8"
        )

    def _close(self) -> None:
        self.save_results()
        self.result_window = MyResultWindow(
            name=self.name,
            result=self.prepared_results,
            language=self.language
        )
        self.result_window.show()
        self.close()

    @property
    def prepared_results(self) -> dict:
        self.result_df["is_right"] = (
            self.result_df["correct_answer"] == self.result_df["real_answer"]
        ).astype(int)
        incorrect_data = self.result_df[self.result_df["correct_answer"] == 0]
        correct_data = self.result_df[self.result_df["correct_answer"] == 1]
        result = {
            "total": round((self.result_df["is_right"] == 1).sum() / len(self.result_df), 2),
            "correct": round((correct_data["is_right"] == 1).sum() / len(correct_data), 2),
            "incorrect": round((incorrect_data["is_right"] == 1).sum() / len(incorrect_data), 2),
            "reaction_times": self.result_df["RT"].tolist()  # Add reaction times to the result
        }
        return result
