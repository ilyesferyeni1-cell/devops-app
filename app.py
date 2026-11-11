print("hello devops")
print("version 2")
def greet(name):
    return f"Hello {name}"
print(greet("Ilyes"))
print("from GitHub")
APP_VERSION = "1.0.0"
print(f"App version: {APP_VERSION}")
print("Ready")

def health():
    return {"status": "ok", "version": APP_VERSION}

print(health())
