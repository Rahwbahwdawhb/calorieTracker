from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                              QLabel, QPushButton, QScrollArea, QLineEdit,QRadioButton, QPlainTextEdit,
                              QSpacerItem,QSizePolicy,QListWidget,QListWidgetItem, QTableWidget, QTableWidgetItem,
                              QHeaderView,QAbstractScrollArea,QStackedLayout,QScrollBar,QSpacerItem)
from PyQt6.QtGui import QCloseEvent, QFont,QBrush,QColor,QTextCursor
from PyQt6.QtCore import Qt, QRect, QTimer
try:
    from .aidFunctionality import *
except:
    from aidFunctionality import *

quantityNames=['Quantity [g]','Calories [kcal]','Protein [g]','Carbohydrates [g]','Fat [g]','Fibers [g]']
ingridientInfo=['Name','Qty [g]','Cal. [kcal]','Protein [g]','Carbs [g]','Fat [g]','Fibers [g]']

class dynamicTable(QWidget):
    def __init__(self):
        super().__init__()
        main_layout=QVBoxLayout()
        # self.table=QTableWidget()
        self.table=QTableWidget(1,len(ingridientInfo)+1)
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setColumnCount(len(ingridientInfo)+1)
        self.table.setHorizontalHeaderLabels(['']+ingridientInfo)
        self.table.setMinimumHeight(135)
        
        self.row_count=1
        self.table.setRowCount(self.row_count)
        self.add_row_add_button=QPushButton('+',self.table)        
        self.add_row_food_name_entry=QTableWidgetItem()
        self.add_row_quantity_entry=QTableWidgetItem()
        row_number=0
        self.table.setCellWidget(row_number,0,self.add_row_add_button)        
        self.table.setItem(row_number,1,self.add_row_food_name_entry)        
        self.table.setItem(row_number,2,self.add_row_quantity_entry)
        self.add_row_marco_entry_list=[]
        for i,name in enumerate(quantityNames[2:]):
            cellItem=QTableWidgetItem()
            cellItem.setFlags(Qt.ItemFlag.NoItemFlags)
            self.add_row_marco_entry_list.append(cellItem)
            self.table.setItem(row_number,i+3,cellItem)
        self.add_row_add_button.clicked.connect(self.add_entry)

        main_layout.addWidget(self.table)
        self.setLayout(main_layout)
    def add_entry(self):
        insert_row_index=self.row_count-1
        self.table.insertRow(insert_row_index)
        remove_button=QPushButton('-')
        remove_button.clicked.connect(self.remove_entry)
        self.table.setCellWidget(insert_row_index,0,remove_button)
        for i,_ in enumerate(quantityNames):
            cellItem=QTableWidgetItem()
            cellItem.setText(self.table.item(self.row_count,i+1).text())
            self.table.item(self.row_count,i+1).setText('')
            if i!=1:
                cellItem.setFlags(Qt.ItemFlag.NoItemFlags)
            self.table.setItem(insert_row_index,i+1,cellItem)
        self.row_count+=1
        self.table.setRowCount(self.row_count)
        self.table.scrollToBottom()
        
    def remove_entry(self):
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i,0)==self.sender():
                self.table.removeRow(i)
                self.row_count-=1
                self.table.setRowCount(self.row_count)
                break


class mealHolderPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.meal_tables={}
        self.tags=set()

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
        self.ingridientScroll=QScrollArea()
        self.ingridientScroll.setWidgetResizable(True)
        self.scroll_layout=QVBoxLayout()
        self.container=QWidget()
        self.container.setLayout(self.scroll_layout)
        self.ingridientScroll.setWidget(self.container)
        
        ingridientScrollLayout=QGridLayout()
        ingridientScrollLayout.addWidget(ingridientLabel,1,0)
        ingridientScrollLayout.addWidget(self.ingridientScroll,2,0)
        ingridientScrollLayout.setRowMinimumHeight(0,80)        
        topWrapLayout.addLayout(quantityLayout,0,0,1,8)        
        topWrapLayout.addLayout(ingridientScrollLayout,0,0,1,8)
        topWrapLayout.addLayout(self.nameEntry,0,0,1,8)
        #stack layout here to make searchfield suggestions end up on top
        #try to use Qt.Popup in searchfield instead to make it appear on top

        add_meal_layout=QHBoxLayout()
        self.add_meal_button=QPushButton('Add meal')
        self.add_meal_button.clicked.connect(self.add_meal)
        self.add_meal_name=QLineEdit()
        add_meal_layout.addWidget(self.add_meal_button)
        add_meal_layout.addWidget(self.add_meal_name)
        topWrapLayout.addLayout(add_meal_layout,8,0)

        tag_layout=QHBoxLayout()
        self.add_tag_button=QPushButton('Add tag')
        self.add_tag_button.clicked.connect(self.add_tag)
        self.add_tag_name=QLineEdit()
        self.tag_scoll=QScrollArea()
        self.tag_scoll.setWidgetResizable(True)
        self.tag_scoll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.container2=QWidget()
        self.tag_scroll_layout=QHBoxLayout()
        self.container2.setLayout(self.tag_scroll_layout)
        self.tag_scoll.setWidget(self.container2)
        tag_layout.addWidget(self.add_tag_button)
        tag_layout.addWidget(self.add_tag_name)
        tag_layout.addWidget(self.tag_scoll)
        topWrapLayout.addLayout(tag_layout,9,0)

        mixPanelLayout=QGridLayout()
        mixPanelLayout.addLayout(topWrapLayout,0,0)
        mixPanelLayout.setRowStretch(0,10)
        mixPanelLayout.setRowStretch(1,1)
        self.setLayout(mixPanelLayout)
        self.hide()
    def add_meal(self):
        meal_name=self.add_meal_name.text()
        if meal_name not in self.meal_tables:
            scroll_container=QWidget()
            meal_table=dynamicTable()
            self.meal_tables[meal_name]=meal_table
            def remove_meal():
                self.scroll_layout.removeWidget(scroll_container)
                scroll_container.setParent(None)
                scroll_container.deleteLater()
                del self.meal_tables[meal_name]
            label_button_layout=QHBoxLayout()
            label_button_layout.addWidget(QLabel(meal_name))
            delete_meal_button=QPushButton('Remove')
            label_button_layout.addWidget(delete_meal_button)
            delete_meal_button.clicked.connect(remove_meal)
            self.add_meal_name.setText('')
            scroll_container_layout=QVBoxLayout()
            scroll_container_layout.addLayout(label_button_layout)
            scroll_container_layout.addWidget(meal_table)
            scroll_container.setLayout(scroll_container_layout)
            self.scroll_layout.addWidget(scroll_container)
            self.container.adjustSize()
            QTimer.singleShot(0, lambda: self.ingridientScroll.verticalScrollBar().setValue(
            self.ingridientScroll.verticalScrollBar().maximum()))
    def add_tag(self):
        tag_name=self.add_tag_name.text()
        if tag_name not in self.tags:
            tag_widget=QWidget()
            def remove_tag():
                self.tags.remove(tag_name)
                self.tag_scroll_layout.removeWidget(tag_widget)
                tag_widget.setParent(None)
                tag_widget.deleteLater()
            self.add_tag_name.setText('')
            self.tags.add(tag_name)
            tag_remove_button=QPushButton('x')
            tag_remove_button.clicked.connect(remove_tag)
            tag_widget_layout=QHBoxLayout()
            tag_widget.setLayout(tag_widget_layout)
            tag_widget_layout.addWidget(tag_remove_button)
            tag_widget_layout.addWidget(QLabel(tag_name))
            tag_widget_layout.setSpacing(2)
            tag_remove_button.setStyleSheet("padding: 0px; margin: 0px;")
            tag_remove_button.setFixedSize(tag_remove_button.sizeHint())
            self.tag_scroll_layout.addWidget(tag_widget)
            self.container2.adjustSize()
            self.container2.updateGeometry()
            QTimer.singleShot(0, lambda: self.tag_scoll.horizontalScrollBar().setValue(
            self.tag_scoll.horizontalScrollBar().maximum()))
if __name__ == '__main__':
    app = QApplication([])
    # window = dynamicTable()
    window = mealHolderPanel()
    window.show()
    app.exec()