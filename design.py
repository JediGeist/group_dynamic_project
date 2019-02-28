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
        MainWindow.resize(1420, 565)
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
        self.createGraph = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.createGraph.setEnabled(True)
        self.createGraph.setObjectName("createGraph")
        self.horizontalLayout.addWidget(self.createGraph)
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
        self.plot_widget = QtWidgets.QWidget(self.centralWidget)
        self.plot_widget.setGeometry(QtCore.QRect(819, 9, 591, 481))
        self.plot_widget.setObjectName("plot_widget")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(950, 510, 41, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(1000, 510, 351, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.OK = QtWidgets.QPushButton(self.centralWidget)
        self.OK.setGeometry(QtCore.QRect(1360, 500, 51, 41))
        self.OK.setObjectName("OK")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnBrowse.setText(_translate("MainWindow", "choose video"))
        self.createGraph.setText(_translate("MainWindow", "create graph"))
        self.playBtn.setText(_translate("MainWindow", "Ply"))
        self.fullScreen.setText(_translate("MainWindow", "full"))
        self.label.setText(_translate("MainWindow", "Name:"))
        self.OK.setText(_translate("MainWindow", "Ok"))


from PyQt5.QtMultimediaWidgets import QVideoWidget
