import random
import sys
import winsound

from PyQt5.QtCore import QBasicTimer, Qt, pyqtSignal, QRect
from PyQt5.QtGui import QIcon, QPainter, QImage
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication

from classic_snake import Board
from helpers import load_res, load_style_res


class SnakeGame(QMainWindow):
    def __init__(self):
        super(SnakeGame, self).__init__()
        self.sboard = Board(self)
        self.statusbar = self.statusBar()
        self.sboard.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.setCentralWidget(self.sboard)
        self.setWindowTitle('Snakes')
        self.setWindowIcon(QIcon(load_res('icon.png')))
        self.resize(1280, 720)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


def main():
    app = QApplication([])

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
