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


class LabelEditInt(LabelAndLineEdit):
    def text(self):
        return {self.label.text(): int(self.line.text())}


class PointEdit(QWidget):
    def __init__(self, parent=None, name=None, placeholder=None):
        QWidget.__init__(self, parent)

        self.point_layout = QHBoxLayout()
        self.name = name.split(",")

        if placeholder:
            placeholder = placeholder.split(",")
        else:
            placeholder = self.name

        for enum, variable in enumerate(self.name):
            var_input = QLineEdit()
            var_input.setPlaceholderText(placeholder[enum])
            self.point_layout.addWidget(var_input)
        
        self.setLayout(self.point_layout)


class PointEditInt(PointEdit):
    def text(self):
        return {self.name[i]: int(self.point_layout.itemAt(i).widget().text())
                for i in range(self.point_layout.count())}


class PointEditFloat(PointEdit):
    def text(self):
        return {self.name[i]: float(self.point_layout.itemAt(i).widget().text())
                for i in range(self.point_layout.count())}
