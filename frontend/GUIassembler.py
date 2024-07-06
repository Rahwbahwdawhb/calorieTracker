from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                              QLabel, QPushButton, QScrollArea, QLineEdit,QRadioButton, QPlainTextEdit,
                              QSpacerItem,QSizePolicy,QListWidget,QListWidgetItem, QTableWidget, QTableWidgetItem,
                              QHeaderView,QAbstractScrollArea,QStackedLayout,QScrollBar)
from PyQt6.QtGui import QCloseEvent, QFont,QBrush,QColor,QTextCursor
from PyQt6.QtCore import Qt, QRect
from .aidFunctionality import *
from .foodContainerPanel import *
from .addFoodPanel import *
from .mixFoodPanel import *


class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400,300)
        self.show()
        mainLayout=QGridLayout()
        self.setLayout(mainLayout)

        self.addFoodPanel=addFoodPanel()
        self.mixFoodPanel=mixFoodPanel()
        self.foodContainerPanel=foodContainerPanel()

        self.addFoodButton=QPushButton('Add food')
        self.addFoodButton.clicked.connect(self.panelToggler)
        self.mixFoodButton=QPushButton('Mix foods')
        self.mixFoodButton.clicked.connect(self.panelToggler)
        self.foodContainerButton=QPushButton('Food containers')
        self.foodContainerButton.clicked.connect(self.panelToggler)
        buttonLayout=QVBoxLayout()
        buttonLayout.addWidget(self.addFoodButton)
        buttonLayout.addWidget(self.mixFoodButton)
        buttonLayout.addWidget(self.foodContainerButton)

        mainLayout.addLayout(buttonLayout,0,0,1,1)
        mainLayout.addWidget(self.addFoodPanel,0,1,3,3)
        mainLayout.addWidget(self.mixFoodPanel,0,1,3,3)
        mainLayout.addWidget(self.foodContainerPanel,0,1,3,3)
        mainLayout.setColumnStretch(0,1)
        mainLayout.setColumnStretch(1,3)

    def closeEvent(self, a0: QCloseEvent):
        self.additionalCloseEvents()
        return super().closeEvent(a0)
    def additionalCloseEvents(self):
        pass
    def foodContainerPanelUpdate(self):
        pass
    def panelToggler(self):
        if self.sender()==self.addFoodButton:
            self.addFoodPanel.show()
            self.addFoodPanel.populateFoodContainers()
            self.addFoodPanel.populateFoods()
            self.addFoodPanel.addFoodActivation()
            self.mixFoodPanel.hide()
            self.foodContainerPanel.hide()
        elif self.sender()==self.mixFoodButton:
            self.addFoodPanel.hide()
            self.mixFoodPanel.show()
            self.mixFoodPanel.populateFoodContainers()
            self.mixFoodPanel.populateFoods()
            self.foodContainerPanel.hide()
        else:
            self.addFoodPanel.hide()
            self.mixFoodPanel.hide()
            self.foodContainerPanel.show()
            self.foodContainerPanelUpdate()

class frontendSetup(QApplication):
    def __init__(self):
        super().__init__([])
        self.setApplicationName('Calorie Tracker')
        self.mW=mainWindow()
    def startGUI(self):
        self.mW
        self.exec()

if __name__=='__main__':
    app=frontendSetup()
    app.startGUI()


