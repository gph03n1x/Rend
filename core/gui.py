#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QFrame, QComboBox, QTableWidget, \
    QLabel, QTableWidgetItem

from plugins.config import PLUGINS


class GUIControls(QWidget):
    def __init__(self, cardinal, parent=None):
        QWidget.__init__(self, parent)
        
        self.cardinal = cardinal
        self.cardinal.associate(self)

        self.plugins = QComboBox()
        for plugin in PLUGINS:
            self.plugins.addItem(plugin)

        self.plugins.currentIndexChanged.connect(self.switch_plugin)
        self.plugin_parameters = QVBoxLayout()

        self.index_button = QPushButton()
        self.index_button.setText("Update Index")
        self.index_button.clicked.connect(self.update_index)

        self.points_dat = QLineEdit()
        self.points_dat.setPlaceholderText("points.dat")

        self.points_button = QPushButton()
        self.points_button.setText("Update points")
        self.points_button.clicked.connect(self.load_dat)

        self.sep_1 = QFrame()
        self.sep_1.setFrameShape(QFrame.HLine)
        self.sep_1.setFrameShadow(QFrame.Sunken)

        self.center = PointEdit()
        self.distance = QLineEdit()
        self.distance.setPlaceholderText("circle radius")
        #self.distance.setText("5")

        self.intersect_button = QPushButton()
        self.intersect_button.setText("Search in circle")
        self.intersect_button.clicked.connect(self.intersect)

        self.nearest_button = QPushButton()
        self.nearest_button.setText("Nearest K")
        self.nearest_button.clicked.connect(self.nearest)

        self.sep_2 = QFrame()
        self.sep_2.setFrameShape(QFrame.HLine)
        self.sep_2.setFrameShadow(QFrame.Sunken)

        self.labels_toggle_button = QPushButton()
        self.labels_toggle_button.setText("Toggle labels")
        self.labels_toggle_button.clicked.connect(self.toggle_labels)
        self.clear_button = QPushButton()
        self.clear_button.setText("Toggle Cardinal")

        control_layout = QVBoxLayout()
        control_layout.addWidget(self.plugins)
        control_layout.addLayout(self.plugin_parameters)
        control_layout.addWidget(self.index_button)
        control_layout.addWidget(self.points_dat)
        control_layout.addWidget(self.points_button)
        control_layout.addWidget(self.sep_1)
        control_layout.addWidget(self.center)
        control_layout.addWidget(self.distance)
        control_layout.addWidget(self.intersect_button)
        control_layout.addWidget(self.nearest_button)
        control_layout.addWidget(self.sep_2)
        control_layout.addWidget(self.labels_toggle_button)
        control_layout.addWidget(self.clear_button)

        self.query_time = QLabel()
        #self.query_time.setText("")

        self.spatial_results = QTableWidget()
        self.items = 0
        self.spatial_results.setRowCount(self.items)
        self.spatial_results.setColumnCount(3)

        info_layout = QVBoxLayout()
        info_layout.addWidget(self.query_time)
        info_layout.addWidget(self.spatial_results)

        layout = QHBoxLayout()
        layout.addLayout(control_layout)
        layout.addLayout(info_layout)
        self.setLayout(layout)

        self.switch_plugin()
        #self.load_dat("points.dat")
        #self.deactivate()
    def update_index(self):
        print(len(PLUGINS[self.plugins.currentText()].GUI))
        d = [self.plugin_parameters.itemAt(i).widget().text() for i in range(self.plugin_parameters.count())]
        print({k: int(i) for k, i in d})
        PLUGINS[self.plugins.currentText()].GUI = {k: int(i) for k, i in d}
        if PLUGINS[self.plugins.currentText()].VISUAL:
            # TODO: make sure it doesn't update
            self.cardinal.activate()
        else:
            self.cardinal.deactivate()
        self.cardinal.switch_index(PLUGINS[self.plugins.currentText()])

    def set_query_time(self, query_time):
        self.query_time.setText("Query took {0}ms".format(int(query_time*1000)))

    def add_items(self, items):

        self.spatial_results.clear()
        self.items = 0
        for item in items:
            self.spatial_results.setRowCount(self.items + 1)
            self.spatial_results.setItem(self.items, 0, QTableWidgetItem(str(item[0])))
            self.spatial_results.setItem(self.items, 1, QTableWidgetItem(str(item[1])))
            self.spatial_results.setItem(self.items, 2, QTableWidgetItem(str(item[2])))
            self.items += 1


    def load_dat(self, dat_file="points.dat"):
        # TODO: FileNotFoundError, IOERRORS
        if not dat_file:
            dat_file = self.points_dat.text()
        self.cardinal.load_points(dat_file)
        self.update_index()

    def switch_plugin(self, e=None):
        parameters = PLUGINS[self.plugins.currentText()].GUI

        while not self.plugin_parameters.isEmpty():
            self.plugin_parameters.takeAt(0).widget().setParent(None)

        for parameter in parameters:
            label_edit = LabelEdit(name=parameter, placeholder=parameters[parameter])
            self.plugin_parameters.addWidget(label_edit)

    def toggle_labels(self):
        self.cardinal.show_text = not self.cardinal.show_text
        self.cardinal.repaint()

    def nearest(self):
        self.cardinal.nearest(*self.center.getPoint(), int(self.distance.text()))

    def intersect(self):
        self.cardinal.intersect(*self.center.getPoint(), int(self.distance.text()))


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
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.x = QLineEdit()
        self.x.setPlaceholderText("x")

        self.y = QLineEdit()
        self.y.setPlaceholderText("y")

        #self.x.setText("50")
        #self.y.setText("20")

        layout = QHBoxLayout()
        layout.addWidget(self.x)
        layout.addWidget(self.y)
        self.setLayout(layout)

    def getPoint(self):
        return int(self.x.text()), int(self.y.text())