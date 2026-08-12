#!/usr/bin/env python3
"""
Image Generation Gallery v3 — clean, working.
Split panel: gallery left, controls right.
Click image → loads recipe. Generate from scratch or remix.
"""

import os, sys, json, time, uuid, threading, subprocess, glob, traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

GALLERY_DIR = os.path.expanduser("~/.openclaw/workspace/output/images/gallery")
EXTRA_DIRS = [
    os.path.expanduser("~/.openclaw/workspace/output/images/tap-scenes"),
    os.path.expanduser("~/.openclaw/workspace/output/images"),
]
GEN_SCRIPT = os.path.expanduser("~/.openclaw/workspace/scripts/generate_image_v2.py")
CHECKPOINT_DIR = "/mnt/c/Users/casey/Documents/ComfyUI/models/checkpoints"
LORA_DIR = "/mnt/c/Users/casey/Documents/ComfyUI/models/loras"
PORT = 5555
QUEUE_FILE = os.path.expanduser("~/.openclaw/workspace/output/images/gallery/.queue.json")
STATUS_FILE = os.path.expanduser("~/.openclaw/workspace/output/images/gallery/.gen-status.json")

def list_models():
    models = []
    if os.path.isdir(CHECKPOINT_DIR):
        for f in sorted(os.listdir(CHECKPOINT_DIR)):
            if f.endswith(('.safetensors', '.ckpt')):
                models.append(f.replace('.safetensors', '').replace('.ckpt', ''))
    return models

def list_loras():
    loras = []
    if os.path.isdir(LORA_DIR):
        for f in sorted(os.listdir(LORA_DIR)):
            if f.endswith(('.safetensors', '.ckpt')):
                loras.append(f.replace('.safetensors', '').replace('.ckpt', ''))
    return loras

def scan_gallery():
    items = []
    seen = set()
    for d in [GALLERY_DIR] + EXTRA_DIRS:
        if not os.path.isdir(d):
            continue
        for ext in ('*.png', '*.jpg', '*.jpeg'):
            for img_path in sorted(glob.glob(os.path.join(d, ext)), reverse=True):
                if img_path in seen:
                    continue
                seen.add(img_path)
                meta = None
                meta_path = img_path.rsplit('.', 1)[0] + '.json'
                if os.path.exists(meta_path):
                    try:
                        with open(meta_path) as f:
                            meta = json.load(f)
                    except:
                        pass
                if not meta:
                    # Guess model from filename
                    fname = os.path.basename(img_path)
                    guessed_model = "unknown"
                    for m in list_models():
                        if m.lower() in fname.lower():
                            guessed_model = m
                            break
                    meta = {
                        "prompt": "",
                        "negative_prompt": "",
                        "model": guessed_model,
                        "steps": 25,
                        "guidance": 7.5,
                        "seed": "",
                        "width": 512,
                        "height": 512,
                        "loras": [],
                        "filename": fname,
                    }
                meta['_path'] = img_path
                meta['_serve'] = f"/image?path={img_path}"
                items.append(meta)
    return items


def generation_worker():
    while True:
        try:
            if not os.path.exists(QUEUE_FILE):
                time.sleep(2)
                continue
            
            with open(QUEUE_FILE) as f:
                queue = json.load(f)
            
            if not queue:
                time.sleep(2)
                continue
            
            job = queue.pop(0)
            with open(QUEUE_FILE, 'w') as f:
                json.dump(queue, f)
            
            with open(STATUS_FILE, 'w') as f:
                json.dump({"status": "generating", "job": job, "started": time.time()}, f)
            
            # Build command carefully — no None values
            prompt = job.get("prompt") or ""
            negative = job.get("negative_prompt") or ""
            model = job.get("model") or "dreamshaper_8"
            steps = int(job.get("steps") or 25)
            guidance = float(job.get("guidance") or 7.5)
            width = int(job.get("width") or 512)
            height = int(job.get("height") or 512)
            seed = job.get("seed")
            loras = job.get("loras") or []
            
            output_path = os.path.join(GALLERY_DIR, f"{int(time.time())}-{uuid.uuid4().hex[:6]}.png")
            
            # Write a JSON params file and use --json-input
            params = {
                "prompt": prompt,
                "negative_prompt": negative,
                "model": model,
                "steps": steps,
                "guidance": guidance,
                "width": width,
                "height": height,
                "output": output_path,
                "loras": loras,
            }
            if seed is not None:
                params["seed"] = int(seed)
            
            params_file = output_path.replace('.png', '.params.json')
            with open(params_file, 'w') as f:
                json.dump(params, f)
            
            cmd = ["python3", GEN_SCRIPT, "--json-input", params_file]
            
            print(f"[Worker] Running: model={model}, steps={steps}, cfg={guidance}", flush=True)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                with open(STATUS_FILE, 'w') as f:
                    json.dump({"status": "done", "job": job, "finished": time.time(), "output": output_path}, f)
                print(f"[Worker] Done: {output_path}", flush=True)
            else:
                with open(STATUS_FILE, 'w') as f:
                    json.dump({"status": "error", "job": job, "error": result.stderr[-500:] if result.stderr else "unknown error"}, f)
                print(f"[Worker] Error: {result.stderr[-200:]}", flush=True)
            
            # Clean up params file
            try:
                os.remove(params_file)
            except:
                pass
            
            time.sleep(1)
            
        except Exception as e:
            print(f"[Worker] Exception: {e}", flush=True)
            traceback.print_exc()
            with open(STATUS_FILE, 'w') as f:
                json.dump({"status": "error", "job": {}, "error": str(e)}, f)
            time.sleep(2)


HTML = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>🎨 Generation Studio</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#0a0a0f; color:#e0e0e0; font-family:system-ui,sans-serif; height:100vh; overflow:hidden; display:flex; flex-direction:column; }
.header { background:#0d0d14; padding:10px 20px; border-bottom:1px solid #1e1e2e; display:flex; align-items:center; gap:16px; }
.header h1 { font-size:15px; color:#7c8cf0; }
.header .stats { font-size:11px; color:#555; }
.main { display:flex; flex:1; overflow:hidden; }
.gallery-panel { flex:1; overflow-y:auto; padding:14px; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:10px; }
.gi { background:#111; border-radius:6px; overflow:hidden; cursor:pointer; border:2px solid transparent; transition:all .12s; position:relative; }
.gi:hover { transform:scale(1.04); border-color:#556; }
.gi.active { border-color:#4a9; }
.gi img { width:100%; aspect-ratio:1; object-fit:cover; display:block; }
.gi .tag { position:absolute; bottom:0; left:0; right:0; background:rgba(0,0,0,.75); font-size:9px; padding:2px 4px; color:#9ad; }
.gi .new { position:absolute; top:4px; right:4px; background:#4a9; color:#000; font-size:8px; font-weight:bold; padding:1px 5px; border-radius:3px; }
.cp { width:380px; flex-shrink:0; background:#0d0d14; border-left:1px solid #1e1e2e; overflow-y:auto; padding:16px; }
.cp h2 { font-size:13px; color:#7c8cf0; margin-bottom:12px; }
.f { margin-bottom:10px; }
.f label { display:block; font-size:10px; color:#666; text-transform:uppercase; margin-bottom:3px; }
.f textarea, .f input, .f select { width:100%; background:#06060c; border:1px solid #1e1e2e; color:#ccc; padding:7px 9px; border-radius:5px; font-size:12px; font-family:inherit; }
.f textarea { min-height:50px; resize:vertical; }
.f input:focus, .f textarea:focus, .f select:focus { outline:none; border-color:#7c8cf0; }
.fr { display:flex; gap:8px; }
.fr .f { flex:1; }
.lr { display:flex; gap:6px; align-items:center; margin-bottom:5px; }
.lr select { flex:1; font-size:11px; }
.lr input { width:50px; font-size:11px; }
.lr b { background:#2a1a1a; color:#e55; width:22px; height:22px; border-radius:4px; cursor:pointer; border:none; font-size:10px; }
.ab { background:#15152a; border:1px dashed #333; color:#777; padding:4px 10px; border-radius:4px; cursor:pointer; font-size:11px; }
.ab:hover { border-color:#7c8cf0; color:#7c8cf0; }
.btn { background:#7c8cf0; color:#fff; border:none; padding:9px 18px; border-radius:5px; cursor:pointer; font-size:13px; font-weight:600; }
.btn:hover { background:#6a7ae0; }
.bg { background:#1a1a2a; color:#888; }
.bg:hover { background:#2a2a3a; color:#ccc; }
.br { display:flex; gap:8px; margin-top:14px; }
.st { position:fixed; bottom:14px; right:14px; background:#0d0d14; border:1px solid #333; padding:10px 16px; border-radius:6px; font-size:12px; display:none; z-index:500; }
.st.active { display:block; }
.st.gen { border-color:#7c8cf0; }
.st.done { border-color:#4a9; }
.st.err { border-color:#e55; }
.hint { font-size:10px; color:#444; margin-top:6px; }
</style>
</head>
<body>
<div class="header">
  <h1>🎨 Generation Studio</h1>
  <div class="stats" id="stats">Loading...</div>
</div>
<div class="main">
  <div class="gallery-panel"><div class="grid" id="grid"></div></div>
  <div class="cp"><h2 id="panel-title">⚡ New Generation</h2><div id="pc"></div></div>
</div>
<div class="st" id="st"></div>
<script>
const M=__MODELS__, L=__LORAS__;
let items=[], sel=-1;
const BLANK={prompt:'',negative_prompt:'',model:M[0]||'dreamshaper_8',steps:25,guidance:7.5,seed:null,width:512,height:768,loras:[],_blank:true};

function renderPanel(it){
  const b=it._blank;
  let lh='';
  if(it.loras) it.loras.forEach((l,i)=>{lh+=lr(l.name,l.weight);});
  document.getElementById('pc').innerHTML=`
    ${!b?'<div style="font-size:10px;color:#444;margin-bottom:10px;word-break:break-all">'+esc(it._path||'')+'</div>':''}
    <div class="f"><label>Prompt</label><textarea id="fP" placeholder="Describe what you want...">${esc(it.prompt||'')}</textarea></div>
    <div class="f"><label>Negative Prompt</label><textarea id="fN" placeholder="What to avoid...">${esc(it.negative_prompt||'')}</textarea></div>
    <div class="f"><label>Model</label><select id="fM">${M.map(m=>'<option value="'+m+'"'+(m===it.model?' selected':'')+'>'+m+'</option>').join('')}</select></div>
    <div class="fr"><div class="f"><label>Steps</label><input type="number" id="fS" value="${it.steps||25}"></div>
    <div class="f"><label>CFG</label><input type="number" step="0.5" id="fG" value="${it.guidance||7.5}"></div></div>
    <div class="fr"><div class="f"><label>Width</label><input type="number" id="fW" value="${it.width||512}" step="64"></div>
    <div class="f"><label>Height</label><input type="number" id="fH" value="${it.height||768}" step="64"></div>
    <div class="f"><label>Seed</label><input type="number" id="fSeed" value="${(it.seed&&!b)?it.seed:''}" placeholder="rand"></div></div>
    <div class="f"><label>LoRAs</label><div id="lL">${lh}</div><button class="ab" onclick="addLora()">+ Add LoRA</button></div>
    <div class="br"><button class="btn" onclick="gen(false)">⚡ Generate</button><button class="btn bg" onclick="gen(true)">🎲 Variation</button></div>
    <div class="hint">${b?'Write a prompt and hit Generate. Try different models to see how they interpret it.':'Edit any field and Generate to remix. Variation = new random seed.'}</div>
  `;
}
function lr(n,w){return '<div class="lr"><select>'+L.map(l=>'<option value="'+l+'"'+(l===n?' selected':'')+'>'+l+'</option>').join('')+'</select><input type="number" step="0.1" value="'+(w||0.7)+'"><b onclick="this.parentElement.remove()">✕</b></div>';}
function addLora(){const d=document.createElement('div');d.className='lr';d.innerHTML='<select><option value="">-- LoRA --</option>'+L.map(l=>'<option value="'+l+'">'+l+'</option>').join('')+'</select><input type="number" step="0.1" value="0.7"><b onclick="this.parentElement.remove()">✕</b>';document.getElementById('lL').appendChild(d);}
function params(){
  const ls=[];
  document.querySelectorAll('#lL .lr').forEach(r=>{const s=r.querySelector('select'),i=r.querySelector('input');if(s&&s.value&&i)ls.push({name:s.value,weight:parseFloat(i.value)});});
  const sv=document.getElementById('fSeed').value;
  return{prompt:document.getElementById('fP').value,negative_prompt:document.getElementById('fN').value,model:document.getElementById('fM').value,steps:parseInt(document.getElementById('fS').value)||25,guidance:parseFloat(document.getElementById('fG').value)||7.5,seed:sv?parseInt(sv):null,width:parseInt(document.getElementById('fW').value)||512,height:parseInt(document.getElementById('fH').value)||768,loras:ls};
}
function gen(v){let p=params();if(v)p.seed=null;if(!p.prompt.trim()){alert('Write a prompt first!');return;}sst('Queuing...','gen');fetch('/api/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)}).then(r=>r.json()).then(()=>{sst('Queued! ~60s...','gen');setTimeout(poll,3000);});}
async function poll(){try{const r=await fetch('/api/status');const d=await r.json();if(d.status==='generating'){sst('⚙️ '+(Math.round(Date.now()/1000-d.started))+'s','gen');setTimeout(poll,4000);}else if(d.status==='done'){sst('✅ Reloading...','done');await load(true);setTimeout(hst,2000);}else if(d.status==='error'){sst('❌ '+(d.error||'').substring(0,100),'err');setTimeout(hst,8000);}}catch(e){setTimeout(poll,5000);}}
function sst(m,t){const s=document.getElementById('st');s.textContent=m;s.className='st active '+t;}
function hst(){document.getElementById('st').className='st';}
async function load(mkNew){
  const r=await fetch('/api/gallery');const ni=await r.json();
  if(mkNew&&items.length){const op=new Set(items.map(i=>i._path));ni.forEach(i=>{if(!op.has(i._path))i._new=true;});}
  items=ni;const g=document.getElementById('grid');g.innerHTML='';
  document.getElementById('stats').textContent=items.length+' images | '+new Set(items.map(i=>i.model)).size+' models';
  items.forEach((it,idx)=>{
    const d=document.createElement('div');d.className='gi'+(it._new?' new':'')+(idx===sel?' active':'');
    d.onclick=()=>selImg(idx);
    const im=document.createElement('img');im.src=it._serve;im.loading='lazy';d.appendChild(im);
    const t=document.createElement('div');t.className='tag';t.textContent=(it.model||'?').substring(0,20);d.appendChild(t);
    g.appendChild(d);
  });
}
function selImg(idx){sel=idx;document.querySelectorAll('.gi').forEach((e,i)=>{e.className=e.className.replace(' active','')+(i===idx?' active':'');});renderPanel(items[idx]);document.getElementById('panel-title').textContent='📷 Loaded — Edit & Remix';}
function esc(t){if(!t)return'';const d=document.createElement('div');d.textContent=t;return d.innerHTML;}
renderPanel(BLANK);load();setTimeout(poll,2000);
document.addEventListener('keydown',e=>{if(e.key==='Escape'){sel=-1;renderPanel(BLANK);document.getElementById('panel-title').textContent='⚡ New Generation';}});
</script>
</body></html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        p = parsed.path
        try:
            if p in ('/', '/index.html'):
                html = HTML.replace('__MODELS__', json.dumps(list_models())).replace('__LORAS__', json.dumps(list_loras()))
                self.send_response(200); self.send_header('Content-Type','text/html'); self.end_headers()
                self.wfile.write(html.encode())
            elif p == '/api/gallery':
                self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers()
                self.wfile.write(json.dumps(scan_gallery()).encode())
            elif p == '/api/models':
                self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers()
                self.wfile.write(json.dumps(list_models()).encode())
            elif p == '/api/loras':
                self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers()
                self.wfile.write(json.dumps(list_loras()).encode())
            elif p == '/api/status':
                self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers()
                if os.path.exists(STATUS_FILE):
                    self.wfile.write(open(STATUS_FILE).read().encode())
                else:
                    self.wfile.write(json.dumps({"status":"idle"}).encode())
            elif p == '/image':
                params = parse_qs(parsed.query)
                img_path = params.get('path',[''])[0]
                if img_path and os.path.exists(img_path):
                    data = open(img_path,'rb').read()
                    self.send_response(200)
                    ext = img_path.rsplit('.',1)[-1].lower()
                    self.send_header('Content-Type', 'image/png' if ext=='png' else 'image/jpeg')
                    self.send_header('Content-Length', str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                else:
                    self.send_response(404); self.end_headers()
            else:
                self.send_response(404); self.end_headers()
        except Exception as e:
            print(f"[GET error] {e}")
            self.send_response(500); self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        try:
            if parsed.path == '/api/generate':
                body = self.rfile.read(int(self.headers['Content-Length']))
                params = json.loads(body)
                queue = []
                if os.path.exists(QUEUE_FILE):
                    queue = json.load(open(QUEUE_FILE))
                queue.append(params)
                with open(QUEUE_FILE,'w') as f:
                    json.dump(queue, f)
                self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers()
                self.wfile.write(json.dumps({"ok":True,"position":len(queue)}).encode())
            else:
                self.send_response(404); self.end_headers()
        except Exception as e:
            print(f"[POST error] {e}")
            self.send_response(500); self.end_headers()

    def log_message(self, *a):
        pass


def main():
    os.makedirs(GALLERY_DIR, exist_ok=True)
    # Clear stale queue/status
    if os.path.exists(QUEUE_FILE):
        os.remove(QUEUE_FILE)
    if os.path.exists(STATUS_FILE):
        os.remove(STATUS_FILE)
    threading.Thread(target=generation_worker, daemon=True).start()
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"🎨 Studio v3 at http://localhost:{PORT}", flush=True)
    print(f"   {len(scan_gallery())} images | {len(list_models())} models | {len(list_loras())} LoRAs", flush=True)
    server.serve_forever()

if __name__ == '__main__':
    main()
