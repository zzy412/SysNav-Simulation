
import numpy as np
from algorithms.exploration import RoomExplorer

# Rebuild the current map
grid = np.zeros((30, 45), dtype=int)

grid[0, :] = grid[-1, :] = 1
grid[:, 0] = grid[:, -1] = 1

grid[1:29, 15] = 1
grid[1:29, 30] = 1

grid[13:17, 15] = 0
grid[13:17, 30] = 0

grid[5:11, 4:10] = 1
grid[5:10, 20:25] = 1
grid[5:11, 32:35] = 1

explorer = RoomExplorer(
    grid,
    room_columns=(31, 43)
)

viewpoints = explorer.generate_viewpoints()

print("Candidate viewpoints:", len(viewpoints))
print(viewpoints)

current = (19, 37)

next_point, path = explorer.select_next_viewpoint(
    current,
    viewpoints
)

print("Current position:", current)
print("Next viewpoint:", next_point)
print("Path length:", len(path) - 1 if path else None)
