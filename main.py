import sys  # 
import os  # 
import pickle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.gridspec as gridspec

from PyQt5 import QtWidgets
from PyQt5 import QtMultimediaWidgets
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QDir, Qt, QUrl, QTimer, QThread
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QShortcut)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon, QKeySequence
from mplForWidget import MyMplCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from reader import eegSmtReader
import feature_extraction as fexec
import model
import time
from multiprocessing import Process



import design  # 

t = eegSmtReader('/dev/ttyUSB0')

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # 
        # 
        super().__init__()
        self.setupUi(self)  # 

        #
        self.fullScreen.setEnabled(False)
        self.playBtn.setEnabled(False)
        self.createGraph.setEnabled(False)

        #
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.scrolLayout.setContentsMargins(0, 0, 0, 0)
        self.scrolLayout.addWidget(self.positionSlider)
        #

        self.shortcut = QShortcut(QKeySequence("q"), self)
        self.shortcut.activated.connect(self.exitFullScreen)



        #
        self.paintGrph = QVBoxLayout(self.plot_widget)

        self.initial()

        #
        self.btnBrowse.clicked.connect(self.open_video)

        self.OK.clicked.connect(self.oK_click)

    def initial(self):
        #
        self.Video_Player = QtMultimediaWidgets.QVideoWidget(self.videoWidget)
        self.Video_Player.setObjectName("mediaPlayer")
        self.horizontalLayout_3.addWidget(self.Video_Player)
        self.Video_Player.show()
        self.mediaPlayer = QtMultimedia.QMediaPlayer()
        self.thread = ThreadForRead(self.mediaPlayer)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

    #
    def open_video(self):
        self.lineEdit.setReadOnly(False)
        self.fullScreen.setEnabled(False)
        #
        for i in reversed(range(self.paintGrph.count())):
            self.paintGrph.itemAt(i).widget().setParent(None)
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose video")
        #
        if fileName != '':
                   self.mediaPlayer.setParent(None)
                   self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
                   self.mediaPlayer.setVideoOutput(self.Video_Player)
                   self.fullScreen.setEnabled(True)
                   self.playBtn.setEnabled(True)
                   self.lineEdit.clear()
                   self.lineEdit.setText(os.path.basename(fileName))
                   self.playBtn.clicked.connect(self.play_video)
        self.fullScreen.clicked.connect(self.full_screen)
        self.createGraph.clicked.connect(self.read_data)



    #
    def play_video(self):


        self.mediaPlayer.play()
        self.thread.start()
        print("end")



    def workWithData(self):
        #t = eegSmtReader('/dev/ttyUSB0')
        print("start read...")
        data = t.read_data(100000)
        time.sleep(0)
        print("end read...")
        dataFeature = fexec.get_fuature(data)
        path = "/Users/antonsavacenko/untitled/test.eegpic"
        self.write(dataFeature, path)

        md = model.get_model()
        pred = md.predict(dataFeature)
        path = "/Users/antonsavacenko/untitled/testRes.eegpic"
        self.write(pred, path)


    #
    def exitFullScreen(self):
        self.Video_Player.setFullScreen(False)
        self.Video_Player.setParent(None)
        self.initial()


    #
    def full_screen(self):
       self.Video_Player.setFullScreen(True)



    #
    def mediaStateChanged(self, state):
        if state == QMediaPlayer.StoppedState:
            t.read = False
            self.exitFullScreen()
            self.createGraph.setEnabled(True)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
    #

    #
    def read_data(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose file")
        #
        if fileName != '':
            path_to_data = fileName
            with open(path_to_data, "rb") as f:
                data = pickle.load(f)
            self.print_graph(data)

    #
    def print_graph(self, data):
        print(data)
        fig, axes = plt.subplots()

        plt.axis([0,70, -0.1, 1.1])

        xs = []
        value = []
        for i in range(len(data)):
            value += [data[i]]
            xs += [i]

        plt.plot(xs, value)

        #
        for i in reversed(range(self.paintGrph.count())):
            self.paintGrph.itemAt(i).widget().setParent(None)
        self.canavas = MyMplCanvas(fig)
        self.paintGrph.addWidget(self.canavas)
        self.toolbar = NavigationToolbar(self.canavas, self)
        self.paintGrph.addWidget(self.toolbar)

    #
    def oK_click(self):
        self.lineEdit.setReadOnly(True)

def write(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

class ThreadForRead(QThread):
    def __init__(self, mediaPlayer):
        super().__init__()
        self.mediaPlayer = mediaPlayer


    def run(self):
        print("start read...")
        data = t.read_data()
        time.sleep(0)
        with open("/Users/antonsavacenko/untitled/data_test.eegpic", 'wb') as f:
            pickle.dump(data, f)
        print("end read...")
        dataFeature = fexec.get_fuature(data)
        path = "/Users/antonsavacenko/untitled/test.eegpic"
        write(dataFeature, path)

        md = model.get_model()
        pred = md.predict(dataFeature)
        path = "/Users/antonsavacenko/untitled/testRes.eegpic"
        write(pred, path)

def main(): 
    app = QtWidgets.QApplication(sys.argv)  #
    window = ExampleApp()  #
    window.show()  #
    app.exec_()  #

if __name__ == '__main__':  #
    main()  #
