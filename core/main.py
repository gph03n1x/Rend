#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QMainWindow

from core.cardinal import Cardinal
from core.gui import GUIControls

class MainApplication(QMainWindow):
    def __init__(self):
        QApplication.__init__(self)
        self.setWindowTitle("Rend - Spatial Simulator")
        self.cardinal = Cardinal()
        self.cardinal.setWindowTitle("Rend - Cardinal")
        self.cardinal.show()
        self.gui_controls = GUIControls(self.cardinal)
        self.setCentralWidget(self.gui_controls)
        self.show()
