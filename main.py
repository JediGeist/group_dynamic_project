import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий

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

        #shortcut для того, чтобы свернуть видео
        self.shortcut = QShortcut(QKeySequence("Esc"), self)
        self.shortcut.activated.connect(self.exitFullScreen)

        #Слайдер начало
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.scrolLayout.setContentsMargins(0, 0, 0, 0)
        self.scrolLayout.addWidget(self.positionSlider)
        #Слайдер конец

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
                   self.playBtn.clicked.connect(self.play_video)
        self.fullScreen.clicked.connect(self.full_screen)

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
            self.Video_Player.setFullScreen(False)
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
    #Конец


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
