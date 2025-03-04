from typing import Tuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ds import DataStructureVisualizer

class QueueVisualizer(DataStructureVisualizer):
    """Visualizes queue operations (FIFO) with code tracking."""
    
    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (10, 5),
                         highlight_front_rear: bool = True, show_code: bool = True,
                         title: str = None):
        """
        Display a snapshot of the queue with code that produced it.
        
        Args:
            step: Snapshot step to display (-1 for latest)
            figsize: Figure size in inches (width, height)
            highlight_front_rear: Whether to highlight front and rear
            show_code: Whether to show code information
            title: Custom title for the plot
        """
        data, metadata = self.tracer.get_snapshot(step)
        if data is None:
            print("No data available")
            return
        
        # Create figure with code display if needed
        fig, main_ax, code_ax = self._create_figure_with_code(figsize, show_code)
        
        # Draw queue visualization on main axis
        queue = data  # List where index 0 is front
        N = len(queue)
        
        if N == 0:
            main_ax.text(0.5, 0.5, "Empty Queue", ha='center', va='center')
        else:
            element_width = 0.8 / max(1, N)
            for i in range(N):
                x = i * element_width
                rect = plt.Rectangle((x, 0.1), element_width, 0.8,
                                    facecolor='lightgreen', edgecolor='black')
                main_ax.add_patch(rect)
                main_ax.text(x + element_width / 2, 0.5, str(queue[i]),
                           ha='center', va='center')
                
            if highlight_front_rear and N > 0:
                # Highlight front
                rect = plt.Rectangle((0, 0.1), element_width, 0.8,
                                    facecolor='yellow', edgecolor='black', alpha=0.5)
                main_ax.add_patch(rect)
                main_ax.text(element_width / 2, 0.05, "Front", ha='center', va='top')
                # Highlight rear
                rect = plt.Rectangle(((N - 1) * element_width, 0.1), element_width, 0.8,
                                    facecolor='yellow', edgecolor='black', alpha=0.5)
                main_ax.add_patch(rect)
                main_ax.text((N - 1) * element_width + element_width / 2, 0.05, "Rear", ha='center', va='top')
        
        main_ax.set_xlim(0, max(1, N * element_width))
        main_ax.set_ylim(0, 1)
        main_ax.axis('off')
        
        # Set title
        if title:
            main_ax.set_title(title)
        elif metadata.get('description'):
            main_ax.set_title(f"Step {metadata['step']}: {metadata['description']}")
        else:
            main_ax.set_title(f"Step {metadata['step']}")
        
        # Display code information
        if show_code:
            self._display_code(code_ax, metadata)
        
        plt.tight_layout()
        plt.show()
    
    def create_animation(self, figsize: Tuple[int, int] = (10, 5),
                         interval: int = 1000, repeat: bool = False,
                         show_code: bool = True):
        """
        Animate queue operations over all snapshots with code tracking.
        
        Args:
            figsize: Figure size in inches
            interval: Time between frames in milliseconds
            repeat: Whether the animation loops
            show_code: Whether to show code information
            
        Returns:
            Matplotlib FuncAnimation object
        """
        if not self.tracer.snapshots:
            print("No snapshots available")
            return None
        
        # Create figure with code display if needed
        fig, main_ax, code_ax = self._create_figure_with_code(figsize, show_code)
        
        def update(frame):
            # Clear axes
            main_ax.clear()
            main_ax.axis('off')
            
            # Get data for this frame
            queue = self.tracer.snapshots[frame]
            metadata = self.tracer.metadata[frame]
            N = len(queue)
            
            # Draw queue
            if N == 0:
                main_ax.text(0.5, 0.5, "Empty Queue", ha='center', va='center')
            else:
                element_width = 0.8 / max(1, N)
                for i in range(N):
                    x = i * element_width
                    rect = plt.Rectangle((x, 0.1), element_width, 0.8,
                                         facecolor='lightgreen', edgecolor='black')
                    main_ax.add_patch(rect)
                    main_ax.text(x + element_width / 2, 0.5, str(queue[i]),
                                 ha='center', va='center')
                
                # Highlight front and rear
                rect = plt.Rectangle((0, 0.1), element_width, 0.8,
                                     facecolor='yellow', edgecolor='black', alpha=0.5)
                main_ax.add_patch(rect)
                main_ax.text(element_width / 2, 0.05, "Front", ha='center', va='top')
                
                rect = plt.Rectangle(((N - 1) * element_width, 0.1), element_width, 0.8,
                                     facecolor='yellow', edgecolor='black', alpha=0.5)
                main_ax.add_patch(rect)
                main_ax.text((N - 1) * element_width + element_width / 2, 0.05, "Rear", ha='center', va='top')
            
            main_ax.set_xlim(0, max(1, N * element_width))
            main_ax.set_ylim(0, 1)
            
            # Set title using metadata
            if metadata.get('description'):
                main_ax.set_title(f"Step {metadata['step']}: {metadata['description']}")
            else:
                main_ax.set_title(f"Step {metadata['step']}")
            
            # Display code information
            if show_code:
                self._display_code(code_ax, metadata)
        
        anim = FuncAnimation(fig, update, frames=len(self.tracer.snapshots),
                             interval=interval, repeat=repeat)
        
        plt.tight_layout()
        plt.close()  # Don't display the animation right away
        return anim