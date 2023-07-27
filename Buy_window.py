import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QMessageBox
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QTextDocument
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel
from check_db import *
from UI.buy import *
from request.request_db import global_username
from datetime import datetime


class Buy_product(QMainWindow):
    def __init__(self):
        super().__init__()
        self.buy_window = Ui_Buy()
        self.buy_window.setupUi(self)
        self.flag = True

        # Отображает перечень товаров в comboBox
        con = sqlite3.connect("./request/users.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM stock")
        names = cur.fetchall()
        value = [i[0] for i in names]
        self.buy_window.comboBox.addItems(value)

        # Обрабатывает нажатие на кнопки
        self.buy_window.pushButton_2.clicked.connect(self.select_table)
        self.buy_window.spinBox.valueChanged.connect(self.max_spin)
        self.buy_window.pushButton_3.clicked.connect(self.delete_last_sale)
        self.buy_window.pushButton.clicked.connect(self.sale_product)

    # Устанавливает максимальное значение spinBox
    def max_spin(self):
        text_on_box = self.buy_window.comboBox.currentText()
        con = sqlite3.connect("./request/users.db")
        cur = con.cursor()
        cur.execute(
            f"SELECT name,amount FROM stock WHERE name = '{text_on_box}'")
        value_mx = cur.fetchall()
        max_value = value_mx[0][1]
        self.buy_window.spinBox.setMaximum(max_value)

    # Формирует чека товара
    def select_table(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./request/users.db')
        self.db.open()
        self.model = QSqlQuery()

        self.text_on_box = self.buy_window.comboBox.currentText()
        self.text_on_spin_box = self.buy_window.spinBox.text()
        self.model.exec(
            f"INSERT INTO sale (name,price,amount,type,total) SELECT name, price, '{self.text_on_spin_box}', type, price * '{self.text_on_spin_box}' FROM stock WHERE name = '{self.text_on_box}' ")
        self.model.exec(
            f"UPDATE stock SET amount = amount - '{self.text_on_spin_box}' WHERE name = '{self.text_on_box}'")
        self.model.exec(
            "SELECT name as Наименование, price as Цена, SUM(amount) as Количество, type as Тип, ROUND(SUM(total),2) as Итог FROM sale GROUP BY name")
        self.buy_window.spinBox.setValue(0)

        self.view_table()
        self.view_sum()

    # Удаляет последний добавленный товар
    def delete_last_sale(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./request/users.db')
        self.db.open()
        self.model = QSqlQuery()

        con = sqlite3.connect("./request/users.db")
        cur = con.cursor()
        cur.execute("SELECT MAX(id),name,amount FROM sale")
        val_select = cur.fetchall()
        new_val_amount = val_select[0][2]
        new_val_name = val_select[0][1]
        self.model.exec(
            f"UPDATE stock SET amount = amount +'{new_val_amount}' WHERE name = '{new_val_name}'")
        self.model.exec(
            "DELETE FROM sale WHERE id = (SELECT MAX(id) FROM sale)")
        self.model.exec(
            "SELECT name as Наименование, price as Цена, SUM(amount) as Количество, type as Тип, SUM(total) as Итог FROM sale GROUP BY name")

        self.view_table()
        self.view_sum()

    # Продает товар, печатает чек, удаляет данные из таблицы sale
    def sale_product(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./request/users.db')
        self.db.open()
        self.model = QSqlQuery()

        con = sqlite3.connect("./request/users.db")
        cur = con.cursor()
        cur.execute("SELECT name,amount FROM sale")
        values = cur.fetchall()
        for i in values:
            name_in_sale = i[0]
            amount_in_sale = int(i[1])
            self.model.exec(
                f"UPDATE stock SET amount = amount - '{amount_in_sale}' WHERE name = '{name_in_sale}'")
        user_name = global_username(self)

        self.message = QMessageBox.question(
            self, 'Извещение', 'Печатать чек?', QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if self.message == QMessageBox.Ok:

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            printer = QPrinter()
            doc = QTextDocument()
            cur.execute(
                "SELECT id, name, price, amount,ROUND(total,2) FROM sale")
            check_info = cur.fetchall()
            check = []
            for id, name, price, amount, total in check_info:
                result = f"{id} {name} {price} * {amount} = {total} BYN"
                check.append(result)
            result_check = "<br>".join(check)

            cur.execute("SELECT SUM(total) FROM sale")
            total = cur.fetchall()
            total_sum = round(total[0][0], 2)
            doc.setHtml(
                f'<div align="center">ООО "The BAzzAR Box"<br>ИНН:4659215602<br>Кассир: {user_name}<br>{current_time}<br>*******************<br>{result_check}<br>*******************<br>ИТОГ = {total_sum} BYN<br>СПАСИБО ЗА ПОКУПКУ! </div>')
            doc.print_(printer)

        self.model.exec(
            f"INSERT INTO user_sale (username, name, price, amount, type, total, date_of_sale) SELECT '{user_name}',name, price, amount, type, total, DATETIME('now','localtime') FROM sale GROUP BY name")
        self.model.exec("DELETE FROM sale")
        Buy_product.close(self)

    # Отображает таблицу продажи товара
    def view_table(self):
        self.table = QSqlTableModel()
        self.table.setQuery(self.model)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.table)
        self.buy_window.tableView.setModel(self.proxy_model)
        self.buy_window.tableView.setSortingEnabled(True)

    # Отображает сумму товаров в таблице
    def view_sum(self):
        con = sqlite3.connect("./request/users.db")
        cur = con.cursor()
        cur.execute("SELECT SUM(total) FROM sale")
        total_val = cur.fetchall()
        if total_val[0][0] != None:
            total_sum = round(total_val[0][0], 2)
            self.buy_window.lineEdit_2.setText(str(total_sum)+" BYN")
        else:
            Buy_product.close(self)


