from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QFrame, QComboBox
from plugins.config import PLUGINS

class GUIControls(QWidget):
    def __init__(self, cardinal, parent=None):
        QWidget.__init__(self, parent)
        self.cardinal = cardinal

        self.plugins = QComboBox()
        for plugin in PLUGINS:
            self.plugins.addItem(plugin)
        self.plugins.currentIndexChanged.connect(self.switch_plugin)

        self.points_dat = QLineEdit()
        self.points_dat.setPlaceholderText("points.dat")

        self.points_button = QPushButton()
        self.points_button.setText("Update points")
        #self.points_button.clicked.connect(self.update_center)

        self.sep_1 = QFrame()
        self.sep_1.setFrameShape(QFrame.HLine)
        self.sep_1.setFrameShadow(QFrame.Sunken)

        self.center = PointEdit()
        self.distance = QLineEdit()
        self.distance.setPlaceholderText("circle radius")

        self.update_button = QPushButton()
        self.update_button.setText("Search in circle")
        self.update_button.clicked.connect(self.intersect)

        self.sep_2 = QFrame()
        self.sep_2.setFrameShape(QFrame.HLine)
        self.sep_2.setFrameShadow(QFrame.Sunken)

        self.labels_toggle_button = QPushButton()
        self.labels_toggle_button.setText("Toggle labels")
        self.labels_toggle_button.clicked.connect(self.toggle_labels)
        self.clear_button = QPushButton()
        self.clear_button.setText("Clear")


        control_layout = QVBoxLayout()
        control_layout.addWidget(self.plugins)
        control_layout.addWidget(self.points_dat)
        control_layout.addWidget(self.points_button)
        control_layout.addWidget(self.sep_1)
        control_layout.addWidget(self.center)
        control_layout.addWidget(self.distance)
        control_layout.addWidget(self.update_button)
        control_layout.addWidget(self.sep_2)
        control_layout.addWidget(self.labels_toggle_button)
        control_layout.addWidget(self.clear_button)

        layout = QVBoxLayout()
        layout.addLayout(control_layout)
        self.setLayout(layout)
        self.load_dat("points.dat")
        self.switch_plugin(0)

    def load_dat(self, dat_file=None):
        if not dat_file:
            dat_file = self.points_dat.text()
        self.cardinal.load_points(dat_file)

    def switch_plugin(self, e):
        print("switched")
        self.cardinal.switch_index(PLUGINS[self.plugins.currentText()])


    def toggle_labels(self):
        self.cardinal.show_text = not self.cardinal.show_text
        self.cardinal.repaint()


    def intersect(self):
        self.cardinal.intersect(*self.center.getPoint(), int(self.distance.text()))


class PointEdit(QWidget):
    def __init__(self, parent=None):
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