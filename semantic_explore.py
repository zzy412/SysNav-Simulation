
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from algorithms.astar import astar
from algorithms.exploration import RoomExplorer
from simulation.robot import Robot
from simulation.world import World
from semantic.scene_graph import SceneGraph
from semantic.semantic_planner import SemanticPlanner


# =====================================
# 1. Create the indoor map
# =====================================

grid = np.zeros((30, 45), dtype=int)

# Outer walls
grid[0, :] = 1
grid[-1, :] = 1
grid[:, 0] = 1
grid[:, -1] = 1

# Room partitions
grid[1:29, 15] = 1
grid[1:29, 30] = 1

# Doors
grid[13:17, 15] = 0
grid[13:17, 30] = 0

# Furniture
grid[5:11, 4:10] = 1
grid[5:10, 20:25] = 1

# Move kitchen cabinet to avoid covering fridge
grid[5:11, 32:35] = 1


# =====================================
# 2. Define rooms
# =====================================

rooms = {
    "Bedroom": {
        "columns": (1, 14),
        "waypoint": (19, 7)
    },
    "Living Room": {
        "columns": (16, 29),
        "waypoint": (19, 22)
    },
    "Kitchen": {
        "columns": (31, 43),
        "waypoint": (19, 37)
    }
}


def get_room(position):
    _, col = position

    for name, info in rooms.items():
        left, right = info["columns"]

        if left <= col <= right:
            return name

    return None


# =====================================
# 3. Initialize modules
# =====================================

robot = Robot((20, 7))
world = World()
scene = SceneGraph()
planner = SemanticPlanner()

for name, info in rooms.items():
    scene.add_room(name, info["waypoint"])

import os

OUTPUT_GIF = "assets/semantic_explore.gif"
os.makedirs("assets", exist_ok=True)

task = "Find the refrigerator."
target = planner.parse_task(task)

ranked_rooms = planner.rank_rooms(
    target, list(rooms.keys())
)

selected_room = ranked_rooms[0]

print("Task:", task)
print("Target:", target)
print("Room priority:", ranked_rooms)
print("Selected room:", selected_room)


# =====================================
# 4. Observation and robot movement
# =====================================

found = False
observed_ids = set()

# Store animation history
positions = [robot.position]
found_history = [False]


def observe_current_position():
    global found

    current_room = get_room(robot.position)

    if current_room is None:
        return

    detections = world.observe(
        robot.position,
        current_room,
        grid,
        sensor_range=5
    )

    for obj in detections:
        obj_id = (
            obj["room"],
            obj["category"],
            obj["position"]
        )

        if obj_id not in observed_ids:
            observed_ids.add(obj_id)

            scene.add_object(
                obj["category"],
                obj["room"]
            )

            print(
                "Observed:",
                obj["category"],
                "at",
                obj["position"]
            )

        if obj["category"] == target:
            found = True
            print("TARGET FOUND:", obj["position"])


def follow_path(path):
    """
    Move along a path, observing at every step.
    Stop immediately if the target is found.
    """
    if path is None:
        return

    for position in path[1:]:
        if found:
            break

        robot.move_to(position)
        observe_current_position()

        positions.append(robot.position)
        found_history.append(found)


# Observe the starting position
observe_current_position()
found_history[0] = found


# =====================================
# 5. Navigate to selected room
# =====================================

destination = rooms[selected_room]["waypoint"]

initial_path = astar(
    grid,
    robot.position,
    destination
)

if initial_path is None:
    raise RuntimeError("Cannot reach selected room.")

print("\nNavigating to:", selected_room)

follow_path(initial_path)


# =====================================
# 6. Explore the selected room
# =====================================

explorer = RoomExplorer(
    grid,
    rooms[selected_room]["columns"]
)

viewpoints = explorer.generate_viewpoints(step=4)

print("Candidate viewpoints:", len(viewpoints))

remaining = list(viewpoints)
visited_count = 0

while not found and remaining:

    next_point, path = explorer.select_next_viewpoint(
        robot.position,
        remaining
    )

    if next_point is None:
        print("No reachable viewpoints remain.")
        break

    remaining.remove(next_point)

    print("Exploring viewpoint:", next_point)

    follow_path(path)

    visited_count += 1


# =====================================
# 7. Report result
# =====================================

print("\n===== Search Result =====")
print("Task success:", found)
print("Visited viewpoints:", visited_count)
print("Total movement steps:", len(positions) - 1)

print("\nObserved scene graph:")
scene.show_rooms()

# =====================================
# 8. Animate recorded movement
# =====================================

fig, ax = plt.subplots(figsize=(12, 7))

ax.imshow(grid, cmap="Greys", origin="upper")

ax.text(7, 3, "Bedroom", ha="center")
ax.text(22, 3, "Living Room", ha="center")
ax.text(37, 3, "Kitchen", ha="center")

ax.plot(
    destination[1],
    destination[0],
    "gx",
    markersize=10,
    label="Initial Room Waypoint"
)

robot_marker, = ax.plot(
    [], [],
    "bo",
    markersize=10,
    label="Robot"
)

trajectory_line, = ax.plot(
    [], [],
    color="blue",
    linewidth=2,
    label="Trajectory"
)

status_text = ax.text(
    0.02, 0.02, "",
    transform=ax.transAxes,
    fontsize=11
)

ax.set_title("SysNav - In-room Exploration")
ax.set_xlabel("Grid Column")
ax.set_ylabel("Grid Row")
ax.legend()
ax.grid(alpha=0.2)

def update(frame):
    row, col = positions[frame]

    robot_marker.set_data([col], [row])

    visited = positions[:frame + 1]

    trajectory_line.set_data(
        [p[1] for p in visited],
        [p[0] for p in visited]
    )

    status_text.set_text(
        f"Step: {frame}/{len(positions)-1} "
        f"| Target: {target} "
        f"| Found: {found_history[frame]}"
    )

    return robot_marker, trajectory_line, status_text

ani = FuncAnimation(
    fig,
    update,
    frames=len(positions),
    interval=100,
    repeat=False,
    blit=False
)

print("Saving GIF...")
ani.save(
    OUTPUT_GIF,
    writer=PillowWriter(fps=10)
)
print(f"GIF saved to: {OUTPUT_GIF}")

plt.show()
