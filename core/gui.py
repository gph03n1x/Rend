#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QLineEdit, QFrame, QComboBox, QTableWidget, QLabel, QTableWidgetItem, QStyle

from plugins.config import PLUGINS
import core.components
from core.index_struct import SpatialIndex
from core.utils import merge_dicts


class GUIControls(QWidget):
    def __init__(self, cardinal, parent=None):
        QWidget.__init__(self, parent)
        
        self.cardinal = cardinal
        self.index = SpatialIndex(cardinal)


        self.plugins = QComboBox()
        for plugin in PLUGINS:
            self.plugins.addItem(plugin)

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

        self.actions = QComboBox()

        self.actions_parameters = QVBoxLayout()

        self.query_button = QPushButton()
        self.query_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.query_button.clicked.connect(self.query)

        self.action_layout = QHBoxLayout()
        self.action_layout.addWidget(self.actions)
        self.action_layout.addWidget(self.query_button)

        self.sep_2 = QFrame()
        self.sep_2.setFrameShape(QFrame.HLine)
        self.sep_2.setFrameShadow(QFrame.Sunken)

        self.labels_toggle_button = QPushButton()
        self.labels_toggle_button.setText("Toggle labels")
        self.labels_toggle_button.clicked.connect(self.toggle_labels)
        self.clear_button = QPushButton()
        self.clear_button.setText("Toggle Cardinal")
        # TODO: complete the toggle cardinal function

        control_layout = QVBoxLayout()
        control_layout.addWidget(self.plugins)
        control_layout.addLayout(self.plugin_parameters)
        control_layout.addWidget(self.index_button)
        control_layout.addWidget(self.points_dat)
        control_layout.addWidget(self.points_button)
        control_layout.addWidget(self.sep_1)
        control_layout.addLayout(self.action_layout)
        control_layout.addLayout(self.actions_parameters)
        control_layout.addWidget(self.sep_2)
        control_layout.addWidget(self.labels_toggle_button)
        control_layout.addWidget(self.clear_button)


        self.query_time = QLabel()
        # TODO: make it look good
        self.spatial_results = QTableWidget()
        # self.spatial_results.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.items = 0
        self.spatial_results.setRowCount(self.items)
        # self.spatial_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.spatial_results.horizontalHeader().setStretchLastSection(True)
        # self.spatial_results.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.spatial_results.setColumnCount(3)
        self.spatial_results.setColumnWidth(0, 30)
        self.spatial_results.setColumnWidth(1, 30)
        self.spatial_results.setColumnWidth(2, 160)

        info_layout = QVBoxLayout()
        info_layout.addWidget(self.query_time)
        info_layout.addWidget(self.spatial_results)

        layout = QHBoxLayout()
        layout.addLayout(control_layout)
        layout.addLayout(info_layout)
        self.setLayout(layout)

        self.switch_plugin()
        self.switch_actions()

        self.plugins.currentIndexChanged.connect(self.switch_plugin)
        self.actions.currentIndexChanged.connect(self.switch_actions)

    def update_index(self):
        params = merge_dicts([self.plugin_parameters.itemAt(i).widget().text()
                              for i in range(self.plugin_parameters.count())])

        PLUGINS[self.plugins.currentText()].PARAMETERS["data"] = params

        if PLUGINS[self.plugins.currentText()].PARAMETERS['visual']:
            self.cardinal.activate()
        else:
            self.cardinal.deactivate()
        self.index.set(PLUGINS[self.plugins.currentText()])

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
        self.resize(self.sizeHint())

    def load_dat(self):
        # TODO: FileNotFoundError, IOERRORS
        dat_file = self.points_dat.text()
        if not dat_file:
            dat_file = "points.dat"

        self.index.load_points(dat_file)

    def switch_plugin(self, e=None):
        elements = PLUGINS[self.plugins.currentText()].PARAMETERS["elements"]
        data = PLUGINS[self.plugins.currentText()].PARAMETERS["data"]

        while not self.plugin_parameters.isEmpty():
            self.plugin_parameters.takeAt(0).widget().setParent(None)

        for parameter in elements:
            widget_ = getattr(core.components, elements[parameter])(name=parameter, placeholder=data[parameter])
            self.plugin_parameters.addWidget(widget_)

        actions = PLUGINS[self.plugins.currentText()].ACTIONS
        self.actions.clear()
        for action in actions:
            self.actions.addItem(action)
        self.resize(self.sizeHint())

    def switch_actions(self, e=None):
        if self.actions.currentText() == '':
            return

        elements = PLUGINS[self.plugins.currentText()].ACTIONS[self.actions.currentText()]["elements"]

        while not self.actions_parameters.isEmpty():
            self.actions_parameters.takeAt(0).widget().setParent(None)

        for parameter in elements:
            widget_ = getattr(core.components, elements[parameter])(name=parameter)
            self.actions_parameters.addWidget(widget_)
        self.resize(self.sizeHint())

    def toggle_labels(self):
        self.cardinal.show_text = not self.cardinal.show_text
        self.cardinal.repaint()

    def query(self):
        try:
            params = merge_dicts([self.actions_parameters.itemAt(i).widget().text()
                              for i in range(self.actions_parameters.count())])
        except ValueError:
            pass
        else:
            action = PLUGINS[self.plugins.currentText()].ACTIONS[self.actions.currentText()]["action"]
            results = self.index.action(action, params)

            self.set_query_time(results["metrics"]["time"])
            self.add_items(results["data"])
