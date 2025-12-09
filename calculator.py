from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="MATEMATICA"
)

@mcp.tool()
def say_hello(name: str):
    return f"Hello to {name}!"

@mcp.tool()
def add(a: float, b: float):
    return a + b

@mcp.tool()
def subtract(a: float, b: float):
    return a - b

@mcp.tool()
def multiply(a: float, b: float):
    return a * b

@mcp.tool()
def divide(a: float, b: float):
    if b == 0:
        return "Error: manjmouch n9smou 3la sfer"
    return a / b

if __name__ == "__main__":
    mcp.run(transport="stdio")