import matplotlib.pyplot as plt
import networkx as nx
from typing import  List, Any, Tuple
from matplotlib.animation import FuncAnimation
from ds import DataStructureVisualizer
from tracer import DataStructureTracer

class TreeVisualizer(DataStructureVisualizer):
    """Visualizes operations on trees."""
    
    def __init__(self, tracer: DataStructureTracer):
        """Initialize the tree visualizer."""
        super().__init__(tracer)
    
    def _tree_to_networkx(self, tree_node):
        """
        Convert a tree node to a NetworkX graph.
        
        Args:
            tree_node: The root node of a tree
            
        Returns:
            NetworkX DiGraph
        """
        G = nx.DiGraph()
        
        # Handle different tree node representations
        if hasattr(tree_node, 'left') and hasattr(tree_node, 'right'):
            # Binary tree node with left and right children
            def add_nodes(node, node_id=0):
                if node is None:
                    return
                
                # Add the current node
                label = str(getattr(node, 'val', getattr(node, 'value', node)))
                G.add_node(node_id, label=label)
                
                # Process left child
                if node.left:
                    left_id = len(G.nodes)
                    G.add_edge(node_id, left_id)
                    add_nodes(node.left, left_id)
                
                # Process right child
                if node.right:
                    right_id = len(G.nodes)
                    G.add_edge(node_id, right_id)
                    add_nodes(node.right, right_id)
            
            add_nodes(tree_node)
            
        elif hasattr(tree_node, 'children'):
            # Node with a list of children
            def add_nodes(node, node_id=0):
                if node is None:
                    return
                
                # Add the current node
                label = str(getattr(node, 'val', getattr(node, 'value', node)))
                G.add_node(node_id, label=label)
                
                # Process all children
                if node.children:
                    for child in node.children:
                        if child:
                            child_id = len(G.nodes)
                            G.add_edge(node_id, child_id)
                            add_nodes(child, child_id)
            
            add_nodes(tree_node)
            
        elif isinstance(tree_node, dict) and 'value' in tree_node:
            # Dictionary representation
            def add_nodes(node, node_id=0):
                if node is None:
                    return
                
                # Add the current node
                G.add_node(node_id, label=str(node.get('value', '')))
                
                # Process all children
                children = node.get('children', [])
                for child in children:
                    if child:
                        child_id = len(G.nodes)
                        G.add_edge(node_id, child_id)
                        add_nodes(child, child_id)
            
            add_nodes(tree_node)
            
        return G
    
    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (10, 6),
                         highlight_nodes: List[Any] = None,
                         layout: str = 'dot',
                         title: str = None):
        """
        Display a specific snapshot of a tree.
        
        Args:
            step: The step to display (-1 for latest)
            figsize: Figure size
            highlight_nodes: List of node values to highlight
            layout: Layout algorithm to use ('dot', 'circular', etc.)
            title: Title for the visualization
        """
        data, metadata = self.tracer.get_snapshot(step)
        if data is None:
            print("No data available")
            return
            
        plt.figure(figsize=figsize)
        
        # Convert tree to NetworkX graph
        G = self._tree_to_networkx(data)
        
        if not G.nodes:
            plt.text(0.5, 0.5, "Empty Tree", ha='center', va='center')
            plt.axis('off')
            plt.tight_layout()
            plt.show()
            return
            
        # Set up node colors
        node_colors = []
        for node in G.nodes:
            node_data = G.nodes[node]
            label = node_data.get('label', '')
            if highlight_nodes and label in [str(h) for h in highlight_nodes]:
                node_colors.append('#ff7f7f')  # Highlight color
            else:
                node_colors.append('#aed9e6')  # Default color
        
        # Create layout
        if layout == 'dot':
            try:
                # Try using pygraphviz for better tree layout
                pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
            except:
                # Fall back to builtin layout
                pos = nx.spring_layout(G)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        else:
            pos = nx.spring_layout(G)
        
        # Draw the graph
        nx.draw(G, pos, 
                node_color=node_colors, 
                node_size=2500, 
                arrows=True,
                with_labels=False, 
                edge_color='#666666')
        
        # Add node labels
        node_labels = {node: G.nodes[node].get('label', '') for node in G.nodes}
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)
        
        # Set title
        if title:
            plt.title(title)
        elif metadata.get('description'):
            plt.title(f"Step {metadata['step']}: {metadata['description']}")
        else:
            plt.title(f"Step {metadata['step']}")
        
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def create_animation(self, figsize: Tuple[int, int] = (10, 6), 
                        interval: int = 1000, repeat: bool = False,
                        layout: str = 'dot'):
        """
        Create an animation of tree operations.
        
        Args:
            figsize: Figure size
            interval: Time between frames in milliseconds
            repeat: Whether to loop the animation
            layout: Layout algorithm to use
            
        Returns:
            Matplotlib animation
        """
        if not self.tracer.snapshots:
            print("No snapshots available")
            return None
            
        fig, ax = plt.subplots(figsize=figsize)
        
        def update(frame):
            ax.clear()
            data = self.tracer.snapshots[frame]
            metadata = self.tracer.metadata[frame]
            
            # Convert tree to NetworkX graph
            G = self._tree_to_networkx(data)
            
            if not G.nodes:
                ax.text(0.5, 0.5, "Empty Tree", ha='center', va='center')
                ax.axis('off')
                return
                
            # Create layout
            if layout == 'dot':
                try:
                    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
                except:
                    pos = nx.spring_layout(G)
            elif layout == 'circular':
                pos = nx.circular_layout(G)
            else:
                pos = nx.spring_layout(G)
            
            # Draw the graph
            nx.draw(G, pos, ax=ax,
                    node_color='#aed9e6', 
                    node_size=2500, 
                    arrows=True,
                    with_labels=False, 
                    edge_color='#666666')
            
            # Add node labels
            node_labels = {node: G.nodes[node].get('label', '') for node in G.nodes}
            nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, ax=ax)
            
            # Set title based on metadata
            if metadata.get('description'):
                ax.set_title(f"Step {metadata['step']}: {metadata['description']}")
            else:
                ax.set_title(f"Step {metadata['step']}")
            
            ax.axis('off')
        
        anim = FuncAnimation(fig, update, frames=len(self.tracer.snapshots),
                            interval=interval, repeat=repeat)
        
        plt.close()  # Prevent duplicate display
        return anim