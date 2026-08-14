"""Load the DeepInfra API key for the lucineer-system scripts.

Resolution order:
1. First line of the form ``DEEPINFRA_API_KEY=...`` (with optional ``export``
   prefix) in the local mcp .env file. The directory is named ``mcp-deeinfra``
   on disk — a long-standing typo that other tooling depends on, so it stays.
2. The ``DEEPINFRA_API_KEY`` environment variable.

The env-var fallback only works if the .env file is absent or lacks the key;
a missing file must not raise, or the fallback would be dead code.
"""

import os


def get_key():
    env_path = "/home/eileen/mcp-deeinfra/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("export "):
                    line = line[len("export "):]
                if line.startswith("DEEPINFRA_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("DEEPINFRA_API_KEY", "")
