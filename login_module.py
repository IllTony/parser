import json
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QGridLayout, QVBoxLayout, QApplication
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
import hashlib

from register_module import UserRegister


class UserLogin(QWidget):
    closeApp = pyqtSignal()
    openApp = pyqtSignal(str)
    toLog = pyqtSignal(str)

    def __init__(self):
        """Конструктор класса UserLogin, иницииализация элементов и переменных"""
        super().__init__()
        # Describing interface's elements
        self.v_lay = QVBoxLayout()

        self.user_label = QLabel("Имя пользователя:")
        self.user_label.setFixedSize(115, 30)
        self.user_label.setAlignment(Qt.AlignLeft)

        self.password_label = QLabel("Пароль:")
        self.password_label.setFixedSize(115, 30)
        self.password_label.setAlignment(Qt.AlignLeft)

        self.user_edit = QLineEdit()
        self.user_edit.setFixedSize(190, 30)
        self.password_edit = QLineEdit()
        self.password_edit.setFixedSize(190, 30)

        self.login_btn = QPushButton("Логин")
        self.login_btn.setFixedSize(160, 30)
        self.exit_btn = QPushButton("Выход")
        self.exit_btn.setFixedSize(160, 30)

        self.reg_btn = QPushButton("Создать новую учетную запись")

        self.grid_lay = QGridLayout()
        self.grid_lay.addWidget(self.user_label, 0, 0)
        self.grid_lay.addWidget(self.user_edit, 0, 1)
        self.grid_lay.addWidget(self.password_label, 1, 0)
        self.grid_lay.addWidget(self.password_edit, 1, 1)

        self.grid_btn_lay = QGridLayout()
        self.grid_btn_lay.addWidget(self.login_btn, 0, 0)
        self.grid_btn_lay.addWidget(self.exit_btn, 0, 1)

        self.v_lay.addLayout(self.grid_lay)
        self.v_lay.addLayout(self.grid_btn_lay)
        self.v_lay.addWidget(self.reg_btn)
        self.setLayout(self.v_lay)

        self.login_flag = False
        self.filename = "authorised_data.json"
        self.authorised_data = {}
        self.load_authorised_data()
        self.register_window = UserRegister()
        self._connects()

    def _connects(self):
        """Describe all connects for signal and slots for UserLogin class"""
        self.login_btn.clicked.connect(self.login_slot)
        self.register_window.registerDone.connect(self.register_done_slot)
        self.reg_btn.clicked.connect(self.reg_btn_slot)
        self.exit_btn.clicked.connect(self.exit_btn_slot)

    def check_login_data(self, user_str, password_str):
        """Check username and password in LineEdit"""
        if user_str.lower() in self.authorised_data.keys():
            if hashlib.sha1(password_str.encode('utf-8')).hexdigest() == self.authorised_data[user_str.lower()]:
                return True
            else:
                return False
        else:
            return False

    def load_authorised_data(self):
        try:
            with open(self.filename, 'r') as file_object:
               self.authorised_data = json.load(file_object)
        except(FileExistsError, FileNotFoundError):
            with open(self.filename, 'w') as f_obj:
                json.dump({'user': '1234'}, f_obj)
            with open(self.filename, 'r') as file_object:
                self.authorised_data = json.load(file_object)

    @pyqtSlot()
    def register_done_slot(self):
        self.load_authorised_data()
        self.show()

    @pyqtSlot()
    def login_slot(self):
        self.login_flag = self.check_login_data(self.user_edit.text(), self.password_edit.text())
        print(self.login_flag)
        if self.login_flag:
            self.toLog.emit("Авторизация выполнены")
            self.openApp.emit(self.user_edit.text().lower())
        else:
            self.toLog.emit("Ошибка авторизации")
            self.openApp.emit(self.user_edit.text().lower())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setFixedSize(200, 100)
            msg.setWindowTitle("Ошибка авторизации")
            msg.setText("Проверьте введенные данные:")
            msg.setInformativeText("Проверьте имя пользователя и пароль.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    @pyqtSlot()
    def reg_btn_slot(self):
        self.hide()
        self.register_window.show()

    @pyqtSlot()
    def exit_btn_slot(self):
        """Action for button "Cancel" """
        self.closeApp.emit()

