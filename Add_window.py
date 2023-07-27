import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from check_db import *
from UI.add import *



class Add_product(QMainWindow):
    def __init__(self):
        super().__init__()
        self.wind = Add_Form()
        self.wind.setupUi(self)
        
        self.check_db = CheckValue()

        # Обрабатывает нажатие на кнопки
        self.wind.pushButton.clicked.connect(self.add_pr_on_table)


    # Отправляет запрос на добавление товара
    def add_pr_on_table(self):
        name_pr = self.wind.lineEdit_1.text()
        price_pr = self.wind.lineEdit_2.text()
        amount_pr = self.wind.lineEdit_3.text()
        type_pr = self.wind.comboBox.currentText()
        price_pr = price_pr
        self.check_db.cor_add_product(name_pr, price_pr, amount_pr, type_pr)
        Add_product.close(self)
    
    
        

        
        
        


