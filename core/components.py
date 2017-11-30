#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel


class LabelAndLineEdit(QWidget):
    def __init__(self, parent=None, name="None", placeholder=None):
        QWidget.__init__(self, parent)
        self.label = QLabel()
        self.label.setText(name)
        self.line = QLineEdit()
        if placeholder:
            self.line.setText(str(placeholder))
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line)
        self.setLayout(layout)


class LabelEditString(LabelAndLineEdit):
    def text(self):
        return {self.label.text(): self.line.text()}


class LabelEditFloat(LabelAndLineEdit):
    def text(self):
        return {self.label.text(): float(self.line.text())}


class PointEdit(QWidget):
    def __init__(self, parent=None, name=None, placeholder=None):
        QWidget.__init__(self, parent)
        self.name = name.split(",")
        self.x = QLineEdit()
        self.x.setPlaceholderText("x")

        self.y = QLineEdit()
        self.y.setPlaceholderText("y")

        if placeholder:
            x_placeholder, y_placeholder = placeholder.split(",")
        else:
            x_placeholder, y_placeholder = self.name

        self.x.setPlaceholderText(x_placeholder)
        self.y.setPlaceholderText(y_placeholder)

        layout = QHBoxLayout()
        layout.addWidget(self.x)
        layout.addWidget(self.y)
        self.setLayout(layout)

    def text(self):
        return {self.name[0]: float(self.x.text()), self.name[1]: float(self.y.text())}
