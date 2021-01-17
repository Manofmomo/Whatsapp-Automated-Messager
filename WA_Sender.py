#!/usr/bin/env python3
from functools import partial
import sys
import os
from PyQt5 import uic
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtTest

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


__version__="0.1"
__author__="Dhruv Bhatia"
wa_spam=QApplication(sys.argv)
def number_mobile_checker(num):
    temp=str(num)
    num=""
    Handle=True
    for i in temp:
        if ord(i)>47 and ord(i)<58:
            num=num+i
        if i=='+':
            Handle=False
        if i==':':
            break

    i=0
    if num[0]=='0':
        i=1
        num=num[1:-1]
    if num[i]=='9' or num[i]=='8' or num[i]=='7':

        if Handle:
            if len(num)==10 and num[0]!="1":
                num="91"+num
        print(temp," --->> ",num)
        return int(num)
    else:
        return None


class WA_Spam_UI(QMainWindow):
    def __init__(self):
        super(WA_Spam_UI, self).__init__() # Call the inherited classes __init__ method
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
        WA_sender(bools, paths, message)



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

            WA_sender(bools, paths, message)


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
        wa_spam.processEvents()



def WA_sender(bools,paths,message):
    global view

    Send_Final,check_file,check_image=bools
    csv_path,file_path,image_path,selenium_path,test_num=paths
    textToSendList=list(message.split('\n'))
    try:
        input_file= open(csv_path)
    except:
        sys.exit("Please enter a valid csv file. ")
    csv_reader = csv.reader(input_file, delimiter=',')

    column_with_name=1
    column_with_number=2

    list_name_number=[]

    for row in csv_reader:

        temp=row[column_with_number-1]
        temp=number_mobile_checker(temp)
        list_name_number.append([str(row[column_with_name-1]),temp])
        total_num=len(list_name_number)

    try:
        temp_file= open('logfile.csv', mode='r')
        csv_reader_temp = csv.reader(temp_file, delimiter=',')
        row_count = len(list(csv_reader_temp))
        print("Will skip to the ",row_count)
        temp_file.close()
    except:
        row_count=0

    output_file= open('logfile.csv', mode='a',newline='')
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    if not Send_Final:
        list_name_number=[[list_name_number[0][0],number_mobile_checker(test_num)]]

    try:
        driver = webdriver.Chrome(selenium_path)
    except WebDriverException:
        options = Options()
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        driver = webdriver.Chrome(chrome_options = options, executable_path=selenium_path)


    driver.get('http://web.whatsapp.com')

    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Press OK after scanning QR code of Whatsapp")
    msgBox.setWindowTitle("QR Scan")
    msgBox.setStandardButtons(QMessageBox.Ok )
    returnValue = msgBox.exec_()

    actions = ActionChains(driver)
    print(list_name_number)
    for i in list(range(len(list_name_number))):
        if Send_Final:
            view.update_progress_bar(int((100*i)/total_num))
            if i<row_count:
                print("Skipped since row was already done last time")
                print("If this was not the case delete the logfile.csv")

                continue
        if list_name_number[i][1]==None:
            continue
        url="https://web.whatsapp.com/send?phone="+str(list_name_number[i][1])
        driver.get(url)


        try:
            wait = WebDriverWait(driver, 25, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,NoSuchElementException])
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_1awRl copyable-text selectable-text"]')))
            sending_box=driver.find_element_by_xpath("(//div[@class='_1awRl copyable-text selectable-text'])[2]")

        except:
            csv_writer.writerow([list_name_number[i][0],list_name_number[i][1],"Sending Failed"])
            continue


        for textToSend in textToSendList:
            sending_box.send_keys(textToSend.format(list_name_number[i][0])+Keys.CONTROL+Keys.ENTER)
        sending_box.send_keys(Keys.ENTER)
        QtTest.QTest.qWait(2000)

        if check_file:

            try:
                wait = WebDriverWait(driver, 25, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,NoSuchElementException])
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@title = "Attach"]')))
            except TimeoutException:
                csv_writer.writerow([list_name_number[i][0],list_name_number[i][1],"Only Message sent, file Failed"])
                continue

            attachment_box=driver.find_element_by_xpath('//div[@title = "Attach"]')

            attachment_box.click()
            image_box=driver.find_element_by_xpath('//input[@accept="*"]')
            image_box.send_keys(file_path)
            wait = WebDriverWait(driver, 10, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,NoSuchElementException])
            try:
                element = wait.until(EC.element_to_be_clickable((By.XPATH,'//span[@data-icon="send"]')))

                sending_box=driver.find_element_by_xpath('//span[@data-icon="send"]')
                sending_box.click()
            except TimeoutException:
                csv_writer.writerow([list_name_number[i][0],list_name_number[i][1],"Only Message sent, file Failed. Check File path"])
                continue
            QtTest.QTest.qWait(5000)

        if check_image:

            try:
                wait = WebDriverWait(driver, 25, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,NoSuchElementException])
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@title = "Attach"]')))
            except TimeoutException:
                csv_writer.wriTimeoutExceptionterow([list_name_number[i][0],list_name_number[i][1],"Image Failed"])
                continue

            attachment_box=driver.find_element_by_xpath('//div[@title = "Attach"]')

            attachment_box.click()
            image_box=driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            image_box.send_keys(image_path)
            wait = WebDriverWait(driver, 10, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,NoSuchElementException])
            try:
                element = wait.until(EC.element_to_be_clickable((By.XPATH,'//span[@data-icon="send"]')))

                sending_box=driver.find_element_by_xpath('//span[@data-icon="send"]')
                sending_box.click()
            except TimeoutException:
                csv_writer.writerow([list_name_number[i][0],list_name_number[i][1],"Image Failed. Check File path"])
                continue
            QtTest.QTest.qWait(5000)

        csv_writer.writerow([list_name_number[i][0],list_name_number[i][1],"Sent successfully"])
        output_file.flush()
        QtTest.QTest.qWait(4000)




    driver.quit()
    if Send_Final:
        Handle=True
        output_file.close()
        i=0
        while Handle and i<10:

            try:
                os.rename('logfile.csv','report'+str(i)+'.csv')
                Handle=False
                break
            except:
                i=i+1
                continue

        msgBox = QMessageBox()
        msgBox.setText(""" Task Ended, Please see the file report.csv
        for the report on the result of each individual task.
        """)
        msgBox.setWindowTitle("Thank You")
        msgBox.setStandardButtons(QMessageBox.Ok )

        sys.exit(msgBox.exec_())

    else:
        view.show()


def main():
    global view
    view = WA_Spam_UI()

    view.show()
    sys.exit(wa_spam.exec_())

if __name__ == '__main__':
    main()
