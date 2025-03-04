from typing import List, Any, Tuple
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
from ds import DataStructureVisualizer
from tracer import DataStructureTracer

class GraphVisualizer(DataStructureVisualizer):
    def __init__(self, tracer: DataStructureTracer):
        """Initialize the graph visualizer."""
        self.tracer = tracer
    
    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (10, 8),
                         highlight_nodes: List[Any] = None,
                         highlight_edges: List[Tuple] = None,
                         layout: str = 'spring',
                         title: str = None, show_code : bool = True):
        """
        Display a specific snapshot of a graph.
        """
        data, metadata = self.tracer.get_snapshot(step)
        if data is None:
            print("No data available")
            return
        
        _, _, code_ax = self._create_figure_with_code(figsize, show_code)
        
        plt.figure(figsize=figsize)
        
        if isinstance(data, nx.Graph):
            G = data
        else:
            print("Unsupported graph type")
            return
            
        if not G.nodes:
            plt.text(0.5, 0.5, "Empty Graph", ha='center', va='center')
            plt.axis('off')
            plt.tight_layout()
            plt.show()
            return
            
        # Select layout algorithm
        if layout == 'spring':
            pos = nx.spring_layout(G)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        elif layout == 'shell':
            pos = nx.shell_layout(G)
        else:
            pos = nx.spring_layout(G)
        
        # Set up node colors
        node_colors = []
        for node in G.nodes:
            if highlight_nodes and node in highlight_nodes:
                node_colors.append('#ff7f7f')  # Highlight color
            else:
                node_colors.append('#aed9e6')  # Default color
        
        # Set up edge colors
        edge_colors = []
        if highlight_edges:
            highlight_edges_set = set((u, v) for u, v in highlight_edges) | set((v, u) for u, v in highlight_edges)
            for edge in G.edges:
                if edge in highlight_edges_set:
                    edge_colors.append('red')
                else:
                    edge_colors.append('#666666')
        else:
            edge_colors = ['#666666'] * len(G.edges)
        
        # Draw the graph
        nx.draw(G, pos, 
                node_color=node_colors, 
                edge_color=edge_colors,
                node_size=1500, 
                with_labels=True, 
                font_size=10)
        
        # Set title
        if title:
            plt.title(title)
        elif metadata.get('description'):
            plt.title(f"Step {metadata['step']}: {metadata['description']}")
        else:
            plt.title(f"Step {metadata['step']}")
        
        if show_code:
            self._display_code(code_ax, metadata)

        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def create_animation(self, figsize: Tuple[int, int] = (10, 8), 
                        interval: int = 1000, repeat: bool = False,
                        layout: str = 'spring'):
        """
        Create an animation of graph operations with highlighted nodes from metadata.
        """
        if not self.tracer.snapshots:
            print("No snapshots available")
            return None
            
        fig, ax = plt.subplots(figsize=figsize)
        
        # Precompute layouts for consistency across frames
        pos_frames = []
        for data in self.tracer.snapshots:
            if isinstance(data, nx.Graph):
                G = data
                if layout == 'spring':
                    pos = nx.spring_layout(G)
                elif layout == 'circular':
                    pos = nx.circular_layout(G)
                elif layout == 'kamada_kawai':
                    pos = nx.kamada_kawai_layout(G)
                elif layout == 'shell':
                    pos = nx.shell_layout(G)
                else:
                    pos = nx.spring_layout(G)
                pos_frames.append(pos)
            else:
                pos_frames.append(None)
        
        def update(frame):
            ax.clear()
            data = self.tracer.snapshots[frame]
            metadata = self.tracer.metadata[frame]
            pos = pos_frames[frame]
            
            if not isinstance(data, nx.Graph) or pos is None:
                ax.text(0.5, 0.5, "Unsupported Graph Type", ha='center', va='center')
                ax.axis('off')
                return
                
            G = data
            
            if not G.nodes:
                ax.text(0.5, 0.5, "Empty Graph", ha='center', va='center')
                ax.axis('off')
                return
                
            # Get nodes to highlight from metadata
            highlight_nodes = metadata.get('highlight_nodes', [])
            
            # Set node colors based on visited status
            node_colors = []
            for node in G.nodes:
                if node in highlight_nodes:
                    node_colors.append('#ff7f7f')  # Highlight visited nodes
                else:
                    node_colors.append('#aed9e6')  # Default color
            
            # Draw the graph
            nx.draw(G, pos, ax=ax,
                    node_color=node_colors,
                    node_size=1500,
                    with_labels=True,
                    font_size=10,
                    edge_color='#666666')
            
            # Set title using metadata
            if metadata.get('description'):
                ax.set_title(f"Step {metadata['step']}: {metadata['description']}")
            else:
                ax.set_title(f"Step {metadata['step']}")
            
            ax.axis('off')
        
        anim = FuncAnimation(fig, update, frames=len(self.tracer.snapshots),
                            interval=interval, repeat=repeat)
        
        plt.close()  # Avoid displaying a static plot
        return anim