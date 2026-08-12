#!/usr/bin/env python3
"""
Image Generation Gallery — local web app.
Browse generated images, inspect params, tweak and regenerate.
"""

import os
import sys
import json
import time
import uuid
import threading
import subprocess
import glob
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

GALLERY_DIR = os.path.expanduser("~/.openclaw/workspace/output/images/gallery")
# Also scan the older tap-scenes and hermes dirs
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
    """Scan all image dirs, return list of {image, metadata} dicts."""
    items = []
    seen = set()
    
    all_dirs = [GALLERY_DIR] + EXTRA_DIRS
    for d in all_dirs:
        if not os.path.isdir(d):
            continue
        for ext in ('*.png', '*.jpg', '*.jpeg'):
            for img_path in sorted(glob.glob(os.path.join(d, ext)), reverse=True):
                if img_path in seen:
                    continue
                seen.add(img_path)
                
                # Look for metadata sidecar
                meta = None
                for meta_ext in ('.json',):
                    meta_path = img_path.rsplit('.', 1)[0] + meta_ext
                    if os.path.exists(meta_path):
                        try:
                            with open(meta_path) as f:
                                meta = json.load(f)
                        except:
                            pass
                        break
                
                # If no sidecar, try to infer from filename
                if not meta:
                    fname = os.path.basename(img_path)
                    meta = {
                        "prompt": "(no metadata — pre-gallery image)",
                        "model": "unknown",
                        "steps": "?",
                        "guidance": "?",
                        "seed": "?",
                        "filename": fname,
                    }
                
                meta['_path'] = img_path
                meta['_dirname'] = os.path.basename(d)
                # Relative path for serving
                meta['_serve'] = f"/image?path={img_path}"
                items.append(meta)
    
    return items

def generation_worker():
    """Background thread that processes the generation queue."""
    while True:
        try:
            if os.path.exists(QUEUE_FILE):
                with open(QUEUE_FILE) as f:
                    queue = json.load(f)
                
                if queue:
                    job = queue.pop(0)
                    with open(QUEUE_FILE, 'w') as f:
                        json.dump(queue, f)
                    
                    # Update status
                    with open(STATUS_FILE, 'w') as f:
                        json.dump({"status": "generating", "job": job, "started": time.time()}, f)
                    
                    # Build command
                    cmd = ["python3", GEN_SCRIPT, "-p", job["prompt"]]
                    if job.get("negative_prompt"):
                        cmd += ["-n", job["negative_prompt"]]
                    cmd += ["-m", job.get("model", "dreamshaper_8")]
                    cmd += ["-s", str(job.get("steps", 25))]
                    cmd += ["-g", str(job.get("guidance", 7.5))]
                    if job.get("seed") is not None:
                        cmd += ["--seed", str(job["seed"])]
                    cmd += ["-W", str(job.get("width", 512))]
                    cmd += ["-H", str(job.get("height", 512))]
                    
                    output_name = f"gallery/{int(time.time())}-{uuid.uuid4().hex[:6]}.png"
                    output_path = os.path.expanduser(f"~/.openclaw/workspace/output/images/{output_name}")
                    cmd += ["-o", output_path]
                    
                    # Add LoRAs
                    for lora in job.get("loras", []):
                        cmd += ["--lora", lora["name"]]
                        cmd += ["--lora-weight", str(lora.get("weight", 0.7))]
                    
                    # Run generation
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    
                    # Update status
                    with open(STATUS_FILE, 'w') as f:
                        if result.returncode == 0:
                            json.dump({"status": "done", "job": job, "finished": time.time(), 
                                       "output": output_path}, f)
                        else:
                            json.dump({"status": "error", "job": job, "error": result.stderr[-500:]}, f)
                    
                    time.sleep(1)
                    continue
        except Exception as e:
            print(f"Queue error: {e}", file=sys.stderr)
        
        time.sleep(2)

HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>🎨 Image Generation Gallery</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0a0a0f; color: #e0e0e0; font-family: 'Segoe UI', system-ui, sans-serif; min-height: 100vh; }

/* Header */
.header { background: #12121a; padding: 16px 24px; border-bottom: 1px solid #2a2a3a; position: sticky; top: 0; z-index: 100; }
.header h1 { font-size: 18px; color: #7c8cf0; }
.header .stats { font-size: 12px; color: #666; margin-top: 4px; }

/* Gallery Grid */
.gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; padding: 20px; }
.gallery-item { background: #12121a; border-radius: 8px; overflow: hidden; cursor: pointer; transition: transform 0.15s, border 0.15s; border: 2px solid transparent; }
.gallery-item:hover { transform: scale(1.03); border-color: #7c8cf0; }
.gallery-item img { width: 100%; aspect-ratio: 1; object-fit: cover; display: block; }
.gallery-item .label { padding: 6px 8px; font-size: 11px; color: #888; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.gallery-item .model-tag { display: inline-block; background: #1e1e30; color: #9a9adc; padding: 2px 6px; border-radius: 3px; font-size: 10px; }

/* Modal */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 200; display: none; justify-content: center; align-items: flex-start; padding: 20px; overflow-y: auto; }
.modal-overlay.active { display: flex; }
.modal { background: #12121a; border-radius: 12px; max-width: 1100px; width: 100%; display: flex; gap: 0; overflow: hidden; }
.modal-image { flex: 0 0 45%; background: #000; display: flex; align-items: center; justify-content: center; }
.modal-image img { max-width: 100%; max-height: 80vh; object-fit: contain; }
.modal-params { flex: 1; padding: 24px; overflow-y: auto; max-height: 85vh; }
.modal-params h2 { font-size: 16px; color: #7c8cf0; margin-bottom: 16px; }

/* Form fields */
.field-group { margin-bottom: 14px; }
.field-group label { display: block; font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.field-group textarea, .field-group input, .field-group select { width: 100%; background: #0a0a12; border: 1px solid #2a2a3a; color: #e0e0e0; padding: 8px 10px; border-radius: 6px; font-size: 13px; font-family: inherit; }
.field-group textarea { min-height: 60px; resize: vertical; }
.field-group input:focus, .field-group textarea:focus, .field-group select:focus { outline: none; border-color: #7c8cf0; }
.field-row { display: flex; gap: 10px; }
.field-row .field-group { flex: 1; }

/* LoRA entries */
.lora-entry { display: flex; gap: 8px; align-items: center; margin-bottom: 6px; }
.lora-entry select { flex: 1; }
.lora-entry input { width: 70px; }
.lora-entry button { background: #3a1a1a; border: none; color: #e55; padding: 6px 10px; border-radius: 4px; cursor: pointer; font-size: 12px; }

/* Buttons */
.btn { background: #7c8cf0; color: #fff; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 600; transition: background 0.15s; }
.btn:hover { background: #6a7ae0; }
.btn-secondary { background: #2a2a3a; }
.btn-secondary:hover { background: #3a3a4a; }
.btn-row { display: flex; gap: 10px; margin-top: 20px; }

/* Status banner */
.status-banner { position: fixed; bottom: 20px; right: 20px; background: #12121a; border: 1px solid #2a2a3a; padding: 12px 20px; border-radius: 8px; z-index: 300; display: none; }
.status-banner.active { display: block; }
.status-banner.generating { border-color: #7c8cf0; }
.status-banner.done { border-color: #4a4; }
.status-banner.error { border-color: #e55; }

/* Close button */
.close-btn { position: absolute; top: 12px; right: 12px; background: #2a2a3a; border: none; color: #aaa; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-size: 18px; }

/* Param display (read-only view) */
.param-display { background: #0a0a12; border: 1px solid #1e1e30; border-radius: 6px; padding: 10px 12px; margin-bottom: 8px; }
.param-display .key { font-size: 10px; color: #666; text-transform: uppercase; }
.param-display .val { font-size: 13px; color: #ccc; margin-top: 2px; word-break: break-word; }
.prompt-display { font-size: 13px; color: #a0d0a0; background: #0a1208; border: 1px solid #1a2a1a; }
</style>
</head>
<body>

<div class="header">
  <h1>🎨 Image Generation Gallery</h1>
  <div class="stats" id="stats">Loading...</div>
</div>

<div class="gallery" id="gallery"></div>

<div class="modal-overlay" id="modal">
  <div class="modal" style="position: relative;">
    <button class="close-btn" onclick="closeModal()">&times;</button>
    <div class="modal-image">
      <img id="modal-img" src="">
    </div>
    <div class="modal-params" id="modal-params"></div>
  </div>
</div>

<div class="status-banner" id="status-banner"></div>

<script>
const MODELS = __MODELS__;
const LORAS = __LORAS__;

let allItems = [];

async function loadGallery() {
  const resp = await fetch('/api/gallery');
  allItems = await resp.json();
  
  const gallery = document.getElementById('gallery');
  gallery.innerHTML = '';
  
  document.getElementById('stats').textContent = 
    allItems.length + ' images | ' + 
    new Set(allItems.map(i => i.model)).size + ' models | ' +
    new Set(allItems.map(i => i._dirname)).size + ' folders';
  
  allItems.forEach((item, idx) => {
    const div = document.createElement('div');
    div.className = 'gallery-item';
    div.onclick = () => openModal(idx);
    
    const img = document.createElement('img');
    img.src = item._serve;
    img.loading = 'lazy';
    
    const label = document.createElement('div');
    label.className = 'label';
    const modelName = item.model || 'unknown';
    label.innerHTML = '<span class="model-tag">' + modelName.substring(0, 20) + '</span>';
    
    div.appendChild(img);
    div.appendChild(label);
    gallery.appendChild(div);
  });
}

function openModal(idx) {
  const item = allItems[idx];
  document.getElementById('modal-img').src = item._serve;
  
  const paramsDiv = document.getElementById('modal-params');
  paramsDiv.innerHTML = `
    <h2>Generation Parameters</h2>
    <p style="color:#666;font-size:11px;margin-bottom:16px;">Source: ${item._dirname}/${item.filename || ''}</p>
    
    <div class="field-group">
      <label>Prompt</label>
      <textarea id="f-prompt">${escapeHtml(item.prompt || '')}</textarea>
    </div>
    
    <div class="field-group">
      <label>Negative Prompt</label>
      <textarea id="f-negative">${escapeHtml(item.negative_prompt || '')}</textarea>
    </div>
    
    <div class="field-row">
      <div class="field-group">
        <label>Model</label>
        <select id="f-model">${MODELS.map(m => '<option value="'+m+'"'+(m===item.model?' selected':'')+'>'+m+'</option>').join('')}</select>
      </div>
      <div class="field-group">
        <label>Seed</label>
        <input type="number" id="f-seed" value="${item.seed !== undefined && item.seed !== '?' ? item.seed : ''}" placeholder="random">
      </div>
    </div>
    
    <div class="field-row">
      <div class="field-group">
        <label>Steps</label>
        <input type="number" id="f-steps" value="${item.steps || 25}">
      </div>
      <div class="field-group">
        <label>CFG Scale</label>
        <input type="number" step="0.5" id="f-guidance" value="${item.guidance || 7.5}">
      </div>
    </div>
    
    <div class="field-row">
      <div class="field-group">
        <label>Width</label>
        <input type="number" id="f-width" value="${item.width || 512}">
      </div>
      <div class="field-group">
        <label>Height</label>
        <input type="number" id="f-height" value="${item.height || 512}">
      </div>
    </div>
    
    <div class="field-group">
      <label>LoRAs</label>
      <div id="lora-list">${buildLoraEntries(item.loras)}</div>
      <button class="btn btn-secondary" style="margin-top:6px;font-size:12px;padding:4px 12px;" onclick="addLora()">+ Add LoRA</button>
    </div>
    
    <div class="btn-row">
      <button class="btn" onclick="generateFromForm()">⚡ Generate</button>
      <button class="btn btn-secondary" onclick="generateVariation()">🎲 Variation (new seed)</button>
    </div>
  `;
  
  document.getElementById('modal').classList.add('active');
}

function buildLoraEntries(loras) {
  if (!loras || !loras.length) return '';
  return loras.map((l, i) => `
    <div class="lora-entry">
      <select id="lora-${i}-name">
        ${LORAS.map(lo => '<option value="'+lo+'"'+(lo===l.name?' selected':'')+'>'+lo+'</option>').join('')}
        ${!LORAS.includes(l.name) ? '<option value="'+l.name+'" selected>'+l.name+' (not found)</option>' : ''}
      </select>
      <input type="number" step="0.1" id="lora-${i}-weight" value="${l.weight || 0.7}">
      <button onclick="this.parentElement.remove()">✕</button>
    </div>
  `).join('');
}

function addLora() {
  const list = document.getElementById('lora-list');
  const idx = list.children.length;
  const div = document.createElement('div');
  div.className = 'lora-entry';
  div.innerHTML = `
    <select id="lora-${idx}-name-new">
      <option value="">-- select LoRA --</option>
      ${LORAS.map(lo => '<option value="'+lo+'">'+lo+'</option>').join('')}
    </select>
    <input type="number" step="0.1" value="0.7">
    <button onclick="this.parentElement.remove()">✕</button>
  `;
  list.appendChild(div);
}

function collectParams() {
  const loras = [];
  document.querySelectorAll('#lora-list .lora-entry').forEach(entry => {
    const select = entry.querySelector('select');
    const input = entry.querySelector('input[type="number"]');
    if (select && select.value && input) {
      loras.push({name: select.value, weight: parseFloat(input.value)});
    }
  });
  
  const seedVal = document.getElementById('f-seed').value;
  
  return {
    prompt: document.getElementById('f-prompt').value,
    negative_prompt: document.getElementById('f-negative').value,
    model: document.getElementById('f-model').value,
    steps: parseInt(document.getElementById('f-steps').value),
    guidance: parseFloat(document.getElementById('f-guidance').value),
    seed: seedVal ? parseInt(seedVal) : null,
    width: parseInt(document.getElementById('f-width').value),
    height: parseInt(document.getElementById('f-height').value),
    loras: loras,
  };
}

async function generateFromForm() {
  const params = collectParams();
  await submitGeneration(params);
}

async function generateVariation() {
  const params = collectParams();
  params.seed = null; // random
  await submitGeneration(params);
}

async function submitGeneration(params) {
  showStatus('Queuing generation...', 'generating');
  
  const resp = await fetch('/api/generate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(params),
  });
  
  if (resp.ok) {
    showStatus('Generation queued! Check back in ~60s...', 'generating');
    closeModal();
    setTimeout(pollStatus, 3000);
  } else {
    showStatus('Failed to queue!', 'error');
  }
}

async function pollStatus() {
  try {
    const resp = await fetch('/api/status');
    const data = await resp.json();
    
    if (data.status === 'generating') {
      showStatus('Generating... (' + Math.round((Date.now()/1000 - data.started)) + 's)', 'generating');
      setTimeout(pollStatus, 5000);
    } else if (data.status === 'done') {
      showStatus('✅ Done! Reloading gallery...', 'done');
      setTimeout(() => { loadGallery(); hideStatus(); }, 2000);
    } else if (data.status === 'error') {
      showStatus('❌ Error: ' + (data.error || '').substring(0, 100), 'error');
      setTimeout(hideStatus, 8000);
    }
  } catch {
    setTimeout(pollStatus, 5000);
  }
}

function showStatus(msg, type) {
  const banner = document.getElementById('status-banner');
  banner.textContent = msg;
  banner.className = 'status-banner active ' + type;
}

function hideStatus() {
  document.getElementById('status-banner').className = 'status-banner';
}

function closeModal() {
  document.getElementById('modal').classList.remove('active');
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
});

// Initial load
loadGallery();
// Poll for status on load
setTimeout(pollStatus, 2000);
</script>

</body>
</html>'''


class GalleryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/' or path == '/index.html':
            html = HTML_TEMPLATE.replace('__MODELS__', json.dumps(list_models()))
            html = html.replace('__LORAS__', json.dumps(list_loras()))
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        
        elif path == '/api/gallery':
            items = scan_gallery()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(items).encode())
        
        elif path == '/api/models':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(list_models()).encode())
        
        elif path == '/api/loras':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(list_loras()).encode())
        
        elif path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            if os.path.exists(STATUS_FILE):
                with open(STATUS_FILE) as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(json.dumps({"status": "idle"}).encode())
        
        elif path == '/image':
            params = parse_qs(parsed.query)
            img_path = params.get('path', [''])[0]
            if img_path and os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    self.send_response(200)
                    ext = img_path.rsplit('.', 1)[-1].lower()
                    ct = 'image/png' if ext == 'png' else 'image/jpeg'
                    self.send_header('Content-Type', ct)
                    self.end_headers()
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/generate':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            params = json.loads(body)
            
            # Add to queue
            queue = []
            if os.path.exists(QUEUE_FILE):
                with open(QUEUE_FILE) as f:
                    queue = json.load(f)
            
            queue.append(params)
            
            with open(QUEUE_FILE, 'w') as f:
                json.dump(queue, f)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "position": len(queue)}).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[Gallery] {args[0]}")


def main():
    os.makedirs(GALLERY_DIR, exist_ok=True)
    
    # Start generation worker thread
    worker = threading.Thread(target=generation_worker, daemon=True)
    worker.start()
    
    server = HTTPServer(('0.0.0.0', PORT), GalleryHandler)
    print(f"🎨 Gallery running at http://localhost:{PORT}")
    print(f"   Images: {len(scan_gallery())} loaded")
    print(f"   Models: {len(list_models())} available")
    print(f"   LoRAs: {len(list_loras())} available")
    server.serve_forever()

if __name__ == '__main__':
    main()
