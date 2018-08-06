# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/main.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tv_output = QtWidgets.QTreeView(self.centralwidget)
        self.tv_output.setObjectName("tv_output")
        self.gridLayout.addWidget(self.tv_output, 1, 1, 1, 1)
        self.tv_input = QtWidgets.QTreeView(self.centralwidget)
        self.tv_input.setObjectName("tv_input")
        self.gridLayout.addWidget(self.tv_input, 1, 0, 1, 1)
        self.lv_pattern = QtWidgets.QListView(self.centralwidget)
        self.lv_pattern.setObjectName("lv_pattern")
        self.gridLayout.addWidget(self.lv_pattern, 0, 0, 1, 2)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pb_progress = QtWidgets.QProgressBar(self.centralwidget)
        self.pb_progress.setTextVisible(False)
        self.pb_progress.setObjectName("pb_progress")
        self.horizontalLayout_3.addWidget(self.pb_progress)
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setObjectName("btn_start")
        self.horizontalLayout_3.addWidget(self.btn_start)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FBX Renamer"))
        self.btn_start.setText(_translate("MainWindow", "Start"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

