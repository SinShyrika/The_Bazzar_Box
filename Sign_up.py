import sys
import hashlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from check_db import *
from UI.sign_up import *
from Sign_in import *


class SignUp_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sec_wind = Ui_Registration()
        self.sec_wind.setupUi(self)

        # Обрабатывает нажатие на кнопки

        self.sec_wind.radioButton.clicked.connect(self.show_passw_2)
        self.sec_wind.radioButton.setChecked(False)
        self.sec_wind.pushButton.clicked.connect(self.close_sec_wind)
        self.line_edit = [self.sec_wind.lineEdit_2, self.sec_wind.lineEdit_3,
                          self.sec_wind.lineEdit_4, self.sec_wind.lineEdit_5]

        # Обработчик сигналов
        self.check_db = CheckValue()
        self.check_db.mysignal.connect(self.signal_handler)

    # Декоратор, проверяет что поля ввода логина и пароля не пусты
    def check_input_info(func):
        def wrapper(self):
            for i in self.line_edit:
                if len(i.text()) == 0:
                    return
            func(self)

        return wrapper
    # Обработчик сигналов

    def signal_handler(self, value):
        msg_box = QtWidgets.QMessageBox.about(self, "Уведомление", value)

    # Отправляет запрос на регистрацию в БД и закрывает окно
    @check_input_info
    def close_sec_wind(self):
        login = self.sec_wind.lineEdit_3.text()
        password = hashlib.sha256(
            self.sec_wind.lineEdit_4.text().encode()).hexdigest()
        username = self.sec_wind.lineEdit_2.text() + " " + self.sec_wind.lineEdit_5.text()
        self.check_db.cor_registration(login, password, username)

        SignUp_window.close(self)

    # Скрывает/показывает пароль для окна регистрации
    def show_passw_2(self):
        if self.sec_wind.radioButton.isChecked():
            self.sec_wind.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.sec_wind.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)

