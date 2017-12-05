#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rend a spatial data database/application")

    parser.add_argument("-t", "--tests", action="store_true")
    parser.add_argument("-p", "--port", type=int)
    parser.add_argument("-i", "--index")
    parser.add_argument("-d", "--data")

    args = parser.parse_args()

    if args.tests:
        import tests
        sys.exit()

    if args.port and args.index and args.data:
        from plugins.config import PLUGINS
        from core.index_struct import SpatialIndex
        from core.http_handler import make_http_server
        spatial_index = SpatialIndex()
        spatial_index.set(PLUGINS[args.index])
        spatial_index.load_points(args.data)
        httpd = make_http_server(spatial_index, port=args.port)
        print('Starting httpd...')
        httpd.serve_forever()
        sys.exit()

    elif args.port or args.index or args.data:
        parser.print_help()
        sys.exit()

    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QColor, QPalette
    from PyQt5.QtWidgets import QApplication
    from core.main import MainApplication

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
