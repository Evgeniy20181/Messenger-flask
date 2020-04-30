from datetime import datetime

import requests
from PyQt5 import QtWidgets,QtCore
import clientui

class MessengerWindow(QtWidgets.QMainWindow,clientui.Ui_MainWindow):
    def addText(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.last_message_time = 0
        self.pushButton.pressed.connect(self.sendMessage)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getUpdates)
        self.timer.start(1000)
    def getUpdates(self):
        responce = requests.get(f'http://localhost:5000/history',
                                params={'after': self.last_message_time})
        data = responce.json()
        for message in data['messages']:
            beaty_time = datetime.fromtimestamp(message['time'])
            beaty_time = beaty_time.strftime('%Y/%m/%d %H:%M:%S')
            self.addText(f'{beaty_time} {message["username"]} {message["text"]}')
            self.addText('')
            self.last_message_time = message['time']
    def sendMessage(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.textEdit.toPlainText()
        if not username:
            self.addText('ERROR: username in empty!')
            return
        if not password:
            self.addText('ERROR: password in empty!')
            return
        if not text:
            self.addText('ERROR: text in empty!')
            return
        responce = requests.post('http://localhost:5000/send',
                                     json={"username": username, "password": password, "text": text})
        if not  responce.json()['ok']:
            self.addText('ERROR: Access denided!')
            return
        self.textEdit.clear()
        self.textEdit.repaint()
            #https://www.youtube.com/watch?v=45OYwgmWqmc        -57:14
app = QtWidgets.QApplication([])
window = MessengerWindow()
window.show()
app.exec()