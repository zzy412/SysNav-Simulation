
from algorithms.astar import astar


class RoomExplorer:
    def __init__(self, grid, room_columns):
        self.grid = grid
        self.room_columns = room_columns

    def generate_viewpoints(self, step=4):
        """
        Generate candidate observation positions
        inside the room.
        """
        rows, cols = self.grid.shape
        left, right = self.room_columns

        viewpoints = []

        for r in range(2, rows - 1, step):
            for c in range(left + 1, right, step):
                if self.grid[r, c] == 0:
                    viewpoints.append((r, c))

        return viewpoints

    def select_next_viewpoint(self, current, viewpoints):
        """
        Select the nearest reachable viewpoint
        using actual A* path length.
        """
        best_point = None
        best_path = None
        best_cost = float("inf")

        for point in viewpoints:
            path = astar(self.grid, current, point)

            if path is None:
                continue

            cost = len(path) - 1

            if cost < best_cost:
                best_cost = cost
                best_point = point
                best_path = path

        return best_point, best_path
