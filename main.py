# main.py

import sys
import json

def hello(name):
    return f"Hello {name}, SyftBox is working!"

if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    name = data.get("name", "World")

    result = hello(name)

    print(json.dumps({
        "result": result
    }))