import copy
import time
import inspect
import linecache
from typing import Dict, Any, Tuple, List, Optional, Callable


class DataStructureTracer:
    """Base class for tracking changes to data structures during algorithm execution."""
    
    def __init__(self, track_code_lines: bool = True):
        """
        Initialize the data structure tracer.
        
        Args:
            track_code_lines: Whether to track the lines of code being executed
        """
        self.snapshots = []
        self.metadata = []
        self.current_step = 0
        self.track_code_lines = track_code_lines
        self.parent_frame = None
    
    def _get_caller_info(self) -> Dict[str, Any]:
        """Get information about the caller function and line of code."""
        if not self.track_code_lines:
            return {}
            
        # Get the caller's frame
        frame = inspect.currentframe()
        try:
            # Move up frames until we're outside this method and class
            frame = frame.f_back  # caller of _get_caller_info
            frame = frame.f_back  # caller of capture or other method
            
            # If we haven't stored the parent frame yet, store it
            if self.parent_frame is None:
                self.parent_frame = frame
            
            # Get file, line number, and function name
            filename = frame.f_code.co_filename
            line_num = frame.f_lineno
            func_name = frame.f_code.co_name
            
            # Get the actual line of code
            line = linecache.getline(filename, line_num).strip()
            
            return {
                'filename': filename,
                'line_num': line_num,
                'function': func_name,
                'code_line': line
            }
        finally:
            # Clean up to prevent reference cycles
            del frame
    
    def capture(self, data: Any, description: str = "", custom_code_line: str = None, **kwargs):
        """
        Capture the current state of a data structure.
        
        Args:
            data: The data structure to capture
            description: A description of the current algorithm step
            custom_code_line: Override the automatically detected code line
            **kwargs: Additional metadata to store
        """
        # Create a deep copy to prevent reference issues
        snapshot = copy.deepcopy(data)
        self.snapshots.append(snapshot)
        
        # Get caller information
        caller_info = self._get_caller_info()
        
        # Override code line if provided
        if custom_code_line:
            caller_info['code_line'] = custom_code_line
        
        metadata = {
            'step': self.current_step,
            'description': description,
            'timestamp': time.time(),
            **caller_info,
            **kwargs
        }
        self.metadata.append(metadata)
        
        self.current_step += 1
    
    def get_snapshot(self, step: int = -1) -> Tuple[Any, Dict]:
        """
        Get a specific snapshot and its metadata.
        
        Args:
            step: The step number to retrieve (-1 for latest)
            
        Returns:
            Tuple of (snapshot data, metadata)
        """
        if not self.snapshots:
            return None, {}
            
        if step == -1:
            return self.snapshots[-1], self.metadata[-1]
            
        if 0 <= step < len(self.snapshots):
            return self.snapshots[step], self.metadata[step]
            
        return None, {}
    
    def reset(self):
        """Reset the tracer."""
        self.snapshots = []
        self.metadata = []
        self.current_step = 0
        self.parent_frame = None
        
    def auto_trace(self, func: Callable) -> Callable:
        """
        Decorator that automatically traces a function's execution.
        
        Args:
            func: The function to trace
            
        Returns:
            Wrapped function that captures state at each step
        """
        def wrapper(*args, **kwargs):
            # Reset tracer to start fresh
            self.reset()
            
            # Get the source code of the function
            source_lines = inspect.getsourcelines(func)[0]
            clean_source = [line.strip() for line in source_lines]
            
            # Extract parameter that represents the data structure
            # Assuming the first parameter is the data structure
            if len(args) > 0:
                data_structure = args[0]
            else:
                # Try to find the data structure in kwargs
                sig = inspect.signature(func)
                first_param = next(iter(sig.parameters))
                data_structure = kwargs.get(first_param)
            
            # Capture initial state
            self.capture(data_structure, description="Initial state")
            
            # Run the function and capture final state
            result = func(*args, **kwargs)
            
            # Capture final state if it returned a value
            if result is not None:
                self.capture(result, description="Final state")
            elif data_structure is not None:
                # If no return value, assume the data structure was modified in place
                self.capture(data_structure, description="Final state")
                
            return result
            
        return wrapper