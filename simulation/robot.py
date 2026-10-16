
class Robot:
    def __init__(self, start):
        """
        Initialize robot position.

        start: (row, column)
        """
        self.position = start
        self.trajectory = [start]

    def move_to(self, new_position):
        """
        Move robot to a new grid position.
        """
        self.position = new_position
        self.trajectory.append(new_position)

    def get_position(self):
        return self.position

    def get_trajectory(self):
        return self.trajectory
