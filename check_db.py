from PyQt5 import QtCore, QtGui, QtWidgets
from request.request_db import *


class CheckValue(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def cor_authorization(self, name, passw):
        authorization(name, passw, self.mysignal)

    def cor_registration(self, name, passw, username):
        registration(name, passw, username, self.mysignal)

    def cor_add_product(self,name,price,amount,type):
        add_product(name,price,amount,type)
    
    
    
   