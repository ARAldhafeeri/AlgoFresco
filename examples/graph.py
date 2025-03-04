# from typing import List, Any
# from algofresco.tracer import DataStructureTracer
# from algofresco.graph import GraphVisualizer
# import networkx as nx

# # Initialize components
# tracer = DataStructureTracer(track_code_lines=True)
# G = nx.Graph()

# @tracer.auto_trace
# def graph_operations():
#     # Initial state captured automatically
#     G.add_node(1)
#     tracer.capture(G, description="Added node 1")
#     G.add_nodes_from([2, 3])
#     tracer.capture(G, description="Added nodes 2-3")
#     G.add_edge(1, 2)
#     tracer.capture(G, description="Connected 1-2", highlight_edges=[(1,2)])
#     G.add_edge(2, 3)
#     tracer.capture(G, description="Connected 2-3", highlight_nodes=[2,3])

# graph_operations()

# # Visualization
# visualizer = GraphVisualizer(tracer)

# # Show specific step with highlights
# # visualizer.display_snapshot(step=2, layout='circular', show_code=True)

# # Create full animation
# anim = visualizer.create_animation(layout='kamada_kawai', show_code=True)
# anim.save("graph_evolution.gif", writer="pillow")