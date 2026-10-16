
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from algorithms.astar import astar
from simulation.robot import Robot
from simulation.world import World
from semantic.scene_graph import SceneGraph
from semantic.semantic_planner import SemanticPlanner


# ==================================
# 1. Map construction
# ==================================
grid = np.zeros((30, 45), dtype=int)
grid[0, :] = grid[-1, :] = 1
grid[:, 0] = grid[:, -1] = 1

grid[1:29, 15] = 1
grid[1:29, 30] = 1
grid[13:17, 15] = 0
grid[13:17, 30] = 0

grid[5:11, 4:10] = 1
grid[5:10, 20:25] = 1
grid[5:11, 35:40] = 1

# Named room regions and their central positions
rooms = {
    "Bedroom": {"columns": (1, 14), "waypoint": (19, 7)},
    "Living Room": {"columns": (16, 29), "waypoint": (19, 22)},
    "Kitchen": {"columns": (31, 43), "waypoint": (19, 37)}
}


def get_room(position):
    _, col = position
    for name, info in rooms.items():
        left, right = info["columns"]
        if left <= col <= right:
            return name
    return None


# ==================================
# 2. Initialize components
# ==================================
robot = Robot((20, 7))
world = World()
scene = SceneGraph()
planner = SemanticPlanner()

for name, info in rooms.items():
    scene.add_room(name, info["waypoint"])

task = "Find the refrigerator."
target = planner.parse_task(task)

print("Task:", task)
print("Target:", target)

ranked_rooms = planner.rank_rooms(target, list(rooms))

print("Room search priority:", ranked_rooms)

# This first version only visits the top-ranked room.
selected_room = ranked_rooms[0]
waypoint = rooms[selected_room]["waypoint"]

path = astar(grid, robot.position, waypoint)

if path is None:
    raise RuntimeError("No route to selected room")


# ==================================
# 3. Visualization
# ==================================
fig, ax = plt.subplots(figsize=(12, 7))
ax.imshow(grid, cmap="Greys", origin="upper")

ax.text(7, 3, "Bedroom", ha="center")
ax.text(22, 3, "Living Room", ha="center")
ax.text(37, 3, "Kitchen", ha="center")

ax.plot(
    [p[1] for p in path],
    [p[0] for p in path],
    "--",
    color="skyblue",
    label="Planned Path"
)

marker, = ax.plot(
    [robot.position[1]],
    [robot.position[0]],
    "bo",
    markersize=10,
    label="Robot"
)

trail, = ax.plot([], [], color="blue", label="Trajectory")

status = ax.text(
    0.02, 0.02, "",
    transform=ax.transAxes,
    fontsize=10
)

ax.legend()
ax.set_title("SysNav - Semantic Object Navigation")


# ==================================
# 4. Animation and observation
# ==================================
found = False
observed_ids = set()


def update(frame):
    global found

    if not found and frame > 0:
        robot.move_to(path[frame])

    current_room = get_room(robot.position)

    if current_room is not None and not found:
        detections = world.observe(
            robot.position, current_room, grid
        )

        for obj in detections:
            object_id = (
                obj["room"],
                obj["category"],
                obj["position"]
            )

            if object_id not in observed_ids:
                observed_ids.add(object_id)
                scene.add_object(
                    obj["category"], obj["room"]
                )
                print("Observed:", obj["category"])

            if obj["category"] == target:
                found = True
                print("Target found!", obj["position"])

    row, col = robot.position
    marker.set_data([col], [row])

    trajectory = robot.get_trajectory()
    trail.set_data(
        [p[1] for p in trajectory],
        [p[0] for p in trajectory]
    )

    status.set_text(
        f"Task: {target} | Searching: {selected_room}"
        f" | Found: {found}"
    )

    return marker, trail, status


ani = FuncAnimation(
    fig, update, frames=len(path),
    interval=120, repeat=False,
    blit=False
)

plt.show()

print("\nFinal observed scene graph:")
scene.show_rooms()
print("Task success:", found)
