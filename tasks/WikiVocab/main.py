"""
This file is part of WikiVocab, a local PyQt6 implementation of VocabTest.

Based on the original VocabTest project: https://github.com/polvanrijn/VocabTest

Original Citation:
Pol van Rijn et al. (2023).
Around the world in 60 words: A generative vocabulary test for online research.

Copyright (C) 2024-2026 MultiplEYE Project
"""

import hashlib
import os
import time
from functools import partial

import arabic_reshaper
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
plt.rcParams['svg.fonttype'] = 'path'
import pandas as pd
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtWidgets import QMainWindow
from bidi import algorithm as bidialg

from result import MyResultWindow
from table_loader import load_table_file, resolve_table_file

# Maximum number is 63
NUM_OF_WORDS = 63
_INSTALLED_FONT_FAMILIES = None


def _get_installed_font_families():
    global _INSTALLED_FONT_FAMILIES
    if _INSTALLED_FONT_FAMILIES is None:
        _INSTALLED_FONT_FAMILIES = {font.name for font in fm.fontManager.ttflist}
    return _INSTALLED_FONT_FAMILIES


def _pick_first_installed(candidates):
    installed = _get_installed_font_families()
    for font_name in candidates:
        if font_name in installed:
            return font_name
    return "DejaVu Sans"


def get_font_for_language(language):
    language = str(language).lower()
    if language in {"ar", "fa", "fas", "ur", "ug"}:
        return _pick_first_installed([
            "Noto Naskh Arabic",
            "Noto Sans Arabic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ])
    if language in {"he", "yi"}:
        return _pick_first_installed([
            "Noto Sans Hebrew",
            "Arial Hebrew",
            "Arial Unicode MS",
            "DejaVu Sans",
        ])
    if language in {"hi", "mr", "sa"}:
        return _pick_first_installed([
            "Noto Sans Devanagari",
            "Kohinoor Devanagari",
            "Arial Unicode MS",
            "DejaVu Sans",
        ])
    if language in {"ja"}:
        return _pick_first_installed(["Noto Sans JP", "Hiragino Sans", "DejaVu Sans"])
    if language in {"ko"}:
        return _pick_first_installed(["Noto Sans KR", "Apple SD Gothic Neo", "DejaVu Sans"])
    if language in {"ta"}:
        return _pick_first_installed(["Noto Sans Tamil", "InaiMathi", "DejaVu Sans"])
    if language in {"te"}:
        return _pick_first_installed(["Noto Sans Telugu", "Arial Unicode MS", "DejaVu Sans"])
    return _pick_first_installed([
        "Arial Unicode MS",
        "Arial",
        "Helvetica Neue",
        "Liberation Sans",
        "DejaVu Sans",
    ])

def prepare_display_text(text, language):
    language = str(language).lower()
    arabic_script_langs = {'ar', 'fa', 'fas', 'ur', 'ug'}
    rtl_non_joining_langs = {'he', 'yi'}
    if language in arabic_script_langs:
        text = arabic_reshaper.reshape(text)
        text = bidialg.get_display(text)
    elif language in rtl_non_joining_langs:
        text = bidialg.get_display(text)
    return text


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
        super().__init__()
        self.name = name
        self.language = language
        self.result_folder = f'data/{result_folder}/WikiVocab/'
        self.result_filename = result_filename
        self.data_df = None
        self.result_df = None
        self.current_index = -1
        self.stimulus_shown_time = None  # To capture the time when stimulus is shown

        instructions_path = resolve_table_file(
            f'languages/{self.language.upper()}/instructions/WikiVocab_instructions_{self.language.lower()}',
            file_label='WikiVocab instructions file'
        )
        instructions_df = load_table_file(instructions_path, index_col='screen')
        key_instruction = instructions_df.loc['key_instruction', self.language.upper()]
        self.key_instruction = key_instruction.replace('\\n', '\n')
        self.real_text = instructions_df.loc['real_text', self.language.upper()]
        self.fake_text = instructions_df.loc['fake_text', self.language.upper()]

        self.initUI()

    def initUI(self) -> None:
        self.prepare_data()
        self.stimulies = self._get_stimuli()
        self.stimuli = next(self.stimulies)

        self.resize(1200, 800)
        # self.showFullScreen()
        self.setStyleSheet("background-color: rgb(221, 235, 255);")
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        # Define styles
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(20)
        font.setItalic(False)  # Set italic to False

        # Chinese stimuli are pre-rendered PNGs, others are generated SVGs.
        if self.language == 'zh':
            self.imageLabel = QtWidgets.QLabel(self.centralWidget)
            self.imageLabel.setFixedSize(471, 191)
            self.imageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        else:
            self.scene = QGraphicsScene(self.centralWidget)
            self.imageLabel = QGraphicsView(self.scene, self.centralWidget)
            self.imageLabel.setFixedSize(471, 191)

        self.imageLabel.setObjectName("imageLabel")
        self.load_image()
        self.stimulus_shown_time = time.time()  # Capture the time when stimulus is shown

        self.centralWidget.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        self.real = QtWidgets.QPushButton(self.centralWidget)
        self.real.setMinimumSize(250, 71)
        self.real.setFont(font)
        self.real.setStyleSheet("color: rgb(0, 0, 0);")  # Set font color to black
        self.real.setObjectName("real")
        self.real.setText(self.real_text)
        self.real.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.real.clicked.connect(partial(self.process_action, "real"))

        self.fake = QtWidgets.QPushButton(self.centralWidget)
        self.fake.setMinimumSize(250, 71)
        self.fake.setFont(font)
        self.fake.setAutoFillBackground(False)
        self.fake.setStyleSheet("color: rgb(0, 0, 0);")  # Set font color to black
        self.fake.setObjectName("fake")
        self.fake.setText(self.fake_text)
        self.fake.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.fake.clicked.connect(partial(self.process_action, "fake"))

        self.tips = QtWidgets.QLabel(self.centralWidget)
        self.tips.setFixedWidth(850)
        self.tips.setMinimumHeight(120)
        self.tips.setFont(font)
        self.tips.setStyleSheet("color: rgb(0, 0, 0);")  # Set font color to black
        self.tips.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tips.setWordWrap(True)
        self.tips.setObjectName("tips")
        self.tips.setText(self.key_instruction)

        self.progressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.progressBar.setFixedWidth(451)
        self.progressBar.setStyleSheet("color: rgb(0, 0, 0);")  # Set font color to black
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        # Layout-based positioning keeps content centered for any window size,
        # including full screen mode.
        main_layout = QtWidgets.QVBoxLayout(self.centralWidget)
        main_layout.setContentsMargins(80, 60, 80, 60)
        main_layout.addStretch(1)
        main_layout.addWidget(self.imageLabel, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(72)
        main_layout.addWidget(self.tips, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(56)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.fake)
        buttons_layout.addSpacing(240)
        buttons_layout.addWidget(self.real)
        buttons_layout.addStretch(1)
        main_layout.addLayout(buttons_layout)

        main_layout.addSpacing(28)
        main_layout.addWidget(self.progressBar, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch(3)

        self.setCentralWidget(self.centralWidget)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key.Key_Right or key == 16777236:  # Add Windows-specific key code
            self.real.animateClick()
        elif key == QtCore.Qt.Key.Key_Left or key == 16777234:  # Add Windows-specific key code
            self.fake.animateClick()

    def load_image(self):

        if self.language == 'zh':
            # Use QPixmap for PNG images
            path = f"languages/{self.language.upper()}/WikiVocab/ch_items/LEXTALE_CH_{self.stimuli['hash']}.png"
            pixmap = QPixmap(path)
            self.imageLabel.setPixmap(pixmap)
        else:
            path = f"{self.get_result_folder()}/images/{self.stimuli['hash']}.svg"
            svg_item = QGraphicsSvgItem(path)
            self.scene.clear()  # Clear the scene before adding a new item
            self.scene.addItem(svg_item)
            self.imageLabel.setScene(self.scene)

    def process_action(self, answer) -> None:
        key_press_time = time.time()
        reaction_time = key_press_time - self.stimulus_shown_time
        result = 1 if answer == "real" else 0
        self.result_df.loc[self.current_index, "real_answer"] = result
        self.result_df.loc[self.current_index, "RT"] = reaction_time
        try:
            self.stimuli = next(self.stimulies)
        except StopIteration:
            self._close()
        # Load the new image
        self.load_image()
        self.stimulus_shown_time = time.time()

    def prepare_data(self) -> None:
        vocab_path = resolve_table_file(
            f"tasks/WikiVocab/vocab/{self.language}",
            file_label=f"WikiVocab vocab file for language '{self.language}'"
        )
        self.data_df = load_table_file(vocab_path, encoding="utf-8")
        self.data_df = self.data_df.sample(NUM_OF_WORDS, ignore_index=True, replace=False)

        result_rows = []
        # Use a short fallback chain per script/language and a stable default.
        font_name = get_font_for_language(self.language)
        is_chinese = self.language == 'zh'
        img_dir = f'{self.get_result_folder()}/images'
        if not is_chinese:
            os.makedirs(img_dir, exist_ok=True)

        for _, row in self.data_df.iterrows():
            text = row.stimulus
            hash_value = text if is_chinese else hashlib.md5(text.encode('utf-8')).hexdigest()
            result_rows.append({
                "hash": hash_value,
                "stimuli": text,
                "correct_answer": 1 if row.correct_answer == "correct" else 0,
                "real_answer": -1,
                "RT": None,
                "language": self.language
            })

            if not is_chinese:
                img_name = f'{img_dir}/{hash_value}.svg'
                display_text = prepare_display_text(text, self.language)
                plot_text(display_text, img_name, font_name)

        self.result_df = pd.DataFrame(
            result_rows,
            columns=("hash", "stimuli", "correct_answer", "real_answer", "RT", "language")
        )

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
            "reaction_times": self.result_df["RT"].tolist()
        }
        return result
