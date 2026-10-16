
import networkx as nx


class SceneGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_room(self, room_name, position):
        self.graph.add_node(
            room_name,
            type="room",
            position=position
        )

    def add_object(self, object_name, room_name):
        if room_name not in self.graph:
            raise ValueError(f"Unknown room: {room_name}")

        object_id = f"{room_name}:{object_name}"

        self.graph.add_node(
            object_id,
            type="object",
            category=object_name
        )

        self.graph.add_edge(
            room_name,
            object_id,
            relation="contains"
        )

    def get_room_objects(self, room_name):
        objects = []

        for neighbor in self.graph.neighbors(room_name):
            if self.graph.nodes[neighbor]["type"] == "object":
                objects.append(
                    self.graph.nodes[neighbor]["category"]
                )

        return objects

    def show_rooms(self):
        for node, data in self.graph.nodes(data=True):
            if data["type"] == "room":
                print(node, ":", self.get_room_objects(node))
