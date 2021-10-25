import random

import board


class Malus(object):
    def __init__(self):
        self.pos = []

    def drop_malus(self):

        x = random.randint(3, 56)
        y = random.randint(3, 36)
        # for pos in snake:  # Do not drop food on snake
        #     if pos == [x, y]:
        #         self.drop_food()
        self.pos.append([x, y])