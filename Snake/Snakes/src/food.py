import random

import board


class Food(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos = []

    def drop_food(self):

        self.x = random.randint(3, 56)
        self.y = random.randint(3, 36)

        self.pos.append([self.x, self.y])

    def move_food(self):

        for i in range(len(self.pos)):
            k = random.randint(0, 1)
            if k == 0:
                j = random.randint(0, 1)
                if j == 0:
                    if self.pos[i][0] > 53:
                        self.pos[i][0] = random.randint(self.pos[i][0] - 3, self.pos[i][0])
                    else:
                        self.pos[i][0] = random.randint(self.pos[i][0], self.pos[i][0] + 3)

                else:
                    if self.pos[i][1] > 33:
                        self.pos[i][1] = random.randint(self.pos[i][1] - 3, self.pos[i][1])
                    else:
                        self.pos[i][1] = random.randint(self.pos[i][1], self.pos[i][1] + 3)

            else:
                j = random.randint(0, 1)
                if j == 0:
                    if self.pos[i][0] < 6:
                        self.pos[i][0] = random.randint(self.pos[i][0], self.pos[i][0] + 3)
                    else:
                        self.pos[i][0] = random.randint(self.pos[i][0] - 3, self.pos[i][0])
                else:
                    if self.pos[i][1] < 6:
                        self.pos[i][1] = random.randint(self.pos[i][1], self.pos[i][1] + 3)
                    else:
                        self.pos[i][1] = random.randint(self.pos[i][1] - 3, self.pos[i][1])


