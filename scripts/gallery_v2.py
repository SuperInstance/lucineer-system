#!/usr/bin/env python3
"""
Image Generation Gallery v2 — split panel design.
Left: gallery grid + new generation panel always visible.
Click image → right panel shows params, editable, generate from there.
"""

import os, sys, json, time, uuid, threading, subprocess, glob
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
        if not os.path.isdir(d): continue
        for ext in ('*.png', '*.jpg', '*.jpeg'):
            for img_path in sorted(glob.glob(os.path.join(d, ext)), reverse=True):
                if img_path in seen: continue
                seen.add(img_path)
                meta = None
                meta_path = img_path.rsplit('.', 1)[0] + '.json'
                if os.path.exists(meta_path):
                    try:
                        with open(meta_path) as f: meta = json.load(f)
                    except: pass
                if not meta:
                    fname = os.path.basename(img_path)
                    meta = {"prompt": "(no metadata)", "model": "unknown", "steps": "?", "guidance": "?", "seed": "?", "filename": fname}
                meta['_path'] = img_path
                meta['_serve'] = f"/image?path={img_path}"
                items.append(meta)
    return items

def generation_worker():
    while True:
        try:
            if os.path.exists(QUEUE_FILE):
                with open(QUEUE_FILE) as f: queue = json.load(f)
                if queue:
                    job = queue.pop(0)
                    with open(QUEUE_FILE, 'w') as f: json.dump(queue, f)
                    with open(STATUS_FILE, 'w') as f:
                        json.dump({"status": "generating", "job": job, "started": time.time()}, f)
                    cmd = ["python3", GEN_SCRIPT, "-p", job["prompt"]]
                    if job.get("negative_prompt"): cmd += ["-n", job["negative_prompt"]]
                    cmd += ["-m", str(job.get("model") or "dreamshaper_8")]
                    cmd += ["-s", str(job.get("steps") or 25)]
                    cmd += ["-g", str(job.get("guidance") or 7.5)]
                    if job.get("seed") is not None: cmd += ["--seed", str(job["seed"])]
                    cmd += ["-W", str(job.get("width") or 512), "-H", str(job.get("height") or 512)]
                    output_path = os.path.expanduser(f"~/.openclaw/workspace/output/images/gallery/{int(time.time())}-{uuid.uuid4().hex[:6]}.png")
                    cmd += ["-o", output_path]
                    for lora in job.get("loras", []):
                        cmd += ["--lora", lora["name"], "--lora-weight", str(lora.get("weight", 0.7))]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    with open(STATUS_FILE, 'w') as f:
                        if result.returncode == 0:
                            json.dump({"status": "done", "job": job, "finished": time.time(), "output": output_path}, f)
                        else:
                            json.dump({"status": "error", "job": job, "error": result.stderr[-500:]}, f)
                    time.sleep(1); continue
        except Exception as e:
            print(f"Queue error: {e}", file=sys.stderr)
        time.sleep(2)

HTML = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>🎨 Generation Studio</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#0a0a0f; color:#e0e0e0; font-family:'Segoe UI',system-ui,sans-serif; height:100vh; overflow:hidden; display:flex; flex-direction:column; }

/* Header */
.header { background:#0d0d14; padding:10px 20px; border-bottom:1px solid #1e1e2e; display:flex; align-items:center; gap:16px; flex-shrink:0; }
.header h1 { font-size:16px; color:#7c8cf0; white-space:nowrap; }
.header .stats { font-size:11px; color:#555; }

/* Main layout */
.main { display:flex; flex:1; overflow:hidden; }

/* LEFT: Gallery */
.gallery-panel { flex:1; overflow-y:auto; padding:16px; }
.gallery-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(160px,1fr)); gap:10px; }
.gallery-item { background:#12121a; border-radius:6px; overflow:hidden; cursor:pointer; transition:all 0.12s; border:2px solid transparent; position:relative; }
.gallery-item:hover { transform:scale(1.04); border-color:#7c8cf0; z-index:5; }
.gallery-item.active { border-color:#4a9; }
.gallery-item img { width:100%; aspect-ratio:1; object-fit:cover; display:block; }
.gallery-item .tag { position:absolute; bottom:0; left:0; right:0; background:rgba(0,0,0,0.7); font-size:9px; padding:2px 4px; color:#9a9adc; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.gallery-item.new-badge::after { content:'NEW'; position:absolute; top:4px; right:4px; background:#4a9; color:#000; font-size:9px; font-weight:bold; padding:1px 4px; border-radius:3px; }

/* RIGHT: Control Panel */
.control-panel { width:380px; flex-shrink:0; background:#0d0d14; border-left:1px solid #1e1e2e; overflow-y:auto; padding:16px; }
.control-panel h2 { font-size:14px; color:#7c8cf0; margin-bottom:12px; }
.control-panel .source { font-size:10px; color:#555; margin-bottom:14px; word-break:break-all; }

/* Form */
.field { margin-bottom:10px; }
.field label { display:block; font-size:10px; color:#666; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:3px; }
.field textarea, .field input, .field select { width:100%; background:#07070d; border:1px solid #1e1e2e; color:#d0d0d0; padding:7px 9px; border-radius:5px; font-size:12px; font-family:inherit; }
.field textarea { min-height:54px; resize:vertical; }
.field input:focus, .field textarea:focus, .field select:focus { outline:none; border-color:#7c8cf0; }
.field-row { display:flex; gap:8px; }
.field-row .field { flex:1; }

/* LoRAs */
.lora-row { display:flex; gap:6px; align-items:center; margin-bottom:5px; }
.lora-row select { flex:1; font-size:11px; }
.lora-row input { width:55px; font-size:11px; }
.lora-row .remove-lora { background:#2a1a1a; border:none; color:#e55; width:24px; height:24px; border-radius:4px; cursor:pointer; font-size:11px; }
.add-lora-btn { background:#15152a; border:1px dashed #2e2e4e; color:#777; padding:4px 10px; border-radius:4px; cursor:pointer; font-size:11px; }
.add-lora-btn:hover { border-color:#7c8cf0; color:#7c8cf0; }

/* Buttons */
.btn { background:#7c8cf0; color:#fff; border:none; padding:9px 18px; border-radius:5px; cursor:pointer; font-size:13px; font-weight:600; transition:background 0.12s; }
.btn:hover { background:#6a7ae0; }
.btn-ghost { background:#1a1a2a; color:#888; }
.btn-ghost:hover { background:#2a2a3a; color:#ccc; }
.btn-row { display:flex; gap:8px; margin-top:14px; }

/* Status */
.status { position:fixed; bottom:14px; right:14px; background:#0d0d14; border:1px solid #2e2e4e; padding:10px 16px; border-radius:6px; z-index:500; display:none; font-size:12px; }
.status.active { display:block; }
.status.gen { border-color:#7c8cf0; }
.status.done { border-color:#4a9; }
.status.err { border-color:#e55; }

/* Loading overlay for selected image */
.img-loading { opacity:0.4; }

/* Hint text */
.hint { font-size:10px; color:#444; margin-top:6px; font-style:italic; }
</style>
</head>
<body>

<div class="header">
  <h1>🎨 Generation Studio</h1>
  <div class="stats" id="stats">Loading...</div>
</div>

<div class="main">
  <!-- LEFT: GALLERY -->
  <div class="gallery-panel">
    <div class="gallery-grid" id="grid"></div>
  </div>

  <!-- RIGHT: CONTROL PANEL -->
  <div class="control-panel" id="panel">
    <h2>⚡ New Generation</h2>
    <div id="panel-content"></div>
  </div>
</div>

<div class="status" id="status"></div>

<script>
const MODELS = __MODELS__;
const LORAS = __LORAS__;
let items = [];
let selectedIdx = -1;

// Default blank form
const BLANK = {
  prompt: '', negative_prompt: '',
  model: MODELS[0] || 'dreamshaper_8',
  steps: 25, guidance: 7.5, seed: null,
  width: 512, height: 768, loras: [], _blank: true
};

function renderPanel(item) {
  const isBlank = item._blank;
  const div = document.getElementById('panel-content');
  
  let loraHtml = '';
  if (item.loras) {
    item.loras.forEach((l, i) => {
      loraHtml += loraRowHtml(l.name, l.weight, i);
    });
  }
  
  div.innerHTML = `
    ${!isBlank ? '<div class="source">From: ' + escapeHtml(item._path||'') + '</div>' : ''}
    
    <div class="field">
      <label>Prompt</label>
      <textarea id="p-prompt" placeholder="Describe what you want...">${escapeHtml(item.prompt||'')}</textarea>
    </div>
    
    <div class="field">
      <label>Negative Prompt</label>
      <textarea id="p-negative" placeholder="What to avoid...">${escapeHtml(item.negative_prompt||'')}</textarea>
    </div>
    
    <div class="field">
      <label>Model</label>
      <select id="p-model">
        ${MODELS.map(m => '<option value="'+m+'"'+(m===item.model?' selected':'')+'>'+m+'</option>').join('')}
      </select>
    </div>
    
    <div class="field-row">
      <div class="field"><label>Steps</label><input type="number" id="p-steps" value="${item.steps||25}"></div>
      <div class="field"><label>CFG</label><input type="number" step="0.5" id="p-guidance" value="${item.guidance||7.5}"></div>
    </div>
    
    <div class="field-row">
      <div class="field"><label>Width</label><input type="number" id="p-width" value="${item.width||512}" step="64"></div>
      <div class="field"><label>Height</label><input type="number" id="p-height" value="${item.height||768}" step="64"></div>
      <div class="field"><label>Seed</label><input type="number" id="p-seed" value="${item.seed&&!isBlank?item.seed:''}" placeholder="random"></div>
    </div>
    
    <div class="field">
      <label>LoRAs <span style="color:#444">(detail enhancers, style modifiers)</span></label>
      <div id="lora-list">${loraHtml}</div>
      <button class="add-lora-btn" onclick="addLora()">+ Add LoRA</button>
    </div>
    
    <div class="btn-row">
      <button class="btn" onclick="doGenerate(false)">⚡ Generate</button>
      <button class="btn btn-ghost" onclick="doGenerate(true)">🎲 Variation</button>
    </div>
    
    ${!isBlank ? '<div class="hint">Edit any field and Generate to remix. Variation = same settings, new random seed.</div>' : '<div class="hint">Write a prompt and hit Generate. Try different models to see how they interpret it.</div>'}
  `;
}

function loraRowHtml(name, weight, idx) {
  const opts = LORAS.map(l => '<option value="'+l+'"'+(l===name?' selected':'')+'>'+l+'</option>').join('');
  return '<div class="lora-row"><select>'+opts+'</select><input type="number" step="0.1" value="'+(weight||0.7)+'"><button class="remove-lora" onclick="this.parentElement.remove()">✕</button></div>';
}

function addLora() {
  const list = document.getElementById('lora-list');
  const div = document.createElement('div');
  div.className = 'lora-row';
  div.innerHTML = '<select><option value="">-- LoRA --</option>' + LORAS.map(l => '<option value="'+l+'">'+l+'</option>').join('') + '</select><input type="number" step="0.1" value="0.7"><button class="remove-lora" onclick="this.parentElement.remove()">✕</button>';
  list.appendChild(div);
}

function collectParams() {
  const loras = [];
  document.querySelectorAll('#lora-list .lora-row').forEach(row => {
    const sel = row.querySelector('select');
    const inp = row.querySelector('input');
    if (sel && sel.value && inp) loras.push({name: sel.value, weight: parseFloat(inp.value)});
  });
  const seedVal = document.getElementById('p-seed').value;
  return {
    prompt: document.getElementById('p-prompt').value,
    negative_prompt: document.getElementById('p-negative').value,
    model: document.getElementById('p-model').value,
    steps: parseInt(document.getElementById('p-steps').value),
    guidance: parseFloat(document.getElementById('p-guidance').value),
    seed: seedVal ? parseInt(seedVal) : null,
    width: parseInt(document.getElementById('p-width').value),
    height: parseInt(document.getElementById('p-height').value),
    loras: loras
  };
}

function doGenerate(variation) {
  let params = collectParams();
  if (variation) params.seed = null;
  if (!params.prompt.trim()) { alert('Write a prompt first!'); return; }
  
  showStatus('Queuing generation...', 'gen');
  fetch('/api/generate', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(params)})
    .then(r => r.json())
    .then(data => {
      showStatus('Generation queued! ~60s...', 'gen');
      setTimeout(pollStatus, 3000);
    });
}

async function pollStatus() {
  try {
    const r = await fetch('/api/status');
    const d = await r.json();
    if (d.status === 'generating') {
      const elapsed = Math.round(Date.now()/1000 - d.started);
      showStatus('⚙️ Generating... ' + elapsed + 's', 'gen');
      setTimeout(pollStatus, 4000);
    } else if (d.status === 'done') {
      showStatus('✅ Done! Reloading...', 'done');
      await loadGallery(true);
      setTimeout(hideStatus, 2000);
    } else if (d.status === 'error') {
      showStatus('❌ ' + (d.error||'').substring(0,120), 'err');
      setTimeout(hideStatus, 8000);
    }
  } catch { setTimeout(pollStatus, 5000); }
}

function showStatus(msg, type) {
  const s = document.getElementById('status');
  s.textContent = msg;
  s.className = 'status active ' + type;
}
function hideStatus() { document.getElementById('status').className = 'status'; }

async function loadGallery(markNew) {
  const r = await fetch('/api/gallery');
  const newItems = await r.json();
  
  // Mark new images
  if (markNew && items.length) {
    const oldPaths = new Set(items.map(i => i._path));
    newItems.forEach(i => { if (!oldPaths.has(i._path)) i._new = true; });
  }
  
  items = newItems;
  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  
  document.getElementById('stats').textContent = items.length + ' images | ' + new Set(items.map(i=>i.model)).size + ' models';
  
  items.forEach((item, idx) => {
    const div = document.createElement('div');
    div.className = 'gallery-item' + (item._new ? ' new-badge' : '');
    if (idx === selectedIdx) div.className += ' active';
    div.onclick = () => selectImage(idx);
    
    const img = document.createElement('img');
    img.src = item._serve;
    img.loading = 'lazy';
    div.appendChild(img);
    
    const tag = document.createElement('div');
    tag.className = 'tag';
    tag.textContent = (item.model||'?').substring(0, 22);
    div.appendChild(tag);
    
    grid.appendChild(div);
  });
}

function selectImage(idx) {
  selectedIdx = idx;
  document.querySelectorAll('.gallery-item').forEach((el, i) => {
    el.className = el.className.replace(' active', '');
    if (i === idx) el.className += ' active';
  });
  renderPanel(items[idx]);
}

function escapeHtml(t) { if(!t) return ''; const d=document.createElement('div'); d.textContent=t; return d.innerHTML; }

// Init
renderPanel(BLANK);
loadGallery();
setTimeout(pollStatus, 2000);

// Keyboard: Escape deselects
document.addEventListener('keydown', e => { if(e.key==='Escape'){ selectedIdx=-1; renderPanel(BLANK); } });
</script>
</body>
</html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        p = parsed.path
        if p == '/' or p == '/index.html':
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
            self.wfile.write(open(STATUS_FILE).read().encode() if os.path.exists(STATUS_FILE) else json.dumps({"status":"idle"}).encode())
        elif p == '/image':
            params = parse_qs(parsed.query)
            img_path = params.get('path',[''])[0]
            if img_path and os.path.exists(img_path):
                with open(img_path,'rb') as f:
                    self.send_response(200)
                    ext = img_path.rsplit('.',1)[-1].lower()
                    self.send_header('Content-Type', 'image/png' if ext=='png' else 'image/jpeg')
                    self.end_headers(); self.wfile.write(f.read())
            else: self.send_response(404); self.end_headers()
        else: self.send_response(404); self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/generate':
            body = self.rfile.read(int(self.headers['Content-Length']))
            params = json.loads(body)
            queue = json.load(open(QUEUE_FILE)) if os.path.exists(QUEUE_FILE) else []
            queue.append(params)
            with open(QUEUE_FILE,'w') as f: json.dump(queue, f)
            self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"position":len(queue)}).encode())
        else: self.send_response(404); self.end_headers()

    def log_message(self, *a): pass

def main():
    os.makedirs(GALLERY_DIR, exist_ok=True)
    threading.Thread(target=generation_worker, daemon=True).start()
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"🎨 Studio running at http://localhost:{PORT}")
    print(f"   {len(scan_gallery())} images | {len(list_models())} models | {len(list_loras())} LoRAs")
    server.serve_forever()

if __name__ == '__main__': main()
