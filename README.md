## door-constraints-finder

This is a prototype for a preprocessing algorithm to use in combination with
a **Inventory-Aware Pathfinding** algorithm. The goal is to speedup the
pathfinding search by identifying a set o _"mandatory keys"_ that have to be
used in order to reach the destination. This will (hoepfully) allow to avoid
search for that "item layers" that are guaranteed to have no solution.

Note that the output is a "necessary set". This means that it is possible that
for one the key combination a solution can not be found (e.g., because the
key for the door is unreachable by itself).

Actually, this is just an exploratory repository used to validate some algorithms and
ideas.
