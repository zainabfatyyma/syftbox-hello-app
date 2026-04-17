import sys
import json

def hello(name):
    return f"Hello {name}, SyftBox is working!"

if __name__ == "__main__":
    raw_input = sys.stdin.read().strip()

    if not raw_input:
        data = {}
    else:
        data = json.loads(raw_input)

    name = data.get("name", "World")

    result = hello(name)

    print(json.dumps({
        "result": result
    }))