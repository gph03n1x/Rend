#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect


class Cardinal(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(280, 170, 600, 600)
        self.scale = 3
        self.offset_X = 0
        self.offset_Y = 0
        self.show_text = True
        self.centerY = self.height() / 2
        self.centerX = self.width() / 2
        self.qp = QPainter()
        self.points = []
        self.setFixedSize(self.width(), self.height())
        self.center_point = None

        self.detected = []
        self.active = True

    def deactivate(self):
        self.active = False
        self.hide()
    
    def activate(self):
        self.active = True
        self.show()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.offset_X += 1
            self.repaint()
        elif event.key() == Qt.Key_Up:
            self.offset_Y += 1
            self.repaint()
        elif event.key() == Qt.Key_Down:
            self.offset_Y -= 1
            self.repaint()
        elif event.key() == Qt.Key_Right:
            self.offset_X -= 1
            self.repaint()
        elif event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
            self.scale += 0.5
            self.repaint()
        elif event.key() == Qt.Key_Minus:
            self.scale -= 0.5
            self.repaint()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale += 0.5
        else:
            if self.scale > 0:
                self.scale -= 0.5
        self.repaint()

    def update(self, detected=None):
        if detected:
            self.detected = detected
        self.repaint()

    def translate_point(self, x, y, label_offset=0):
        return self.centerX-label_offset+(x+self.offset_X)*self.scale, self.centerY-(y-self.offset_Y)*self.scale

    def draw_tasks(self):
        pass

    def draw_rectangle(self, point1=None, point2=None):
        t_point1 = self.translate_point(*point1)
        width = point2[0] - point1[0]
        height = point2[1] - point1[1]
        self.qp.drawRect(*t_point1, width, height)

    def draw_point(self, x, y, uiid=None):
        self.qp.drawPoint(*self.translate_point(x, y))
        if self.show_text:
            label = "X:" + str(x) + " Y:" + str(y)

            self.qp.drawText(*self.translate_point(x, y, label_offset=len(label)), label)

    def paintEvent(self, event):
        if self.active:
            self.draw_cardinal_canvas(event)

    def draw_cardinal_canvas(self, event):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(0, 0, 0))

        self.centerY = self.width() / 2
        self.centerX = self.height() / 2

        self.qp.begin(self)

        self.qp.setPen(pen)
        self.qp.fillRect(QRect(0, 0, self.height(), self.width()), Qt.white)
        self.qp.drawLine(self.width() // 2 + self.offset_X * self.scale, 0,
                         self.width() // 2 + self.offset_X * self.scale, self.height())
        self.qp.drawLine(0, self.height() // 2 + self.offset_Y * self.scale,
                         self.width(), self.height() // 2 + self.offset_Y * self.scale)

        pen.setColor(QColor(156, 91, 28))
        self.qp.setPen(pen)
        # self.draw_rectangle(qp)

        pen.setColor(QColor(0, 179, 0))
        self.qp.setPen(pen)

        if self.center_point:
            self.draw_point(*self.center_point)

        for i, p in enumerate(self.points):
            if p in self.detected:
                pen.setColor(QColor(153, 0, 0))
                self.qp.setPen(pen)
                self.draw_point(*p)

            else:
                pen.setColor(QColor(0, 69, 88))
                self.qp.setPen(pen)
                self.draw_point(*p)
        self.qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cardinal = Cardinal()
    sys.exit(app.exec_())
