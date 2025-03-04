# 📌 Introduction

This library lets you visualize algorithms that operate on fundamental data structures like stacks, queues, trees, and graphs. It helps you trace your algorithm line by line while bringing its execution to life with animations.

## 🚀 Install

```Bash
pip install algofresco
```

## 🚀 Example: Stack Visualization

Here’s a simple example of how you can visualize a stack using the library:

```python
tracer = DataStructureTracer(track_code_lines=True)
stack = []

# Tracked operations
def stack_operations():
    tracer.capture(stack, description="Initial state")
    stack.append(10)  # Tracked
    tracer.capture(stack, description="Pushed 10")
    stack.append(20)  # Tracked
    tracer.capture(stack, description="Pushed 20")
    stack.pop()       # Tracked
    tracer.capture(stack, description="Popped 20")

stack_operations()

# Visualization
visualizer = StackVisualizer(tracer)

# Show the final state
# visualizer.display_snapshot(show_code=True, title="Final Stack State")

# Generate animation (save as GIF)
anim = visualizer.create_animation(show_code=True, interval=1500)
# anim.save("stack_demo.gif", writer="pillow")
```

### 🔍 Breaking It Down:

- `tracer = DataStructureTracer(track_code_lines=True)`: Enables tracking of code execution.
- `stack = []`: Initializes the stack we’ll trace.
- `visualizer = StackVisualizer(tracer)`: Prepares the visualization.
- `anim = visualizer.create_animation(show_code=True, interval=1500)`: Generates an animation—no need for `plt.show()`, the library handles that for you.

🎯 **Result:**
<img src="./examples/stack.gif" width="500" />

---

## 🛠 Creating Your Own Custom Data Structure

Let’s go step by step to create a **Singly Linked List** visualization using the library.

### Step 1: Understanding the Core Components

- **`DataStructureTracer`** - Tracks changes in data structures.
- **`DataStructureVisualizer`** - Base class for visualization.
- **Matplotlib** - Used for rendering.

### Step 2: Define Your Data Structure

```python
class LinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tracer = DataStructureTracer()

    def append(self, value):
        """Instrumented append operation"""
        new_node = LinkedListNode(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.tracer.capture(self, description=f"Appended {value}")
```

### Step 3: Implement the Visualization Class

```python
class LinkedListVisualizer(DataStructureVisualizer):
    def __init__(self, tracer):
        super().__init__(tracer)
        self.node_spacing = 1.0  # Horizontal spacing between nodes

    def _convert_to_digraph(self, linked_list):
        """Convert linked list to NetworkX graph for visualization"""
        G = nx.DiGraph()
        current = linked_list.head
        node_id = 0

        while current:
            G.add_node(node_id, value=current.value)
            if current.next:
                G.add_edge(node_id, node_id + 1)
            current = current.next
            node_id += 1

        return G

    def display_snapshot(self, step=-1, figsize=(10, 4), show_code=True):
        data, metadata = self.tracer.get_snapshot(step)
        fig, main_ax, code_ax = self._create_figure_with_code(figsize, show_code)

        if not data.head:
            main_ax.text(0.5, 0.5, "Empty List", ha='center', va='center')
        else:
            G = self._convert_to_digraph(data)
            pos = self._calculate_layout(G)
            self._draw_nodes(main_ax, G, pos)
            self._draw_edges(main_ax, G, pos)

        fig.suptitle(metadata.get('description', f"Step {metadata['step']}"))
        if show_code:
            self._display_code(code_ax, metadata)

        plt.show()
```

### Step 4: Use the Visualization

```python
# Create and populate the linked list
ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)

# Visualize
visualizer = LinkedListVisualizer(ll.tracer)
visualizer.display_snapshot(show_code=True)
visualizer.create_animation(interval=1500).save("list_evolution.gif")
```

---

## 🎨 Customization Options

### 1️⃣ Highlighting Specific Nodes

```python
def display_snapshot(self, step=-1, highlight_nodes=None, ...):
    # In drawing code:
    if highlight_nodes and node.value in highlight_nodes:
        circle.set_fc('#ff7f7f')  # Change color
```

### 2️⃣ Adding Metadata for Better Insights

```python
self.tracer.capture(self, custom_code_line="ll.insert_at(index, value)",
                   algorithm_step="Insertion")
```

### 3️⃣ Customizing Layouts

```python
def _calculate_layout(self, G):
    """Vertical layout example"""
    pos = {}
    y = 0
    for node in nx.topological_sort(G):
        pos[node] = (0, y)
        y -= self.node_spacing
    return pos
```

---

## 🔥 Best Practices

✅ Always capture the **initial and final states** of the data structure.
✅ Call `reset()` when processing multiple sequences to **free up memory**.
✅ Ensure valid **state transitions** before visualization.
✅ Optimize **animations** by precomputing layouts.
✅ Maintain a **consistent** color scheme and styling.

---

## 🌟 Advanced Features

### 📌 Composite Visualizations

Combine multiple data structures in a single visualization:

```python
class MultiStructureVisualizer(DataStructureVisualizer):
    def display_snapshot(self, step=-1):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        # Draw stack on ax1, queue on ax2
```

This lets you analyze interactions between different structures in the same run.

### 📌 Auto Tracer : Automatically trace function execution

Combine multiple data structures in a single visualization:

```python
# Initialize components
tracer = DataStructureTracer(track_code_lines=True)

# Binary tree node class
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

@tracer.auto_trace
def tree_operations():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(4)
```

---

## 🎯 Conclusion

This library makes it easy to **see** your algorithms in action. Whether you’re debugging, teaching, or just curious, visualization makes concepts more intuitive.

🚀 **Try it out, tweak it, and make your algorithms come to life!**
