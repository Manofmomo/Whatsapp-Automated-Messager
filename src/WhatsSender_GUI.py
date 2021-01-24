
from functools import partial
from PyQt5 import uic
import sys
from WA_sender import WA_sender
from PyQt5.QtWidgets import QApplication,QProgressBar
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import Qt


class WhatsSender_GUI(QMainWindow):
    def __init__(self):
        super(WhatsSender_GUI, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('WhatsappMainDialog.ui', self) # Load the .ui file
        self.progressBar = self.findChild(QProgressBar,'progress')
        self.progressBar.setValue(0)
        self.selenium_path.setText("chromedriver")

        self.info_popup()
        self.connect_signals()


        self.show() # Show the GUI


    def connect_signals(self):
        self.add_path_file.clicked.connect(partial(self.openFileNameDialog,self.file_path))
        self.add_path_image.clicked.connect(partial(self.openFileNameDialog,self.image_path))
        self.add_path_csv.clicked.connect(partial(self.openFileNameDialog,self.csv_path))
        self.add_path_selenium.clicked.connect(partial(self.openFileNameDialog,self.selenium_path))
        self.Send_Test.clicked.connect(self.test_clicked)
        self.Send_Final.clicked.connect(self.final_clicked)


    def test_clicked(self):
        Send_Final=False
        bools=[Send_Final,self.check_file.isChecked(),self.check_image.isChecked()]
        paths=[self.csv_path.text(),self.file_path.text(),self.image_path.text(),self.selenium_path.text(),self.test_num.text()]
        paths=[str(i) for i in paths]
        message=str(QPlainTextEdit.toPlainText(self.message))

        print("Test clicked")
        WA_sender(bools, paths, message,self)



    def final_clicked(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Are You Sure?")
        msgBox.setWindowTitle("Confirm To Send")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec_()
        if returnValue == QMessageBox.Ok:
            print('Sending...')
            Send_Final=True
            bools=[Send_Final,self.check_file.isChecked(),self.check_image.isChecked()]
            paths=[self.csv_path.text(),self.file_path.text(),self.image_path.text(),self.selenium_path.text(),self.test_num.text()]
            bools=[bool(i) for i in bools]
            paths=[str(i) for i in paths]
            message=str(QPlainTextEdit.toPlainText(self.message))

            WA_sender(bools, paths, message,self)


    def info_popup(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(""" Hello, This is a utility to send personalised Whatsapp messages automatically.
        Create a csv file with the Name and Phone number as the first two columns.
        Add paths to an image or any file if you want an attachment to be sent along with your message.
        The test number will be send a message using the first name of your csv file.
        Ignore the chrome path, that is mainly for debugging.
        Once you are happy with the test, press send Final. After this messages will start sending on its own.
        """)
        msgBox.setWindowTitle("How to use")
        msgBox.setStandardButtons(QMessageBox.Ok )
        returnValue = msgBox.exec_()

    def setDisplayText(self,display_obj,text):
        display_obj.setText(text)
        display_obj.setFocus()


    def openFileNameDialog(self,display_obj):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, okPressed= QFileDialog.getOpenFileName(self,"Add Path", "","All Files (*);;PNG Files (*.png);;CSV Files (*.csv)", options=options)
        if okPressed:
            self.setDisplayText(display_obj,fileName)

    def update_progress_bar(self,value):
        self.progressBar = self.findChild(QProgressBar,'progress')
        self.progressBar.setValue(value)
        QApplication.processEvents()

    def final_message_box(self):
        msgBox = QMessageBox()
        msgBox.setText(""" Task Ended, Please see the file report.csv
        for the report on the result of each individual task.
        """)
        msgBox.setWindowTitle("Thank You")
        msgBox.setStandardButtons(QMessageBox.Ok )

        sys.exit(msgBox.exec_())

    def dialog_box(self,title,text,icon="Error"):
        msgBox = QMessageBox()
        if icon=="Error":
            msgBox.setIcon(QMessageBox.Error)
        else:
            msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok )
        msgBox.exec_()
        return None
