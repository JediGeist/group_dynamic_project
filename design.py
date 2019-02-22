# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 565)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(70, 520, 681, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnBrowse = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnBrowse.setObjectName("btnBrowse")
        self.horizontalLayout.addWidget(self.btnBrowse)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setEnabled(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.videoWidget = QVideoWidget(self.centralWidget)
        self.videoWidget.setGeometry(QtCore.QRect(9, 9, 800, 480))
        self.videoWidget.setObjectName("videoWidget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.videoWidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 801, 481))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.playBtn = QtWidgets.QPushButton(self.centralWidget)
        self.playBtn.setEnabled(True)
        self.playBtn.setGeometry(QtCore.QRect(70, 490, 61, 31))
        self.playBtn.setObjectName("playBtn")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(130, 490, 561, 31))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.scrolLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.scrolLayout.setContentsMargins(11, 11, 11, 11)
        self.scrolLayout.setSpacing(6)
        self.scrolLayout.setObjectName("scrolLayout")
        self.fullScreen = QtWidgets.QPushButton(self.centralWidget)
        self.fullScreen.setGeometry(QtCore.QRect(690, 490, 61, 31))
        self.fullScreen.setObjectName("fullScreen")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnBrowse.setText(_translate("MainWindow", "Выбрать видео"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.playBtn.setText(_translate("MainWindow", "Ply"))
        self.fullScreen.setText(_translate("MainWindow", "full"))


from PyQt5.QtMultimediaWidgets import QVideoWidget
