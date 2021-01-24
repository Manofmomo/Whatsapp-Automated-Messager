#!/usr/bin/env python3
import os
import csv
from Number_fixer import phone_number_fixer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from PyQt5.QtWidgets import QMessageBox

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5 import QtTest



def WA_sender(bools,paths,message,view):

    Send_Final,check_file,check_image=bools
    csv_path,file_path,image_path,selenium_path,test_num=paths
    textToSendList=list(message.split('\n'))
    Test_no_file=False
    try:
        input_file= open(csv_path)
        csv_reader = csv.reader(input_file, delimiter=',')

    except:
        if Send_Final:
            view.dialog_box("Error","Press enter valid csv file")
            return
        else:
            Test_no_file=True


    column_with_name=1
    column_with_number=2

    list_name_number=[]
    if not Test_no_file:

        for row in csv_reader:

            temp=row[column_with_number-1]
            temp=phone_number_fixer(temp)
            list_name_number.append([str(row[column_with_name-1]),temp])
            total_num=len(list_name_number)

        try:
            temp_file= open('logfile.csv', mode='r')
            csv_reader_temp = csv.reader(temp_file, delimiter=',')
            row_count = len(list(csv_reader_temp))
            print("Will skip to the ",row_count," entry")
            print("Skipped since row was already done last time")
            print("If this was not the case delete the logfile.csv")

            temp_file.close()
        except:
            row_count=0

    output_file= open('logfile.csv', mode='a',newline='')
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    if not Send_Final:
        if Test_no_file:
                list_name_number=[["Test",phone_number_fixer(test_num)]]
        else:
            list_name_number=[[list_name_number[0][0],phone_number_fixer(test_num)]]

    try:
        driver = webdriver.Chrome(selenium_path)
    except WebDriverException:
        options = Options()
        #issues with chrome location on windows machines
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        driver = webdriver.Chrome(chrome_options = options, executable_path=selenium_path)


    driver.get('http://web.whatsapp.com')
    view.dialog_box("QR Scan","Press OK after scanning QR code of Whatsapp","Information")

    actions = ActionChains(driver)
    print(list_name_number)
    for i in list(range(len(list_name_number))):
        if Send_Final:
            view.update_progress_bar(int((100*i)/total_num))
            if i<row_count:

                continue
        if list_name_number[i][1]==None:
            continue
        url="https://web.whatsapp.com/send?phone="+str(list_name_number[i][1])
        driver.get(url)
        try:
            wait = WebDriverWait(driver, 50, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,NoSuchElementException])
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_1awRl copyable-text selectable-text"]')))
            sending_box=driver.find_element_by_xpath("(//div[@class='_1awRl copyable-text selectable-text'])[2]")

        except:
            if (("Phone number shared via url is invalid") in driver.page_source):
                csv_writer.writerow([list_name_number[i][0],list_name_number[i][1],"Number Invalid"])
                continue
            else:
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

        view.final_message_box()

    else:
        view.show()
