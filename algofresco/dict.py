import numpy as np
from typing import List, Any, Tuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ds import DataStructureVisualizer
from tracer import DataStructureTracer

class DictionaryVisualizer(DataStructureVisualizer):
    """Visualizes operations on dictionaries."""
    
    def __init__(self, tracer: DataStructureTracer):
        """Initialize the dictionary visualizer."""
        super().__init__(tracer)
    
    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (10, 6),
                         highlight_keys: List[Any] = None,
                         highlight_values: List[Any] = None,
                         title: str = None):
        """
        Display a specific snapshot of a dictionary.
        
        Args:
            step: The step to display (-1 for latest)
            figsize: Figure size
            highlight_keys: List of keys to highlight
            highlight_values: List of values to highlight
            title: Title for the visualization
        """
        data, metadata = self.tracer.get_snapshot(step)
        if data is None:
            print("No data available")
            return
            
        plt.figure(figsize=figsize)
        
        # Convert dictionary to list of (key, value) pairs for visualization
        items = list(data.items())
        n_items = len(items)
        
        if n_items == 0:
            plt.text(0.5, 0.5, "Empty Dictionary", ha='center', va='center')
        else:
            # Determine grid dimensions
            grid_size = int(np.ceil(np.sqrt(n_items)))
            grid_width = 1.0 / grid_size
            grid_height = 1.0 / grid_size
            
            # Draw each key-value pair
            for i, (key, value) in enumerate(items):
                # Calculate position
                row = i // grid_size
                col = i % grid_size
                x = col * grid_width
                y = 1.0 - (row + 1) * grid_height
                
                # Set colors based on highlights
                key_color = '#ffcf75' if highlight_keys and key in highlight_keys else '#f0f0f0'
                value_color = '#8dc7f3' if highlight_values and value in highlight_values else '#f0f0f0'
                
                # Draw key rectangle
                key_rect = plt.Rectangle((x, y + grid_height/2), grid_width, grid_height/2, 
                                        facecolor=key_color, edgecolor='black')
                plt.gca().add_patch(key_rect)
                
                # Draw value rectangle
                value_rect = plt.Rectangle((x, y), grid_width, grid_height/2, 
                                          facecolor=value_color, edgecolor='black')
                plt.gca().add_patch(value_rect)
                
                # Add text
                plt.text(x + grid_width/2, y + 3*grid_height/4, str(key), 
                        ha='center', va='center', fontsize=9)
                plt.text(x + grid_width/2, y + grid_height/4, str(value), 
                        ha='center', va='center', fontsize=9)
        
        # Set title
        if title:
            plt.title(title)
        elif metadata.get('description'):
            plt.title(f"Step {metadata['step']}: {metadata['description']}")
        else:
            plt.title(f"Step {metadata['step']}")
        
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def create_animation(self, figsize: Tuple[int, int] = (10, 6), 
                        interval: int = 1000, repeat: bool = False):
        """
        Create an animation of dictionary operations.
        
        Args:
            figsize: Figure size
            interval: Time between frames in milliseconds
            repeat: Whether to loop the animation
            
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
            
            # Convert dictionary to list of (key, value) pairs
            items = list(data.items())
            n_items = len(items)
            
            if n_items == 0:
                ax.text(0.5, 0.5, "Empty Dictionary", ha='center', va='center')
            else:
                # Determine grid dimensions
                grid_size = int(np.ceil(np.sqrt(n_items)))
                grid_width = 1.0 / grid_size
                grid_height = 1.0 / grid_size
                
                # Draw each key-value pair
                for i, (key, value) in enumerate(items):
                    # Calculate position
                    row = i // grid_size
                    col = i % grid_size
                    x = col * grid_width
                    y = 1.0 - (row + 1) * grid_height
                    
                    # Draw key rectangle
                    key_rect = plt.Rectangle((x, y + grid_height/2), grid_width, grid_height/2, 
                                            facecolor='#f0f0f0', edgecolor='black')
                    ax.add_patch(key_rect)
                    
                    # Draw value rectangle
                    value_rect = plt.Rectangle((x, y), grid_width, grid_height/2, 
                                              facecolor='#f0f0f0', edgecolor='black')
                    ax.add_patch(value_rect)
                    
                    # Add text
                    ax.text(x + grid_width/2, y + 3*grid_height/4, str(key), 
                           ha='center', va='center', fontsize=9)
                    ax.text(x + grid_width/2, y + grid_height/4, str(value), 
                           ha='center', va='center', fontsize=9)
            
            # Set title based on metadata
            if metadata.get('description'):
                ax.set_title(f"Step {metadata['step']}: {metadata['description']}")
            else:
                ax.set_title(f"Step {metadata['step']}")
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        anim = FuncAnimation(fig, update, frames=len(self.tracer.snapshots),
                            interval=interval, repeat=repeat)
        
        plt.close() 
        return anim