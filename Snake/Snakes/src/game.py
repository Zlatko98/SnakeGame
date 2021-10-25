import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QMessageBox

from board import Board
from helpers import load_res
import classic_snake

class SnakeGame(QMainWindow):
    def __init__(self, usernames_list: list, speed: int, multiple: bool, food: int):
        super(SnakeGame, self).__init__()

        self.usernames = usernames_list
        self.game_speed = speed
        self.multiple_snakes = multiple
        self.food_count = food

        self.game_board = Board(self, self.usernames, self.game_speed, self.multiple_snakes, self.food_count)
        self.statusbar = self.statusBar()
        self.game_board.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.setCentralWidget(self.game_board)
        self.setWindowTitle('Snakes')
        self.setWindowIcon(QIcon(load_res('icon.png')))
        self.resize(1280, 720)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))
        self.game_board.start()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Really?',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            if self.game_board.bonus_timer.is_alive:
                self.game_board.bonus_timer.cancel()
            if self.game_board.malus_timer.is_alive:
                self.game_board.malus_timer.cancel()
            self.game_board.t.cancel()
            self.game_board.r.cancel()

        else:
            event.ignore()


class ClassicSnake(QMainWindow):
    def __init__(self):
        super(ClassicSnake, self).__init__()
        self.sboard = classic_snake.Board(self)
        self.statusbar = self.statusBar()
        self.sboard.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.setCentralWidget(self.sboard)
        self.setWindowTitle('Snakes')
        self.setWindowIcon(QIcon(load_res('icon.png')))
        self.resize(1280, 720)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Really?',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
def main():
    app = QApplication([])

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
