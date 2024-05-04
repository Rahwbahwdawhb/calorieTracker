from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                              QLabel, QPushButton, QScrollArea, QLineEdit,QRadioButton, QPlainTextEdit,
                              QSpacerItem,QSizePolicy,QListWidget,QListWidgetItem, QTableWidget, QTableWidgetItem,
                              QHeaderView,QAbstractScrollArea,QStackedLayout,QScrollBar)
from PyQt6.QtGui import QCloseEvent, QFont,QBrush,QColor,QTextCursor
from PyQt6.QtCore import Qt, QRect
from .aidFunctionality import *

quantityNames=['Calories [kcal]','Protein [g]','Carbohydrates [g]','Fat [g]','Fibers [g]']
class addFoodPanel(QWidget):
    def __init__(self):
        super().__init__()
        quantityLayout=QGridLayout()        
        self.nameEntry=searchField('Name:',0)
        quantityLayout.setContentsMargins(0,60,0,0)
        self.quantityLineEdits=[]
        for iter,qtn in enumerate(['Quantity [g]']+quantityNames):
            iterLabel=QLabel(qtn)
            iterLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            quantityLayout.addWidget(iterLabel,0,iter)
            loopLineEdit=QLineEdit()
            if iter==0:
                loopLineEdit.setText('100')
            else:
                loopLineEdit.setText('0')
            self.quantityLineEdits.append(loopLineEdit)
            quantityLayout.addWidget(loopLineEdit,1,iter)
            quantityLayout.setColumnStretch(iter,1)
        quantityLayout.setRowMinimumHeight(1,20)
        quantityLayout.setRowMinimumHeight(3,20)
        self.foodContainerScroll=searchField('Add to food container:',20) 
        topWrapLayout=QGridLayout()
        topWrapLayout.addLayout(quantityLayout,0,0,1,8)
        topWrapLayout.addLayout(self.nameEntry,0,0,1,8)
        
        self.notes=QPlainTextEdit()
        noteLayout=QGridLayout()
        noteLayout.setContentsMargins(0,45,0,0)
        noteLayout.addWidget(QLabel('Notes:'),0,0)
        noteLayout.addWidget(self.notes,1,0)
        self.addButton=QPushButton('Add')
        self.addButton.clicked.connect(self.addButtonAction)
        foodContainerLayout=QGridLayout()
        foodContainerLayout.addLayout(noteLayout,0,0,1,8)
        foodContainerLayout.addLayout(self.foodContainerScroll,0,0,1,8,alignment=Qt.AlignmentFlag.AlignTop)
        foodContainerLayout.addWidget(self.addButton,2,0,2,1)

        foodPanelLayout=QGridLayout()
        foodPanelLayout.addLayout(topWrapLayout,0,0)
        foodPanelLayout.addLayout(foodContainerLayout,1,0)
        foodPanelLayout.setRowStretch(0,1)
        foodPanelLayout.setRowStretch(1,3)
        
        self.setLayout(foodPanelLayout)
        self.hide()
    def addButtonAction(self):
        pass
    def populateFoodContainers(self):
        pass
    def populateFoods(self):
        pass