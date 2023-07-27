import sys
import hashlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from UI.sign_in import *
from check_db import *
from App_window import *
from Sign_up import *



class SignIn_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.myapp = Ui_Sign()
        self.myapp.setupUi(self)

    # Обрабатывает нажатие на кнопки
    def button_handler(self):
        self.myapp.pushButton.clicked.connect(self.authorization)
        self.myapp.pushButton_2.clicked.connect(self.registration_window)
        self.line_edit = [self.myapp.lineEdit, self.myapp.lineEdit_2]
        self.myapp.radioButton.clicked.connect(self.show_passw)
        self.myapp.radioButton.setChecked(False)

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

    # Для отправки запроса на авторизацию в БД
    @check_input_info
    def authorization(self):

        login = self.myapp.lineEdit.text()
        password = hashlib.sha256(
            self.myapp.lineEdit_2.text().encode()).hexdigest()
        self.check_db.cor_authorization(login, password)

    # Окно магазина
    def open_app(self):
        self.app = App_wind()
        self.app.show()
        SignIn_window.close(self)

    # Вывод сообщения
    def signal_handler(self, value):
        msg_box = QtWidgets.QMessageBox.about(self, "Уведомление", value)

        if value[0:6] == "Привет":
            self.open_app()

    # Скрывает/показывает пароль для окна авторизации
    def show_passw(self):
        if self.myapp.radioButton.isChecked():
            self.myapp.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.myapp.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

    # Открывает окно регистрации
    def registration_window(self):
        self.registration_window = SignUp_window()
        self.registration_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    fir_win = SignIn_window()
    fir_win.button_handler()
    fir_win.show()
    sys.exit(app.exec_())
