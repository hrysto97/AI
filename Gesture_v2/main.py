# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 18:21:11 2019

@author: simeon.pavlov & hristo.dinkov
"""
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from views import UIProgram


if __name__ == "__main__":

    app=QApplication(sys.argv)
    window=UIProgram()
    app_icon = QtGui.QIcon()
    window.showFullScreen()
    window.setWindowTitle('Gesture Recognition')
    window.setWindowIcon(QIcon(r"icons8-easy-48.png"))
    window.show()

    exit(app.exec_())