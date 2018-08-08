# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from widget import Ui_MainWindow

from utils import *
from model import PatternListModel, FileItemModel
from delegate import PatternDelegate, FileItemDelegate


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.total = 0

        pattern_model = PatternListModel()
        file_model = FileItemModel(pattern_model)

        self.lv_pattern.setItemDelegate(PatternDelegate())
        self.lv_pattern.setAcceptDrops(True)
        self.lv_pattern.setDropIndicatorShown(True)
        self.lv_pattern.setModel(pattern_model)
        self.tv_input.setAcceptDrops(True)
        self.tv_input.setDropIndicatorShown(True)
        self.tv_input.setModel(file_model)
        self.tv_input.setHeaderHidden(True)
        self.tv_input.setRootIsDecorated(False)
        self.tv_input.setItemDelegate(FileItemDelegate())
        self.tv_input.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tv_output.setModel(file_model)
        self.tv_output.setHeaderHidden(True)
        self.tv_output.setRootIsDecorated(False)
        self.tv_output.setItemDelegate(FileItemDelegate(file_convert))
        self.tv_output.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tv_output.setSelectionModel(self.tv_input.selectionModel())

        file_model.launched.connect(self.on_launched)
        file_model.progress.connect(self.on_progress)
        file_model.complete.connect(self.on_complete)
        file_model.dataChanged.connect(self.on_data_changed)

        self.btn_start.clicked.connect(file_model.execute)
        self.cb_preview.toggled.connect(lambda val: file_model.setAutoLoad(val))

    def on_launched(self, val):
        self.total = val
        self.pb_progress.setMaximum(0)
        self.pb_progress.setValue(0)
        self.btn_start.setEnabled(False)
        self.cb_preview.setEnabled(False)

    def on_progress(self, val):
        self.pb_progress.setMaximum(self.total)
        self.pb_progress.setValue(val)

    def on_complete(self):
        self.btn_start.setEnabled(True)
        self.cb_preview.setEnabled(True)
        self.pb_progress.setMaximum(1)
        self.pb_progress.setValue(1)

    def on_data_changed(self, *_):
        self.tv_input.expandAll()
        self.tv_output.expandAll()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
