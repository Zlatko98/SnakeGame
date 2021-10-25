import random
import time
from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QFrame

from collisions import is_suicide, snake_collision, wall_collision, is_food_collision
from food import Food
from bonus import Bonus
from malus import Malus
from helpers import load_style_res, load_res
from player import Player, change_active_player
from helpers import PerpetualTimer
from snake import Snake, change_active_snake, split_snake


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)
    WIDTHINBLOCKS = 60
    HEIGHTINBLOCKS = 40

    def __init__(self, parent, usernames: list, speed: int, multiple: bool, food: int):
        super(Board, self).__init__(parent)

        self.usernames = usernames
        self.game_speed = speed
        self.num_of_players = len(usernames)
        self.food_count = food
        self.game_over = False
        self.tab_mode = multiple
        self.dead_players = 0
        self.players = []
        self.interrupt_skip = False
        for k in range(len(self.usernames)):
            self.players.append(Player(usernames[k]))
            self.players[k].snakes.append(Snake())

        self.board = []
        self.steps = 1

        self.moves = 1
        self.active_snake = 0
        self.active_player = 0
        self.key_presses = 0
        self.flag = False
        self.t = None

        self.pos_x = None
        self.pos_y = None
        self.th = Thread(target=self.move_snake, args=())
        self.th.daemon = True
        self.th.start()
        self.bonus_timer = PerpetualTimer(random.randint(5, 20), self.deus_ex_machine_bonus)
        self.malus_timer = PerpetualTimer(random.randint(5, 20), self.deus_ex_machine_malus)

        if self.game_speed == 1:

            self.t = PerpetualTimer(15.05, change_active_player, self)

        elif self.game_speed == 2:

            self.t = PerpetualTimer(12.05, change_active_player, self)

        elif self.game_speed == 3:

            self.t = PerpetualTimer(10.05, change_active_player, self)

        else:

            self.t = PerpetualTimer(15, change_active_player, self)

        self.r = PerpetualTimer(0.995, self.countdown)
        self.r.start()
        self.t.start()
        self.cntdwn = 0
        self.bonus_timer.start()
        self.malus_timer.start()

        if self.num_of_players == 2:
            self.players[0].snakes[0].snake = [[14, 35], [13, 35], [12, 35], [11, 35], [10, 35]]
            self.players[0].snakes[0].current_x_head = self.players[0].snakes[0].snake[0][0]
            self.players[0].snakes[0].current_y_head = self.players[0].snakes[0].snake[0][1]
            self.players[0].snakes[0].direction = 'RIGHT'

            self.players[1].snakes[0].snake = [[46, 5], [47, 5], [48, 5], [49, 5], [50, 5]]
            self.players[1].snakes[0].current_x_head = self.players[1].snakes[0].snake[0][0]
            self.players[1].snakes[0].current_y_head = self.players[1].snakes[0].snake[0][1]
            self.players[1].snakes[0].direction = 'LEFT'

        elif self.num_of_players == 3:
            self.players[0].snakes[0].snake = [[14, 35], [13, 35], [12, 35], [11, 35], [10, 35]]
            self.players[0].snakes[0].current_x_head = self.players[0].snakes[0].snake[0][0]
            self.players[0].snakes[0].current_y_head = self.players[0].snakes[0].snake[0][1]
            self.players[0].snakes[0].direction = 'RIGHT'

            self.players[1].snakes[0].snake = [[46, 5], [47, 5], [48, 5], [49, 5], [50, 5]]
            self.players[1].snakes[0].current_x_head = self.players[1].snakes[0].snake[0][0]
            self.players[1].snakes[0].current_y_head = self.players[1].snakes[0].snake[0][1]
            self.players[1].snakes[0].direction = 'LEFT'

            self.players[2].snakes[0].snake = [[10, 10], [10, 9], [10, 8], [10, 7], [10, 6]]
            self.players[2].snakes[0].current_x_head = self.players[2].snakes[0].snake[0][0]
            self.players[2].snakes[0].current_y_head = self.players[2].snakes[0].snake[0][1]
            self.players[2].snakes[0].direction = 'DOWN'

        elif self.num_of_players == 4:
            self.players[0].snakes[0].snake = [[14, 35], [13, 35], [12, 35], [11, 35], [10, 35]]
            self.players[0].snakes[0].current_x_head = self.players[0].snakes[0].snake[0][0]
            self.players[0].snakes[0].current_y_head = self.players[0].snakes[0].snake[0][1]
            self.players[0].snakes[0].direction = 'RIGHT'

            self.players[1].snakes[0].snake = [[46, 5], [47, 5], [48, 5], [49, 5], [50, 5]]
            self.players[1].snakes[0].current_x_head = self.players[1].snakes[0].snake[0][0]
            self.players[1].snakes[0].current_y_head = self.players[1].snakes[0].snake[0][1]
            self.players[1].snakes[0].direction = 'LEFT'

            self.players[2].snakes[0].snake = [[10, 10], [10, 9], [10, 8], [10, 7], [10, 6]]
            self.players[2].snakes[0].current_x_head = self.players[2].snakes[0].snake[0][0]
            self.players[2].snakes[0].current_y_head = self.players[2].snakes[0].snake[0][1]
            self.players[2].snakes[0].direction = 'DOWN'

            self.players[3].snakes[0].snake = [[50, 30], [50, 31], [50, 32], [50, 33], [50, 34]]
            self.players[3].snakes[0].current_x_head = self.players[3].snakes[0].snake[0][0]
            self.players[3].snakes[0].current_y_head = self.players[3].snakes[0].snake[0][1]
            self.players[3].snakes[0].direction = 'UP'

        self.food = Food()
        self.bonus = Bonus()
        self.malus = Malus()

        for i in range(self.food_count):
            self.food.drop_food()

        self.countdown()
        self.setFocusPolicy(Qt.StrongFocus)

        self.setStyleSheet('border-image: url(' +
                           load_style_res('grass' + str(self.num_of_players) + 'ps.png') + ') 0 0 0 0 stretch center')

    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS

    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTINBLOCKS

    def start(self):

        self.msg2statusbar.emit('Welcome! ' + self.usernames[0] + '\'s turn. You\'ve got ' + str(self.cntdwn + 1) +
                                ' seconds ')

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()

        for i in range(len(self.players)):
            for x in range(len(self.players[i].snakes)):
                if not self.players[i].snakes[x].is_dead:

                    self.draw_head(painter,
                                   rect.left() + self.players[i].snakes[x].current_x_head * self.square_width(),
                                   boardtop + self.players[i].snakes[x].current_y_head * self.square_height(),
                                   'head' + str(i + 1) + '.png')

                    for j, pos in enumerate(self.players[i].snakes[x].snake):
                        if pos[0] == self.players[i].snakes[x].current_x_head \
                                and pos[1] == self.players[i].snakes[x].current_y_head:
                            pass
                        elif j == len(self.players[i].snakes[x].snake) - 1:
                            self.draw_tail(painter, rect.left() + pos[0] * self.square_width(),
                                           boardtop + pos[1] * self.square_height(), 'tail' + str(i + 1) + '.png')
                        else:
                            self.draw_body(painter, rect.left() + pos[0] * self.square_width(),
                                           boardtop + pos[1] * self.square_height(), 'body' + str(i + 1) + '.png')

        for pos in self.food.pos:
            self.draw_food(painter, rect.left() + pos[0] * self.square_width(),
                           boardtop + pos[1] * self.square_height(), 'apple.png')
        for pos in self.bonus.pos:
            self.draw_bonus_or_malus(painter, rect.left() + pos[0] * self.square_width(),
                                     boardtop + pos[1] * self.square_height(), 'bonus.png')
        for pos in self.malus.pos:
            self.draw_bonus_or_malus(painter, rect.left() + pos[0] * self.square_width(),
                                     boardtop + pos[1] * self.square_height(), 'malus.png')
        for pos in self.players[self.active_player].snakes[self.active_snake].snake:
            self.draw_glow(painter, rect.left() + pos[0] * self.square_width(),
                           boardtop + pos[1] * self.square_height(), 'glow.png')

    def draw_food(self, painter, x, y, file):

        image = QImage(load_res(file))

        painter.drawImage(QRect(x + 1, y + 1, self.square_width() + 5, self.square_height() + 10), image)

    def draw_bonus_or_malus(self, painter, x, y, file):

        image = QImage(load_res(file))

        painter.drawImage(QRect(x + 1, y + 1, 30, 30), image)

    def draw_head(self, painter, x, y, file):
        image = QImage(load_res(file))

        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          image)

    def draw_body(self, painter, x, y, file):
        body = QImage(load_res(file))
        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          body)

    def draw_tail(self, painter, x, y, file):
        tail = QImage(load_res(file))
        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          tail)

    def draw_glow(self, painter, x, y, file):
        glow = QImage(load_res(file))
        painter.drawImage(QRect(int(x + 1), int(y + 1), int(self.square_width() + 5), int(self.square_height() + 5)),
                          glow)

    def keyPressEvent(self, event):
        key = event.key()
        if not self.game_over:
            if key == Qt.Key_Left:
                if self.players[self.active_player].snakes[self.active_snake].direction != 'RIGHT':
                    self.players[self.active_player].snakes[self.active_snake].direction = 'LEFT'
                    self.flag = True

            elif key == Qt.Key_Right:
                if self.players[self.active_player].snakes[self.active_snake].direction != 'LEFT':
                    self.players[self.active_player].snakes[self.active_snake].direction = 'RIGHT'
                    self.flag = True

            elif key == Qt.Key_Down:
                if self.players[self.active_player].snakes[self.active_snake].direction != 'UP':
                    self.players[self.active_player].snakes[self.active_snake].direction = 'DOWN'
                    self.flag = True

            elif key == Qt.Key_Up:
                if self.players[self.active_player].snakes[self.active_snake].direction != 'DOWN':
                    self.players[self.active_player].snakes[self.active_snake].direction = 'UP'
                    self.flag = True

            elif key == Qt.Key_S:
                if self.tab_mode:
                    if self.players[self.active_player].food_eaten >= 5:
                        split_snake(self, self.active_player)
                    else:
                        self.msg2statusbar.emit('Splitting is currently impossible')

            elif key == Qt.Key_N:
                self.interrupt_skip = True
                change_active_player(self)

            elif key == Qt.Key_Tab:
                if len(self.players[self.active_player].snakes) > 1:
                    change_active_snake(self)

    def move_snake(self):
        while True:
            if self.game_over:
                break
            if self.flag:
                if self.players[self.active_player].snakes[self.active_snake].steps_moved < \
                        len(self.players[self.active_player].snakes[self.active_snake].snake):
                    if self.players[self.active_player].snakes[self.active_snake].direction == 'LEFT':

                        self.players[self.active_player].snakes[self.active_snake].current_x_head, \
                        self.players[self.active_player].snakes[self.active_snake].current_y_head = \
                            self.players[self.active_player].snakes[self.active_snake].current_x_head - 1, \
                            self.players[self.active_player].snakes[self.active_snake].current_y_head
                        self.flag = False
                        self.players[self.active_player].snakes[self.active_snake].steps_moved += 1
                        if self.players[self.active_player].snakes[self.active_snake].current_x_head < 0:
                            self.players[self.active_player].snakes[
                                self.active_snake].current_x_head = Board.WIDTHINBLOCKS - 1
                    if self.players[self.active_player].snakes[self.active_snake].direction == 'RIGHT':
                        self.players[self.active_player].snakes[self.active_snake].current_x_head, \
                        self.players[self.active_player].snakes[self.active_snake].current_y_head = \
                            self.players[self.active_player].snakes[self.active_snake].current_x_head + 1, \
                            self.players[self.active_player].snakes[self.active_snake].current_y_head
                        self.flag = False
                        if self.players[self.active_player].snakes[
                            self.active_snake].current_x_head == Board.WIDTHINBLOCKS:
                            self.players[self.active_player].snakes[self.active_snake].current_x_head = 0
                        self.players[self.active_player].snakes[self.active_snake].steps_moved += 1

                    if self.players[self.active_player].snakes[self.active_snake].direction == 'DOWN':
                        self.players[self.active_player].snakes[self.active_snake].current_x_head, \
                        self.players[self.active_player].snakes[self.active_snake].current_y_head = \
                            self.players[self.active_player].snakes[self.active_snake].current_x_head, \
                            self.players[self.active_player].snakes[self.active_snake].current_y_head + 1
                        self.flag = False
                        if self.players[self.active_player].snakes[
                            self.active_snake].current_y_head == Board.HEIGHTINBLOCKS:
                            self.players[self.active_player].snakes[self.active_snake].current_y_head = 0
                        self.players[self.active_player].snakes[self.active_snake].steps_moved += 1

                    if self.players[self.active_player].snakes[self.active_snake].direction == 'UP':
                        self.players[self.active_player].snakes[self.active_snake].current_x_head, \
                        self.players[self.active_player].snakes[self.active_snake].current_y_head = \
                            self.players[self.active_player].snakes[self.active_snake].current_x_head, \
                            self.players[self.active_player].snakes[self.active_snake].current_y_head - 1
                        self.flag = False
                        if self.players[self.active_player].snakes[self.active_snake].current_y_head < 0:
                            self.players[self.active_player].snakes[
                                self.active_snake].current_y_head = Board.HEIGHTINBLOCKS
                        self.players[self.active_player].snakes[self.active_snake].steps_moved += 1

                    head = [self.players[self.active_player].snakes[self.active_snake].current_x_head,
                            self.players[self.active_player].snakes[self.active_snake].current_y_head]
                    self.players[self.active_player].snakes[self.active_snake].snake.insert(0, head)


                    if not self.players[self.active_player].snakes[self.active_snake].grow_snake:
                        self.players[self.active_player].snakes[self.active_snake].snake.pop()
                    else:
                        self.players[self.active_player].snakes[self.active_snake].grow_snake = False

                    self.check_collisions()
                    self.update()
            time.sleep(0.1)

    def deus_ex_machine_bonus(self):
        self.bonus_timer.cancel()
        self.drop_bonus()
        consumed = False
        time.sleep(2)
        for pos in self.bonus.pos:
            for i in range(len(self.players)):
                for x in range(len(self.players[i].snakes)):
                    for t in range(len(self.players[i].snakes[x].snake)):
                        if pos == self.players[i].snakes[x].snake[t]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True
                        elif self.players[i].snakes[x].snake[t] == [(pos[0] + 1), pos[1]]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [(pos[0] - 1), pos[1]]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [pos[0], (pos[1] + 1)]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [pos[0], (pos[1] - 1)]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [(pos[0] + 2), pos[1]]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [(pos[0] - 2), pos[1]]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [pos[0], (pos[1] + 2)]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [pos[0], (pos[1] - 2)]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [(pos[0] + 3), pos[1]]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [(pos[0] - 3), pos[1]]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [pos[0], (pos[1] + 3)]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [pos[0], (pos[1] - 3)]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [(pos[0] + 4), pos[1]]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [(pos[0] - 4), pos[1]]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [pos[0], (pos[1] + 4)]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [pos[0], (pos[1] - 4)]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [(pos[0] + 5), pos[1]]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [(pos[0] - 5), pos[1]]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [pos[0], (pos[1] + 5)]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True

                        elif self.players[i].snakes[x].snake[t] == [pos[0], (pos[1] - 5)]:
                            self.players[i].snakes[x].grow_snake = True
                            consumed = True
                    if consumed:
                        head = [self.players[i].snakes[x].current_x_head,
                                self.players[i].snakes[x].current_y_head]
                        self.players[i].snakes[x].snake.insert(0, head)
                        self.players[i].food_eaten += 2

            self.bonus.pos.remove(pos)
            self.update()

    def deus_ex_machine_malus(self):
        self.malus_timer.cancel()
        self.drop_malus()
        time.sleep(2)
        for pos in self.malus.pos:
            for i in range(len(self.players)):
                for x in range(len(self.players[i].snakes)):

                    if pos == self.players[i].snakes[x].snake[0]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 1), pos[1]]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 1), pos[1]]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 1)]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 1)]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 2), pos[1]]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 2), pos[1]]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 2)]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 2)]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 3), pos[1]]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 3), pos[1]]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 3)]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 3)]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 4), pos[1]]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 4), pos[1]]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 4)]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 4)]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] + 5), pos[1]]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [(pos[0] - 5), pos[1]]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] + 5)]:
                        self.players[i].snakes[x].snake.pop()
                    elif self.players[i].snakes[x].snake[0] == [pos[0], (pos[1] - 5)]:
                        self.players[i].snakes[x].snake.pop()

            self.malus.pos.remove(pos)
            self.update()

    def check_if_alive(self):
        for i in range(len(self.players)):
            for j in range(len(self.players[i].snakes)):
                if not self.players[i].snakes[j].is_dead:
                    break
            else:
                self.players[i].is_dead = True

    def check_winner(self):
        for i in range(len(self.players)):
            if self.players[i].is_dead:
                self.dead_players += 1

        if self.dead_players == len(self.players) - 1:
            self.setStyleSheet(
                'border-image: url(' + load_style_res(str(self.active_player + 1) + 'won' + '.png') +
                ') 0 0 0 0 stretch center')

            self.r.cancel()
            self.t.cancel()
            self.bonus_timer.cancel()
            self.malus_timer.cancel()
            self.game_over = True
            self.msg2statusbar.emit('Game over!')

        else:
            self.dead_players = 0

    def countdown(self):
        if self.cntdwn == 0:
            if self.game_speed == 1:
                self.cntdwn = 15
            elif self.game_speed == 2:
                self.cntdwn = 12
            elif self.game_speed == 3:
                self.cntdwn = 10
        self.cntdwn -= 1

        self.msg2statusbar.emit(self.players[self.active_player].name + '\'s turn. ' + str(self.cntdwn + 1)
                                + ' seconds left.' + ' Snake ' + str(self.active_snake + 1) + ' active')

    def check_collisions(self):
        is_suicide(self)
        is_food_collision(self)
        wall_collision(self)
        snake_collision(self)
        self.check_winner()

    def drop_bonus(self):
        rand_p = random.choice(self.players)

        rand_s = random.choice(rand_p.snakes)

        x = random.randint(rand_s.snake[0][0] + 1, rand_s.snake[0][0] + 5)
        y = random.randint(rand_s.snake[0][1] + 1, rand_s.snake[0][1] + 5)
        if [x, y] == rand_s.snake[0] or x > 58 or x < 2 or y > 38 or y < 2:
            self.drop_bonus()
        else:
            self.bonus.pos.append([x, y])
            self.update()

    def drop_malus(self):
        rand_p = random.choice(self.players)

        rand_s = random.choice(rand_p.snakes)
        x = random.randint(rand_s.snake[0][0] + 1, rand_s.snake[0][0] + 5)
        y = random.randint(rand_s.snake[0][1] + 1, rand_s.snake[0][1] + 5)

        if [x, y] == rand_s.snake[0] or x > 58 or x < 2 or y > 38 or y < 2:
            self.drop_malus()
        else:
            self.malus.pos.append([x, y])
            self.update()
