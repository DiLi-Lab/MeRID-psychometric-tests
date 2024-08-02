from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
import pandas as pd


class MyResultWindow(QMainWindow):
    def __init__(self, name, result, language):
        super(MyResultWindow, self).__init__()
        self.name = name
        self.result = result
        self.language = language
        instructions_df = pd.read_excel(f'languages/{self.language.upper()}/instructions/WikiVocab_instructions_{self.language}.xlsx',
                                        index_col='screen')
        Goodbye_text = instructions_df.loc['Goodbye_text', self.language.upper()]
        self.Goodbye_text = Goodbye_text.replace('\\n', '\n')

        self.initUI()

    def initUI(self) -> None:
        self.resize(900, 600)
        # self.showFullScreen()
        self.setStyleSheet("background-color: rgb(221, 235, 255);")
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")

        # Define font settings
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)

        # Adjust QLabel to occupy the full width
        self.resultLabel = QtWidgets.QLabel(self.centralWidget)
        self.resultLabel.setGeometry(QtCore.QRect(0, 50, 900, 400))  # Adjusted to full width
        self.resultLabel.setFont(font)
        self.resultLabel.setStyleSheet("color: rgb(0, 0, 0);")
        self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)  # Center the text
        self.resultLabel.setObjectName("result")

        # Set the text with formatted result
        self.resultLabel.setText(self.Goodbye_text
                                 # + f"\n\nYour result - \n{self.format_result()}"
                                 )

        self.setCentralWidget(self.centralWidget)

    def format_result(self) -> str:
        return (
            f"Score with real words - {self.result['correct'] * 100}%\n"
            f"Score with fake words - {self.result['incorrect'] * 100}%\n"
            f"Total score - {self.result['total'] * 100}%\n"
        )

