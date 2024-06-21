from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                              QLabel, QPushButton, QScrollArea, QLineEdit,QRadioButton, QPlainTextEdit,
                              QSpacerItem,QSizePolicy,QListWidget,QListWidgetItem, QTableWidget, QTableWidgetItem,
                              QHeaderView,QAbstractScrollArea,QStackedLayout,QScrollBar)
from PyQt6.QtGui import QCloseEvent, QFont,QBrush,QColor,QTextCursor
from PyQt6.QtCore import Qt, QRect
from .aidFunctionality import *

quantityNames=['Quantity [g]','Calories [kcal]','Protein [g]','Carbohydrates [g]','Fat [g]','Fibers [g]']

class mixFoodPanel(QWidget):
    def __init__(self):
        super().__init__()

        quantityLayout=QGridLayout()        
        self.nameEntry=searchField('Name:',0)
        quantityLayout.setContentsMargins(0,60,0,0)
        self.quantityStatLabels=[]
        for iter,qtn in enumerate(quantityNames):
            iterLabel=QLabel(qtn)
            iterLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            quantityLayout.addWidget(iterLabel,0,iter)
            quantity=QLabel('0')
            quantity.setAlignment(Qt.AlignmentFlag.AlignCenter)
            quantityLayout.addWidget(quantity,1,iter)
            self.quantityStatLabels.append(quantity)
            quantityLayout.setColumnStretch(iter,1)
        quantityLayout.setRowMinimumHeight(1,20)
        quantityLayout.setRowMinimumHeight(3,30)

        topWrapLayout=QGridLayout()
        topWrapLayout.addLayout(quantityLayout,0,0,1,8)
        topWrapLayout.addLayout(self.nameEntry,0,0,1,8)

        ingridientLabel=QLabel('Ingridients')
        ingridientLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingridientScroll=QScrollArea()
        ingridientScrollLayout=QVBoxLayout()
        ingridientScrollLayout.addWidget(ingridientLabel)
        ingridientScrollLayout.addWidget(self.ingridientScroll)

        self.ingridientAddScroll=searchField('Add ingridient:',0)
        self.addIngridientButton=QPushButton('Add')
        ingridientLayout=QGridLayout()
        ingridientLayout.addLayout(self.ingridientAddScroll,0,0,1,8)
        ingridientLayout.addWidget(self.addIngridientButton,1,0,2,1)
        ingridientLayout.setContentsMargins(0,0,0,0)
        self.ingridientWidget=QWidget()
        self.ingridientWidget.setLayout(ingridientLayout)

        self.foodContainerScroll=searchField('Add to food container:',0)        
        self.addToFoodContainerButton=QPushButton('Add')
        foodContainerLayout=QGridLayout()
        foodContainerLayout.addLayout(self.foodContainerScroll,0,0,1,8)
        foodContainerLayout.addWidget(self.addToFoodContainerButton,1,0,2,1)
        foodContainerLayout.setContentsMargins(0,0,0,0)
        self.foodContainerWidget=QWidget()
        self.foodContainerWidget.setLayout(foodContainerLayout)

        self.noteArea=QPlainTextEdit()
        self.addNoteButton=QPushButton('Add')
        noteLayout=QGridLayout()
        noteLayout.addWidget(self.noteArea,1,0,1,8)
        noteLayout.addWidget(self.addNoteButton,2,0,2,1)
        noteLayout.setContentsMargins(0,0,0,0)
        self.noteWidget=QWidget()
        self.noteWidget.setLayout(noteLayout)

        self.rbAddIngridient=QRadioButton('Add ingridient')        
        self.rbAddIngridient.clicked.connect(self.toggleAddSubPanel)
        self.rbAddNote=QRadioButton('Add note')
        self.rbAddNote.clicked.connect(self.toggleAddSubPanel)
        self.rbAddToFoodContainer=QRadioButton('Add to food container')
        self.rbAddToFoodContainer.clicked.connect(self.toggleAddSubPanel)
        self.rbAddIngridient.click()
        rbLayout=QHBoxLayout()
        rbLayout.addWidget(self.rbAddIngridient)
        rbLayout.addWidget(self.rbAddNote)
        rbLayout.addWidget(self.rbAddToFoodContainer)
        rbLayout.setStretch(0,3)
        rbLayout.setStretch(1,2)
        rbLayout.setStretch(2,1)

        mixPanelLayout=QGridLayout()
        mixPanelLayout.addLayout(topWrapLayout,0,0)
        mixPanelLayout.addLayout(ingridientScrollLayout,1,0)
        bottomWrapLayout=QGridLayout()
        bottomWrapLayout.addLayout(rbLayout,0,0,1,8)
        bottomWrapLayout.addWidget(self.ingridientWidget,1,0,2,8)
        bottomWrapLayout.addWidget(self.foodContainerWidget,1,0,2,8) 
        bottomWrapLayout.addWidget(self.noteWidget,1,0,2,8)
        mixPanelLayout.addLayout(bottomWrapLayout,2,0)
        mixPanelLayout.setRowStretch(0,2)
        mixPanelLayout.setRowStretch(1,2)
        mixPanelLayout.setRowStretch(2,3)
        
        self.setLayout(mixPanelLayout)

        self.hide()
    def toggleAddSubPanel(self):
        if self.sender()==self.rbAddIngridient:
            self.ingridientWidget.show()
            self.foodContainerWidget.hide()
            self.noteWidget.hide()
        elif self.sender()==self.rbAddToFoodContainer:
            self.ingridientWidget.hide()
            self.foodContainerWidget.show()
            self.noteWidget.hide()
        else:
            self.ingridientWidget.hide()
            self.foodContainerWidget.hide()
            self.noteWidget.show()