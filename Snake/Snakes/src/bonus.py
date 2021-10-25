import random

import board


class Bonus(object):
    def __init__(self):
        self.pos = []

    def drop_bonus(self):

        x = random.randint(3, 56)
        y = random.randint(3, 36)
        # for pos in snake:  # Do not drop food on snake
        #     if pos == [x, y]:
        #         self.drop_food()
        self.pos.append([x, y])