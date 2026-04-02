import requests
from rich import print
url="http://127.0.0.1:8000/mcp/"

header={
    "Accept":"application/json,text/event-stream",
}

body={
    "jsonrpc":"2.0",
    "method":"tools/call",
    "params":{
        "name":"multiply_tool",
        "arguments":{
            "n1":123,
            "n2":243
        }
    },
    "id":1
}

response=requests.post(url=url,headers=header,json=body)
print(response.text)