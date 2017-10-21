#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
from ast import literal_eval

from PyQt5.QtWidgets import QWidget, QApplication, QLayout, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect, QPointF


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
        # TODO: use icons, fix them better
        # TODO: canvas shouldn't be below the buttons.
        """
        self.button_top = QPushButton(self)
        self.button_top.setText("Up")
        self.button_top.move(self.centerX-self.button_top.width()/2, 0)

        self.button_right = QPushButton(self)
        self.button_right.setText("<")
        self.button_right.move(0, self.centerY)

        self.button_left = QPushButton(self)
        self.button_left.setText(">")
        self.button_left.move(self.width()-self.button_left.width(), self.centerY)

        self.button_down = QPushButton(self)
        self.button_down.setText("Down")
        self.button_down.move(self.centerX, self.height()-self.button_down.height())
        """
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.offset_X +=1
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

    def associate(self, gui):
        self.gui = gui

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale += 0.5
        else:
            if self.scale > 0:
                self.scale -= 0.5
        self.repaint()


    def load_points(self, dat_file):
        with open(dat_file, "r") as points_dat:
            self.points = literal_eval(points_dat.read())

    def switch_index(self, plugin):
        self.detected = []
        self.center_point = None
        self.r = None
        self.distance = None
        self.index = plugin(self)
        self.index.add_points(self.points)
        self.repaint()

    def intersect(self, x=50, y=50, r=20):
        self.center_point = (x, y)
        self.r = r
        t = time.time()
        self.detected = self.index.intersection(x, y, r)
        self.gui.set_query_time(time.time() - t)
        print(self.detected)
        self.gui.add_items(self.detected)

        self.repaint()

    def nearest(self, x=50, y=50, k=20):
        self.center_point = (x, y)
        t = time.time()
        self.detected = self.index.nearest(x, y, k)
        self.gui.set_query_time(time.time() - t)

        self.r = -self.index.point_distance(x, y, *self.detected[0])
        self.gui.add_items(self.detected)

        self.repaint()

    def draw_rectangle(self, point1=None, point2=None):
        t_point1 = self.translate_point(*point1)
        width = point2[0] - point1[0]
        height = point2[1] - point1[1]
        self.qp.drawRect(*t_point1, width, height)

    def translate_point(self, x ,y):
        return self.centerX+(x+self.offset_X)*self.scale, self.centerY-(y-self.offset_Y)*self.scale

    def drawPoint(self, x, y, uiid=None):
        self.qp.drawPoint(*self.translate_point(x ,y))
        if self.show_text:
            self.qp.drawText(*self.translate_point(x ,y), "X:" + str(x) + " Y:" + str(y))

    def paintEvent(self, event):
        self.drawText(event)

    def drawText(self, event):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(0, 0, 0))

        self.centerY = self.width() / 2
        self.centerX = self.height() / 2

        self.qp.begin(self)

        self.qp.setPen(pen)
        self.qp.fillRect(QRect(0, 0, self.height(), self.width()), Qt.white)
        self.qp.drawLine(self.width() // 2+ self.offset_X*self.scale, 0, self.width() // 2+self.offset_X*self.scale, self.height())
        self.qp.drawLine(0, self.height() // 2+self.offset_Y*self.scale, self.width(), self.height() // 2+self.offset_Y * self.scale)

        pen.setColor(QColor(156, 91, 28))
        self.qp.setPen(pen)
        # self.draw_rectangle(qp)

        pen.setColor(QColor(0, 179, 0))
        self.qp.setPen(pen)

        if self.center_point:
            self.drawPoint(*self.center_point)

        if self.r:
            self.qp.drawEllipse(QPointF(*self.translate_point(*self.center_point)), self.r * self.scale,
                                self.r * self.scale)

        for i, p in enumerate(self.points):
            if p in self.detected:
                pen.setColor(QColor(153, 0, 0))
                self.qp.setPen(pen)
                self.drawPoint(*p)

            else:
                pen.setColor(QColor(0, 69, 88))
                self.qp.setPen(pen)
                self.drawPoint(*p)
        self.qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cardinal = Cardinal()
    sys.exit(app.exec_())
