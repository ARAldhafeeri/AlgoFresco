from typing import Tuple, Optional
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .ds import DataStructureVisualizer

class QueueVisualizer(DataStructureVisualizer):
    """Visualizes queue operations (FIFO) with integrated code tracking."""
    
    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (10, 5),
                        highlight_front_rear: bool = True, title: Optional[str] = None,
                        show_code: bool = True):
        """
        Display a queue snapshot with code context.
        
        Args:
            step: Snapshot step (-1 for latest)
            figsize: Figure dimensions
            highlight_front_rear: Highlight first/last elements
            title: Custom title
            show_code: Show associated code
        """
        data, metadata = self.tracer.get_snapshot(step)
        if data is None:
            print("No data available")
            return

        fig, main_ax, code_ax = self._create_figure_with_code(figsize, show_code)
        queue = data
        N = len(queue)
        element_width = 0.8 / max(1, N) if N > 0 else 0.8

        # Visualization
        if N == 0:
            main_ax.text(0.5, 0.5, "Empty Queue", ha='center', va='center', fontsize=14)
        else:
            for i in range(N):
                x = i * element_width
                rect = plt.Rectangle((x, 0.1), element_width, 0.8,
                                    facecolor='lightgreen', edgecolor='black')
                main_ax.add_patch(rect)
                main_ax.text(x + element_width/2, 0.5, str(queue[i]),
                           ha='center', va='center', fontsize=12)
                
            if highlight_front_rear:
                # Front highlight
                main_ax.add_patch(plt.Rectangle(
                    (0, 0.1), element_width, 0.8,
                    facecolor='yellow', edgecolor='black', alpha=0.5
                ))
                main_ax.text(element_width/2, 0.05, "Front",
                            ha='center', va='top', fontsize=10)
                # Rear highlight
                main_ax.add_patch(plt.Rectangle(
                    ((N-1)*element_width, 0.1), element_width, 0.8,
                    facecolor='yellow', edgecolor='black', alpha=0.5
                ))
                main_ax.text((N-1)*element_width + element_width/2, 0.05, "Rear",
                            ha='center', va='top', fontsize=10)

        main_ax.set_xlim(0, max(1, N*element_width))
        main_ax.set_ylim(0, 1)
        main_ax.axis('off')

        # Code display
        if show_code and code_ax is not None:
            self._display_code(code_ax, metadata)

        # Title handling
        title = title or metadata.get('description', f"Step {metadata.get('step', 'N/A')}")
        fig.suptitle(title, y=0.95 if show_code else 0.9, fontsize=14)
        plt.tight_layout()
        plt.show()

    def create_animation(self, figsize: Tuple[int, int] = (10, 5),
                        interval: int = 1000, repeat: bool = False,
                        show_code: bool = True) -> Optional[FuncAnimation]:
        """
        Create queue operation animation with code context.
        
        Args:
            figsize: Figure dimensions
            interval: Frame delay (ms)
            repeat: Loop animation
            show_code: Show code context
            
        Returns:
            Matplotlib animation object
        """
        if not self.tracer.snapshots:
            print("No snapshots available")
            return None

        fig, main_ax, code_ax = self._create_figure_with_code(figsize, show_code)

        def update(frame: int):
            main_ax.clear()
            if code_ax is not None:
                code_ax.clear()
                code_ax.axis('off')

            queue = self.tracer.snapshots[frame]
            metadata = self.tracer.metadata[frame]
            N = len(queue)
            element_width = 0.8 / max(1, N) if N > 0 else 0.8

            # Visualization
            if N == 0:
                main_ax.text(0.5, 0.5, "Empty Queue", ha='center', va='center', fontsize=14)
            else:
                for i in range(N):
                    x = i * element_width
                    rect = plt.Rectangle((x, 0.1), element_width, 0.8,
                                       facecolor='lightgreen', edgecolor='black')
                    main_ax.add_patch(rect)
                    main_ax.text(x + element_width/2, 0.5, str(queue[i]),
                               ha='center', va='center', fontsize=12)
                    
                # Front and rear highlights
                main_ax.add_patch(plt.Rectangle(
                    (0, 0.1), element_width, 0.8,
                    facecolor='yellow', edgecolor='black', alpha=0.5
                ))
                main_ax.text(element_width/2, 0.05, "Front",
                            ha='center', va='top', fontsize=10)
                main_ax.add_patch(plt.Rectangle(
                    ((N-1)*element_width, 0.1), element_width, 0.8,
                    facecolor='yellow', edgecolor='black', alpha=0.5
                ))
                main_ax.text((N-1)*element_width + element_width/2, 0.05, "Rear",
                            ha='center', va='top', fontsize=10)

            main_ax.set_xlim(0, max(1, N*element_width))
            main_ax.set_ylim(0, 1)
            main_ax.axis('off')
            main_ax.set_title(f"Step {metadata['step']}: {metadata.get('description', '')}", 
                            pad=20)

            # Code display
            if show_code and code_ax is not None:
                self._display_code(code_ax, metadata)

        anim = FuncAnimation(fig, update, frames=len(self.tracer.snapshots),
                            interval=interval, repeat=repeat)
        plt.tight_layout()
        plt.show()
        return anim
    


# usage
# tracer = DataStructureTracer(track_code_lines=True)
# queue = []

# # Tracked operations
# def queue_operations():
#     tracer.capture(queue, description="Initial state")
#     queue.append(10)  # Enqueue
#     tracer.capture(queue, description="Enqueued 10")
#     queue.append(20)  # Enqueue
#     tracer.capture(queue, description="Enqueued 20")
#     queue.pop(0)      # Dequeue
#     tracer.capture(queue, description="Dequeued 10")

# queue_operations()

# # Visualization
# visualizer = QueueVisualizer(tracer)

# # Show final state with code
# visualizer.display_snapshot(show_code=True, 
#                           title="Final Queue State")

# # Generate animation
# anim = visualizer.create_animation(show_code=True, interval=1500)
# anim.save("queue_operations.gif", writer="pillow")