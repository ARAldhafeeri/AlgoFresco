import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Any, Tuple, Optional, Dict
from matplotlib.animation import FuncAnimation
from .ds import DataStructureVisualizer
from .tracer import DataStructureTracer
class GraphVisualizer(DataStructureVisualizer):
    """Visualizes graph operations with code context tracking."""
    
    def __init__(self, tracer: DataStructureTracer):
        super().__init__(tracer)
        self.layout_cache: Dict[int, Dict[Any, Tuple[float, float]]] = {}

    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (10, 8),
                        highlight_nodes: Optional[List[Any]] = None,
                        highlight_edges: Optional[List[Tuple]] = None,
                        layout: str = 'spring', title: Optional[str] = None,
                        show_code: bool = True):
        """
        Display graph snapshot with code context.
        
        Args:
            step: Snapshot step (-1 for latest)
            figsize: Figure dimensions
            highlight_nodes: Nodes to highlight
            highlight_edges: Edges to highlight
            layout: Layout algorithm (spring, circular, kamada_kawai, shell)
            title: Custom title
            show_code: Show associated code
        """
        data, metadata = self.tracer.get_snapshot(step)
        if data is None or not isinstance(data, nx.Graph):
            print("No valid graph data available")
            return

        fig, main_ax, code_ax = self._create_figure_with_code(figsize, show_code)
        G = data
        
        if not G.nodes:
            main_ax.text(0.5, 0.5, "Empty Graph", ha='center', va='center', fontsize=14)
        else:
            # Get or calculate layout
            pos = self._calculate_layout(G, layout, step)
            
            # Style parameters
            node_colors = self._get_node_colors(G, highlight_nodes, metadata)
            edge_colors = self._get_edge_colors(G, highlight_edges, metadata)
            
            # Draw graph components
            nx.draw_networkx_nodes(G, pos, ax=main_ax, node_color=node_colors, node_size=800)
            nx.draw_networkx_edges(G, pos, ax=main_ax, edge_color=edge_colors, width=2)
            nx.draw_networkx_labels(G, pos, ax=main_ax, font_size=10)

        # Title handling
        title = title or metadata.get('description', f"Step {metadata.get('step', 'N/A')}")
        fig.suptitle(title, y=0.95 if show_code else 0.9, fontsize=14)
        
        # Code display
        if show_code and code_ax is not None:
            self._display_code(code_ax, metadata)

        main_ax.axis('off')
        plt.tight_layout()
        plt.show()

    def create_animation(self, figsize: Tuple[int, int] = (10, 8),
                        interval: int = 1000, repeat: bool = False,
                        layout: str = 'spring', show_code: bool = True) -> Optional[FuncAnimation]:
        """
        Create graph operation animation with code context.
        
        Args:
            figsize: Figure dimensions
            interval: Frame delay (ms)
            repeat: Loop animation
            layout: Layout algorithm
            show_code: Show code context
            
        Returns:
            Matplotlib animation object
        """
        if not self.tracer.snapshots:
            print("No snapshots available")
            return None

        fig, main_ax, code_ax = self._create_figure_with_code(figsize, show_code)
        plt.tight_layout()

        # Precompute layouts for consistency
        layout_cache = []
        for i, snapshot in enumerate(self.tracer.snapshots):
            if isinstance(snapshot, nx.Graph):
                layout_cache.append(self._calculate_layout(snapshot, layout, i))
            else:
                layout_cache.append({})

        def update(frame: int):
            main_ax.clear()
            if code_ax is not None:
                code_ax.clear()
                code_ax.axis('off')

            data = self.tracer.snapshots[frame]
            metadata = self.tracer.metadata[frame]
            
            if not isinstance(data, nx.Graph) or not data.nodes:
                main_ax.text(0.5, 0.5, "Empty Graph", ha='center', va='center')
                return

            G = data
            pos = layout_cache[frame]
            
            # Get styling from metadata
            h_nodes = metadata.get('highlight_nodes', [])
            h_edges = metadata.get('highlight_edges', [])
            
            node_colors = self._get_node_colors(G, h_nodes, metadata)
            edge_colors = self._get_edge_colors(G, h_edges, metadata)
            
            # Draw components
            nx.draw_networkx_nodes(G, pos, ax=main_ax, node_color=node_colors, node_size=800)
            nx.draw_networkx_edges(G, pos, ax=main_ax, edge_color=edge_colors, width=2)
            nx.draw_networkx_labels(G, pos, ax=main_ax, font_size=10)
            
            # Set title and code
            main_ax.set_title(f"Step {metadata['step']}: {metadata.get('description', '')}", pad=20)
            if show_code and code_ax is not None:
                self._display_code(code_ax, metadata)

            main_ax.axis('off')

        anim = FuncAnimation(fig, update, frames=len(self.tracer.snapshots),
                            interval=interval, repeat=repeat)
        plt.show()
        return anim

    def _calculate_layout(self, G: Optional[nx.Graph], layout: str, step: int) -> Dict[Any, Tuple[float, float]]:
        """Calculate or retrieve cached graph layout with validation."""
        # Validate input graph
        if not isinstance(G, nx.Graph) or len(G.nodes) == 0:
            return {}

        # Return cached layout if available
        if step in self.layout_cache:
            return self.layout_cache[step]

        # Handle different graph sizes appropriately
        layout_funcs = {
            'spring': nx.spring_layout,
            'circular': nx.circular_layout,
            'kamada_kawai': self._safe_kamada_kawai,
            'shell': nx.shell_layout
        }

        # Get layout function with fallback
        layout_func = layout_funcs.get(layout, nx.spring_layout)
        pos = layout_func(G)
        self.layout_cache[step] = pos
        return pos

    def _safe_kamada_kawai(self, G: nx.Graph) -> Dict[Any, Tuple[float, float]]:
        """Safe wrapper for kamada-kawai layout that handles small graphs."""
        try:
            return nx.kamada_kawai_layout(G)
        except:
            # Fallback to spring layout if KK fails
            return nx.spring_layout(G)

    def _get_node_colors(self, G: nx.Graph, 
                        highlights: Optional[List[Any]],
                        metadata: Dict) -> List[str]:
        """Generate node color list based on highlights and metadata."""
        h_nodes = set(highlights or []).union(set(metadata.get('highlight_nodes', [])))
        return ['#ff7f7f' if node in h_nodes else '#aed9e6' for node in G.nodes]

    def _get_edge_colors(self, G: nx.Graph, 
                        highlights: Optional[List[Tuple]], 
                        metadata: Dict) -> List[str]:
        """Generate edge color list based on highlights and metadata."""
        h_edges = set(highlights or []).union(set(metadata.get('highlight_edges', [])))
        bidirectional = set((v, u) for (u, v) in h_edges)
        return ['red' if edge in h_edges or edge in bidirectional 
               else '#666666' for edge in G.edges]