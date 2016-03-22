import random

import numpy as np
import matplotlib.pyplot as plt

import movingaiparser

def connected_component_labeling(map):
    labels_map = np.zeros(shape=(map.height, map.width))

    def find_neighbors(r, c):
        return [labels_map[x,y] for x,y in [(r-1,c), (r, c-1)] if x >= 0 and y >= 0 and map.is_free(x,y)]

    def find(element, set_dictionary):
        for key, value in set_dictionary.items():
            if element in value:
                return key

    # First Pass
    next_label = 1
    linked = {}
    for r, row in enumerate(map.matrix):
        for c, column in enumerate(row):
            if map.is_free(r, c):
                neighbors = find_neighbors(r, c)

                if len(neighbors) == 0:
                    labels_map[r,c] = next_label
                    linked[next_label] = { next_label }
                    next_label += 1
                else:
                    min_label = min(neighbors)
                    labels_map[r,c] = min_label
                    linked[min_label] = linked[min_label].union(set(neighbors))

    # Second Pass
    for r, row in enumerate(map.matrix):
        for c, column in enumerate(row):
            if map.is_free(r, c):
                labels_map[r,c] = find(labels_map[r,c], linked)

    return labels_map

def plot_label_map(map, labels_map):
    color_dict = {}

    def pick_color(r,c):
        free = map.is_free(r, c)
        if map.is_door(r, c):
            return [0.0,0.0,1.0]
        if not free:
            return [0.0,0.0,0.0]
        if labels_map[r,c] in color_dict.keys():
            return color_dict[labels_map[r,c]]
        else:
            color_dict[labels_map[r,c]] = [random.uniform(0.0,1.0), random.uniform(0.0,1.0), random.uniform(0.0,1.0)]
            return color_dict[labels_map[r,c]]


    img_width = map.width
    img_height = map.height
    image_array = np.array([[pick_color(r, c) for c in range(img_width)] for r in range(img_height)])
    fig, ax = plt.subplots()
    plt.imshow(image_array, interpolation="nearest")
    ax.autoscale(False)
    plt.grid()

def connectivity_graph(map, labels_map):
    doors = [d for partial_doors in map.doors.values() for d in partial_doors]
    connectivity = {}

    def find_neighbors(pos):
        r, c = pos
        return set([labels_map[x,y] for x,y in [(r-1,c), (r+1,c), (r,c-1), (r,c+1)] if labels_map[x,y] != 0])

    for d in doors:
        doors_key = map.find_key(d)
        if doors_key in connectivity:
            connectivity[doors_key] = connectivity[doors_key].union(find_neighbors(d))
        else:
            connectivity[doors_key] = find_neighbors(d)
    return connectivity
