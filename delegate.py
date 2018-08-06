from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QLinearGradient, QColor, QGradient, QPen
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle


file_convert = Qt.UserRole + 3
item_height = Qt.UserRole + 4
item_color = Qt.UserRole + 5


class FileItemDelegate(QStyledItemDelegate):
    
    def __init__(self, role=Qt.DisplayRole, parent=None):
        self.role = role
        super(FileItemDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        name_rect = option.rect.adjusted(4, 0, -4, 0)
        item_rect = option.rect.adjusted(1, 1, -1, 0)

        painter.fillRect(item_rect, QColor(240, 240, 240, 255))

        if option.state & QStyle.State_Selected:
            g_selected = QLinearGradient(0, item_rect.y(), 0, item_rect.y() + item_rect.height())
            g_selected.setColorAt(0.0, QColor(100, 100, 100, 200))
            g_selected.setColorAt(1.0 / item_rect.height(), QColor(100, 100, 100, 30))
            g_selected.setColorAt(1.0 - 1.0 / item_rect.height(), QColor(100, 100, 100, 20))
            g_selected.setColorAt(1.0, QColor(255, 255, 255, 0))
            g_selected.setSpread(QGradient.ReflectSpread)
            painter.fillRect(item_rect, g_selected)

        elif option.state & QStyle.State_MouseOver:
            g_hover = QLinearGradient(0, item_rect.y(), 0, item_rect.y() + item_rect.height())
            g_hover.setColorAt(0.0, QColor(255, 255, 255, 200))
            g_hover.setColorAt(1.0 / item_rect.height(), QColor(255, 255, 255, 50))
            g_hover.setColorAt(1.0 - 1.0 / item_rect.height(), QColor(255, 255, 255, 0))
            g_hover.setColorAt(1.0, QColor(100, 100, 100, 200))
            painter.fillRect(item_rect, g_hover)

        painter.save()
        painter.setPen(QPen(QColor(index.data(item_color)if self.role == file_convert else '#000')))
        painter.drawText(name_rect, Qt.AlignVCenter, index.data(self.role))
        painter.restore()

    def sizeHint(self, option, index):
        height = index.data(item_height)
        return QSize(100, height)
