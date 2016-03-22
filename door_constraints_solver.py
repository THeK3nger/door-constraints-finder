"""
Given a starting and an ending cell it returns the "validity doors" sets in which the solution may apply.
"""

def constraints_solver(start, end, map, label_map, connectivity_graph):
    sr, sc = start
    er, ec = end
    start_label = label_map[sr,sc]
    end_label = label_map[er,ec]

    closed_paths = []

    if start_label == end_label:
        print("Start and End in the Same Area")
        closed_paths.append([])

    current_label = end_label
    open_paths = []
    adjacent_labels = label_neighbors(current_label, connectivity_graph)
    open_paths += [[a, (None, current_label)] for a in adjacent_labels]

    while len(open_paths) > 0:
        current_path = open_paths.pop()
        required_key, current_label = current_path[0]
        if current_label == start_label:
            closed_paths.append(current_path)
            continue
        adjacent_labels = label_neighbors(current_label, connectivity_graph)
        for k,l in adjacent_labels:
            if not label_in_path(l, current_path):
                new_path = current_path[:]
                new_path.insert(0, (k, l))
                open_paths.append(new_path)

    return closed_paths

def label_in_path(label, path):
    """
    path is a list such that [(k3,l3),(k2,l2),(k1,l1)]

    check if label is in there
    """
    labels_in_path = [l for _,l in path]
    return label in labels_in_path

def label_neighbors(current, connectivity_graph):
    neighbs = []
    for key, labels in connectivity_graph.items():
        if current in labels:
            # (key, label) stand for "I can go to \label\ passing through a dore opened by \key\"
            neighbs += [(key, label) for label in labels if current != label]
    return set(neighbs)