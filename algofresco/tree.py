import matplotlib.pyplot as plt
import networkx as nx
from typing import  Any, Tuple, Optional, Dict, List
from matplotlib.animation import FuncAnimation
from .ds import DataStructureVisualizer 
from .tracer import DataStructureTracer

class TreeVisualizer(DataStructureVisualizer):
    """Visualizes tree operations with code context tracking."""
    
    def __init__(self, tracer: DataStructureTracer):
        super().__init__(tracer)
        self.layout_cache: Dict[int, Dict[Any, Tuple[float, float]]] = {}

    def _tree_to_networkx(self, tree_node) -> Optional[nx.DiGraph]:
        """Convert tree structure to NetworkX graph with validation."""
        try:
            G = nx.DiGraph()
            if not tree_node:  # Handle empty trees
                return G

            # Handle different tree representations
            if hasattr(tree_node, 'left') and hasattr(tree_node, 'right'):
                self._add_binary_nodes(G, tree_node)
            elif hasattr(tree_node, 'children'):
                self._add_nary_nodes(G, tree_node)
            elif isinstance(tree_node, dict) and 'value' in tree_node:
                self._add_dict_nodes(G, tree_node)
            else:
                raise ValueError("Unsupported tree format")
                
            return G
        except Exception as e:
            print(f"Error converting tree: {e}")
            return None

    def _add_binary_nodes(self, G: nx.DiGraph, node, node_id: int = 0):
        """Recursively add binary tree nodes."""
        if node is None:
            return
            
        label = str(getattr(node, 'val', getattr(node, 'value', node)))
        G.add_node(node_id, label=label)
        
        if node.left:
            left_id = len(G.nodes)
            G.add_edge(node_id, left_id)
            self._add_binary_nodes(G, node.left, left_id)
            
        if node.right:
            right_id = len(G.nodes)
            G.add_edge(node_id, right_id)
            self._add_binary_nodes(G, node.right, right_id)

    def _add_nary_nodes(self, G: nx.DiGraph, node, node_id: int = 0):
        """Recursively add n-ary tree nodes."""
        if node is None:
            return
            
        label = str(getattr(node, 'val', getattr(node, 'value', node)))
        G.add_node(node_id, label=label)
        
        for child in getattr(node, 'children', []):
            if child:
                child_id = len(G.nodes)
                G.add_edge(node_id, child_id)
                self._add_nary_nodes(G, child, child_id)

    def _add_dict_nodes(self, G: nx.DiGraph, node: Dict, node_id: int = 0):
        """Recursively add dictionary-based tree nodes."""
        if not node:
            return
            
        label = str(node.get('value', ''))
        G.add_node(node_id, label=label)
        
        for child in node.get('children', []):
            if child:
                child_id = len(G.nodes)
                G.add_edge(node_id, child_id)
                self._add_dict_nodes(G, child, child_id)

    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (10, 6),
                        highlight_nodes: Optional[List[Any]] = None,
                        layout: str = 'dot', title: Optional[str] = None,
                        show_code: bool = True):
        """
        Display tree snapshot with code context.
        
        Args:
            step: Snapshot step (-1 for latest)
            figsize: Figure dimensions
            highlight_nodes: Node values to highlight
            layout: Layout algorithm ('dot', 'circular', etc.)
            title: Custom title
            show_code: Show associated code
        """
        data, metadata = self.tracer.get_snapshot(step)
        G = self._tree_to_networkx(data) if data else nx.DiGraph()

        fig, main_ax, code_ax = self._create_figure_with_code(figsize, show_code)
        
        if not G or len(G.nodes) == 0:
            main_ax.text(0.5, 0.5, "Empty Tree", ha='center', va='center', fontsize=14)
        else:
            # Calculate or retrieve layout
            pos = self._calculate_layout(G, layout, step)
            
            # Get node colors
            node_colors = self._get_node_colors(G, highlight_nodes, metadata)
            
            # Draw tree components
            nx.draw_networkx_nodes(G, pos, ax=main_ax, node_color=node_colors, node_size=1500)
            nx.draw_networkx_edges(G, pos, ax=main_ax, arrows=True, edge_color='#666666')
            labels = {n: G.nodes[n].get('label', '') for n in G.nodes}
            nx.draw_networkx_labels(G, pos, labels=labels, ax=main_ax, font_size=10)

        # Title handling
        title = title or metadata.get('description', f"Step {metadata.get('step', 'N/A')}")
        fig.suptitle(title, y=0.95 if show_code else 0.9, fontsize=14)
        
        # Code display
        if show_code and code_ax is not None:
            self._display_code(code_ax, metadata)

        main_ax.axis('off')
        plt.tight_layout()
        plt.show()

    def create_animation(self, figsize: Tuple[int, int] = (10, 6), 
                        interval: int = 1000, repeat: bool = False,
                        layout: str = 'dot', show_code: bool = True) -> Optional[FuncAnimation]:
        """
        Create tree operation animation with code context.
        
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

        # Precompute layouts and graphs
        graphs = [self._tree_to_networkx(data) for data in self.tracer.snapshots]
        layout_cache = [self._calculate_layout(G, layout, i) 
                       for i, G in enumerate(graphs)]

        def update(frame: int):
            main_ax.clear()
            if code_ax is not None:
                code_ax.clear()
                code_ax.axis('off')

            G = graphs[frame]
            metadata = self.tracer.metadata[frame]
            pos = layout_cache[frame]

            if not G or len(G.nodes) == 0:
                main_ax.text(0.5, 0.5, "Empty Tree", ha='center', va='center')
            else:
                # Get styling from metadata
                h_nodes = metadata.get('highlight_nodes', [])
                node_colors = self._get_node_colors(G, h_nodes, metadata)
                
                # Draw components
                nx.draw_networkx_nodes(G, pos, ax=main_ax, node_color=node_colors, node_size=1500)
                nx.draw_networkx_edges(G, pos, ax=main_ax, arrows=True, edge_color='#666666')
                labels = {n: G.nodes[n].get('label', '') for n in G.nodes}
                nx.draw_networkx_labels(G, pos, labels=labels, ax=main_ax, font_size=10)

            # Set title and code
            main_ax.set_title(f"Step {metadata['step']}: {metadata.get('description', '')}")
            if show_code and code_ax is not None:
                self._display_code(code_ax, metadata)

            main_ax.axis('off')

        anim = FuncAnimation(fig, update, frames=len(self.tracer.snapshots),
                            interval=interval, repeat=repeat)
        plt.close()
        return anim

    def _calculate_layout(self, G: nx.DiGraph, layout: str, step: int) -> Dict[Any, Tuple[float, float]]:
        """Calculate tree layout with validation and caching."""
        if not G or len(G.nodes) == 0:
            return {}

        if step in self.layout_cache:
            return self.layout_cache[step]

        try:
            if layout == 'dot':
                pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
            elif layout == 'circular':
                pos = nx.circular_layout(G)
            else:
                pos = nx.spring_layout(G)
        except Exception as e:
            print(f"Layout {layout} failed, using spring layout: {e}")
            pos = nx.spring_layout(G)

        self.layout_cache[step] = pos
        return pos

    def _get_node_colors(self, G: nx.DiGraph, 
                        highlights: Optional[List[Any]],
                        metadata: Dict) -> List[str]:
        """Generate node colors based on highlights."""
        label_map = {n: G.nodes[n].get('label', '') for n in G.nodes}
        h_labels = set(str(h) for h in (highlights or [])) | set(metadata.get('highlight_nodes', []))
        return ['#ff7f7f' if label_map[n] in h_labels else '#aed9e6' for n in G.nodes]