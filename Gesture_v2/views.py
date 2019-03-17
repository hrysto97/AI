# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 14:45:23 2019

@author: simeon.pavlov & hristo.dinkov
"""
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog,QWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage,QPixmap,QIcon
import time
import threading
import preview
import sys
import subprocess

class UIProgram(QMainWindow):
        
    def __init__(self):
        
        super(UIProgram,self).__init__()
        loadUi("main.ui",self)
        
        self.createButton.clicked.connect(self.createUI)
    
        self.startButton.clicked.connect(self.start_process)
        self.stopButton.clicked.connect(self.stop_process)
        
        self.git_thread = ProcessThread()
    
    def start_process(self):
        print("hi")
        self.statusbar.setStyleSheet("""
        QWidget {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            }
        """)
        self.statusBar().showMessage("Running")
        
        self.git_thread.start()
        
    def stop_process(self):
        self.statusbar.setStyleSheet("""
        QWidget {
            background-color: #f44336 ;
            color: white;
            font-weight: bold;
            }
        """)
        self.statusBar().showMessage("Stopped")
        
        self.git_thread.stop()
    
    def createUI(self):
        self.create_dialog=Create_Dialog()
        self.create_dialog.show()
        
        

class Create_Dialog(QMainWindow):
    def __init__(self):
        
        super(Create_Dialog,self).__init__()
        loadUi("create.ui",self)
        self.showFullScreen()
        self.setWindowIcon(QIcon(r"icons8-easy-48.png"))
        
        self.backButton.clicked.connect(self.close)
        self.trainButton.clicked.connect(self.training)
        self.recordButton.clicked.connect(self.counting)
        self.previewButton.clicked.connect(self.camera)
        
        self.git_thread = CreateThread()
    
    def camera(self):
        subprocess.call(['python', 'preview.py'])
    def training(self):
        print("hi")
        self.statusbar.setStyleSheet("""
        QWidget {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            }
        """)
        self.statusBar().showMessage("Training...")
        
        self.git_thread.start()
    
    def counting(self):
        timer=None
        
        self.counting_dialog=Recording_Dialog()
        self.counting_dialog.show()
        
        self.recording_3()
        
    def recording_3(self):
        self.counting_dialog.label.setText("3")
        timer = threading.Timer(1, self.recording_2)
        timer.start()
    
    def recording_2(self):
        self.counting_dialog.label.setText("2")
        timer = threading.Timer(1, self.recording_1)
        timer.start()
        
    def recording_1(self):
        self.counting_dialog.label.setText("1")
        timer = threading.Timer(1, self.recording_message)
        timer.start()
        
    def recording_message(self):
        self.counting_dialog.label.setText("LOADING...")
        timer = threading.Timer(0.1, self.recording_recording)
        timer.start()
        
    def recording_recording(self):
        choice = str(self.comboBox.currentText())
        if choice=="Lights":
            subprocess.call(['python', 'record.py', 'records/lights', '15'])
        elif choice=='Start Music':
            subprocess.call(['python', 'record.py', 'records/start_music', '15'])
        elif choice=='Stop Music':
            subprocess.call(['python', 'record.py', 'records/stop_music', '15'])
        elif choice=='Greeting':
            subprocess.call(['python', 'record.py', 'records/greeting', '15'])
        elif choice=='Random':
            subprocess.call(['python', 'record.py', 'records/random', '15'])
        elif choice=='Empty':
            subprocess.call(['python', 'record.py', 'records/empty', '15'])
        timer = threading.Timer(0.01, self.close_recording)
        timer.start()
    def close_recording(self):
        self.counting_dialog.close()

        self.statusbar.setStyleSheet("""
            QWidget {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                }
            """)
            
        self.statusBar().showMessage("Recorded successfully!")
    
class Recording_Dialog(QMainWindow):
    def __init__(self):
        
        super(Recording_Dialog,self).__init__()
        loadUi("counting.ui",self)
        self.showFullScreen()
        self.setWindowIcon(QIcon(r"icons8-easy-48.png"))


class ProcessThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.threadactive = True

    def run(self):
        self.threadactive = True
        self.p = subprocess.Popen(['python', 'run.py', 'models/model1.h5'])
        
    def stop(self):
        print("stop")
        self.p.kill()
        self.threadactive = False
        self.wait()
        
class CreateThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.threadactive = True

    def run(self):
        self.threadactive = True
        self.p = subprocess.call(['python', 'train.py', 'models/model1.h5', 'records/lights', 'records/random', 'records/start_music', 'records/stop_music', 'records/greeting', 'records/empty'])
        
    def stop(self):
        print("stop")
        self.threadactive = False
        self.wait()