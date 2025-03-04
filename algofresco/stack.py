
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from typing import Tuple, Optional
from .ds import DataStructureVisualizer

class StackVisualizer(DataStructureVisualizer):
    """Visualizes stack operations (LIFO) with code tracking support."""
    
    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (6, 8),
                        highlight_top: bool = True, title: Optional[str] = None,
                        show_code: bool = True):
        """
        Display a snapshot of the stack with optional code context.
        
        Args:
            step: Snapshot step (-1 for latest)
            figsize: Figure dimensions
            highlight_top: Highlight top element
            title: Custom title
            show_code: Show associated code
        """
        data, metadata = self.tracer.get_snapshot(step)
        if data is None:
            print("No data available")
            return

        fig, main_ax, code_ax = self._create_figure_with_code(figsize, show_code)
        stack = data
        N = len(stack)
        element_height = 0.8 / N if N > 0 else 0

        # Visualization
        if N == 0:
            main_ax.text(0.5, 0.5, "Empty Stack", ha='center', va='center', fontsize=14)
        else:
            for i in range(N):
                y = i * element_height
                rect = plt.Rectangle((0.1, y), 0.8, element_height, 
                                    facecolor='lightblue', edgecolor='black')
                main_ax.add_patch(rect)
                main_ax.text(0.5, y + element_height/2, str(stack[i]), 
                            ha='center', va='center', fontsize=12)
                
            if highlight_top:
                top_y = (N-1)*element_height
                main_ax.add_patch(plt.Rectangle(
                    (0.1, top_y), 0.8, element_height,
                    facecolor='yellow', edgecolor='black', alpha=0.5
                ))
                main_ax.text(0.05, top_y + element_height/2, "Top", 
                            ha='right', va='center', fontsize=10)

        main_ax.set_xlim(0, 1)
        main_ax.set_ylim(0, max(1, N*element_height))
        main_ax.axis('off')

        # Code display
        if show_code and code_ax is not None:
            self._display_code(code_ax, metadata)

        plt.tight_layout()
        plt.show()

    def create_animation(self, figsize: Tuple[int, int] = (6, 8), 
                        interval: int = 1000, repeat: bool = True,
                        show_code: bool = True) -> Optional[FuncAnimation]:
        """
        Create animation with code context.
        
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
        plt.tight_layout()

        def update(frame: int):
            main_ax.clear()
            if code_ax is not None: 
                code_ax.clear()
                code_ax.axis('off')

            stack = self.tracer.snapshots[frame]
            metadata = self.tracer.metadata[frame]
            N = len(stack)
            element_height = 0.8 / N if N > 0 else 0

            # Visualization
            if N == 0:
                main_ax.text(0.5, 0.5, "Empty Stack", ha='center', va='center', fontsize=14)
            else:
                for i in range(N):
                    y = i * element_height
                    rect = plt.Rectangle((0.1, y), 0.8, element_height, 
                                        facecolor='lightblue', edgecolor='black')
                    main_ax.add_patch(rect)
                    main_ax.text(0.5, y + element_height/2, str(stack[i]), 
                                ha='center', va='center', fontsize=12)
                    
                top_y = (N-1)*element_height
                main_ax.add_patch(plt.Rectangle(
                    (0.1, top_y), 0.8, element_height,
                    facecolor='yellow', edgecolor='black', alpha=0.5
                ))
                main_ax.text(0.05, top_y + element_height/2, "Top", 
                            ha='right', va='center', fontsize=10)

            main_ax.set_xlim(0, 1)
            main_ax.set_ylim(0, max(1, N*element_height))
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
# stack = []

# # Tracked operations
# def stack_operations():
#     tracer.capture(stack, description="Initial state")
#     stack.append(10)  # This line will be tracked
#     tracer.capture(stack, description="Pushed 10")
#     stack.append(20)  # This line will be tracked
#     tracer.capture(stack, description="Pushed 20")
#     stack.pop()       # This line will be tracked
#     tracer.capture(stack, description="Popped 20")

# stack_operations()

# # Visualization
# visualizer = StackVisualizer(tracer)

# # Show final state with code
# visualizer.display_snapshot(show_code=True, 
#                           title="Final Stack State")

# # Generate animation (save as GIF)
# anim = visualizer.create_animation(show_code=True, interval=1500)
# plt.show()
# anim.save("stack_demo.gif", writer="pillow")