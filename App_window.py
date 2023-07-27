import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
import sqlite3
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from UI.sign_in import *
from check_db import *
from UI.app import *
from UI.sign_up import *
from UI.add import *
from Add_window import *
from Buy_window import *
from request.request_db import global_username



class App_wind(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sec_wind = Ui_App()
        self.sec_wind.setupUi(self)
        self.sort_order = Qt.AscendingOrder
        
        

        # Обработчик сигналов
        self.check_db = CheckValue()

        # Обрабатывает нажатие на кнопки
        self.sec_wind.pushButton.clicked.connect(self.view_stock)
        self.sec_wind.pushButton_2.clicked.connect(self.view_sale)
        self.sec_wind.pushButton_3.clicked.connect(self.view_graph)
        self.sec_wind.pushButton_5.clicked.connect(self.add_product_menu)
        self.sec_wind.pushButton_6.clicked.connect(self.buy_product)

    # Сортирует данные в таблице
    def view_table(self):
        self.table = QSqlTableModel()
        self.table.setQuery(self.model)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.table)
        self.sec_wind.tableView.setModel(self.proxy_model)
        self.sec_wind.tableView.setSortingEnabled(True)

    # Отображает таблицу stock
    def view_stock(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("./request/users.db")
        self.db.open()
        self.model = QSqlQuery()
        self.model.exec_(
            f"SELECT username as 'Имя пользователя', name as 'Наименование товара', price as 'Цена, BYN', amount as 'Количество', type as 'Тип', receipt_date as 'Дата добавления' FROM stock")
        self.view_table()
        self.sec_wind.lineEdit.textChanged.connect(self.search_name_on_stock)   
        self.sec_wind.lineEdit_2.textChanged.connect(self.search_amount_on_stock)
        self.sec_wind.pushButton_10.clicked.connect(self.view_stock)
        
    # Отображает таблицу user_sale
    def view_sale(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("./request/users.db")
        self.db.open()
        self.model = QSqlQuery()
        self.model.exec_(f"SELECT username as 'Имя пользователя', name as 'Наименование товара', price as 'Цена, BYN', amount as 'Количество',type as 'Тип', total as 'Итог, BYN', date_of_sale as 'Дата продажи' FROM user_sale")
        self.view_table()

        self.sec_wind.lineEdit.textChanged.connect(self.search_name_on_sale)   
        self.sec_wind.lineEdit_2.textChanged.connect(self.search_amount_on_sale)
        self.sec_wind.pushButton_10.clicked.connect(self.view_sale)
        
    # Поиск по имени товара в таблице stock
    def search_name_on_stock(self):
        name_search = self.sec_wind.lineEdit.text().capitalize()
        if name_search != 0:
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            self.db.setDatabaseName("./request/users.db")
            self.db.open()
            self.model = QSqlQuery()
            self.model.exec_(
                f"SELECT username as 'Имя пользователя', name as 'Наименование товара', price as 'Цена, BYN', amount as 'Количество', type as 'Тип', receipt_date as 'Дата добавления' FROM stock WHERE name LIKE '{name_search}%'")
            self.view_table()
       
    # Поиск по количеству товара в таблице stock
    def search_amount_on_stock(self):
        amount_search = self.sec_wind.lineEdit_2.text()
        if amount_search != 0:
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            self.db.setDatabaseName("./request/users.db")
            self.db.open()
            self.model = QSqlQuery()
            self.model.exec_(
                f"SELECT username as 'Имя пользователя', name as 'Наименование товара', price as 'Цена, BYN', amount as 'Количество', type as 'Тип', receipt_date as 'Дата добавления' FROM stock WHERE amount LIKE'{amount_search}%'")
            self.view_table()
            

    # Поиск по имени товара в таблице sale
    def search_name_on_sale(self):
        name_search = self.sec_wind.lineEdit.text().capitalize()
        if name_search != 0:
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            self.db.setDatabaseName("./request/users.db")
            self.db.open()
            self.model = QSqlQuery()
            self.model.exec_(
                f"SELECT username as 'Имя пользователя', name as 'Наименование товара', price as 'Цена, BYN', amount as 'Количество',type as 'Тип', total as 'Итог, BYN', date_of_sale as 'Дата продажи' FROM user_sale WHERE name LIKE '{name_search}%'")
            self.view_table()
           

    # Поиск по количеству товара в таблице sale
    def search_amount_on_sale(self):
        amount_search = self.sec_wind.lineEdit_2.text()
        if amount_search != 0:
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            self.db.setDatabaseName("./request/users.db")
            self.db.open()
            self.model = QSqlQuery()
            self.model.exec_(
                f"SELECT username as 'Имя пользователя', name as 'Наименование товара', price as 'Цена, BYN', amount as 'Количество',type as 'Тип', total as 'Итог, BYN', date_of_sale as 'Дата продажи' FROM user_sale WHERE amount LIKE '{amount_search}%'")
            self.view_table()
            

    # Открывает окно продажи товара
    def buy_product(self):
        self.buy_window = Buy_product()
        self.buy_window.show()

    # Открывает окно добавления товара
    def add_product_menu(self):
        self.add = Add_product()
        self.add.show()

    # Показывает графики продаж
    def view_graph(self):
        con = sqlite3.connect("./request/users.db")
        cur1 = con.cursor()
        cur2 = con.cursor()
        cur3 = con.cursor()
        username = global_username(self)
        cur1.execute(
            f"SELECT date_of_sale, SUM(amount) FROM user_sale  WHERE username = '{username}' GROUP BY date_of_sale")
        cur2.execute(
            f"SELECT name, SUM(amount) FROM user_sale  WHERE username = '{username}' GROUP BY name")
        cur3.execute(
            "SELECT username, SUM(amount) FROM user_sale GROUP BY username")
        value1 = cur1.fetchall()
        value2 = cur2.fetchall()
        value3 = cur3.fetchall()

        name_product = []
        amount_product = []
        for name, amount in value2:
            name_product.append(name)
            amount_product.append(amount)

        data_names = []
        data_values = []
        for data, amount in value1:
            data_names.append(data)
            data_values.append(amount)

        user_name = []
        user_amount = []
        for user, amount in value3:
            user_name.append(user)
            user_amount.append(amount)

        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        fig.subplots_adjust(wspace=0.5)
        data_names.insert(0,0)
        data_values.insert(0,0)

        ax[0].plot(data_names, data_values)
        ax[0].set_ylim(bottom=0)
        ax[0].set_xticklabels(ax[0].get_xticklabels(), fontsize=6)
        ax[0].set_yticklabels(ax[0].get_yticklabels(), fontsize=10)
        ax[0].set_title("Мои продажи")
        ax[0].set_ylabel("Количество проданного товара")
        ax[0].set_xlabel("Дата продажи")

        ax[1].pie(amount_product, labels=name_product, autopct='%1.1f%%', labeldistance=1.1, textprops={
                  'fontsize': 8}, wedgeprops={'lw': 1, 'ls': '-', 'edgecolor': 'k'}, rotatelabels=False)
        ax[1].axis('equal')
        ax[1].set_title("Топ товаров")

        ax[2].bar(user_name, user_amount, width=0.5)
        ax[2].set_title("Рейтинг сотрудников")

        ax[2].set_xlabel("Кассир")

        plt.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    fir_win = App_wind()
    fir_win.show()
    sys.exit(app.exec_())

