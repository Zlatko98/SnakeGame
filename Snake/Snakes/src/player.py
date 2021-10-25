from helpers import load_style_res

from food import Food


class Player(object):
    def __init__(self, name):
        self.name = name
        self.snakes = []
        self.score = 0
        self.split = False
        self.is_dead = False
        self.can_split = True
        self.food_eaten = 0
        self.turn = 0


def change_active_player(self):
    if self.interrupt_skip:
        self.t.cancel()
        if self.game_speed == 1:
            self.cntdwn = 15
        elif self.game_speed == 2:
            self.cntdwn = 12
        elif self.game_speed == 3:
            self.cntdwn = 10
        self.t.start()
        self.interrupt_skip = False

    self.flag = False
    for i in self.players[self.active_player].snakes:
        i.steps_moved = 0
    if self.active_player < len(self.players) - 1:
        i = self.active_player + 1
    else:
        i = 0

    while i < len(self.players):
        if not self.players[i].is_dead:
            for x in range(len(self.players[i].snakes)):
                if not self.players[i].snakes[x].is_dead:
                    self.active_snake = x
                    break
            self.active_player = i
            break
        else:

            if i + 1 == len(self.players):
                i = 0
            else:
                i += 1
            continue

    for k in range(len(self.players)):
        for j in range(len(self.players[k].snakes)):
            if self.players[k].snakes[j].grow_snake:
                break
            else:
                self.players[k].turn += 1
                if self.players[k].turn == len(self.players):
                    self.food.move_food()
                    self.players[k].turn = 0

    self.setStyleSheet(
        'border-image: url(' + load_style_res('grassp' + str(self.active_player + 1) + '.png') +
        ') 0 0 0 0 stretch center')


def check_number_of_live_snakes(self):
    i = 0
    for x in self.players[self.active_player].snakes:
        if not x.is_dead:
            i += 1
    if i < 2:
        self.players[self.active_player].can_split = True
    else:
        self.players[self.active_player].can_split = False