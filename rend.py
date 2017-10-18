import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow

from core.cardinal import Cardinal
from core.gui import GUIControls


class MainApplication(QMainWindow):
    def __init__(self):
        QApplication.__init__(self)
        self.setWindowTitle("Rend - Spatial Simulator")
        #self.setGeometry(280, 170, 800, 800)
        self.cardinal = Cardinal()
        self.cardinal.setWindowTitle("Rend - Cardinal")
        self.cardinal.show()
        self.gui_controls = GUIControls(self.cardinal)
        self.setCentralWidget(self.gui_controls)
        self.show()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(15, 15, 15))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(palette)

    main_app = MainApplication()
    sys.exit(app.exec_())