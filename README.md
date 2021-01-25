# Whatsapp-Automated-Messager
This is a automated Whatsapp message sender that is based on selenium and PYQT5 .
It is made to work with Indian Phone Numbers and can add extensions and filter out telephone numbers on its own.

#### Requirements:
For Running Python Code:
* Python >=3.5
* Python Modules required
 * pyqt5
 * selenium
 * functools
* Chrome Webdriver for selenium

You would require the name and number of the contacts in the first two rows of an excel file. This file should be exported as a csv file.


#### Setup (Python):

1. Fork the Github Repository
2. Download the chromedriver for your version of chrome

#### Setup (Windows):

1. Download and extract the zip file present in this [section](#Downloads)
2. Download the chromedriver for your version of chrome


### How to use:
* ##### Python:
Run the main.py file in the src folder.
This can be done by typing the following command in the src folder <br> `python3 main.py`

* ##### Windows:
Run the WA_sender.exe file present in the folder.

The following Window will popup

![Popup](https://github.com/Manofmomo/Whatsapp-Automated-Messager/blob/main/img/popup.png)

* Attachment Type:
 * Image: This checkbox should be ticked if you would like to attach a image file
 * File: This checkbox should be ticked if you would like to attach any document (pdf,zip,exe,docx and so on)

There are various sections where you are required to add the path to the file.
The patch can be added by clicking the + button next to the section
* File: Here the path to the file to attach shoud be added
* Image: Here the path to the image file should be added
* CSV: The csv file path should be added. It's first row should contain the name, and the second row should contain the phone number of the contact.
* Chromedriver: The path to the chromedriver for selenium should be added here.

* Test Ph. Number: Any phone number can be added here in order to send a test message. The number will be sent your message with the first name of the csv file. In case a csv file isn't added the name will be replaced with "test"

* Message: Here the whatsapp message to be sent can be added. Use {} where you would normally add the personalisation in the message.

### Downloads:

 * ##### Chromedriver:
It can be downloaded [here](https://chromedriver.chromium.org/)

* ##### Windows Builds:
They are hosted on Mega at the moment. The download links are available [here]()

### Known Bugs:

* Sometimes upon loading the WebWhatsapp, it skips to the next contact without sending the message. I do not know why this happens at the moment. If you can provide any information, feel free to open an issue [here](https://github.com/Manofmomo/Whatsapp-Automated-Messager/issues)

### Feedback:
For any feedback feel free to email me at bhatiadhruv2001nospam@gmail.com ( Remove nospam before sending me a mail )
