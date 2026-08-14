#!/usr/bin/env python3
"""DeepInfra panel discussion helper."""
import sys, json, urllib.request, os

API_KEY = os.environ.get('DEEPINFRA_API_KEY', '')
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

def call_model(model, system_prompt, user_prompt, temperature=0.8, max_tokens=800):
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }).encode()
    req = urllib.request.Request(API_URL, data=payload, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"ERROR: {e}"

if __name__ == "__main__":
    # args: model, system_file, prompt_file, temperature
    model = sys.argv[1]
    system_prompt = sys.argv[2]
    user_prompt = sys.argv[3]
    temp = float(sys.argv[4]) if len(sys.argv) > 4 else 0.8
    result = call_model(model, system_prompt, user_prompt, temp)
    print(result)
