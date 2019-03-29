# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/ylhu/Documents/workspace/Renamer/resources/main.ui'
#
# Created: Thu Aug 09 16:52:19 2018
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tv_output = QtGui.QTreeView(self.centralwidget)
        self.tv_output.setObjectName("tv_output")
        self.gridLayout.addWidget(self.tv_output, 2, 1, 1, 1)
        self.lv_pattern = QtGui.QListView(self.centralwidget)
        self.lv_pattern.setObjectName("lv_pattern")
        self.gridLayout.addWidget(self.lv_pattern, 0, 0, 1, 2)
        self.tv_input = QtGui.QTreeView(self.centralwidget)
        self.tv_input.setObjectName("tv_input")
        self.gridLayout.addWidget(self.tv_input, 2, 0, 1, 1)
        self.pb_progress = QtGui.QProgressBar(self.centralwidget)
        self.pb_progress.setTextVisible(False)
        self.pb_progress.setObjectName("pb_progress")
        self.gridLayout.addWidget(self.pb_progress, 1, 0, 1, 2)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(2, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.le_output = QtGui.QLineEdit(self.centralwidget)
        self.le_output.setObjectName("le_output")
        self.horizontalLayout_2.addWidget(self.le_output)
        self.btn_browse = QtGui.QPushButton(self.centralwidget)
        self.btn_browse.setObjectName("btn_browse")
        self.horizontalLayout_2.addWidget(self.btn_browse)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cb_preview = QtGui.QCheckBox(self.centralwidget)
        self.cb_preview.setChecked(True)
        self.cb_preview.setObjectName("cb_preview")
        self.horizontalLayout.addWidget(self.cb_preview)
        self.btn_start = QtGui.QPushButton(self.centralwidget)
        self.btn_start.setObjectName("btn_start")
        self.horizontalLayout.addWidget(self.btn_start)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "FBX Renamer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Output To:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_browse.setText(QtGui.QApplication.translate("MainWindow", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_preview.setText(QtGui.QApplication.translate("MainWindow", "Preview Takes", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_start.setText(QtGui.QApplication.translate("MainWindow", "Rename", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))

