import numpy as np
from typing import List, Any, Tuple, Optional
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .ds import DataStructureVisualizer

class DictionaryVisualizer(DataStructureVisualizer):
    """Visualizes dictionary operations with code context tracking."""
    
    def display_snapshot(self, step: int = -1, figsize: Tuple[int, int] = (10, 6),
                        highlight_keys: Optional[List[Any]] = None,
                        highlight_values: Optional[List[Any]] = None,
                        title: Optional[str] = None,
                        show_code: bool = True):
        """
        Display dictionary snapshot with code context.
        
        Args:
            step: Snapshot step (-1 for latest)
            figsize: Figure dimensions
            highlight_keys: Keys to highlight
            highlight_values: Values to highlight
            title: Custom title
            show_code: Show associated code
        """
        data, metadata = self.tracer.get_snapshot(step)
        if data is None:
            print("No data available")
            return

        fig, main_ax, code_ax = self._create_figure_with_code(figsize, show_code)
        items = list(data.items())
        n_items = len(items)
        grid_size = int(np.ceil(np.sqrt(n_items))) if n_items > 0 else 1
        grid_width = 1.0 / grid_size
        grid_height = 1.0 / grid_size

        # Visualization
        if n_items == 0:
            main_ax.text(0.5, 0.5, "Empty Dictionary", 
                        ha='center', va='center', fontsize=14)
        else:
            for i, (key, value) in enumerate(items):
                row = i // grid_size
                col = i % grid_size
                x = col * grid_width
                y = 1.0 - (row + 1) * grid_height

                # Key highlighting
                key_color = '#ffcf75' if highlight_keys and key in highlight_keys \
                           else '#f0f0f0'
                # Value highlighting
                value_color = '#8dc7f3' if highlight_values and value in highlight_values \
                            else '#f0f0f0'

                # Key rectangle
                main_ax.add_patch(plt.Rectangle(
                    (x, y + grid_height/2), grid_width, grid_height/2,
                    facecolor=key_color, edgecolor='black'
                ))
                main_ax.text(x + grid_width/2, y + 3*grid_height/4, str(key),
                           ha='center', va='center', fontsize=10)

                # Value rectangle
                main_ax.add_patch(plt.Rectangle(
                    (x, y), grid_width, grid_height/2,
                    facecolor=value_color, edgecolor='black'
                ))
                main_ax.text(x + grid_width/2, y + grid_height/4, str(value),
                           ha='center', va='center', fontsize=10)

        main_ax.set_xlim(0, 1)
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

    def create_animation(self, figsize: Tuple[int, int] = (10, 6),
                        interval: int = 1000, repeat: bool = False,
                        show_code: bool = True) -> Optional[FuncAnimation]:
        """
        Create dictionary operation animation with code context.
        
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

            data = self.tracer.snapshots[frame]
            metadata = self.tracer.metadata[frame]
            items = list(data.items())
            n_items = len(items)
            grid_size = int(np.ceil(np.sqrt(n_items))) if n_items > 0 else 1
            grid_width = 1.0 / grid_size
            grid_height = 1.0 / grid_size

            # Visualization
            if n_items == 0:
                main_ax.text(0.5, 0.5, "Empty Dictionary", 
                            ha='center', va='center', fontsize=14)
            else:
                for i, (key, value) in enumerate(items):
                    row = i // grid_size
                    col = i % grid_size
                    x = col * grid_width
                    y = 1.0 - (row + 1) * grid_height

                    # Key/value rectangles
                    main_ax.add_patch(plt.Rectangle(
                        (x, y + grid_height/2), grid_width, grid_height/2,
                        facecolor='#f0f0f0', edgecolor='black'
                    ))
                    main_ax.text(x + grid_width/2, y + 3*grid_height/4, str(key),
                               ha='center', va='center', fontsize=10)
                    
                    main_ax.add_patch(plt.Rectangle(
                        (x, y), grid_width, grid_height/2,
                        facecolor='#f0f0f0', edgecolor='black'
                    ))
                    main_ax.text(x + grid_width/2, y + grid_height/4, str(value),
                               ha='center', va='center', fontsize=10)

            main_ax.set_xlim(0, 1)
            main_ax.set_ylim(0, 1)
            main_ax.axis('off')
            main_ax.set_title(f"Step {metadata['step']}: {metadata.get('description', '')}", 
                            pad=20)

            # Code display
            if show_code and code_ax is not None:
                self._display_code(code_ax, metadata)

        anim = FuncAnimation(fig, update, frames=len(self.tracer.snapshots),
                            interval=interval, repeat=repeat)
        plt.show()
        return anim