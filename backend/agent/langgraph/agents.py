from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class Tool:
    """Simple container for callable tools used by the agent.

    Attributes:
        name: Human readable name of the tool.
        func: Callable that implements the tool's logic.
        description: Optional description of what the tool does.
    """
    name: str
    func: Callable[..., Any]
    description: str = ""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Allow the tool instance to be called like the wrapped function."""
        return self.func(*args, **kwargs)
