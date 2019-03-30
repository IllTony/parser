import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
import datetime

from login_module import UserLogin


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widg = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widg)
        self.v_lay = QtWidgets.QVBoxLayout()
        self.central_widg.setLayout(self.v_lay)

        # Action for file menu
        self.new_action = QtWidgets.QAction("&Новый")
        self.new_action.setStatusTip("Создать новый отчет")
        self.new_action.triggered.connect(self.new_action_slot)

        self.exit_action = QtWidgets.QAction("&Выход")
        self.exit_action.setStatusTip("Выход из программы")
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.exit_slot)

        self.choose_filedir_action = QtWidgets.QAction("Выбрать директорию")
        self.choose_filedir_action.setStatusTip("Выбрать директорию с ФГОС")
        self.choose_filedir_action.triggered.connect(self.choose_filedir_slot)

        # Action for help menu
        self.userguide_action = QtWidgets.QAction("Р&уководство пользователя")
        self.userguide_action.setStatusTip("Открыть руководство пользователя")
        self.userguide_action.setShortcut("F1")
        self.userguide_action.triggered.connect(self.userguide_slot)

        self.about_programm_action = QtWidgets.QAction("О& программе")
        self.about_programm_action.setStatusTip("Справка о программе")
        self.about_programm_action.triggered.connect(self.about_programm_slot)

        # Меню программы
        # Section menu - File
        self.file_menu = QtWidgets.QMenu()
        self.file_menu = self.menuBar().addMenu("Файл")
        self.file_menu.addAction(self.new_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.choose_filedir_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        # Section menu - Settings
        self.setting_menu = QtWidgets.QMenu()
        self.setting_menu = self.menuBar().addMenu("Настройки")

        # Section menu - Help
        self.help_menu = QtWidgets.QMenu()
        self.help_menu = self.menuBar().addMenu("Справка")
        self.help_menu.addAction(self.userguide_action)
        self.file_menu.addSeparator()
        self.help_menu.addAction(self.about_programm_action)

        # Interface for central window

        self.download_lay = QtWidgets.QHBoxLayout()

        self.download_label = QtWidgets.QLabel("Загрузить ФГОСы:")
        self.download_label.setFixedSize(110, 20)
        self.download_label.setAlignment(Qt.AlignLeft)

        self.download_edit = QtWidgets.QLineEdit()
        self.download_edit.setFixedSize(250, 20)

        self.download_btn = QtWidgets.QPushButton("...")
        self.download_btn.setFixedSize(30, 20)
        self.download_btn.clicked.connect(self.choose_filedir_slot)

        self.download_lay.addWidget(self.download_label)
        self.download_lay.addWidget(self.download_edit)
        self.download_lay.addWidget(self.download_btn)

        self.p_bar = QtWidgets.QProgressBar()

        self.report_label = QtWidgets.QLabel("Сформировать отчет:")
        self.report_label.setFixedSize(390, 40)
        self.report_label.setAlignment(Qt.AlignCenter)

        self.report_lay = QtWidgets.QHBoxLayout()
        self.report_box = QtWidgets.QGroupBox("Тип отчета")
        self.combine_report = QtWidgets.QCheckBox("Единый отчет")
        self.sep_report = QtWidgets.QCheckBox("Отдельный отчет")
        self.type_lay = QtWidgets.QVBoxLayout()
        self.type_lay.addWidget(self.combine_report)
        self.type_lay.addWidget(self.sep_report)
        self.report_box.setLayout(self.type_lay)
        self.report_btn = QtWidgets.QPushButton("Сформировать отчет")
        self.report_btn.setFixedSize(150, 30)
        self.report_lay.addWidget(self.report_box)
        self.report_lay.addWidget(self.report_btn)

        self.v_lay.addLayout(self.download_lay)
        self.v_lay.addSpacing(20)
        self.v_lay.addWidget(self.p_bar)
        self.v_lay.addSpacing(20)
        self.v_lay.addWidget(self.report_label)
        self.v_lay.addLayout(self.report_lay)
        self.v_lay.setAlignment(Qt.AlignCenter)

        self.file_dir = ""

        self.login_window = UserLogin()

    def _connects(self):
        self.login_window.closeApp.connect(self.close_app_slot)

    @pyqtSlot()
    def close_app_slot(self):
        QtWidgets.QApplication.exit()

    @pyqtSlot()
    def new_action_slot(self):
        print("new action")
        return

    @pyqtSlot()
    def exit_slot(self):
        QtWidgets.QApplication.quit()

    @pyqtSlot()
    def choose_filedir_slot(self):
        print("choose filedir action")
        self.file_dir = QtWidgets.QFileDialog.getExistingDirectory()
        self.download_edit.setText(self.file_dir)
        return

    @pyqtSlot()
    def userguide_slot(self):
        print("userguide action")
        return

    @pyqtSlot()
    def about_programm_slot(self):
        print("about programm action")
        global help_window
        help_window = QtWidgets.QWidget()
        help_window.setWindowTitle("О программе")
        help_window.setWindowModality(Qt.ApplicationModal)
        help_window.setAttribute(Qt.WA_DeleteOnClose, True)
        help_window.setFixedSize(400, 100)
        info_label = QtWidgets.QLabel("Programm was developed by Schetinin G. A. and Illarionov A.A. \n"
                                      "04.2019 \n"
                                      "All rights reserved!")
        info_label.setFixedSize(390, 80)
        info_label.setAlignment(Qt.AlignCenter)
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(info_label)
        help_window.setLayout(lay)
        help_window.show()
        return


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Обработчик ФГОС")
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()