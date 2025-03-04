from typing import List, Any, Tuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ds import DataStructureVisualizer
from tracer import DataStructureTracer

class ListVisualizer(DataStructureVisualizer):
    """Visualizes operations on lists and arrays."""
    
    def __init__(self, tracer: DataStructureTracer):
        """Initialize the list visualizer."""
        super().__init__(tracer)
    
    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (10, 3),
                         highlight_indices: List[int] = None, 
                         highlight_values: List[Any] = None,
                         highlight_range: List[Tuple[int, int]] = None,
                         title: str = None,
                         show_indices: bool = True):
        """
        Display a specific snapshot of a list.
        
        Args:
            step: The step to display (-1 for latest)
            figsize: Figure size
            highlight_indices: List of indices to highlight
            highlight_values: List of values to highlight
            highlight_range: List of (start, end) ranges to highlight
            title: Title for the visualization
            show_indices: Whether to show indices
        """
        data, metadata = self.tracer.get_snapshot(step)
        if data is None:
            print("No data available")
            return
            
        # Create figure
        plt.figure(figsize=figsize)
        
        # Calculate cell dimensions
        list_len = len(data)
        cell_width = 1.0 / max(list_len, 1)
        
        # Draw cells and values
        for i, val in enumerate(data):
            # Base cell properties
            cell_color = '#f0f0f0'  # Default color
            text_color = 'black'
            
            # Highlight indices if requested
            if highlight_indices and i in highlight_indices:
                cell_color = '#ffcf75'  # Yellow-orange
                
            # Highlight values if requested
            if highlight_values and val in highlight_values:
                cell_color = '#8dc7f3'  # Light blue
            
            # Draw cell rectangle
            rect = plt.Rectangle((i * cell_width, 0), cell_width, 0.5, 
                                 facecolor=cell_color, edgecolor='black')
            plt.gca().add_patch(rect)
            
            # Add value text
            plt.text((i + 0.5) * cell_width, 0.25, str(val), 
                    ha='center', va='center', color=text_color)
            
            # Add index below if requested
            if show_indices:
                plt.text((i + 0.5) * cell_width, -0.1, str(i), 
                        ha='center', va='center', color='darkblue', fontsize=8)
        
        # Highlight ranges if requested
        if highlight_range:
            for start, end in highlight_range:
                if 0 <= start < list_len and 0 <= end < list_len:
                    # Draw a rectangle around the range
                    rect = plt.Rectangle((start * cell_width, 0), 
                                        (end - start + 1) * cell_width, 0.5, 
                                        fill=False, edgecolor='red', linewidth=2)
                    plt.gca().add_patch(rect)
        
        # Set title
        if title:
            plt.title(title)
        elif metadata.get('description'):
            plt.title(f"Step {metadata['step']}: {metadata['description']}")
        else:
            plt.title(f"Step {metadata['step']}")
        
        plt.xlim(0, 1)
        plt.ylim(-0.2, 0.7)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def create_animation(self, figsize: Tuple[int, int] = (10, 3), 
                        interval: int = 1000, repeat: bool = False,
                        show_indices: bool = True):
        """
        Create an animation of list operations.
        
        Args:
            figsize: Figure size
            interval: Time between frames in milliseconds
            repeat: Whether to loop the animation
            show_indices: Whether to show indices
            
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
            
            # Calculate cell dimensions
            list_len = len(data)
            cell_width = 1.0 / max(list_len, 1)
            
            # Draw cells and values
            for i, val in enumerate(data):
                # Draw cell rectangle
                rect = plt.Rectangle((i * cell_width, 0), cell_width, 0.5, 
                                    facecolor='#f0f0f0', edgecolor='black')
                ax.add_patch(rect)
                
                # Add value text
                ax.text((i + 0.5) * cell_width, 0.25, str(val), 
                       ha='center', va='center')
                
                # Add index below if requested
                if show_indices:
                    ax.text((i + 0.5) * cell_width, -0.1, str(i), 
                           ha='center', va='center', color='darkblue', fontsize=8)
            
            # Set title based on metadata
            if metadata.get('description'):
                ax.set_title(f"Step {metadata['step']}: {metadata['description']}")
            else:
                ax.set_title(f"Step {metadata['step']}")
            
            ax.set_xlim(0, 1)
            ax.set_ylim(-0.2, 0.7)
            ax.axis('off')
        
        anim = FuncAnimation(fig, update, frames=len(self.tracer.snapshots),
                            interval=interval, repeat=repeat)
        
        plt.close()  # Prevent duplicate display
        return anim
        
    def interactive_player(self):
        """Create an interactive player for stepping through algorithm steps."""
        from ipywidgets import interact, IntSlider
        
        if not self.tracer.snapshots:
            print("No snapshots available")
            return
            
        max_step = len(self.tracer.snapshots) - 1
        
        @interact(step=IntSlider(min=0, max=max_step, step=1, value=0,
                                description="Step:"))
        def show_step(step):
            self.display_snapshot(step)
            
            # Display step information
            metadata = self.tracer.metadata[step]
            if metadata.get('description'):
                print(f"Step {step}: {metadata['description']}")
