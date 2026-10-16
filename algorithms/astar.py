
import heapq


def heuristic(a, b):
    """Manhattan distance between two grid cells."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    """
    Find a shortest path using A*.

    Parameters:
        grid: 2D NumPy array (0 = free, 1 = obstacle)
        start: (row, col)
        goal: (row, col)

    Returns:
        List of grid coordinates, or None if unreachable.
    """

    rows, cols = grid.shape

    def valid(cell):
        r, c = cell
        return (
            0 <= r < rows
            and 0 <= c < cols
            and grid[r, c] == 0
        )

    if not valid(start) or not valid(goal):
        raise ValueError("Start or goal is invalid.")

    # Priority queue: (f_score, position)
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), start))

    came_from = {}
    g_score = {start: 0}
    closed = set()

    # Move up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_list:
        _, current = heapq.heappop(open_list)

        if current in closed:
            continue

        if current == goal:
            path = [current]

            while current in came_from:
                current = came_from[current]
                path.append(current)

            path.reverse()
            return path

        closed.add(current)

        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)

            if not valid(neighbor) or neighbor in closed:
                continue

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = tentative_g + heuristic(neighbor, goal)

                heapq.heappush(
                    open_list,
                    (f_score, neighbor)
                )

    return None
