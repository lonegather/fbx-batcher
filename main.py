import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from widget import Ui_MainWindow

from model import *


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        pattern_model = PatternListModel()
        file_input_model = FileInputItemModel()
        file_output_model = FileOutputItemModel(pattern_model, file_input_model)

        self.lv_pattern.setAcceptDrops(True)
        self.lv_pattern.setDropIndicatorShown(True)
        self.lv_pattern.setModel(pattern_model)
        self.tv_input.setAcceptDrops(True)
        self.tv_input.setDropIndicatorShown(True)
        self.tv_input.setModel(file_input_model)
        self.tv_input.setHeaderHidden(True)
        self.tv_output.setModel(file_output_model)
        self.tv_output.setHeaderHidden(True)

        file_input_model.progress.connect(self.on_progress)
        file_output_model.dataChanged.connect(self.on_data_changed)

    def on_progress(self, *_):
        pass

    def on_data_changed(self, *_):
        self.tv_input.expandAll()
        self.tv_output.expandAll()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
