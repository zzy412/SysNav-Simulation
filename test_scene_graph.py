
from semantic.scene_graph import SceneGraph

scene = SceneGraph()

# Add rooms
scene.add_room("Bedroom", (20, 7))
scene.add_room("Living Room", (20, 22))
scene.add_room("Kitchen", (20, 37))

# Add simulated object observations
scene.add_object("Bed", "Bedroom")
scene.add_object("Desk", "Bedroom")

scene.add_object("Sofa", "Living Room")
scene.add_object("TV", "Living Room")

scene.add_object("Fridge", "Kitchen")
scene.add_object("Cabinet", "Kitchen")

# Display scene graph information
scene.show_rooms()
