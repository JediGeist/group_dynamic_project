import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий
import pickle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.gridspec as gridspec

from PyQt5 import QtWidgets
from PyQt5 import QtMultimediaWidgets
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QDir, Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QShortcut)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon, QKeySequence
from mplForWidget import MyMplCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

import design  # Это наш конвертированный файл дизайна

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        #Кнопки для проигрывания весь экран и запуска делаем неактивными
        self.fullScreen.setEnabled(False)
        self.playBtn.setEnabled(False)
        self.createGraph.setEnabled(False)

        #Слайдер начало
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.scrolLayout.setContentsMargins(0, 0, 0, 0)
        self.scrolLayout.addWidget(self.positionSlider)
        #Слайдер конец

        #Отрисовка графика начало
        self.paintGrph = QVBoxLayout(self.plot_widget)

        #Выполняем функцию для открытия видео
        self.btnBrowse.clicked.connect(self.open_video)

    #Функция для открытия видео
    def open_video(self):
        self.Video_Player = QtMultimediaWidgets.QVideoWidget(self.centralWidget)
        self.Video_Player.setObjectName("mediaPlayer")
        self.horizontalLayout_3.addWidget(self.Video_Player)
        self.Video_Player.show()
        self.mediaPlayer = QtMultimedia.QMediaPlayer()
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose video")
        #Если выбран правильный формат, то открываем видео
        if fileName != '':
                   self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
                   self.mediaPlayer.setVideoOutput(self.Video_Player)
                   self.fullScreen.setEnabled(True)
                   self.playBtn.setEnabled(True)
                   self.label_2.setText(os.path.basename(fileName))
                   self.playBtn.clicked.connect(self.play_video)
        self.fullScreen.clicked.connect(self.full_screen)
        self.createGraph.clicked.connect(self.read_data)

    #Функция для запуска видео
    def play_video(self):
        self.mediaPlayer.play()

    #Функция для выхода из полноэкранного режима
    def exitFullScreen(self):
        self.Video_Player.setFullScreen(False)

    #Функция для открытия полного экрана
    def full_screen(self):
        self.Video_Player.setFullScreen(True)

    #Функции для работы со скроллбаром начало
    def mediaStateChanged(self, state):
        if state == QMediaPlayer.StoppedState:
            self.exitFullScreen()
            self.createGraph.setEnabled(True)
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
    #Конец

    #Функция для чтения данных
    def read_data(self):
        path_to_data = "/Users/antonsavacenko/untitled/azart.pickle"
        with open(path_to_data, "rb") as f:
            data = pickle.load(f)
        self.print_graph(data)

    #Функция для отрисовки графика
    def print_graph(self, data):

        fig, axes = plt.subplots()

        plt.axis([0,70, -0.1, 1.1])

        xs = []
        value = []
        for i in range(len(data[0])):
            value += [data[0][i]]
            xs += [i]

        plt.plot(xs, value)

        self.canavas = MyMplCanvas(fig)
        self.paintGrph.addWidget(self.canavas)
        self.toolbar = NavigationToolbar(self.canavas, self)
        self.paintGrph.addWidget(self.toolbar)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
