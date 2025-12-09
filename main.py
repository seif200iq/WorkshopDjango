from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="sayHello"
)

@mcp.tool()
def say_hello(name: str):
    """Greets someone by name"""
    return f"Hello to {name}!"

if __name__ == "__main__":
    mcp.run(transport="stdio")