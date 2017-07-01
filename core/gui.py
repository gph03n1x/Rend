from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit

class GUIControls(QWidget):
    def __init__(self, cardinal, parent=None):
        QWidget.__init__(self, parent)
        self.cardinal = cardinal
        self.update_button = QPushButton()
        self.update_button.setText("Update")
        self.update_button.clicked.connect(self.update_center)
        self.labels_toggle_button = QPushButton()
        self.labels_toggle_button.setText("Toggle labels")
        self.labels_toggle_button.clicked.connect(self.toggle_labels)

        self.clear_button = QPushButton()
        self.clear_button.setText("Clear")
        self.center = PointEdit()
        self.distance = QLineEdit()

        control_layout = QVBoxLayout()
        control_layout.addWidget(self.center)
        control_layout.addWidget(self.distance)
        control_layout.addWidget(self.update_button)
        control_layout.addWidget(self.labels_toggle_button)
        control_layout.addWidget(self.clear_button)

        layout = QVBoxLayout()
        layout.addLayout(control_layout)
        self.setLayout(layout)

    def toggle_labels(self):
        self.cardinal.show_text = not self.cardinal.show_text
        self.cardinal.repaint()

    def update_center(self):
        self.cardinal.set_center_point(*self.center.getPoint(), int(self.distance.text()))

class PointEdit(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.x = QLineEdit()
        self.y = QLineEdit()
        layout = QHBoxLayout()
        layout.addWidget(self.x)
        layout.addWidget(self.y)
        self.setLayout(layout)

    def getPoint(self):
        return int(self.x.text()), int(self.y.text())