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

        self.rbExtFCs=QRadioButton('Existing food containers')
        self.rbExtFCs.clicked.connect(self.toggleSubPanels)
        self.rbNewFC=QRadioButton('New food container')
        self.rbNewFC.clicked.connect(self.toggleSubPanels)

        foodContainerLayout=QGridLayout()
        foodContainerLayout.addWidget(self.rbExtFCs,0,0,1,1)
        foodContainerLayout.addWidget(self.rbNewFC,0,1,1,2)        

        self.extScroll=QListWidget()
        foodContainerLayout.addWidget(self.extScroll,2,0,5,4)

        self.newFCentry=QLineEdit()
        self.newFCnote=QPlainTextEdit()
        self.addButton=QPushButton('Add')
        nameLayout=QHBoxLayout()
        nameLabel=QLabel('Name:')
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.newFCentry)
        buttonLayout=QHBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addItem(QSpacerItem(20,10,QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum))
        buttonLayout.setStretch(0,1)
        buttonLayout.setStretch(1,10)
        

        newFClayout=QVBoxLayout()
        newFClayout.addLayout(nameLayout)
        newFClayout.addWidget(QLabel('Notes:'))
        newFClayout.addWidget(self.newFCnote)
        newFClayout.addLayout(buttonLayout)
        
        newFClayout.setContentsMargins(0,0,0,0)
        self.newFCwidget=QWidget()
        self.newFCwidget.setLayout(newFClayout)
        foodContainerLayout.addWidget(self.newFCwidget,2,0,5,4)
        
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
        self.rbExtFCs.click()
        self.hide()

    def toggleSubPanels(self):
        if self.sender()==self.rbExtFCs:
            self.newFCwidget.hide()
            self.extScroll.show()
        else:
            self.newFCwidget.show()
            self.extScroll.hide()
    
    def addExtFCtoScroll(self,itemStr):
        self.extScroll.addItem(QListWidgetItem(itemStr))
    def extFCclicked_set(self):
        self.extScroll.itemClicked.connect(self.extFCclicked_external)
    def extFCclicked_external(self):
        pass
    def closeFoodDisplayPanel(self):
        self.stackLayout.setCurrentIndex(0)
        self.resetClickHistory_external()
    def resetClickHistory_external(self):
        pass


class foodDisplayPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.foodDisplayLayout=QStackedLayout()
        
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
                        self.noteArea=QPlainTextEdit()
                        constituentListLayout=QVBoxLayout()
                        constituentListLayout.addWidget(QLabel('Constituents:'))
                        constituentListLayout.addWidget(self.constituentList)
                        displayLayout.addLayout(constituentListLayout,3,0,7,4)
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
        
        self.foodListHolder=displayWidgetCreator('foodContainer')        
        self.foodListHolder.hierarcyScroll.itemClicked.connect(self.hierarcyClick_external)      
        self.foodMixHolder=displayWidgetCreator('foodMix')        
        self.foodMixHolder.hierarcyScroll.itemClicked.connect(self.hierarcyClick_external)      
        self.foodItemHolder=displayWidgetCreator('foodItem')
        self.foodItemHolder.hierarcyScroll.itemClicked.connect(self.hierarcyClick_external)  

        self.foodDisplayLayout.addWidget(self.foodListHolder)
        self.foodDisplayLayout.addWidget(self.foodMixHolder)
        self.foodDisplayLayout.addWidget(self.foodItemHolder)
        self.setLayout(self.foodDisplayLayout)
        self.foodDisplayLayout.setCurrentIndex(0)
        self.activeDisplayType='foodContainer'    
    def populatePanel(self,dataList,headers,panelTitle,displayType,clickList,notes='',dataList2=[]):
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
                self.foodListHolder.constituentList.setColumnCount(len(dataList[0]))
                self.foodListHolder.constituentList.setColumnHidden(len(dataList[0])-1,True)
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

                self.foodMixHolder.constituentList.setRowCount(0)
                self.foodMixHolder.constituentList.setColumnCount(0)
                self.foodMixHolder.constituentList.setRowCount(len(dataList))
                self.foodMixHolder.constituentList.setColumnCount(len(dataList[0]))
                self.foodMixHolder.constituentList.setColumnHidden(len(dataList[0])-1,True)
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
                for i,qle in enumerate(self.foodMixHolder.qtyLineEdits):
                    qle.setText(str(dataList2[i]))
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
                self.foodItemHolder.ingridientList.setColumnCount(len(dataList2[0]))
                self.foodItemHolder.ingridientList.setColumnHidden(len(dataList2[0])-1,True)
                self.populateQTableWidget(dataList2,self.foodItemHolder.ingridientList,headers)

                for i,qle in enumerate(self.foodItemHolder.qtyLineEdits):
                    qle.setText(str(dataList[i]))
                    qle.returnPressed.connect(self.foodItemEdits)
                self.foodItemHolder.noteArea.additionalKeyPressEvent=self.foodItemNoteKeyPressEvent
    def populateQTableWidget(self,dataList,tableWidget,headers):
        for i,subList in enumerate(dataList):
            for ii,item in enumerate(subList):
                listItem=QTableWidgetItem(item)
                tableWidget.setItem(i,ii,listItem)
                listItem.setFlags(Qt.ItemFlag.NoItemFlags)
                listItem.setForeground(QColor(0,0,0))
        tableWidget.setHorizontalHeaderLabels(headers)
    def foodItemNoteKeyPressEvent(self):
        pass
    def foodItemEdits(self):
        pass
    def hierarcyClick_external(self):
        pass
    def tableItemClick_set(self):
        self.foodListHolder.constituentList.itemClicked.connect(self.tableItemClick_external)
        self.foodMixHolder.constituentList.itemClicked.connect(self.tableItemClick_external)
        self.foodItemHolder.ingridientList.itemClicked.connect(self.tableItemClick_external)
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