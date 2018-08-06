import os
import xlrd
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem

import fbx
import FbxCommon


class FileItem(QStandardItem):

    def __init__(self, text):
        self.path = text
        super(FileItem, self).__init__(os.path.basename(self.path))


class TakeItem(QStandardItem):

    def __init__(self, text):
        super(TakeItem, self).__init__(text)


class PatternListModel(QAbstractListModel):

    def __init__(self, parent=None):
        super(PatternListModel, self).__init__(parent)
        self.patterns = []

    def rowCount(self, *_):
        return len(self.patterns)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.patterns[index.row()]

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
            self.patterns.append('%s -> %s' % (old[i], new[i]))

        self.dataChanged.emit(QModelIndex(), QModelIndex())

        return True


class FileInputItemModel(QStandardItemModel):

    progress = pyqtSignal(name='progress')

    def __init__(self, parent=None):
        super(FileInputItemModel, self).__init__(parent)

    def columnCount(self, *_):
        return 1

    def supportedDropActions(self):
        return Qt.CopyAction

    def flags(self, index):
        default_flags = super(FileInputItemModel, self).flags(index)
        return Qt.ItemIsDropEnabled | default_flags

    def mimeTypes(self):
        return ['text/uri-list']

    def dropMimeData(self, data, action, row, column, parent):
        root = self.invisibleRootItem()
        for url in data.urls():
            file_path = url.toLocalFile()
            if file_path[-4:].lower() != '.fbx':
                continue

            (fbx_manager, fbx_scene) = FbxCommon.InitializeSdkObjects()
            status = FbxCommon.LoadScene(fbx_manager, fbx_scene, file_path)
            if not status:
                print("Failed to load %s" % file_path)
                continue

            file_item = FileItem(file_path)
            stack_class_id = fbx.FbxAnimStack.ClassId
            stack_object_type = fbx.FbxCriteria.ObjectType(stack_class_id)
            stack_count = fbx_scene.GetSrcObjectCount(stack_object_type)
            for i in range(stack_count):
                stack = fbx_scene.GetSrcObject(stack_object_type, i)
                take_item = TakeItem(stack.GetName())
                file_item.appendRow(take_item)
            root.appendRow(file_item)

        self.dataChanged.emit(QModelIndex(), QModelIndex())

        return True


class FileOutputItemModel(QStandardItemModel):

    def __init__(self, pattern_model, input_model, parent=None):
        super(FileOutputItemModel, self).__init__(parent)
        self.pattern_model = pattern_model
        self.input_model = input_model
        self.pattern_model.dataChanged.connect(self.on_data_changed)
        self.input_model.dataChanged.connect(self.on_data_changed)

    def columnCount(self, *_):
        return 1

    def on_data_changed(self, *_):
        self.clear()
        root = self.invisibleRootItem()
        input_root = self.input_model.invisibleRootItem()
        for i in range(input_root.rowCount()):
            input_file = input_root.child(i)
            output_file = FileItem(self.convert(input_file.text()))
            for j in range(input_file.rowCount()):
                input_take = input_file.child(j)
                output_take = TakeItem(self.convert(input_take.text()))
                output_file.appendRow(output_take)
            root.appendRow(output_file)

        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def convert(self, text):
        return text
