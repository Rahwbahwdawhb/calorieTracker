import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                              QLabel, QPushButton, QScrollArea, QLineEdit,QRadioButton, QPlainTextEdit,
                              QSpacerItem,QSizePolicy,QListWidget,QListWidgetItem, QTableWidget, QTableWidgetItem,
                              QHeaderView,QAbstractScrollArea,QStackedLayout,QScrollBar)
from PyQt6.QtGui import QCloseEvent, QFont,QBrush,QColor,QTextCursor
from PyQt6.QtCore import Qt, QRect
from frontend.aidFunctionality import *

class PlainTextEdit(QPlainTextEdit):
    def __init__(self,panel):
        self.panel=panel
        super().__init__() 
    def keyPressEvent(self, event):
        super(PlainTextEdit, self).keyPressEvent(event)
        self.additionalKeyPressEvent()
    def additionalKeyPressEvent(self):
        pass

class modQLineEdit(QLineEdit):
    def __init__(self):
        super().__init__() 
    def keyPressEvent(self, event):
        QLineEdit.keyPressEvent(self,event)
        self.additionalKeyPressEvent()
    def additionalKeyPressEvent(self):
        pass

class searchField(QGridLayout):
    def __init__(self,scrollAreaInputStr,zeroRowHeight):
        super().__init__()
        self.addWidget(QLabel(scrollAreaInputStr),1,0)
        self.entryField=modQLineEdit()
        self.entryField.additionalKeyPressEvent=self.additionalKeyPressEvent
        self.entryField.focusInEvent=self.whenEFinFocused
        self.entryField.focusOutEvent=self.whenEFoutFocused
        self.addWidget(self.entryField,1,1)
        self.scrollList=QListWidget()
        self.scrollList.itemClicked.connect(self.scrollListClicked)
        self.addWidget(self.scrollList,2,1,1,1)
        self.addWidget(QLabel(),3,0)
        self.setRowStretch(1,1)
        self.setRowStretch(2,2)
        self.setRowStretch(3,5)
        self.setRowMinimumHeight(0,zeroRowHeight)
        scrollbar=QScrollBar()
        self.scrollList.setVerticalScrollBar(scrollbar)
        self.scrollList.hide()
    def addToScrollList(self,strToAdd):
        self.scrollList.addItem(QListWidgetItem(strToAdd))
    def clearScrollList(self):
        self.scrollList.clear()
    def additionalKeyPressEvent(self):
        self.scrollList.show()
        matchingItems=0
        for i in range(self.scrollList.count()):
            if self.entryField.text() not in self.scrollList.item(i).text():
                self.scrollList.item(i).setHidden(True)
            else:
                self.scrollList.item(i).setHidden(False) 
                matchingItems+=1
        if matchingItems==0:
            self.scrollList.hide()
    def whenEFinFocused(self,event):
        QLineEdit.focusInEvent(self.entryField,event)
        self.scrollList.show()
    def whenEFoutFocused(self,event):
        QLineEdit.focusOutEvent(self.entryField,event)
        self.scrollList.hide()
    def scrollListClicked(self):
        self.entryField.setText(self.sender().currentItem().text())
        self.entryField.setFocus()
        self.scrollList.hide()
    def text(self):
        return self.entryField.text()
    def setText(self,strToSet):
        self.entryField.setText(strToSet)

class returnDeleteDetectQTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(returnDeleteDetectQTableWidget, self).__init__(parent)
    def keyReleaseEvent(self, event):
         key = event.key()
         if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
             self.returnReleaseAction()
         elif key == Qt.Key.Key_Delete:
             self.deleteReleaseAction()
         else:
             super(returnDeleteDetectQTableWidget, self).keyReleaseEvent(event)
    def keyPressEvent(self, event):
         key = event.key()
         if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
             self.returnPressAction()         
         else:
             super(returnDeleteDetectQTableWidget, self).keyPressEvent(event)
    def returnReleaseAction(self):
        pass
    def returnPressAction(self):
        pass
    def deleteReleaseAction(self):
        pass
