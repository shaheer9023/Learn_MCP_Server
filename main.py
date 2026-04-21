from mcp.server.fastmcp import FastMCP
from math_tools import plus,multiply,divide,subtract
app=FastMCP(name="my_server",stateless_http=True)

@app.tool()
def plus_tool(n1:int,n2:int)->str:
    "you are a math teacher, please help me to add two numbers"
    return plus(n1,n2)

@app.tool()
def multiply_tool(n1:int,n2:int)->str:
    "you are a math teacher, please help me to multiply two numbers"
    return multiply(n1,n2)

@app.tool()
def divide_tool(n1:int,n2:int)->str:
    "you are a math teacher, please help me to divide two numbers"
    return divide(n1,n2)

@app.tool()
def subtract_tool(n1:int,n2:int)->str:
    "you are a math teacher, please help me to subtract two numbers"
    return subtract(n1,n2)

app_mcp=app.streamable_http_app()