"""
Example tool for your agent.

This file demonstrates how to create custom tools for your ADK agent.
Copy this file as a template for creating new tools.
"""

from typing import Optional
from google.adk.tools import Tool


# Simple function-based tool
def calculate_sum(a: float, b: float) -> float:
    """
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """
    return a + b


# More complex async tool
async def fetch_data(query: str, limit: Optional[int] = 10) -> dict:
    """
    Example async tool that could fetch data from an API.

    Args:
        query: Search query
        limit: Maximum number of results (default: 10)

    Returns:
        Dictionary with search results
    """
    # TODO: Replace with actual API call
    return {
        "query": query,
        "results": [f"Result {i+1} for '{query}'" for i in range(limit)],
        "count": limit
    }


# Class-based tool for stateful operations
class DataProcessor:
    """Example of a class-based tool with state."""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.processed_count = 0

    def process(self, data: str) -> str:
        """
        Process data and keep track of operations.

        Args:
            data: Input data to process

        Returns:
            Processed data
        """
        self.processed_count += 1
        # TODO: Add your processing logic
        return f"Processed: {data} (#{self.processed_count})"


# Export tools for use in your agent
def get_example_tools():
    """Create and return example tools."""

    # Simple function tool
    sum_tool = Tool(
        name="calculate_sum",
        description="Add two numbers together",
        function=calculate_sum
    )

    # Async tool
    fetch_tool = Tool(
        name="fetch_data",
        description="Fetch data based on a query",
        function=fetch_data
    )

    # Class-based tool
    processor = DataProcessor()
    process_tool = Tool(
        name="process_data",
        description="Process data with state tracking",
        function=processor.process
    )

    return [sum_tool, fetch_tool, process_tool]


# Example of using tools in your agent:
#
# from .tools.example_tool import get_example_tools
#
# def create_my_agent() -> Agent:
#     return Agent(
#         name="my_agent",
#         model=LiteLlm(model="gpt-4"),
#         tools=get_example_tools(),  # Add your tools here
#         # ... other config ...
#     )