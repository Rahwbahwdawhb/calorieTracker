from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QStackedLayout,
                              QLabel, QPushButton, QScrollArea, QLineEdit,QRadioButton, QPlainTextEdit,
                              QSpacerItem,QSizePolicy,QListWidget,QListWidgetItem, QTableWidget, QTableWidgetItem,
                              QHeaderView,QAbstractScrollArea,QStackedLayout,QScrollBar)
from PyQt6.QtGui import QCloseEvent, QFont,QBrush,QColor,QTextCursor
from PyQt6.QtCore import Qt, QRect
from dataclasses import dataclass

class operation_type: pass #could have different operation types for different kinds of calls...
class adder(operation_type): pass
class subtracter(operation_type): pass
class multiplier(operation_type): pass

@dataclass
class request:
    operator: adder|subtracter|multiplier
    inputs: list[str]

class backend:
    def __init__(self):
        self.history=[]
    def multiply(self,inputs):
        product=1
        for inp in inputs:
            product*=float(inp)
        self.history.append(f"{'x'.join(inputs)}={product}")
        return product
    def add(self,inputs):
        sum=0
        for inp in inputs:
            sum+=float(inp)
        self.history.append(f"{'+'.join(inputs)}={sum}")
        return sum
    def subtract(self,inputs):
        remainder=float(inputs[0])
        for inp in inputs[1:]:
            remainder-=float(inp)
        self.history.append(f"{'-'.join(inputs)}={remainder}")
        return remainder
    def get_history(self):
        return self.history
class backend_communicator:
    def __init__(self):
        self.backend=backend()
        self.evaluation_dict={multiplier:self.backend.multiply,adder:self.backend.add,subtracter:self.backend.subtract}
    def evaluate(self,_request):
        return self.evaluation_dict[_request.operator](_request.inputs)
    def retrieve_history(self):
        return self.backend.get_history()

class page_widget(QWidget):
    def __init__(self,operation,default_values=[5,10],backend_communicator=None):
        super().__init__()
        self.backend_communicator=backend_communicator
        operation_symbol={adder:'+',subtracter:'-',multiplier:'x'}[operation]
        self.operation=operation
        main_layout=QVBoxLayout()
        input_layout=QHBoxLayout()
        input_layout.addStretch(1)
        self.qles=[]
        for default_value in default_values:
            qle=QLineEdit()
            qle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qle.setText(str(default_value))
            input_layout.addWidget(qle)
            operator_QLabel=QLabel(operation_symbol)
            input_layout.addWidget(operator_QLabel)
            self.qles.append(qle)
        input_layout.removeWidget(operator_QLabel)
        input_layout.addStretch(1)
        main_layout.addStretch()
        main_layout.addLayout(input_layout)
        equal_button=QPushButton('=')
        equal_button.clicked.connect(self.equal_button_press)
        equal_button_layout=QHBoxLayout()
        equal_button_layout.addStretch(2)
        equal_button_layout.addWidget(equal_button)
        equal_button_layout.addStretch(2)
        main_layout.addStretch()
        main_layout.addLayout(equal_button_layout)        
        self.result_QLabel=QLabel()
        main_layout.addStretch()
        main_layout.addWidget(self.result_QLabel,alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)
    def equal_button_press(self):
        if self.backend_communicator:
            inputs=[]
            for qle in self.qles:
                inputs.append(qle.text())            
            result=self.backend_communicator.evaluate(request(operator=self.operation,inputs=inputs))
            result_str=str(result)
            integer,decimal=result_str.split('.')
            if decimal=='0':
                result_str=integer
            self.result_QLabel.setText(result_str)
class history_widget(QWidget):
    def __init__(self,backend_communicator=None):
        super().__init__()
        self.backend_communicator=backend_communicator
        history_holder=QScrollArea()
        history_holder.setWidgetResizable(True)
        self.container=QWidget()
        self.container_layout=QVBoxLayout(self.container)
        history_holder.setWidget(self.container)
        main_layout=QVBoxLayout()
        main_layout.addWidget(history_holder)
        self.setLayout(main_layout)
    def display_history(self):
        while self.container_layout.count():
            child = self.container_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        history=self.backend_communicator.retrieve_history()
        for h in history:
            self.container_layout.insertWidget(0,QLabel(h),alignment=Qt.AlignmentFlag.AlignCenter)
        self.container.adjustSize()
class main_window(QWidget):
    def __init__(self,backend_communicator=None):
        super().__init__()
        self.setMinimumSize(400,300)
        self.show()
        mainLayout=QHBoxLayout()
        self.left_layout=QVBoxLayout()
        self.right_layout=QStackedLayout()
        blank_widget=QWidget()
        self.right_layout.addWidget(blank_widget)
        self.right_layout.setCurrentIndex(0)
        mainLayout.addLayout(self.left_layout)
        mainLayout.addLayout(self.right_layout)
        self.setLayout(mainLayout)
        self.button_dict={}
        for i,(button_name,operator) in enumerate(zip(['Add','Subtract','Multiply'],[adder,subtracter,multiplier])):
            page_i=page_widget(operator,backend_communicator=backend_communicator)
            self.right_layout.addWidget(page_i)
            button_i=QPushButton(button_name)
            button_i.clicked.connect(lambda _,idx=i+1:self.right_layout.setCurrentIndex(idx)) #1st input is for the checked signal that the button emits, it could also be set to checked=False
            self.left_layout.addWidget(button_i)
            self.button_dict[i]=button_i
        self.hw=history_widget(backend_communicator=backend_communicator)
        self.right_layout.addWidget(self.hw)
        hw_button=QPushButton('History')
        hw_button.clicked.connect(self.hw_button_clicked)
        self.left_layout.addWidget(hw_button)
    def hw_button_clicked(self):
        self.right_layout.setCurrentIndex(4)
        self.hw.display_history()

class app_assembler(QApplication):
    def __init__(self,):
        super().__init__([])
        self.backend_communicator=backend_communicator()
        self.mw=main_window(backend_communicator=self.backend_communicator)
    def start(self):
        self.mw
        self.exec()

if __name__=='__main__':
    app_assembler().start()