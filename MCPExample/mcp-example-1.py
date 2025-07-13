# https://medium.com/@ruchi.awasthi63/integrating-mcp-servers-with-fastapi-2c6d0c9a4749

import uvicorn
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

# Your existing FastAPI application
app = FastAPI()

#You can customize the FastAPI app further if needed
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/bmi/{weight_kg}/{height_m}", operation_id="calculate_bmi", summary="this tool is used to calculate bmi based on weigth and height")
def calculate_bmi(weight_kg: float, height_m: float):
    return {"bmi": weight_kg / (height_m ** 2)}

# MCP server configuration
mcp = FastApiMCP(app, name="Calculator MCP Server")

# Mount the MCP server to your FastAPI app
mcp.mount()

if __name__ == '__main__':
    print("Starting Calculator MCP Server...")
    # Run the FastAPI app with Uvicorn
    # Make sure to install uvicorn: pip install "uvicorn[standard]"
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
