import random
import sys
import time
import winsound
from threading import Thread

from PyQt5.QtCore import pyqtSignal, QBasicTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QFrame, QApplication

from helpers import load_style_res, load_res


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)
    SPEED = 0.15
    WIDTHINBLOCKS = 60
    HEIGHTINBLOCKS = 40
    START_SPEED = SPEED

    def __init__(self, parent):
        super(Board, self).__init__(parent)

        self.food_eaten = 0
        self.snake = [[46, 5], [47, 5], [48, 5], [49, 5], [50, 5]]

        self.current_x_head = self.snake[0][0]
        self.current_y_head = self.snake[0][1]

        self.food = []
        self.grow_snake = False
        self.is_dead = False
        self.board = []
        self.direction = 'LEFT'
        self.th = Thread(target=self.move_snake, args=())
        self.th.daemon = True
        self.th.start()
        self.cc = Thread(target=self.check_collisions, args=())
        self.cc.daemon = True
        self.cc.start()
        self.drop_food()

        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet('border-image: url(' + load_style_res('grass.png') + ') 0 0 0 0 stretch center')

    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS

    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTINBLOCKS

    def start(self, speed: int):

        self.msg2statusbar.emit(
            'Score: ' + str(len(self.snake) - 2) + '                        '

                                                   '                                  '
                                                   '                                      '
                                                   '        '
                                                   '                            '
                                                   '                        '
                                                   ' '
                                                   '            '
        )

        if speed == 1:
            Board.SPEED = 0.15
        elif speed == 2:
            Board.SPEED = 0.125
        elif speed == 3:
            Board.SPEED = 0.1
        Board.START_SPEED = Board.SPEED

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()

        self.draw_head(painter, rect.left() + self.current_x_head * self.square_width(),
                       boardtop + self.current_y_head * self.square_height())

        for i, pos in enumerate(self.snake):
            if pos[0] == self.current_x_head and pos[1] == self.current_y_head:
                pass
            elif i == len(self.snake) - 1:
                self.draw_tail(painter, rect.left() + pos[0] * self.square_width(),
                               boardtop + pos[1] * self.square_height())
            else:
                self.draw_body(painter, rect.left() + pos[0] * self.square_width(),
                               boardtop + pos[1] * self.square_height())
        for pos in self.food:
            self.draw_food(painter, rect.left() + pos[0] * self.square_width(),
                           boardtop + pos[1] * self.square_height())

    def draw_food(self, painter, x, y):

        image = QImage(load_res('apple.png'))

        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 10), int(self.square_height() + 10)),
                          image)

    def draw_head(self, painter, x, y):
        image = QImage(load_res('head3.png'))

        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          image)

    def draw_body(self, painter, x, y):
        body = QImage(load_res('body3.png'))
        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          body)

    def draw_tail(self, painter, x, y):
        tail = QImage(load_res('tail3.png'))
        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          tail)

    def keyPressEvent(self, event):

        key = event.key()
        if key == Qt.Key_Left:
            if self.direction != 'RIGHT':
                self.direction = 'LEFT'
        elif key == Qt.Key_Right:
            if self.direction != 'LEFT':
                self.direction = 'RIGHT'
        elif key == Qt.Key_Down:
            if self.direction != 'UP':
                self.direction = 'DOWN'
        elif key == Qt.Key_Up:
            if self.direction != 'DOWN':
                self.direction = 'UP'

    def move_snake(self):
        while True:
            if self.is_dead:
                break
            else:

                if self.direction == 'LEFT':
                    self.current_x_head, self.current_y_head = self.current_x_head - 1, self.current_y_head
                    if self.current_x_head < 0:
                        self.current_x_head = Board.WIDTHINBLOCKS - 1
                if self.direction == 'RIGHT':
                    self.current_x_head, self.current_y_head = self.current_x_head + 1, self.current_y_head
                    if self.current_x_head == Board.WIDTHINBLOCKS:
                        self.current_x_head = 0
                if self.direction == 'DOWN':
                    self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head + 1
                    if self.current_y_head == Board.HEIGHTINBLOCKS:
                        self.current_y_head = 0
                if self.direction == 'UP':
                    self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head - 1
                    if self.current_y_head < 0:
                        self.current_y_head = Board.HEIGHTINBLOCKS

                head = [self.current_x_head, self.current_y_head]
                self.snake.insert(0, head)
                if not self.grow_snake:
                    self.snake.pop()
                else:

                    self.msg2statusbar.emit(
                        'Score: ' + str(len(self.snake) - 5) + '                        '
            
                                                               '                                  '
                                                               '                                      '
                                                               '        '
                                                               '                            '
                                                               '                        '
                                                               ' '
                                                               '            '
                    )

                    self.grow_snake = False

                self.update()
            time.sleep(Board.SPEED)

    def is_suicide(self):  # If snake collides with itself, game is over
        for i in range(1, len(self.snake)):
            if self.snake[0] == self.snake[i]:
                self.msg2statusbar.emit('Game over suicide! Your final score was: ' + str(len(self.snake) - 2))

                self.setStyleSheet('border-image: url(' + load_style_res('you_died.png') + ') 0 0 0 0 stretch stretch')
                self.remove_food()

                self.is_dead = True

    def is_food_collision(self):
        for pos in self.food:
            if pos == self.snake[0]:
                self.food.remove(pos)
                self.food_eaten = self.food_eaten + 1
                if self.food_eaten < 10:
                    self.drop_food()

                elif 10 <= self.food_eaten < 25:
                    if len(self.food) > 5:
                        pass
                    else:
                        self.drop_food()
                        self.drop_food()
                elif 25 <= self.food_eaten < 60:
                    if len(self.food) > 6:
                        self.drop_food()

                    else:
                        self.drop_food()
                        self.drop_food()
                elif 60 <= self.food_eaten < 100:
                    if len(self.food) > 8:
                        self.drop_food()

                    else:
                        self.drop_food()
                        self.drop_food()
                elif 100 <= self.food_eaten < 175:
                    if len(self.food) > 9:
                        self.drop_food()

                    else:
                        self.drop_food()
                        self.drop_food()
                elif self.food_eaten >= 200:
                    if len(self.food) > 10:
                        self.drop_food()
                    else:
                        self.drop_food()
                        self.drop_food()
                self.grow_snake = True

    def wall_collision(self):
        x_left = 1
        x_right = 58
        y_bottom = 38
        y_top = 1

        for i in range(0, 40):
            if self.snake[0] == [x_left, i] or self.snake[0] == [x_right, i]:

                self.setStyleSheet(
                    'border-image: url(' + load_style_res('you_died.png') + ') 0 0 0 0 stretch stretch')
                self.msg2statusbar.emit('Game over! Your final score was: ' + str(len(self.snake) - 2))

                self.remove_food()
                self.is_dead = True

        for j in range(2, 57):
            if self.snake[0] == [j, y_bottom] or self.snake[0] == [j, y_top]:
                self.setStyleSheet('border-image: url(' + load_style_res('you_died.png') + ') 0 0 0 0 stretch stretch')
                self.msg2statusbar.emit('Game over! Your final score was: ' + str(len(self.snake) - 2))

                self.remove_food()
                self.is_dead = True

    def drop_food(self):

        x = random.randint(3, 56)
        y = random.randint(3, 36)

        self.food.append([x, y])

    def remove_food(self):
        self.food.clear()

    def check_collisions(self):
        while True:
            self.wall_collision()
            self.is_food_collision()
            self.is_suicide()
            time.sleep(0.01)
