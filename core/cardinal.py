import sys

from engine.keystone import Keystone

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QRect


class Cardinal(QWidget):
    def __init__(self):
        super().__init__()
        self.scale = 3
        self.show_text = True
        self.setGeometry(280, 170, 600, 600)

        self.points = [
            (-94, -88),
            (68, -25),
            (-34, 93),
            (14, -86),
            (-42, 9),
            (91, 87),
            (45, 31),
            (-47, 63),
            (-69, -49),
            (-24, -16),
            (-48, -60),
            (32, -63),
            (-83, 17),
            (-18, -27),
            (-73, -59),
            (35, 64),
            (-81, -38),
            (5, -63),
            (-6, 54),
            (29, -89),
        ]
        # radious not defined yet -69 -50
        self.xKey = Keystone()
        self.yKey = Keystone()
        for point in self.points:
            self.xKey.add_index(point[0], point)
            self.yKey.add_index(point[1], point)
        self.set_center_point()

    def set_center_point(self, x=-75, y=-20, distance=20):
        self.center_point = (x, y)
        # xCenter = self.xKey.get_closer_bounds(self.center_point[0])
        # yCenter = self.yKey.get_closer_bounds(self.center_point[1])

        # xbounds = self.xKey.get_bounds(*xCenter, 3, 3)
        # ybounds = self.yKey.get_bounds(*yCenter, 3, 3)

        xbounds = self.xKey.get_box_bounds(x, distance)
        ybounds = self.yKey.get_box_bounds(y, distance)

        xlist = set(self.xKey.get_in_range(*xbounds))
        ylist = set(self.yKey.get_in_range(*ybounds))

        self.detected = xlist & ylist
        self.bounds1 = (self.xKey.ordered_index[xbounds[0]], self.yKey.ordered_index[ybounds[0]])
        self.bounds2 = (self.xKey.ordered_index[xbounds[1]-1], self.yKey.ordered_index[ybounds[1]-1])
        print(self.bounds1, self.bounds2)
        self.setWindowTitle('Cardinal')
        self.repaint()

    def paintEvent(self, event):
        self.drawText(event)

    def drawText(self, event):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(0, 0, 0))

        self.centerY = self.width()/2
        self.centerX = self.height()/2

        qp = QPainter()
        qp.begin(self)

        qp.setPen(pen)
        qp.fillRect(QRect(0, 0, self.height(), self.width()), Qt.white)
        qp.drawLine(0, self.width()/2, self.height(), self.width()/2)
        qp.drawLine(self.height()/2, 0, self.height()/2, self.width())

        pen.setColor(QColor(156, 91, 28))
        qp.setPen(pen)
        self.draw_rectangle(qp)

        pen.setColor(QColor(0, 179, 0))
        qp.setPen(pen)
        self.drawPoint(qp, *self.center_point)

        for i, p in enumerate(self.points):
            if p in self.detected:
                pen.setColor(QColor(153, 0, 0))
                qp.setPen(pen)
                self.drawPoint(qp, *p)

            else:
                pen.setColor(QColor(0, 69, 88))
                qp.setPen(pen)
                self.drawPoint(qp, *p)
        qp.end()

    def draw_rectangle(self, qp, point1=None, point2=None):
        # TODO: use the method properly
        point1 = self.translate_point(*self.bounds1)
        width = self.translate_point(*self.bounds2)[0] - point1[0]
        height = self.translate_point(*self.bounds2)[1] - point1[1]
        qp.drawRect(*point1, width, height)

    def translate_point(self, x ,y):
        return self.centerX+x*self.scale, self.centerY-y*self.scale

    def drawPoint(self, qp, x, y):
        qp.drawPoint(self.centerX+x*self.scale, self.centerY-y*self.scale)
        if self.show_text:
            qp.drawText(self.centerX+x*self.scale, self.centerY-y*self.scale, "X:"+str(x)+" Y:"+str(y))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    cardinal = Cardinal()
    sys.exit(app.exec_())