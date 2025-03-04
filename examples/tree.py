from typing import List, Any
from algofresco.tracer import DataStructureTracer
from algofresco.tree import TreeVisualizer
import networkx as nx

# Initialize components
tracer = DataStructureTracer(track_code_lines=True)

# Binary tree node class
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

@tracer.auto_trace
def tree_operations():
    root = TreeNode(1)
    tracer.capture(root, description="Root created")
    
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    tracer.capture(root, description="Added children")
    
    root.left.right = TreeNode(4)
    tracer.capture(root, description="Added grandchild", highlight_nodes=[4])

tree_operations()

# Visualization
visualizer = TreeVisualizer(tracer)

# Show specific step with highlights
# visualizer.display_snapshot(step=2, layout='dot', show_code=True)

# Create animation
anim = visualizer.create_animation(layout='dot', show_code=True)
anim.save("tree_evolution.gif", writer="pillow")