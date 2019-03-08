import sys  # 
import os  # 
import pickle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.gridspec as gridspec

from PyQt5 import QtWidgets
from PyQt5 import QtCore
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

t = eegSmtReader('/dev/tty.usbserial-AL027NKE')

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # 
        # 
        super().__init__()
        self.setupUi(self)  # 

        #
        self.fullScreen.setEnabled(False)
        self.playBtn.setEnabled(False)

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
        self.createGraph.clicked.connect(self.read_data)

        #
        self.paintGrph = QVBoxLayout(self.plot_widget)

        #
        self.initial()

        #
        self.btnBrowse.clicked.connect(self.open_video)

        self.OK.clicked.connect(self.oK_click)

    def initial(self):
        #
        self.Video_Player = QVideoWidgetExit(self.videoWidget)

        self.Video_Player.setObjectName("mediaPlayer")

        self.horizontalLayout_3.addWidget(self.Video_Player)
        self.Video_Player.show()
        self.mediaPlayer = QtMultimedia.QMediaPlayer()
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
        filter = "mp4(*.mp4)"


        path = "./"
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(QFileDialog(), "Choose video", path, filter)
        #
        if fileName != '':
                   self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
                   self.mediaPlayer.setVideoOutput(self.Video_Player)
                   self.fullScreen.setEnabled(True)
                   self.playBtn.setEnabled(True)
                   self.lineEdit.clear()
                   self.thread = ThreadForRead(self.mediaPlayer, self.lineEdit)
                   self.lineEdit.setText(os.path.basename(fileName))
                   self.playBtn.clicked.connect(self.play_video)
        self.fullScreen.clicked.connect(self.full_screen)




    #
    def play_video(self):
        self.mediaPlayer.play()
        t.read = True
        self.thread.start()
        print("end")

    #
    def exitFullScreen(self):
        self.Video_Player.setFullScreen(False)

    #
    def full_screen(self):
       self.Video_Player.setFullScreen(True)
       self.Video_Player.flag = False

    #
    def mediaStateChanged(self, state):
        if state == QMediaPlayer.StoppedState:
            t.read = False
            self.exitFullScreen()
            self.Video_Player.setParent(None)
            self.initial()


    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        if self.Video_Player.flag == True:
            self.exitFullScreen()
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
    #

    #
    def read_data(self):
        filter = "eegpic(*.eegpic)"

        if "save" in os.listdir("./"):
            path = "./save/"
        else:
            path = "./"
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(QFileDialog(), "Choose file", path, filter)
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
    def __init__(self, mediaPlayer, lineEdit):
        super().__init__()
        self.mediaPlayer = mediaPlayer
        self.lineEdit = lineEdit


    def run(self):
        print("start read...")
        data = t.read_data()
        time.sleep(0)


        if "save" not in os.listdir("."):
            os.mkdir("./save")

        if "data" not in os.listdir("./save"):
            os.mkdir("./save/data")
        if "prediction" not in os.listdir("./save"):
            os.mkdir("./save/prediction")
        if "feature" not in os.listdir("./save"):
            os.mkdir("./save/feature")


        with open(f"./save/data/{self.lineEdit.text()}.eegpic", 'wb') as f:
            pickle.dump(data, f)
        print("end read...")
        dataFeature = fexec.get_feature(data) + np.random.randint(50) / 100 * ((-1)^np.random.randint(2))
        path = f"./save/feature/{self.lineEdit.text()}.eegpic"
        write(dataFeature, path)

        md = model.get_model()
        pred = md.predict(dataFeature)
        path = f"./save/prediction/{self.lineEdit.text()}.eegpic"
        write(pred, path)

class QVideoWidgetExit(QVideoWidget):
    def __init__(self, qwidget):
        super().__init__()
        self.Video_Player = qwidget
        self.flag = False


    def keyPressEvent(self, event):
        if event.key() == QKeySequence("Esc"):
            self.flag = True


def main(): 
    app = QtWidgets.QApplication(sys.argv)  #
    window = ExampleApp()  #
    window.show()  #
    app.exec_()  #

if __name__ == '__main__':  #
    main()  #
