
class World:
    def __init__(self):
        # Hidden ground truth
        # Positions are (row, column)
        self.objects = [
            {"category": "Bed", "room": "Bedroom",
             "position": (8, 7)},
            {"category": "TV", "room": "Living Room",
             "position": (8, 22)},
            {"category": "Sofa", "room": "Living Room",
             "position": (19, 22)},
            {"category": "Fridge", "room": "Kitchen",
             "position": (8, 37)}
        ]

    def observe(self, robot_position, room_name, grid,
                sensor_range=5):
        """
        Simulate object detection within Manhattan range.
        Requires clear line of sight along the grid.
        """
        from math import floor

        def line_clear(start, end):
            r0, c0 = start
            r1, c1 = end
            steps = max(abs(r1-r0), abs(c1-c0)) * 3 + 1

            for i in range(1, steps):
                t = i / steps
                r = floor(r0 + (r1-r0)*t + 0.5)
                c = floor(c0 + (c1-c0)*t + 0.5)
                if grid[r, c] == 1:
                    return False
            return True

        detected = []

        for obj in self.objects:
            if obj["room"] != room_name:
                continue

            distance = (
                abs(robot_position[0]-obj["position"][0])
                + abs(robot_position[1]-obj["position"][1])
            )

            if distance <= sensor_range and line_clear(
                robot_position, obj["position"]
            ):
                detected.append(obj)

        return detected
