import WhatsSender_GUI
from PyQt5.QtWidgets import QApplication
import WA_sender
import sys

__version__="0.1"
__author__="Dhruv Bhatia"
myapp=QApplication(sys.argv)

def main():
    view=WhatsSender_GUI.WhatsSender_GUI()

    print("1",view)
    view.show()
    sys.exit(myapp.exec_())

if __name__ == '__main__':
    main()
