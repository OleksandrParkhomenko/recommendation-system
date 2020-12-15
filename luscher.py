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

    def __get_normalized_vc(self):
        vc_table = {0: range(20, 48),
                    1: range(48, 100),
                    2: range(100, 151),
                    3: range(151, 501)}
        for normalized_value, diapason in vc_table.items():
            if int(self.vegetative_coefficient * 100) in diapason:
                return normalized_value

    def __get_normalized_td(self):
        return self.total_deviation // 8 - 1

    def get_interpretation(self):
        mood_table = [["energetic", "energetic", "energetic", "energetic"],
                      ["happy", "exuberance", "frantic", "anxious/sad"],
                      ["happy", "contentment", "depression", "anxious/sad"],
                      ["calm", "calm", "calm", "calm"]]
        print(self.total_deviation)
        print(self.vegetative_coefficient)
        return mood_table[self.__get_normalized_vc()][self.__get_normalized_td()]


if __name__ == "__main__":
    #    seq = [1, 6, 2, 4, 3, 0, 5, 7]
    #    seq = [2, 3, 6, 7, 0, 4, 1, 5]
    # seq = [4, 2, 7, 1, 0, 5, 6, 3]
    lena_seq = [5, 0, 7, 2, 6, 4, 3, 1]
    seq = lena_seq
    luscher = Luscher(seq)
    print(luscher.get_interpretation())
