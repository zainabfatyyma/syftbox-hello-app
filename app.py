# app.py

def hello(name: str):
    return f"Hello {name}, SyftBox is working!"

EXPOSED_FUNCTIONS = {
    "hello": hello
}