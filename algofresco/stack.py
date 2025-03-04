
from typing import Tuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ds import DataStructureVisualizer

class StackVisualizer(DataStructureVisualizer):
    """Visualizes stack operations (LIFO)."""
    
    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (6, 8),
                         highlight_top: bool = True, title: str = None):
        """
        Display a snapshot of the stack.
        
        Args:
            step: Snapshot step to display (-1 for latest)
            figsize: Figure size in inches (width, height)
            highlight_top: Whether to highlight the top element
            title: Custom title for the plot
        """
        data, metadata = self.tracer.get_snapshot(step)
        if data is None:
            print("No data available")
            return
            
        stack = data  # List where the last element is the top
        N = len(stack)
        
        plt.figure(figsize=figsize)
        ax = plt.gca()
        
        if N == 0:
            ax.text(0.5, 0.5, "Empty Stack", ha='center', va='center')
        else:
            element_height = 0.8 / N
            for i in range(N):
                y = i * element_height
                rect = plt.Rectangle((0.1, y), 0.8, element_height, 
                                     facecolor='lightblue', edgecolor='black')
                ax.add_patch(rect)
                ax.text(0.5, y + element_height / 2, str(stack[i]), 
                        ha='center', va='center')
                
            if highlight_top and N > 0:
                top_y = (N - 1) * element_height
                rect = plt.Rectangle((0.1, top_y), 0.8, element_height, 
                                     facecolor='yellow', edgecolor='black', alpha=0.5)
                ax.add_patch(rect)
                ax.text(0.05, top_y + element_height / 2, "Top", ha='right', va='center')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, max(1, N * element_height))
        ax.axis('off')
        
        if title:
            ax.set_title(title)
        elif metadata.get('description'):
            ax.set_title(f"Step {metadata['step']}: {metadata['description']}")
        else:
            ax.set_title(f"Step {metadata['step']}")
        
        plt.show()
    
    def create_animation(self, figsize: Tuple[int, int] = (6, 8), 
                         interval: int = 1000, repeat: bool = False):
        """
        Animate stack operations over all snapshots.
        
        Args:
            figsize: Figure size in inches
            interval: Time between frames in milliseconds
            repeat: Whether the animation loops
            
        Returns:
            Matplotlib FuncAnimation object
        """
        if not self.tracer.snapshots:
            print("No snapshots available")
            return None
            
        fig, ax = plt.subplots(figsize=figsize)
        
        def update(frame):
            ax.clear()
            stack = self.tracer.snapshots[frame]
            metadata = self.tracer.metadata[frame]
            N = len(stack)
            element_height = 0.8 / N if N > 0 else 0
            for i in range(N):
                y = i * element_height
                rect = plt.Rectangle((0.1, y), 0.8, element_height, 
                                     facecolor='lightblue', edgecolor='black')
                ax.add_patch(rect)
                ax.text(0.5, y + element_height / 2, str(stack[i]), 
                        ha='center', va='center')
            if N > 0:
                top_y = (N - 1) * element_height
                rect = plt.Rectangle((0.1, top_y), 0.8, element_height, 
                                     facecolor='yellow', edgecolor='black', alpha=0.5)
                ax.add_patch(rect)
                ax.text(0.05, top_y + element_height / 2, "Top", ha='right', va='center')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, max(1, N * element_height))
            ax.axis('off')
            ax.set_title(f"Step {metadata['step']}: {metadata.get('description', '')}")
        
        anim = FuncAnimation(fig, update, frames=len(self.tracer.snapshots),
                             interval=interval, repeat=repeat)
        plt.close()  # Prevents duplicate display
        return anim