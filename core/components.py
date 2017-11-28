#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel

class LabelEdit(QWidget):
    def __init__(self, parent=None, name="None", placeholder="None"):
        QWidget.__init__(self, parent)
        self.label = QLabel()
        self.label.setText(name)
        self.line = QLineEdit()
        self.line.setText(str(placeholder))
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line)
        self.setLayout(layout)

    def text(self):
        return self.label.text(), self.line.text()


class PointEdit(QWidget):
    def __init__(self, parent=None, name="None", placeholder="None"):
        QWidget.__init__(self, parent)
        self.x = QLineEdit()
        self.x.setPlaceholderText("x")

        self.y = QLineEdit()
        self.y.setPlaceholderText("y")

        layout = QHBoxLayout()
        layout.addWidget(self.x)
        layout.addWidget(self.y)
        self.setLayout(layout)

    def getPoint(self):
        return int(self.x.text()), int(self.y.text())

# might not need to register it

COMPONENTS = {
    "PointEdit": PointEdit,
    "LabelEdit": LabelEdit
}