# omniverobrix/core/tool_registry.py

from typing import Callable, Dict, Any, Optional


class ToolRegistry:
    """
    Central registry for all OmniVeroBrix tools.
    Tools are registered with:
        - name
        - description
        - callable function
        - optional metadata (permissions, categories, etc.)
    """

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    # ---------------------------------------------------------
    # REGISTRATION
    # ---------------------------------------------------------

    def register(
        self,
        name: str,
        func: Callable,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Register a tool with the system.
        """
        if name in self.tools:
            raise ValueError(f"Tool '{name}' is already registered.")

        self.tools[name] = {
            "func": func,
            "description": description,
            "metadata": metadata or {},
        }

    # ---------------------------------------------------------
    # INVOCATION
    # ---------------------------------------------------------

    def call(self, name: str, **kwargs) -> Any:
        """
        Call a registered tool by name.
        """
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' is not registered.")

        tool = self.tools[name]
        func = tool["func"]

        return func(**kwargs)

    # ---------------------------------------------------------
    # INTROSPECTION
    # ---------------------------------------------------------

    def list_tools(self) -> Dict[str, Dict[str, Any]]:
        """
        Return all registered tools and metadata.
        """
        return self.tools

    def describe(self, name: str) -> str:
        """
        Return description of a tool.
        """
        if name not in self.tools:
            return f"Tool '{name}' not found."

        return self.tools[name]["description"]


# ---------------------------------------------------------
# OPTIONAL: GLOBAL REGISTRY INSTANCE
# ---------------------------------------------------------

global_tool_registry = ToolRegistry()
