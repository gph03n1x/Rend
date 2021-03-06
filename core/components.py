#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel
from PyQt5.QtCore import QRegExp

float_reg_exp = QRegExp("[-+]?([0-9]*[.])?[0-9]+")
int_reg_exp = QRegExp("[-+]?[1-9]\d*")


class LabelAndLineEdit(QWidget):
    """
    Creates a label and an input one next to another.
    """
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
    """
    Subclass of LabelAndLineEdit
    returns raw values of user input upon text()
    """
    def text(self):
        return {self.label.text(): self.line.text()}


class LabelEditFloat(LabelAndLineEdit):
    """
    Subclass of LabelAndLineEdit
    returns float values of user input upon text() and validates float input
    """
    def __init__(self, parent=None, name="None", placeholder=None):
        LabelAndLineEdit.__init__(self, parent, name, placeholder)
        input_validator = QRegExpValidator(float_reg_exp, self.line)
        self.line.setValidator(input_validator)

    def text(self):
        return {self.label.text(): float(self.line.text())}


class LabelEditInt(LabelAndLineEdit):
    """
    Subclass of LabelAndLineEdit
    returns int values of user input upon text() and validates int input
    """
    def __init__(self, parent=None, name="None", placeholder=None):
        LabelAndLineEdit.__init__(self, parent, name, placeholder)
        input_validator = QRegExpValidator(int_reg_exp, self.line)
        self.line.setValidator(input_validator)

    def text(self):
        return {self.label.text(): int(self.line.text())}


class PointEdit(QWidget):
    """
    Creates two or more inputs which represent
    a point in a 2 or more dimensional space
    """
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
    """
    Subclass of PointEdit
    returns int values of user input upon text() and validates int input
    """
    def __init__(self, parent=None, name=None, placeholder=None):
        PointEdit.__init__(self, parent, name, placeholder)
        for i in range(self.point_layout.count()):
            widget = self.point_layout.itemAt(i).widget()
            input_validator = QRegExpValidator(int_reg_exp, widget)
            widget.setValidator(input_validator)

    def text(self):
        return {self.name[i]: int(self.point_layout.itemAt(i).widget().text())
                for i in range(self.point_layout.count())}


class PointEditFloat(PointEdit):
    """
    Subclass of PointEdit
    returns float values of user input upon text() and validates float input
    """
    def __init__(self, parent=None, name=None, placeholder=None):
        PointEdit.__init__(self, parent, name, placeholder)
        for i in range(self.point_layout.count()):
            widget = self.point_layout.itemAt(i).widget()
            input_validator = QRegExpValidator(float_reg_exp, widget)
            widget.setValidator(input_validator)

    def text(self):
        return {self.name[i]: float(self.point_layout.itemAt(i).widget().text())
                for i in range(self.point_layout.count())}
