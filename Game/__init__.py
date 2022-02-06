from pygomo.game.tree_node import *


class Game:
    def __init__(self, board):
        self.board = board

    @staticmethod
    def lgs(data):
        for i in range(len(data)):
            rule = [[1, 0], [0, 1], [1, -1], [1, 1]]
            for rx, ry in rule:
                lst = [data[i]]
                if [lst[0][0] + rx * 4, lst[0][1] + ry * 4] not in data or \
                        [lst[0][0] + rx * 3, lst[0][1] + ry * 3] not in data or \
                        [lst[0][0] + rx * 2, lst[0][1] + ry * 2] not in data or \
                        [lst[0][0] + rx * 1, lst[0][1] + ry * 1] not in data \
                        or [lst[0][0] + rx * 5, lst[0][1] + ry * 5] in data or [lst[0][0] - rx, lst[0][1] - ry] in data:
                    continue
                else:
                    return True
        return False

    def is_win(self):
        data = []
        for i in self.board:
            clean_text = i.replace(' ', '')
            x = int(clean_text.split(',')[0])
            y = int(clean_text.split(',')[1])
            data.append([x, y])
        db = self.lgs(data[::2])
        dw = self.lgs(data[1::2])
        return True in (db, dw)
