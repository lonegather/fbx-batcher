import os
import re
import xlrd
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem

import fbx
import FbxCommon


pattern_exp = Qt.UserRole + 1
pattern_rpl = Qt.UserRole + 2
file_convert = Qt.UserRole + 3
item_height = Qt.UserRole + 4
item_color = Qt.UserRole + 5

basic_patterns = {
    '(?i)_qte_': '_QTE_',
    '(?i)_stp_': '_STP_',
    '(?i)_fulb_': '_FulB_',
    '(?i)_addfacial_': '_AddFacial_',
    '^[a-z]|_[a-z]': lambda m: m.group(0).upper()
}


class FileItem(QStandardItem):

    def __init__(self, text):
        self.path = text
        self.path_new = text
        super(FileItem, self).__init__(os.path.basename(self.path))

    def data(self, role=Qt.DisplayRole):
        if role == file_convert:
            return os.path.basename(self.path_new)
        elif role == item_height:
            return 25
        elif role == item_color:
            return '#999' if self.path == self.path_new else '#00f'
        else:
            return super(FileItem, self).data(role)

    def apply(self, text):
        self.path_new = os.path.join(os.path.dirname(self.path), text).replace('\\', '/')


class TakeItem(QStandardItem):

    def __init__(self, text):
        super(TakeItem, self).__init__(text)
        self.new = text

    def data(self, role=Qt.DisplayRole):
        if role == file_convert:
            return self.new
        elif role == item_height:
            return 20
        elif role == item_color:
            return '#999' if self.text() == self.new else '#00f'
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


class FileItemModel(QStandardItemModel):

    progress = pyqtSignal(name='progress')

    def __init__(self, pattern_model, parent=None):
        super(FileItemModel, self).__init__(parent)
        self.pattern_model = pattern_model
        self.pattern_model.dataChanged.connect(self.on_data_changed)

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

        self.on_data_changed()

        return True

    def on_data_changed(self, *_):
        root = self.invisibleRootItem()
        for i in range(root.rowCount()):
            file_item = root.child(i)
            file_item.apply(self.convert(file_item.text()))
            for j in range(file_item.rowCount()):
                take_item = file_item.child(j)
                take_item.apply(self.convert(take_item.text()))

        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def convert(self, text):
        for i in range(self.pattern_model.rowCount()):
            index = self.pattern_model.index(i)
            exp = self.pattern_model.data(index, pattern_exp)
            rpl = self.pattern_model.data(index, pattern_rpl)
            text = re.sub(exp, rpl, text, flags=re.IGNORECASE)

        for pattern in basic_patterns:
            text = re.sub(pattern, basic_patterns[pattern], text)

        return text
