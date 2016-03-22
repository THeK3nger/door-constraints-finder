import itertools

import numpy as np
import matplotlib.pyplot as plt


class MovingAIMap(object):

    def __init__(self, header, map_matrix):
        self.matrix = map_matrix
        self.height = len(map_matrix)
        self.width = len(map_matrix[0])
        self.type = 'unknown'
        self.doors = {}
        self._parse_header(header)

    def _parse_header(self, header):
        parsed_header = [(h.split(' ')[0], h.split(' ')[1:]) for h in header]
        for command, values in parsed_header:
            if command == "height":
                self.height = int(values[0])
            elif command == "width":
                self.width = int(values[0])
            elif command == "type":
                self.type = values[0]
            elif command == "key":
                self._parse_keys(values)

    def _parse_keys(self, values):
        values = [int(v) for v in values]  # Convert all to integers.
        pairs = list(pairwise(values))
        self.doors[pairs[0]] = pairs[1:]

    def is_door(self, r, c=None):
        if c is None:
            r, c = r
        return any(((r, c) in doors for doors in self.doors.values()))

    def is_key(self, r, c=None):
        if c is None:
            r, c = r
        return (r, c) in self.doors.keys()

    def is_free(self, r, c=None):
        if c is None:
            r, c = r
        return self.matrix[r][c] != '@' and not self.is_door(r, c)

    def find_key(self, r, c=None):
        if c is None:
            r, c = r
        if self.is_door(r, c):
            for k, v in self.doors.items():
                if (r,c) in v:
                    return k

    def plot(self):
        CRed = [1.0, 0.0, 0.0]
        CWhite = [1.0, 1.0, 1.0]
        CBlack = [0.0, 0.0, 0.0]
        CBlue = [0.0, 0.0, 1.0]

        def pick_color(r, c):
            """
            Select a color for the image according to the value of the tile in te map.
            :param r: The row.
            :param c: The column.
            :return:
            """
            free = self.is_free(r, c)
            if self.is_key(r, c):
                return CRed
            if self.is_door(r, c):
                return CBlue
            return CWhite if free else CBlack

        def generate_image_array():
            """
            Generate an image of the map.
            :return:
            """
            img_width = self.width
            img_height = self.height
            image_array = np.array([[pick_color(r, c) for c in range(img_width)] for r in range(img_height)])
            return image_array

        fig, ax = plt.subplots()
        plt.imshow(generate_image_array(), interpolation="nearest")
        ax.autoscale(False)
        plt.grid()
        #fig.show()

    def __str__(self):
        result = "Moving AI Map\n"
        result += "\ttype = {}".format(self.type)
        result += "\theight = {}".format(self.height)
        result += "\twidth = {}".format(self.height)
        result += "\tkey-doors = {}".format(self.doors)
        return result


def parse_map(map_path):
    map_file = open(map_path, 'r')
    raw_map = map_file.read()
    raw_map_lines = raw_map.split('\n')
    header = list(itertools.takewhile(lambda l: l != "map", raw_map_lines))
    map_matrix = list(itertools.dropwhile(lambda l: l != "map", raw_map_lines))[1:]
    return MovingAIMap(header, map_matrix)


def pairwise(iterable):
    return zip(iterable[::2], iterable[1::2])

#######################################################

