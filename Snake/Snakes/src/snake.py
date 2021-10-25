import collisions
from player import check_number_of_live_snakes


class Snake(object):
    def __init__(self):
        self.snake = []
        self.current_x_head = None
        self.current_y_head = None
        self.direction = None
        self.grow_snake = False
        self.is_dead = False
        self.steps_moved = 0


def change_active_snake(self):
    self.flag = False
    if self.active_snake < len(self.players[self.active_player].snakes) - 1:
        i = self.active_snake + 1
    else:
        i = 0
    while i < len(self.players[self.active_player].snakes):
        if not self.players[self.active_player].snakes[i].is_dead:
            self.active_snake = i
            break
        else:
            if i + 1 == len(self.players[self.active_player].snakes):
                i = 0
            else:
                i += 1

            continue


def split_snake(self, active_player: int):
    check_number_of_live_snakes(self)
    new_snake = Snake()
    snake = []
    if self.players[active_player].can_split:

        if self.players[active_player].snakes[self.active_snake].direction == 'RIGHT' or \
                self.players[active_player].snakes[self.active_snake].direction == 'LEFT':
            for i in range(5):
                snake.append([self.players[active_player].snakes[self.active_snake].snake[i][0],
                              self.players[active_player].snakes[self.active_snake].snake[i][1] - 3])
            if not collisions.check_split_collision(self, snake):
                snake.clear()
                for i in range(5):
                    snake.append([self.players[active_player].snakes[self.active_snake].snake[i][0],
                                  self.players[active_player].snakes[self.active_snake].snake[i][1] + 3])

                if not collisions.check_split_collision(self, snake):
                    return
        elif self.players[active_player].snakes[self.active_snake].direction == 'UP' or \
                self.players[active_player].snakes[self.active_snake].direction == 'DOWN':
            for x in range(5):
                snake.append([self.players[active_player].snakes[self.active_snake].snake[x][0] - 3,
                              self.players[active_player].snakes[self.active_snake].snake[x][1]])
            if not collisions.check_split_collision(self, snake):
                snake.clear()
                for x in range(5):
                    snake.append([self.players[active_player].snakes[self.active_snake].snake[x][0] + 3,
                                  self.players[active_player].snakes[self.active_snake].snake[x][1]])
                if not collisions.check_split_collision(self, snake):
                    return
        new_snake.snake = snake
        new_snake.direction = self.players[active_player].snakes[self.active_snake].direction

        new_snake.current_x_head = new_snake.snake[0][0]
        new_snake.current_y_head = new_snake.snake[0][1]
        for k in range(5):
            self.players[active_player].snakes[self.active_snake].snake.pop()
        self.players[active_player].snakes.append(new_snake)
        self.players[self.active_player].food_eaten = 0
        self.update()