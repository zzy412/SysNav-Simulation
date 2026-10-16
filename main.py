
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from algorithms.astar import astar
from simulation.robot import Robot


# ==================================
# 1. Create indoor map
# ==================================

grid = np.zeros((30, 45), dtype=int)

# Outer walls
grid[0, :] = 1
grid[-1, :] = 1
grid[:, 0] = 1
grid[:, -1] = 1

# Room walls
grid[1:29, 15] = 1
grid[1:29, 30] = 1

# Door openings
grid[13:17, 15] = 0
grid[13:17, 30] = 0

# Furniture obstacles
grid[5:11, 4:10] = 1
grid[5:10, 20:25] = 1
grid[5:11, 35:40] = 1


# ==================================
# 2. Initialize robot and goal
# ==================================

start = (20, 7)
goal = (20, 37)

robot = Robot(start)


# ==================================
# 3. A* Path Planning
# ==================================

path = astar(grid, start, goal)

if path is None:
    raise RuntimeError("No valid path found!")

print("Path found!")
print("Total steps:", len(path) - 1)


# ==================================
# 4. Initialize visualization
# ==================================

fig, ax = plt.subplots(figsize=(12, 7))

ax.imshow(grid, cmap="Greys", origin="upper")

# Planned path
path_rows = [p[0] for p in path]
path_cols = [p[1] for p in path]

ax.plot(
    path_cols,
    path_rows,
    color="skyblue",
    linestyle="--",
    linewidth=1.5,
    label="Planned Path"
)

# Robot marker
robot_marker, = ax.plot(
    [start[1]], [start[0]],
    "bo",
    markersize=10,
    label="Robot"
)

# Actual trajectory
trajectory_line, = ax.plot(
    [], [],
    color="blue",
    linewidth=2.5,
    label="Actual Trajectory"
)

# Goal marker
ax.plot(
    goal[1],
    goal[0],
    "r*",
    markersize=14,
    label="Goal"
)

# Room labels
ax.text(7, 3, "Bedroom", ha="center")
ax.text(22, 3, "Living Room", ha="center")
ax.text(37, 3, "Kitchen", ha="center")

ax.set_title("SysNav - Robot Motion Simulation")
ax.set_xlabel("Grid Column")
ax.set_ylabel("Grid Row")
ax.legend()
ax.grid(alpha=0.2)


# ==================================
# 5. Animation update
# ==================================

def update(frame):
    # Move along A* path
    if frame > 0:
        robot.move_to(path[frame])

    row, col = robot.get_position()

    # Update robot position
    robot_marker.set_data([col], [row])

    # Update actual trajectory
    trajectory = robot.get_trajectory()

    rows = [p[0] for p in trajectory]
    cols = [p[1] for p in trajectory]

    trajectory_line.set_data(cols, rows)

    ax.set_title(
        f"SysNav - Step {frame}/{len(path) - 1}"
    )

    return robot_marker, trajectory_line


# ==================================
# 6. Run animation
# ==================================

ani = FuncAnimation(
    fig,
    update,
    frames=len(path),
    interval=300,
    repeat=False,
    blit=False
)

plt.show()

print("Simulation window closed.")
