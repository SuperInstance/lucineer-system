import os
def get_key():
    with open("/home/eileen/mcp-deeinfra/.env") as f:
        for line in f:
            if line.startswith("DEEPINFRA_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("DEEPINFRA_API_KEY", "")
