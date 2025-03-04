from typing import List, Any
from algofresco.tracer import DataStructureTracer
from algofresco.que import QueueVisualizer
import matplotlib as plt

# usage
tracer = DataStructureTracer(track_code_lines=True)
queue = []

# Tracked operations
def queue_operations():
    tracer.capture(queue, description="Initial state")
    queue.append(10)  # Enqueue
    tracer.capture(queue, description="Enqueued 10")
    queue.append(20)  # Enqueue
    tracer.capture(queue, description="Enqueued 20")
    queue.pop(0)      # Dequeue
    tracer.capture(queue, description="Dequeued 10")

queue_operations()

# Visualization
visualizer = QueueVisualizer(tracer)

# Show final state with code
visualizer.display_snapshot(show_code=True, 
                          title="Final Queue State")

# Generate animation
anim = visualizer.create_animation(show_code=True, interval=1500)
anim.save("queue_operations.gif", writer="pillow")