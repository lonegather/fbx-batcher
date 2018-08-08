# -*- coding: utf-8 -*-

import os
import sys
import json
import xlrd
import subprocess
from PyQt5.QtCore import pyqtSignal, QAbstractListModel, QModelIndex, Qt, QThread
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from utils import *


class FileItem(QStandardItem):

    def __init__(self, text):
        self.path = text
        self.path_new = text
        self.loaded = False
        self.executed = False
        super(FileItem, self).__init__(os.path.basename(self.path))
        self.setEditable(False)

    def data(self, role=None, *args, **kwargs):
        if role == file_convert:
            return os.path.basename(self.path_new)
        elif role == item_height:
            return 25
        elif role == item_color:
            return '#999' if self.path == self.path_new else '#00f'
        elif role == item_background:
            return '#ddd'
        else:
            return super(FileItem, self).data(role)

    def apply(self, text):
        self.path_new = os.path.join(os.path.dirname(self.path), text).replace('\\', '/')


class TakeItem(QStandardItem):

    def __init__(self, text):
        super(TakeItem, self).__init__(text)
        self.setEditable(False)
        self.new = text

    def data(self, role=None, *args, **kwargs):
        if role == file_convert:
            return self.new
        elif role == item_height:
            return 20
        elif role == item_color:
            return '#999' if self.text() == self.new else '#00f'
        elif role == item_background:
            return '#eee'
        else:
            return super(TakeItem, self).data(role)

    def apply(self, text):
        self.new = text


class PatternListModel(QAbstractListModel):

    def __init__(self, parent=None):
        super(PatternListModel, self).__init__(parent)
        self.patterns = []

    def rowCount(self, *_):
        return len(self.patterns)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return '%s -> %s' % self.patterns[index.row()]
        elif role == pattern_exp:
            return self.patterns[index.row()][0]
        elif role == pattern_rpl:
            return self.patterns[index.row()][1]

    def supportedDropActions(self):
        return Qt.CopyAction

    def flags(self, index):
        default_flags = super(PatternListModel, self).flags(index)
        return Qt.ItemIsDropEnabled | default_flags

    def mimeTypes(self):
        return ['text/uri-list']

    def dropMimeData(self, data, action, row, column, parent):
        file_path = data.urls()[0].toLocalFile()
        try:
            file_data = xlrd.open_workbook(file_path)
        except xlrd.XLRDError:
            print('File format incorrect.')
            return False

        table = file_data.sheets()[0]
        old = table.col_values(0)
        new = table.col_values(1)
        self.patterns = []
        for i in range(len(old)):
            self.patterns.append((old[i], new[i]))

        self.dataChanged.emit(QModelIndex(), QModelIndex())

        return True

    def pattern_data(self):
        patterns = {}
        for i in range(self.rowCount()):
            index = self.index(i)
            exp = self.data(index, pattern_exp)
            rpl = self.data(index, pattern_rpl)
            if exp not in patterns:
                patterns[exp] = rpl
        return json.dumps(patterns)


class FileItemModel(QStandardItemModel):

    launched = pyqtSignal(int)
    progress = pyqtSignal(int)
    complete = pyqtSignal()

    def __init__(self, pattern_model, parent=None):
        super(FileItemModel, self).__init__(parent)
        self.pattern_model = pattern_model
        self.pattern_model.dataChanged.connect(self.on_data_changed)
        self.file_thread = None
        self.auto_load = True
        self.file_loaded = 0
        self.exe_count = 0

    def setAutoLoad(self, val):
        self.auto_load = val

    def columnCount(self, *_):
        return 1

    def supportedDropActions(self):
        return Qt.CopyAction

    def flags(self, index):
        default_flags = super(FileItemModel, self).flags(index)
        return Qt.ItemIsDropEnabled | default_flags

    def mimeTypes(self):
        return ['text/uri-list']

    def dropMimeData(self, data, action, row, column, parent):
        urls = []
        root = self.invisibleRootItem()
        for url in data.urls():
            file_path = url.toLocalFile()
            if file_path[-4:].lower() != '.fbx':
                continue

            duplicate = False
            for i in range(root.rowCount()):
                if file_path == root.child(i).path:
                    duplicate = True
                    break
            if duplicate:
                continue

            urls.append(file_path)
            root.appendRow(FileItem(file_path))

        if self.auto_load:
            self.file_thread = FileThread(urls)
            self.file_thread.progress.connect(self.on_progress)
            self.file_thread.complete.connect(self.on_complete)
            self.file_thread.start()
            self.launched.emit(len(urls))

        return True

    def on_progress(self, message):
        message = json.loads(message)
        root = self.invisibleRootItem()
        total = 0
        for i in range(root.rowCount()):
            item = root.child(i)
            if item.path == message['path']:
                for take in message['takes']:
                    item.appendRow(TakeItem(take))
                item.loaded = True
            if item.loaded:
                total += 1

        self.on_data_changed()
        self.progress.emit(total - self.file_loaded)

    def on_execute_progress(self, message):
        message = json.loads(message)
        root = self.invisibleRootItem()
        total = 0
        for i in range(root.rowCount()):
            item = root.child(i)
            if item.path == message['path'].replace('\n', ''):
                item.executed = True
            if item.executed:
                root.removeRow(i)
                total += 1
                break

        self.progress.emit(total)

    def on_complete(self, *_):
        root = self.invisibleRootItem()
        self.file_loaded = root.rowCount()
        self.exe_count = 0
        self.complete.emit()

    def on_data_changed(self, *_):
        root = self.invisibleRootItem()
        for i in range(root.rowCount()):
            file_item = root.child(i)
            file_item.apply(convert(self.pattern_model.pattern_data(), file_item.text()))
            for j in range(file_item.rowCount()):
                take_item = file_item.child(j)
                take_item.apply(convert(self.pattern_model.pattern_data(), take_item.text()))

        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def execute(self):
        urls = []
        root = self.invisibleRootItem()

        i = 0
        while i < root.rowCount():
            file_item = root.child(i)
            changed = not self.auto_load
            if file_item.path == file_item.path_new:
                for j in range(file_item.rowCount()):
                    take_item = file_item.child(j)
                    if take_item.text() != take_item.new:
                        changed = True
            else:
                changed = True
            if changed:
                urls.append(root.child(i).path)
                i += 1
            else:
                root.removeRow(i)

        self.file_thread = FileThread(urls, self.pattern_model.pattern_data())
        self.file_thread.progress.connect(self.on_execute_progress)
        self.file_thread.complete.connect(self.on_complete)
        self.file_thread.start()

        self.exe_count = len(urls)
        self.launched.emit(self.exe_count)


class FileThread(QThread):

    progress = pyqtSignal(str)
    complete = pyqtSignal()

    def __init__(self, urls, patterns=None):
        super(FileThread, self).__init__()
        self.urls = urls
        self.patterns = patterns

    def run(self):
        for url in self.urls:
            exe = sys.executable.replace('\\', '/')
            mdu = os.path.join(os.path.dirname(__file__), 'utils.py').replace('\\', '/')
            cmd = '"{exe}" "{mdu}" "{url}"'.format(**locals())
            cmd += ' "%s"' % self.patterns.replace('"', '\'') if self.patterns else ''
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            msg, err = process.communicate()

            self.progress.emit(msg)

        self.complete.emit()
