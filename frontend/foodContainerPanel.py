from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                              QLabel, QPushButton, QScrollArea, QLineEdit,QRadioButton, QPlainTextEdit,
                              QSpacerItem,QSizePolicy,QListWidget,QListWidgetItem, QTableWidget, QTableWidgetItem,
                              QHeaderView,QAbstractScrollArea,QStackedLayout,QScrollBar)
from PyQt6.QtGui import QCloseEvent, QFont,QBrush,QColor,QTextCursor
from PyQt6.QtCore import Qt, QRect
from .aidFunctionality import *

quantityNames=['Calories [kcal]','Protein [g]','Carbohydrates [g]','Fat [g]','Fibers [g]']
class foodContainerPanel(QWidget):
    def __init__(self):
        super().__init__()
        foodContainerLayout=QGridLayout()      
        existingLayout=QVBoxLayout()
        existingLayout.addWidget(QLabel('Existing food containers:'))
        self.extScroll=QListWidget()
        existingLayout.addWidget(self.extScroll)
        foodContainerLayout.addLayout(existingLayout,0,0,5,4)

        self.searchField=modQLineEdit()
        self.searchField.additionalKeyPressEvent=self.additionalKeyPressEvent
        self.createButton=QPushButton('Create')
        self.createButton.setDisabled(True)
        self.createButton.clicked.connect(self.createFC)
        nameLayout=QHBoxLayout()
        nameLayout.addWidget(QLabel('Search:'))
        nameLayout.addWidget(self.searchField)
        nameLayout.addWidget(self.createButton)
        foodContainerLayout.addLayout(nameLayout,5,0,1,4)           
        
        self.foodDisplayPanel=foodDisplayPanel()
        self.foodDisplayPanel.foodListHolder.closeButton.clicked.connect(self.closeFoodDisplayPanel)
        self.foodDisplayPanel.foodItemHolder.closeButton.clicked.connect(self.closeFoodDisplayPanel)
        self.foodDisplayPanel.foodMixHolder.closeButton.clicked.connect(self.closeFoodDisplayPanel)

        foodContainerLayoutContainer=QWidget()
        foodContainerLayoutContainer.setLayout(foodContainerLayout)
        self.stackLayout=QStackedLayout()
        self.stackLayout.addWidget(foodContainerLayoutContainer)
        self.stackLayout.addWidget(self.foodDisplayPanel)
        self.setLayout(self.stackLayout)
        self.hide()
    def additionalKeyPressEvent(self):
        matchingItems=0
        self.createButton.setDisabled(True)
        for i in range(self.extScroll.count()):
            if self.searchField.text() not in self.extScroll.item(i).text():
                self.extScroll.item(i).setHidden(True)
            else:
                self.extScroll.item(i).setHidden(False) 
                matchingItems+=1            
        if matchingItems==0:
            self.createButton.setDisabled(False)
    def addExtFCtoScroll(self,itemStr):
        self.extScroll.addItem(QListWidgetItem(itemStr))
    def extFCclicked_set(self):
        self.extScroll.itemClicked.connect(self.extFCclicked_external)
    def extFCclicked_external(self):
        pass
    def closeFoodDisplayPanel(self):
        self.stackLayout.setCurrentIndex(0)
        self.closeDisplayPanel_external()
    def closeDisplayPanel_external(self):
        pass
    def createFC(self):
        pass

class displayWidgetCreator(QWidget):
    def __init__(self,displayType):
        super().__init__()
        displayLayout=QGridLayout()
        self.hierarcyScroll=QListWidget()
        hierarcyLayout=QVBoxLayout()
        hierarcyLayout.addWidget(QLabel('Hierarcy:'))
        hierarcyLayout.addWidget(self.hierarcyScroll)
        self.closeButton=QPushButton('Food container list')    
        self.displayLabel=QLabel('')    
        displayLayout.addWidget(self.displayLabel,0,2)    
        self.deleteButton=QPushButton('Delete')        
        displayLayout.addWidget(self.deleteButton,0,3)   
        match displayType:
            case 'foodContainer':
                self.constituentList=QTableWidget(self)
                # self.constituentList.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
                self.constituentList.setSortingEnabled(True)
                self.constituentList.verticalHeader().setVisible(False)
                self.constituentList.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
                self.constituentList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                displayLayout.addLayout(hierarcyLayout,1,0,1,4)
                constituentListLayout=QVBoxLayout()
                constituentListLayout.addWidget(QLabel('Foods:'))
                constituentListLayout.addWidget(self.constituentList)
                displayLayout.addLayout(constituentListLayout,2,0,8,4)
                displayLayout.addWidget(self.closeButton,10,0)
            case 'foodMix':
                self.constituentList=QTableWidget(self)
                # self.constituentList.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
                self.constituentList.setSortingEnabled(True)
                self.constituentList.verticalHeader().setVisible(False)
                self.constituentList.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
                self.constituentList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

                self.ingridientList=QTableWidget()
                self.ingridientList.setSortingEnabled(True)
                self.ingridientList.verticalHeader().setVisible(False)
                self.ingridientList.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
                self.ingridientList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

                qtyLabelNames=['Quantity [g]']+[qtyN for qtyN in quantityNames]
                qtyLayout=QGridLayout()
                self.qtyLineEdits=[]
                for i,qtl in enumerate(qtyLabelNames):
                    qtyLayout.addWidget(QLabel(qtl),0,i)
                    qle_i=QLabel()
                    self.qtyLineEdits.append(qle_i)
                    qtyLayout.addWidget(qle_i,1,i)                    
                displayLayout.addLayout(qtyLayout,1,0,1,4)
                displayLayout.addLayout(hierarcyLayout,2,0,1,4)
                self.noteArea=PlainTextEdit(self)

                radioButtonLayout=QHBoxLayout()
                constituentRB=QRadioButton('Constituents:')
                notesRB=QRadioButton('Notes:')
                ingridientInRB=QRadioButton('Ingridient in:')                
                radioButtonLayout.addWidget(constituentRB)
                radioButtonLayout.addWidget(notesRB)
                radioButtonLayout.addWidget(ingridientInRB)
                self.radioButtonList=[constituentRB,notesRB,ingridientInRB]  
                constituentRB.clicked.connect(self.radioButtonToggle)              
                notesRB.clicked.connect(self.radioButtonToggle)              
                ingridientInRB.clicked.connect(self.radioButtonToggle)              

                self.stackLayout=QStackedLayout()
                self.stackLayout.addWidget(self.constituentList)
                self.stackLayout.addWidget(self.noteArea)
                self.stackLayout.addWidget(self.ingridientList)

                constituentRB.clicked.connect(self.radioButtonToggle)
                constituentRB.click()

                # constituentListLayout=QVBoxLayout()
                # constituentListLayout.addWidget(QLabel('Constituents:'))
                # constituentListLayout.addWidget(self.stackLayout)
                
                displayLayout.addLayout(radioButtonLayout,3,0,1,4)
                displayLayout.addLayout(self.stackLayout,4,0,6,4)
                displayLayout.addWidget(self.closeButton,10,0)
            case 'foodItem':
                qtyLabelNames=['Quantity [g]']+[qtyN for qtyN in quantityNames]
                qtyLayout=QGridLayout()
                self.qtyLineEdits=[]
                for i,qtl in enumerate(qtyLabelNames):
                    qtyLayout.addWidget(QLabel(qtl),0,i)
                    qle_i=QLineEdit()
                    self.qtyLineEdits.append(qle_i)
                    qtyLayout.addWidget(qle_i,1,i)                    
                displayLayout.addLayout(qtyLayout,1,0,1,4)
                displayLayout.addLayout(hierarcyLayout,2,0,1,4)
                # self.noteArea=QPlainTextEdit()
                self.noteArea=PlainTextEdit(self)                                       
                # noteAreaLayout=QVBoxLayout()
                # noteAreaLayout.addWidget(self.noteArea)
                # noteAreaLayout.setContentsMargins(0,0,0,0)
                self.ingridientList=QTableWidget()
                self.ingridientList.setSortingEnabled(True)
                self.ingridientList.verticalHeader().setVisible(False)
                self.ingridientList.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
                self.ingridientList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                # noteAreaWidet=QWidget()
                # noteAreaWidet.setLayout(noteAreaLayout)
                self.stackLayout=QStackedLayout()
                self.stackLayout.addWidget(self.noteArea)
                self.stackLayout.addWidget(self.ingridientList)
                radioButtonLayout=QHBoxLayout()
                noteRB=QRadioButton('Notes')
                ingridientsRB=QRadioButton('Ingridient in')
                self.radioButtonList=[noteRB,ingridientsRB]
                noteRB.clicked.connect(self.radioButtonToggle)
                noteRB.click()
                ingridientsRB.clicked.connect(self.radioButtonToggle)
                radioButtonLayout.addWidget(noteRB)
                radioButtonLayout.addWidget(ingridientsRB)
                displayLayout.addLayout(radioButtonLayout,3,0,1,4)
                displayLayout.addLayout(self.stackLayout,4,0,6,4)
                displayLayout.addWidget(self.closeButton,10,0)
        for i in range(11):
            displayLayout.setRowStretch(i,1)
        displayLayout.setContentsMargins(0,0,0,0)
        self.setLayout(displayLayout)
    def radioButtonToggle(self):
        self.stackLayout.setCurrentIndex(self.radioButtonList.index(self.sender()))
    
class foodDisplayPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.foodDisplayLayout=QStackedLayout()
        self.foodListHolder=displayWidgetCreator('foodContainer')        
        self.foodListHolder.hierarcyScroll.itemClicked.connect(self.hierarcyClick_external)  
        self.foodListHolder.deleteButton.clicked.connect(self.deleteButtonAction)    
        self.foodMixHolder=displayWidgetCreator('foodMix')        
        self.foodMixHolder.hierarcyScroll.itemClicked.connect(self.hierarcyClick_external)
        self.foodMixHolder.deleteButton.clicked.connect(self.deleteButtonAction)          
        self.foodItemHolder=displayWidgetCreator('foodItem')
        self.foodItemHolder.hierarcyScroll.itemClicked.connect(self.hierarcyClick_external)  
        self.foodItemHolder.deleteButton.clicked.connect(self.deleteButtonAction)    

        self.foodListHolder.constituentList.itemClicked.connect(self.tableItemClick_external)
        self.foodMixHolder.constituentList.itemClicked.connect(self.tableItemClick_external)
        self.foodMixHolder.ingridientList.itemClicked.connect(self.tableItemClick_external)
        self.foodItemHolder.ingridientList.itemClicked.connect(self.tableItemClick_external)      

        self.foodDisplayLayout.addWidget(self.foodListHolder)
        self.foodDisplayLayout.addWidget(self.foodMixHolder)
        self.foodDisplayLayout.addWidget(self.foodItemHolder)
        self.setLayout(self.foodDisplayLayout)
        self.foodDisplayLayout.setCurrentIndex(0)
        self.activeDisplayType='foodContainer'    
        self.panelTitle=''
    def populatePanel(self,dataList,headers,panelTitle,displayType,clickList,notes='',dataList2=[],dataList3=[]):
        self.panelTitle=panelTitle
        self.clickList=clickList
        self.activeDisplayType=displayType
        q=QFont()
        q.setBold(True)
        match displayType:
            case 'foodContainer':
                self.foodDisplayLayout.setCurrentIndex(0)
                self.foodListHolder.constituentList.setRowCount(0)
                self.foodListHolder.constituentList.setColumnCount(0)
                self.foodListHolder.constituentList.setRowCount(len(dataList))
                self.foodListHolder.constituentList.setColumnCount(len(headers))
                self.foodListHolder.constituentList.setColumnHidden(len(headers)-1,True)
                self.foodListHolder.displayLabel.setText(panelTitle)
                
                self.foodListHolder.hierarcyScroll.clear()
                for prior in clickList[0:-1]:
                    self.foodListHolder.hierarcyScroll.addItem(QListWidgetItem(prior))
                endItem=QListWidgetItem(clickList[-1])
                endItem.setFont(q)
                self.foodListHolder.hierarcyScroll.addItem(endItem)
                self.foodListHolder.hierarcyScroll.scrollToBottom()
                self.populateQTableWidget(dataList,self.foodListHolder.constituentList,headers)                
            case 'foodMix':
                self.foodDisplayLayout.setCurrentIndex(1)
                self.foodMixHolder.displayLabel.setText(panelTitle)
                self.foodMixHolder.noteArea.setPlainText(notes.replace('\\','\n'))

                self.foodMixHolder.constituentList.setRowCount(0)
                self.foodMixHolder.constituentList.setColumnCount(0)
                self.foodMixHolder.constituentList.setRowCount(len(dataList))
                self.foodMixHolder.constituentList.setColumnCount(len(headers))
                self.foodMixHolder.constituentList.setColumnHidden(len(headers)-1,True)
                self.foodMixHolder.displayLabel.setText(panelTitle)

                self.foodMixHolder.hierarcyScroll.clear()
                for prior in clickList[0:-1]:
                    self.foodMixHolder.hierarcyScroll.addItem(QListWidgetItem(prior))
                endItem=QListWidgetItem(clickList[-1])
                endItem.setFont(q)
                self.foodMixHolder.hierarcyScroll.addItem(endItem)
                self.foodMixHolder.hierarcyScroll.scrollToBottom()
                for i,subList in enumerate(dataList):
                    for ii,item in enumerate(subList):
                        listItem=QTableWidgetItem(item)
                        listItem.setFlags(Qt.ItemFlag.NoItemFlags)
                        listItem.setForeground(QColor(0,0,0))
                        self.foodMixHolder.constituentList.setItem(i,ii,listItem)
                self.foodMixHolder.constituentList.setHorizontalHeaderLabels(headers)

                self.foodMixHolder.ingridientList.setRowCount(0)
                self.foodMixHolder.ingridientList.setColumnCount(0)
                self.foodMixHolder.ingridientList.setRowCount(len(dataList3))
                self.foodMixHolder.ingridientList.setColumnCount(len(headers))
                self.foodMixHolder.ingridientList.setColumnHidden(len(headers)-1,True)
                self.populateQTableWidget(dataList3,self.foodMixHolder.ingridientList,headers)
                for i,qle in enumerate(self.foodMixHolder.qtyLineEdits):
                    qle.setText(str(round(dataList2[i],2)))
            case 'foodItem':
                self.foodDisplayLayout.setCurrentIndex(2)
                self.foodItemHolder.displayLabel.setText(panelTitle)
                self.foodItemHolder.noteArea.setPlainText(notes.replace('\\','\n'))

                self.foodItemHolder.hierarcyScroll.clear()
                for prior in clickList[0:-1]:
                    self.foodItemHolder.hierarcyScroll.addItem(QListWidgetItem(prior))
                endItem=QListWidgetItem(clickList[-1])
                endItem.setFont(q)
                self.foodItemHolder.hierarcyScroll.addItem(endItem)
                self.foodItemHolder.hierarcyScroll.scrollToBottom()

                self.foodItemHolder.ingridientList.setRowCount(0)
                self.foodItemHolder.ingridientList.setColumnCount(0)
                self.foodItemHolder.ingridientList.setRowCount(len(dataList2))
                self.foodItemHolder.ingridientList.setColumnCount(len(headers))
                self.foodItemHolder.ingridientList.setColumnHidden(len(headers)-1,True)
                self.populateQTableWidget(dataList2,self.foodItemHolder.ingridientList,headers)

                for i,qle in enumerate(self.foodItemHolder.qtyLineEdits):
                    qle.setText(str(dataList[i]))
                    qle.returnPressed.connect(self.foodItemEdits)
                self.foodItemHolder.noteArea.additionalKeyPressEvent=self.foodItemNoteKeyPressEvent
    def populateQTableWidget(self,dataList,tableWidget,headers):
        if len(dataList)!=0:
            for i,subList in enumerate(dataList):
                for ii,item in enumerate(subList):
                    if ii>0 and ii<7:
                        item=str(round(float(item),2))
                    listItem=QTableWidgetItem(item)
                    tableWidget.setItem(i,ii,listItem)
                    listItem.setFlags(Qt.ItemFlag.NoItemFlags)
                    listItem.setForeground(QColor(0,0,0))
        else:
            for i,_ in enumerate(headers):
                tableWidget.setItem(0,i,QTableWidgetItem(''))
        tableWidget.setHorizontalHeaderLabels(headers)
    def foodItemNoteKeyPressEvent(self):
        pass
    def foodItemEdits(self):
        pass
    def hierarcyClick_external(self):
        pass
    def tableItemClick_external(self):
        pass
    def onClick(self,item):
        self.constituentList.selectRow(item.row())
        rowStr=''
        for i in range(5):
            rowStr+=','+self.constituentList.item(item.row(),i).text()
        print(rowStr)
        print(self.constituentList.item(item.row(),self.constituentList.columnCount()-1).text())
        foodID=self.constituentList.item(item.row(),self.constituentList.columnCount()-1).text()
        self.foodDict[foodID]
    def deleteButtonAction(self):
        pass