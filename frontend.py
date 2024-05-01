import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                              QLabel, QPushButton, QScrollArea, QLineEdit,QRadioButton, QPlainTextEdit,
                              QSpacerItem,QSizePolicy,QListWidget,QListWidgetItem, QTableWidget, QTableWidgetItem,
                              QHeaderView,QAbstractScrollArea,QStackedLayout)
from PyQt6.QtGui import QCloseEvent, QFont,QBrush,QColor,QTextCursor
from PyQt6.QtCore import Qt, QRect
import copy

quantityNames=['Calories [kcal]','Protein [g]','Carbohydrates [g]','Fat [g]','Fibers [g]']


class PlainTextEdit(QPlainTextEdit):
    def __init__(self,panel):
        self.panel=panel
        super().__init__() 
    def keyPressEvent(self, event):
        super(PlainTextEdit, self).keyPressEvent(event)
        self.additionalKeyPressEvent()
        # print(self.panel.displayLabel.text())
        # print(self.toPlainText())
    def additionalKeyPressEvent(self):
        pass

class scrollAreaWidget(QGridLayout):
    def __init__(self,scrollAreaInputStr,zeroRowHeight):
        super().__init__()
        self.addWidget(QLabel(scrollAreaInputStr),1,0)
        self.entryField=QLineEdit()
        self.addWidget(self.entryField,1,1)
        self.scrollList=QScrollArea()
        self.addWidget(self.scrollList,2,0,1,2)
        self.setRowMinimumHeight(0,zeroRowHeight)

class addFoodPanel(QWidget):
    def __init__(self):
        super().__init__()

        quantityLayout=QGridLayout()        
        self.nameEntry=QLineEdit()
        nameLayout=QHBoxLayout()
        nameLayout.addWidget(QLabel('Name:'))
        nameLayout.addWidget(self.nameEntry)
        quantityLayout.addLayout(nameLayout,0,0,1,5)
        self.quantityLineEdits=[]
        for iter,qtn in enumerate(['Quantity [g]']+quantityNames):
            iterLabel=QLabel(qtn)
            iterLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            quantityLayout.addWidget(iterLabel,2,iter)
            loopLineEdit=QLineEdit()
            if iter==0:
                loopLineEdit.setText('100')
            else:
                loopLineEdit.setText('0')
            self.quantityLineEdits.append(loopLineEdit)
            quantityLayout.addWidget(loopLineEdit,3,iter)
            quantityLayout.setColumnStretch(iter,1)
        quantityLayout.setRowMinimumHeight(1,20)
        quantityLayout.setRowMinimumHeight(3,20)
        self.foodContainerScroll=scrollAreaWidget('Add to food container:',20)        
        self.addButton=QPushButton('Add')
        self.addButton.clicked.connect(self.addButtonAction)
        foodContainerLayout=QGridLayout()
        foodContainerLayout.addLayout(self.foodContainerScroll,0,0,1,8)
        foodContainerLayout.addWidget(self.addButton,1,0,2,1)

        foodPanelLayout=QVBoxLayout()
        foodPanelLayout.addLayout(quantityLayout)
        foodPanelLayout.addLayout(foodContainerLayout)
        
        self.setLayout(foodPanelLayout)
        self.hide()
    def addButtonAction(self):
        pass

class mixFoodPanel(QWidget):
    def __init__(self):
        super().__init__()

        quantityLayout=QGridLayout()        
        self.nameEntry=QLineEdit()
        nameLayout=QHBoxLayout()
        nameLayout.addWidget(QLabel('Name:'))
        nameLayout.addWidget(self.nameEntry)
        quantityLayout.addLayout(nameLayout,0,0,1,5)
        self.quantityStatLabels=[]
        for iter,qtn in enumerate(quantityNames):
            iterLabel=QLabel(qtn)
            iterLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            quantityLayout.addWidget(iterLabel,2,iter)
            quantity=QLabel('0')
            quantity.setAlignment(Qt.AlignmentFlag.AlignCenter)
            quantityLayout.addWidget(quantity,3,iter)
            self.quantityStatLabels.append(quantity)
            quantityLayout.setColumnStretch(iter,1)
        quantityLayout.setRowMinimumHeight(1,20)
        quantityLayout.setRowMinimumHeight(3,20)

        ingridientLabel=QLabel('Ingridients')
        ingridientLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingridientScroll=QScrollArea()

        self.ingridientAddScroll=scrollAreaWidget('Add ingridient:',0)
        self.addIngridientButton=QPushButton('Add')
        ingridientLayout=QGridLayout()
        ingridientLayout.addLayout(self.ingridientAddScroll,0,0,1,8)
        ingridientLayout.addWidget(self.addIngridientButton,1,0,2,1)
        ingridientLayout.setContentsMargins(0,0,0,0)
        self.ingridientWidget=QWidget()
        self.ingridientWidget.setLayout(ingridientLayout)

        self.foodContainerScroll=scrollAreaWidget('Add to food container:',0)        
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

        mixPanelLayout=QVBoxLayout()
        mixPanelLayout.addLayout(quantityLayout)
        mixPanelLayout.addWidget(ingridientLabel)
        mixPanelLayout.addWidget(self.ingridientScroll)
        mixPanelLayout.insertSpacing(3,5)
        mixPanelLayout.addLayout(rbLayout)
        mixPanelLayout.addWidget(self.ingridientWidget)
        mixPanelLayout.addWidget(self.foodContainerWidget) 
        mixPanelLayout.addWidget(self.noteWidget)
        mixPanelLayout.setStretch(5,1)
        mixPanelLayout.setStretch(6,1)
        mixPanelLayout.setStretch(7,1)
        
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

        # self.extScroll=QScrollArea()
        # self.extScroll.setWidgetResizable(True)
        # self.extScrollVContainer=QVBoxLayout()
        # QW=QWidget()
        # QW.setLayout(self.extScrollVContainer)
        # self.extScroll.setWidget(QW)
        self.extScroll=QListWidget()
        # self.extScroll.itemClicked.connect(self.extFCclicked)
        foodContainerLayout.addWidget(self.extScroll,2,0,5,4)

        self.newFCentry=QLineEdit()
        self.newFCnote=QPlainTextEdit()
        self.addButton=QPushButton('Add')
        nameLayout=QHBoxLayout()
        nameLabel=QLabel('Name:')
        # nameLabel.setMinimumWidth(1)
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
        # foodContainerLayout.addWidget(self.foodDisplayPanel,0,0,0,0)
        # self.foodDisplayPanel.hide()

        foodContainerLayoutContainer=QWidget()
        foodContainerLayoutContainer.setLayout(foodContainerLayout)
        self.stackLayout=QStackedLayout()
        self.stackLayout.addWidget(foodContainerLayoutContainer)
        self.stackLayout.addWidget(self.foodDisplayPanel)
        self.setLayout(self.stackLayout)
        # self.setLayout(foodContainerLayout)
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
        # self.extScroll.addItem(QListWidgetItem(QLabel(itemStr)))
        self.extScroll.addItem(QListWidgetItem(itemStr))
    def extFCclicked_set(self):
        self.extScroll.itemClicked.connect(self.extFCclicked_external)
    def extFCclicked_external(self):
        pass
    def extFCclicked(self,item):
        data = [['1','2','3','4','abc'],['5','6','7','8','def'],['4','3','2','1','ghi']]
        self.foodDisplayPanel.populatePanel(data,['w','x','y','z'])
        self.stackLayout.setCurrentIndex(1)
        # self.foodDisplayPanel.show()
        # # self.hide()
        # self.newFCwidget.hide()
        # self.extScroll.hide()
        # self.newFCentry.hide()
        # self.newFCnote.hide()
        # self.addButton.hide()
        print(item.text())
    def closeFoodDisplayPanel(self):
        self.stackLayout.setCurrentIndex(0)
        self.resetClickHistory_external()
    def resetClickHistory_external(self):
        pass

        
        
        # self.extScrollVContainer.addWidget(QLabel('hej'))

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
                            # qle_i=QLineEdit()
                            # qle_i.setEnabled(False)
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
                        noteAreaLayout=QVBoxLayout()
                        noteAreaLayout.addWidget(QLabel('Notes:'))
                        noteAreaLayout.addWidget(self.noteArea)
                        displayLayout.addLayout(noteAreaLayout,3,0,7,4)
                        displayLayout.addWidget(self.closeButton,10,0)
                for i in range(11):
                    displayLayout.setRowStretch(i,1)
                displayLayout.setContentsMargins(0,0,0,0)
                self.setLayout(displayLayout)
        
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
        # self.constituentList.itemClicked.connect(self.onClick)
        # self.constituentList.show()
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

                for i,subList in enumerate(dataList):
                    for ii,item in enumerate(subList):
                        listItem=QTableWidgetItem(item)
                        self.foodListHolder.constituentList.setItem(i,ii,listItem)
                        listItem.setFlags(Qt.ItemFlag.NoItemFlags)
                        listItem.setForeground(QColor(0,0,0))
                self.foodListHolder.constituentList.setHorizontalHeaderLabels(headers)
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
                # self.foodItemHolder.hierarcyScroll.setItemda
                # QFont
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
                # self.foodItemHolder.hierarcyScroll.setItemda
                # QFont
                self.foodItemHolder.hierarcyScroll.scrollToBottom()

                for i,qle in enumerate(self.foodItemHolder.qtyLineEdits):
                    qle.setText(str(dataList[i]))
                    qle.returnPressed.connect(self.foodItemEdits)
                self.foodItemHolder.noteArea.additionalKeyPressEvent=self.foodItemNoteKeyPressEvent
    def foodItemNoteKeyPressEvent(self):
        pass
    def foodItemEdits(self):
        pass
    def hierarcyClick_external(self):
        pass
    def tableItemClick_set(self):
        self.foodListHolder.constituentList.itemClicked.connect(self.tableItemClick_external)
        self.foodMixHolder.constituentList.itemClicked.connect(self.tableItemClick_external)
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


class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400,300)
        # self.setBaseSize(300,700)
        self.show()
        mainLayout=QGridLayout()
        self.setLayout(mainLayout)

        self.foodPanel=addFoodPanel()
        self.mixPanel=mixFoodPanel()
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
        mainLayout.addWidget(self.foodPanel,0,1,3,3)
        mainLayout.addWidget(self.mixPanel,0,1,3,3)
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
            self.foodPanel.show()
            self.mixPanel.hide()
            self.foodContainerPanel.hide()
        elif self.sender()==self.mixFoodButton:
            self.foodPanel.hide()
            self.mixPanel.show()
            self.foodContainerPanel.hide()
        else:
            self.foodPanel.hide()
            self.mixPanel.hide()
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


