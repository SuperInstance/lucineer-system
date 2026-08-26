#!/usr/bin/env python3
import json, subprocess, sys

def call(name, args, id=1):
    payload = {"jsonrpc":"2.0","id":id,"method":"tools/call",
               "params":{"name":name,"arguments":args}}
    out = subprocess.run(["curl","-s","http://127.0.0.1:8765/","-X","POST",
                          "-H","Content-Type: application/json",
                          "-d",json.dumps(payload)],
                         capture_output=True, text=True).stdout
    try:
        d = json.loads(out)
    except Exception:
        print("RAW:", out[:2000]); sys.exit(1)
    r = d.get("result", {})
    if r.get("isError"):
        print("TOOL ERROR:", json.dumps(r)[:2000]); sys.exit(2)
    sc = r.get("structuredContent")
    if sc is not None:
        return sc
    for c in r.get("content", []):
        if c.get("type") == "text":
            try: return json.loads(c["text"])
            except Exception: return c["text"]
    return r

if __name__ == "__main__":
    name = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    res = call(name, args)
    print(json.dumps(res, indent=1)[:12000] if not isinstance(res,str) else res[:12000])
