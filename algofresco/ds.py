import matplotlib.pyplot as plt
from typing import Tuple, Any, Dict

class DataStructureVisualizer:
    """Base class for visualizing algorithm execution on data structures."""
    
    def __init__(self, tracer):
        """
        Initialize the visualizer.
        
        Args:
            tracer: DataStructureTracer instance with captured snapshots
        """
        self.tracer = tracer
        
    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (10, 6),
                        show_code: bool = True, title: str = None):
        """
        Display a specific snapshot with its metadata.
        
        Args:
            step: Step number to display (-1 for latest)
            figsize: Figure size (width, height) in inches
            show_code: Whether to show the code that produced this step
            title: Custom title for the plot
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def create_animation(self, figsize: Tuple[int, int] = (10, 6),
                         interval: int = 1000, repeat: bool = False,
                         show_code: bool = True):
        """
        Create an animation of the algorithm execution.
        
        Args:
            figsize: Figure size (width, height) in inches
            interval: Time between frames in milliseconds
            repeat: Whether to loop the animation
            show_code: Whether to show the code that produced each step
            
        Returns:
            Matplotlib animation
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def _create_figure_with_code(self, figsize: Tuple[int, int] = (10, 6), 
                               show_code: bool = True) -> Tuple:
        """
        Create a figure with a subplot layout that can display both visualization and code.
        
        Args:
            figsize: Figure size (width, height) in inches
            show_code: Whether to show code
            
        Returns:
            Tuple of (figure, main_ax, code_ax) where code_ax might be None
        """
        fig = plt.figure(figsize=figsize)
        
        if show_code:
            # Create a grid for visualization and code
            gs = fig.add_gridspec(5, 1)
            main_ax = fig.add_subplot(gs[:4, 0])  # Top 80% for visualization
            code_ax = fig.add_subplot(gs[4, 0])   # Bottom 20% for code
            code_ax.axis('off')
        else:
            # Just use the whole figure for visualization
            main_ax = fig.add_subplot(111)
            code_ax = None
            
        return fig, main_ax, code_ax
    
    def _display_code(self, ax, metadata: Dict[str, Any]):
        """
        Display code information on the given axis.
        
        Args:
            ax: Matplotlib axis
            metadata: Snapshot metadata containing code information
        """
        if ax is None:
            return
            
        # Clear the axis
        ax.clear()
        ax.axis('off')
        
        # Get code information from metadata
        code_line = metadata.get('code_line', 'No code information available')
        function = metadata.get('function', '')
        line_num = metadata.get('line_num', '')
        description = metadata.get('description', '')
        info_line = f"Line: {line_num}  - Description: {description}"
        # Create text to display
        ax.text(0.01, 0.3, info_line, fontsize=12, fontweight='bold', color='black')