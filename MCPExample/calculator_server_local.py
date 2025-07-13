from mcp.server.fastmcp import FastMCP
from typing import Literal

# Initialize the MCP server with a descriptive name
mcp = FastMCP("Calculator Server")

@mcp.tool()
def add(a: float, b: float) -> float:
    """Adds two numbers and returns the sum."""
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtracts the second number from the first and returns the difference."""
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers and returns the product."""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divides the first number by the second and returns the quotient. Handles division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

@mcp.resource("info://calculator")
def get_calculator_info() -> str:
    """Provides information about the calculator server."""
    return "This is a simple calculator MCP server supporting addition, subtraction, multiplication, and division."

@mcp.prompt()
def usage_instructions() -> str:
    """Provides instructions on how to use the calculator tools."""
    return """
You can use the following tools:
- `add(a: float, b: float)`: Adds two numbers.
- `subtract(a: float, b: float)`: Subtracts two numbers.
- `multiply(a: float, b: float)`: Multiplies two numbers.
- `divide(a: float, b: float)`: Divides two numbers (second number cannot be zero).

Example: "What is 5 plus 3?" or "Calculate 10 divided by 2."
"""

# Run the MCP server locally (using STDIO by default)
if __name__ == '__main__':
    print("Starting Calculator MCP Server...")
    mcp.run()