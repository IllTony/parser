import os
import datetime

from PyQt5.QtCore import QThread, QMutex, pyqtSlot


class LogThread(QThread):
    def __init__(self):
        super().__init__()
        self.log_dir = "logs"
        self.log_name = ""
        self.running = False
        self.logs_buffer = []
        self.mutex = QMutex()

    def run(self):
        self.running = True
        self.logs_buffer = []
        self.check_log_dir()
        self.create_file_name()
        with open(self.log_name, 'w') as log_object:
            while self.running:
                if self.logs_buffer:
                    self.mutex.lock()
                    for log in self.logs_buffer:
                        log_object.write(log + '\n')
                    self.logs_buffer = []
                    self.mutex.unlock()
        return

    def check_log_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def create_file_name(self):
        today = datetime.datetime.today()
        self.log_name = self.log_dir + "\\" + today.strftime("%Y-%m-%d-%H.%M.%S") + '.txt'

    @pyqtSlot(str)
    def append_log(self, log_str):
        self.mutex.lock()
        self.logs_buffer.append(log_str)
        self.mutex.unlock()

