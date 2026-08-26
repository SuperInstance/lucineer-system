#!/usr/bin/env python3
import sys; sys.path.insert(0,'.')
from mcp import call

PART_R1 = """@piano | C3-G3-D4 . E4 G4 (rest) C5 . . | Db3-Ab3-Eb4 . F4 Ab4 (rest) Db5 G4 . | A2-E3-G3-D4 . . G4 . F4 E4 . | G2-F3-B3-E4 . A4 . B4 (rest) (rest) (rest) |
@piano | C3-G3-D4 . E4 G4 (rest) C5 . . | C3-G3-D4 . Eb5 . D5 B4 (rest) . | F3-Ab3-C4-E4 . Gb3-B3-Db4-F4 . G3-B3-D4-F4 . A4 . | G2-F3-Ab3-B3 (rest) (rest) D5 (rest) (rest) (rest) (rest) |
@piano | Db4-F4-Ab4-C5 . . . Eb5 Db5 C5 Ab4 | E3-G#3-B3-D5 . . D5 C5 . B4 . | A2-G3-B3-E4 . . C#4-E4-G4-B4 . A4 . . | D3-F3-C4-E4 . Db3-F3-Ab3-B3 . . B4 (rest) . |
@piano | C2-G2-D3 . E3 G3 (rest) C3 . . | Db3-Ab3-Eb4 (rest) (rest) G3-B3-F4 (rest) (rest) (rest) (rest) | C3-G3-Eb4 . D4 . Eb5 D5 B4 (rest) | C2-G2 . . B3-D4-E4-A4 . . . . |"""

res = call("ensemble_write_part", {
    "session":"duke-lab","voice":"piano","agent":"band-glm",
    "base_version":0, "content": PART_R1,
    "summary":"R1 band take: side-slip D-flat bar2, planing F/Gb/G bar7, Dbmaj9 bridge, unresolved C(add9) end"
})
print(json.dumps(res, indent=1)[:4000] if not isinstance(res,str) else res[:4000]) if False else None
import json; print(json.dumps(res, indent=1)[:4000])
