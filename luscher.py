GREY = 0
BLUE = 1
GREEN = 2
RED = 3
YELLOW = 4
VIOLET = 5
BROWN = 6
BLACK = 7

IDEAL_COLOR_SEQUENCE = [3, 4, 2, 5, 1, 6, 0, 7]


class Luscher:

    def __init__(self, color_sequence=[]):
        self.color_sequence = color_sequence
        self.total_deviation = self.get_total_deviation()
        self.vegetative_coefficient = self.get_vegetative_coefficient()

    def __str__(self):
        return "Vegetative coefficient: {}, total deviation: {}".format(self.total_deviation,
                                                                        self.vegetative_coefficient)

    def get_total_deviation(self):
        deviation = 0
        for color in self.color_sequence:
            deviation += abs(self.color_sequence.index(color) - IDEAL_COLOR_SEQUENCE.index(color))

        return deviation

    #  vegetative coefficient equation :
    #  VC = (18 — RED — YELLOW) / (18 — BLUE — GREEN)
    def get_vegetative_coefficient(self):
        return (18 - self.color_sequence.index(RED) - self.color_sequence.index(YELLOW)) / \
               (18 - self.color_sequence.index(BLUE) - self.color_sequence.index(GREEN))


if __name__ == "__main__":
    seq = [1, 6, 2, 4, 3, 0, 5, 7]
    seq = [2, 3, 6, 7, 0, 4, 1, 5]
    luscher = Luscher(seq)
    print(luscher)
