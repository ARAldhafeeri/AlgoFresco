from typing import List, Any
from algofresco.tracer import DataStructureTracer
from algofresco.dict import DictionaryVisualizer
import matplotlib as plt


tracer = DataStructureTracer(track_code_lines=True)
test_dict = {}

# Tracked operations
tracer.capture(test_dict, description="Initial state")

test_dict["age"] = 30
tracer.capture(test_dict, description="age -> 30")


test_dict["name"] = "Alice"
tracer.capture(test_dict, description="name -> Alice")


# Visualization
visualizer = DictionaryVisualizer(tracer)

# # Show specific state with highlights
# visualizer.display_snapshot(step=2, 
#                           highlight_keys=["age"],
#                           show_code=True,
#                           title="Age Update")

# Generate full animation
anim = visualizer.create_animation(show_code=True, interval=1500)
anim.save("dict_changes.gif", writer="pillow")