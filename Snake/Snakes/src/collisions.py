import time

import snake
# from snake import change_active_snake
from player import change_active_player


def is_suicide(self):
    for j in range(2, len(self.players[self.active_player].snakes[self.active_snake].snake)):
        if self.players[self.active_player].snakes[self.active_snake].snake[0] == \
                self.players[self.active_player].snakes[self.active_snake].snake[j]:
            self.players[self.active_player].snakes[self.active_snake].is_dead = True
            self.check_if_alive()
            if self.players[self.active_player].is_dead:
                self.interrupt_skip = True
                change_active_player(self)
            else:
                snake.change_active_snake(self)
            break


def snake_collision(self):
    for i in range(len(self.players)):
        for j in range(len(self.players[i].snakes)):
            if self.players[i].snakes[j].is_dead:
                continue
            for x in range(len(self.players[i].snakes[j].snake)):
                if self.players[self.active_player].snakes[self.active_snake].snake[0] == \
                        self.players[i].snakes[j].snake[x]:
                    if i == self.active_player:
                        continue
                    self.players[self.active_player].snakes[self.active_snake].is_dead = True
                    self.check_if_alive()
                    if not self.players[self.active_player].is_dead:
                        snake.change_active_snake(self)
                    else:
                        self.interrupt_skip = True
                        change_active_player(self)
                    break


def check_split_collision(self, snake) -> bool:
    can_split = True
    x_left = 1
    x_right = 58
    y_bottom = 38
    y_top = 2
    for x in range(len(self.players)):
        for j in range(len(self.players[x].snakes)):
            for q in range(len(self.players[x].snakes[j].snake)):
                for t in range(5):
                    if snake[t] == self.players[x].snakes[j].snake[q]:
                        can_split = False
    for i in range(0, 40):
        for x in range(5):
            for j in range(5):
                if snake[x] == [x_left - j, i] \
                        or snake[x] == [x_right + j, i]:
                    can_split = False
    for j in range(0, 60):
        for x in range(5):
            for k in range(5):
                if snake[x] == [j, y_bottom + k] \
                        or snake[x] == [j, y_top - k]:
                    can_split = False
    if not can_split:
        self.msg2statusbar.emit('Splitting is currently impossible')

    return can_split


def wall_collision(self):
    x_left = 1
    x_right = 58
    y_bottom = 38
    y_top = 1

    for i in range(2, 38):
        if self.players[self.active_player].snakes[self.active_snake].snake[0] == [x_left, i] \
                or self.players[self.active_player].snakes[self.active_snake].snake[0] == [x_right, i]:
            self.players[self.active_player].snakes[self.active_snake].is_dead = True
            self.check_if_alive()
            if self.players[self.active_player].is_dead:
                self.interrupt_skip = True
                change_active_player(self)
            else:
                snake.change_active_snake(self)
            break

    for j in range(2, 58):
        if self.players[self.active_player].snakes[self.active_snake].snake[0] == [j, y_bottom] \
                or self.players[self.active_player].snakes[self.active_snake].snake[0] == [j, y_top]:
            self.players[self.active_player].snakes[self.active_snake].is_dead = True
            self.check_if_alive()
            if self.players[self.active_player].is_dead:
                self.interrupt_skip = True
                change_active_player(self)
            else:
                snake.change_active_snake(self)
            break


def is_food_collision(self):
    for pos in self.food.pos:
        for i in range(len(self.players)):
            for x in range(len(self.players[i].snakes)):
                if pos == self.players[i].snakes[x].snake[0]:
                    self.food.pos.remove(pos)
                    self.food.drop_food()
                    self.players[i].food_eaten += 1
                    self.players[i].snakes[x].grow_snake = True