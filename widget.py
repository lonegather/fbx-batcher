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
        self.gridLayout.addWidget(self.tv_output, 2, 1, 1, 1)
        self.lv_pattern = QtWidgets.QListView(self.centralwidget)
        self.lv_pattern.setObjectName("lv_pattern")
        self.gridLayout.addWidget(self.lv_pattern, 0, 0, 1, 2)
        self.tv_input = QtWidgets.QTreeView(self.centralwidget)
        self.tv_input.setObjectName("tv_input")
        self.gridLayout.addWidget(self.tv_input, 2, 0, 1, 1)
        self.pb_progress = QtWidgets.QProgressBar(self.centralwidget)
        self.pb_progress.setTextVisible(False)
        self.pb_progress.setObjectName("pb_progress")
        self.gridLayout.addWidget(self.pb_progress, 1, 0, 1, 2)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(2, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.le_output = QtWidgets.QLineEdit(self.centralwidget)
        self.le_output.setObjectName("le_output")
        self.horizontalLayout.addWidget(self.le_output)
        self.btn_browse = QtWidgets.QPushButton(self.centralwidget)
        self.btn_browse.setObjectName("btn_browse")
        self.horizontalLayout.addWidget(self.btn_browse)
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setObjectName("btn_start")
        self.horizontalLayout.addWidget(self.btn_start)
        self.cb_preview = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_preview.setChecked(True)
        self.cb_preview.setObjectName("cb_preview")
        self.horizontalLayout.addWidget(self.cb_preview)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        self.label.setText(_translate("MainWindow", "Output To:"))
        self.btn_browse.setText(_translate("MainWindow", "Browse"))
        self.btn_start.setText(_translate("MainWindow", "Rename"))
        self.cb_preview.setText(_translate("MainWindow", "Preview Takes"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

