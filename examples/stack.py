# # Initialize components
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
# anim.save("stack_demo.gif", writer="pillow")