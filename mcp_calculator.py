"""
Simple MCP calculator exposing arithmetic tools via FastMCP.
"""
from fastmcp import FastMCP


mcp = FastMCP(name="MyCalculator")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Return the result of subtracting b from a."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Return the quotient of a divided by b; disallow zero division."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":
    # Change transport to "sse" if needed.
    mcp.run(transport="http")

