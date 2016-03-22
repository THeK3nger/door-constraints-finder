import movingaiparser
import componentlabeling
import door_constraints_solver

key_map = movingaiparser.parse_map('keydoor.map')
labels = componentlabeling.connected_component_labeling(key_map)
cg = componentlabeling.connectivity_graph(key_map, labels)

print(door_constraints_solver.constraints_solver((1,1), (17,9), key_map, labels, cg))