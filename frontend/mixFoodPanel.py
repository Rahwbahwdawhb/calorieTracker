from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                              QLabel, QPushButton, QScrollArea, QLineEdit,QRadioButton, QPlainTextEdit,
                              QSpacerItem,QSizePolicy,QListWidget,QListWidgetItem, QTableWidget, QTableWidgetItem,
                              QHeaderView,QAbstractScrollArea,QStackedLayout,QScrollBar,QSpacerItem)
from PyQt6.QtGui import QCloseEvent, QFont,QBrush,QColor,QTextCursor
from PyQt6.QtCore import Qt, QRect
try:
    from .aidFunctionality import *
except:
    from aidFunctionality import *

quantityNames=['Quantity [g]','Calories [kcal]','Protein [g]','Carbohydrates [g]','Fat [g]','Fibers [g]']
ingridientInfo=['Name','Qty [g]','Cal. [kcal]','Protein [g]','Carbs [g]','Fat [g]','Fibers [g]']
class mixFoodPanel(QWidget):
    def __init__(self):
        super().__init__()

        quantityLayout=QGridLayout()        
        self.nameEntry=searchField('Name:',0)
        quantityLayout.setContentsMargins(0,30,0,0)
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
        quantityLayout.addWidget(QLabel(),2,0)
        quantityLayout.setRowStretch(0,1)
        quantityLayout.setRowStretch(1,1)
        quantityLayout.setRowStretch(2,10)        

        topWrapLayout=QGridLayout()
        
        ingridientLabel=QLabel('Ingridients')
        ingridientLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingridientScroll=returnDeleteDetectQTableWidget()
        self.ingridientScroll.setSortingEnabled(True)
        self.ingridientScroll.verticalHeader().setVisible(False)
        self.ingridientScroll.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.ingridientScroll.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ingridientScroll.setColumnCount(len(ingridientInfo))
        self.ingridientScroll.setHorizontalHeaderLabels(ingridientInfo)
        self.ingridientScroll.returnReleaseAction=self.quantityUpdated
        self.ingridientScroll.returnPressAction=self.quantityEntered
        self.ingridientScroll.deleteReleaseAction=self.deleteIngridient
        self.ingridientScroll.setMinimumHeight(135)
        
        ingridientScrollLayout=QGridLayout()
        ingridientScrollLayout.addWidget(ingridientLabel,1,0)
        ingridientScrollLayout.addWidget(self.ingridientScroll,2,0)
        ingridientScrollLayout.setRowMinimumHeight(0,80)
        topWrapLayout.addLayout(ingridientScrollLayout,0,0,1,8)
        topWrapLayout.addLayout(quantityLayout,0,0,1,8)
        topWrapLayout.addLayout(self.nameEntry,0,0,1,8)

        self.ingridientEntry=searchField('Ingridient:',25)
        self.ingridientQuantityEntry=QLineEdit()
        self.ingridientEntry.addWidget(QLabel('Quantity [g]:'),1,2)
        self.ingridientEntry.addWidget(self.ingridientQuantityEntry,1,3)
        self.addIngridientButton=QPushButton('Add')
        self.addIngridientButton.clicked.connect(self.addIngridient)
        self.ingridientEntry.addWidget(self.addIngridientButton,1,4)
        self.ingridientEntry.setColumnStretch(0,1)
        self.ingridientEntry.setColumnStretch(1,2)
        self.ingridientEntry.setColumnStretch(2,1)
        self.ingridientEntry.setColumnStretch(3,1)
        self.ingridientEntry.setColumnStretch(4,1)

        self.foodContainerScroll=searchField('Save to food container:',350,dropDownAbove=True)
        self.saveToFoodContainerButton=QPushButton('Save')
        self.saveToFoodContainerButton.clicked.connect(self.addMixedFoodToFoodContainer)
        # foodContainerLayout=QGridLayout()
        self.foodContainerScroll.addWidget(self.saveToFoodContainerButton,2,2)
        # self.foodContainerScroll.setRowMinimumHeight(0,50)
        # foodContainerLayout.addLayout(self.foodContainerScroll,0,0)
        # foodContainerLayout.addWidget(self.saveToFoodContainerButton,0,1)

        self.noteArea=PlainTextEdit(self,emptyStr='Notes')
        noteAreaLayout=QGridLayout()
        noteAreaLayout.addWidget(self.noteArea,1,0)
        noteAreaLayout.setRowMinimumHeight(0,50)
        noteAreaLayout.addWidget(QLabel(),2,0)
        # noteAreaLayout.addLayout(self.foodContainerScroll,2,0)
        # noteAreaLayout.setRowMinimumHeight(1,0)
        noteAreaLayout.setRowStretch(0,2)
        noteAreaLayout.setRowStretch(1,5)
        noteAreaLayout.setRowStretch(2,1)

        addLayout=QGridLayout()        
        addLayout.addLayout(noteAreaLayout,0,0,1,8)
        addLayout.addLayout(self.ingridientEntry,0,0,1,8) 
        addLayout.addLayout(self.foodContainerScroll,0,0,1,8)
        

        # self.addWidget=QWidget()
        # self.addWidget.setLayout(addLayout)

        # self.noteArea=QPlainTextEdit()
        # self.addNoteButton=QLabel()
        # # self.addNoteButton.clicked.connect(self.addButtonAction)
        # noteLayout=QGridLayout()
        # noteLayout.addWidget(self.noteArea,1,0,1,8)
        # noteLayout.addWidget(self.addNoteButton,2,0,2,1)
        # noteLayout.setContentsMargins(0,0,0,0)
        # self.noteWidget=QWidget()
        # self.noteWidget.setLayout(noteLayout)

        # self.rbAddIngridient=QRadioButton('Add ingridient')        
        # self.rbAddIngridient.clicked.connect(self.toggleAddSubPanel)
        # self.rbAddNote=QRadioButton('Add note')
        # self.rbAddNote.clicked.connect(self.toggleAddSubPanel)
        # # self.rbAddToFoodContainer=QRadioButton('Add to food container')
        # # self.rbAddToFoodContainer.clicked.connect(self.toggleAddSubPanel)
        # self.rbAddIngridient.click()
        # rbLayout=QHBoxLayout()
        # rbLayout.addWidget(self.rbAddIngridient)
        # rbLayout.addWidget(self.rbAddNote)
        # # rbLayout.addWidget(self.rbAddToFoodContainer)
        # rbLayout.setStretch(0,3)
        # rbLayout.setStretch(1,2)
        # rbLayout.setStretch(2,1)

        # mixPanelLayout=QVBoxLayout()
        # tw=QWidget()
        # tw.setLayout(topWrapLayout)
        # mixPanelLayout.addWidget(tw)
        # aw=QWidget()
        # aw.setLayout(addLayout)
        # mixPanelLayout.addWidget(aw)
        # mixPanelLayout.setStretchFactor(topWrapLayout,10)
        # mixPanelLayout.setStretchFactor(addLayout,1)

        mixPanelLayout=QGridLayout()
        mixPanelLayout.addLayout(topWrapLayout,0,0)
        # mixPanelLayout.addLayout(ingridientScrollLayout,1,0)
        # bottomWrapLayout=QGridLayout()
        # bottomWrapLayout.setRowMinimumHeight(0,100)
        # bottomWrapLayout.addLayout(rbLayout,0,0,1,8)
        # bottomWrapLayout.addWidget(addLayout,1,0,2,8)
        # bottomWrapLayout.addWidget(self.foodContainerWidget,1,0,2,8) 
        # bottomWrapLayout.addWidget(self.noteWidget,1,0,2,8)
        # mixPanelLayout.addLayout(addLayout,1,0)
        mixPanelLayout.addLayout(addLayout,1,0)
        mixPanelLayout.setRowStretch(0,10)
        mixPanelLayout.setRowStretch(1,1)
        # mixPanelLayout.setRowStretch(2,1)
        # mixPanelLayout.setRowStretch(3,1)
        # mixPanelLayout.setRowStretch(4,1)
        
        self.setLayout(mixPanelLayout)

        self.hide()
    def toggleAddSubPanel(self):
        if self.sender()==self.rbAddIngridient:
            self.addWidget.show()
            # self.foodContainerWidget.hide()
            self.noteWidget.hide()
        # elif self.sender()==self.rbAddToFoodContainer:
        #     self.ingridientWidget.hide()
        #     self.foodContainerWidget.show()
        #     self.noteWidget.hide()
        else:
            self.addWidget.hide()
            # self.foodContainerWidget.hide()
            self.noteWidget.show()
    def addButtonAction(self):
        pass
    def populateFoodContainers(self):
        pass
    def populateFoods(self):
        pass
    def addIngridient(self):
        pass
    def quantityUpdated(self):
        pass
    def quantityEntered(self):
        pass
    def deleteIngridient(self):
        pass
    def addMixedFoodToFoodContainer(self):
        pass