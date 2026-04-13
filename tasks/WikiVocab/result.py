"""
This file is part of WikiVocab, a local PyQt6 implementation of VocabTest.

Based on the original VocabTest project: https://github.com/polvanrijn/VocabTest

Original Citation:
Pol van Rijn et al. (2023).
Around the world in 60 words: A generative vocabulary test for online research.

Copyright (C) 2024-2026 MultiplEYE Project
"""

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow

from table_loader import load_table_file, resolve_table_file


class MyResultWindow(QMainWindow):
    def __init__(self, name, result, language):
        super().__init__()
        self.name = name
        self.result = result
        self.language = language
        instructions_path = resolve_table_file(
            f'languages/{self.language.upper()}/instructions/WikiVocab_instructions_{self.language.lower()}',
            file_label='WikiVocab instructions file'
        )
        instructions_df = load_table_file(instructions_path, index_col='screen')
        goodbye_text = instructions_df.loc['Goodbye_text', self.language.upper()]
        self.goodbye_text = goodbye_text.replace('\\n', '\n')

        self.initUI()

    def initUI(self) -> None:
        self.resize(1200, 800)
        # self.showFullScreen()
        self.setStyleSheet("background-color: rgb(221, 235, 255);")
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")

        center_x = self.width() // 2
        center_y = self.height() // 2

        # Define font settings
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)

        # Adjust QLabel to occupy the full width
        self.resultLabel = QtWidgets.QLabel(self.centralWidget)
        self.resultLabel.setGeometry(QtCore.QRect(center_x - 500, 50, 1000, 400))  # Adjusted to full width
        self.resultLabel.setFont(font)
        self.resultLabel.setStyleSheet("color: rgb(0, 0, 0);")
        self.resultLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.resultLabel.setObjectName("result")

        # Set the text with formatted result
        self.resultLabel.setText(self.goodbye_text
                                 # + f"\n\nYour result - \n{self.format_result()}"
                                 )

        self.setCentralWidget(self.centralWidget)

    def format_result(self) -> str:
        return (
            f"Score with real words - {self.result['correct'] * 100}%\n"
            f"Score with fake words - {self.result['incorrect'] * 100}%\n"
            f"Total score - {self.result['total'] * 100}%\n"
        )
