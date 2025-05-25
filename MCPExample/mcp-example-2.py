# https://medium.com/@ruchi.awasthi63/integrating-mcp-servers-with-fastapi-2c6d0c9a4749


#my_script.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool()
def add(x: int, y: int) -> int:
    return x + y

if __name__ == "__main__":
    mcp.run()
