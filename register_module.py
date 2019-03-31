from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QGridLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
import json
import hashlib


class UserRegister(QWidget):
    registerDone = pyqtSignal()

    def __init__(self):
        """Конструктор класса UserRegister, иницииализация элементов и переменных"""
        super().__init__()

        # Describing interface's elements
        self.v_lay = QVBoxLayout()

        self.user_label = QLabel("Имя пользователя:")
        self.user_label.setFixedSize(115, 30)
        self.user_label.setAlignment(Qt.AlignLeft)

        self.password_label = QLabel("Введите пароль:")
        self.password_label.setFixedSize(115, 30)
        self.password_label.setAlignment(Qt.AlignLeft)

        self.re_password_label = QLabel("Подтвердите пароль:")
        self.re_password_label.setFixedSize(115, 30)
        self.re_password_label.setAlignment(Qt.AlignLeft)

        self.user_edit = QLineEdit()
        self.user_edit.setFixedSize(190, 30)
        self.password_edit = QLineEdit()
        self.password_edit.setFixedSize(190, 30)
        self.re_password_edit = QLineEdit()
        self.re_password_edit.setFixedSize(190, 30)

        self.create_btn = QPushButton("Создать")
        self.create_btn.setFixedSize(160, 30)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setFixedSize(160, 30)

        self.grid_lay = QGridLayout()
        self.grid_lay.addWidget(self.user_label, 0, 0)
        self.grid_lay.addWidget(self.user_edit, 0, 1)
        self.grid_lay.addWidget(self.password_label, 1, 0)
        self.grid_lay.addWidget(self.password_edit, 1, 1)
        self.grid_lay.addWidget(self.re_password_label, 2, 0)
        self.grid_lay.addWidget(self.re_password_edit, 2, 1)

        self.grid_btn_lay = QGridLayout()
        self.grid_btn_lay.addWidget(self.create_btn, 0, 0)
        self.grid_btn_lay.addWidget(self.cancel_btn, 0, 1)

        self.v_lay.addLayout(self.grid_lay)
        self.v_lay.addLayout(self.grid_btn_lay)
        self.setLayout(self.v_lay)

        self._connects()
        self.creation_flag = False
        self.filename = "authorised_data.json"
        self.authorised_data = self.load_authorised_data()

    def _connects(self):
        """Describe all connects for signal and slots for UserLogin class"""
        self.create_btn.clicked.connect(self.create_user_slot)
        self.cancel_btn.clicked.connect(self.cancel_btn_slot)

    @pyqtSlot()
    def create_user_slot(self):
        """Create user with hashing password"""
        self.check_register_data()
        if self.creation_flag:
            user_str = self.user_edit.text()
            password_str = self.password_edit.text()
            self.authorised_data[user_str.lower()] = hashlib.sha1(password_str.encode('utf-8')).hexdigest()
            self.write_authorised_data()
            self.registerDone.emit()
            self.close()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setFixedSize(200, 100)
            msg.setWindowTitle("Ошибка создания пользователя")
            msg.setText("Проверьте введенные данные:")
            msg.setInformativeText("Пользователь с таким именем уже существует \n"
                                   "или проверьте правильность паролей")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def cancel_btn_slot(self):
        """Action for button "Cancel" """
        self.registerDone.emit()
        self.close()

    def check_register_data(self):
        """Check username and password in LineEdit"""
        if self.user_edit.text().lower() in self.authorised_data.keys() or \
                        self.user_edit.text() == "" or self.password_edit.text() == "":
            self.creation_flag = False
        else:
            if self.password_edit.text() == self.re_password_edit.text():
                self.creation_flag = True
            else:
                self.creation_flag = False

    def load_authorised_data(self):
        """Load authorised data from json file"""
        with open(self.filename, 'r') as file_object:
            return json.load(file_object)

    def write_authorised_data(self):
        """Write authorised data to json file"""
        with open(self.filename, 'w') as file_object:
            json.dump(self.authorised_data, file_object)