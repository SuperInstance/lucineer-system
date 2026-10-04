#!/usr/bin/env python3
# chiaroscuro terminal renderer — exported from the Studio
# deps:  pip install opencv-python      run:  python chiaroscuro-terminal.py      quit: Ctrl-C
# Your look, in a real terminal: truecolor ANSI, half-blocks, edge glyphs.
import sys, math, cv2, numpy as np

P = {
 "engine": "glyph",
 "ramp": "classic",
 "rampCustom": "",
 "density": 100,
 "brightness": 0,
 "contrast": 25,
 "gamma": 100,
 "blackPt": 0,
 "whitePt": 255,
 "invert": false,
 "posterize": 0,
 "toneAmt": 100,
 "edgeAmt": 0,
 "edgeGain": 8,
 "edgeStyle": "sobel",
 "edgeThresh": 4,
 "colMode": "original",
 "hue": 120,
 "sat": 100,
 "temp": 0,
 "shadowCol": "#0a1030",
 "highCol": "#ffd166",
 "mirror": true
}

ESC = chr(27)
def fg(r,g,b): return ESC + '[38;2;' + str(int(r)) + ';' + str(int(g)) + ';' + str(int(b)) + 'm'
RESET = ESC + '[0m'
RAMPS = {
 'classic': ' .:-=+*#%@@',
 'fine': " .'`^\",:;Il!i><~+_-?][}{1)(|\\\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
 'blocks': ' ░▒▓█', 'minimal': ' .:*#', 'stars': '·∴∗✦✱✳❋█',
 'runes': '·ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃ█', 'binary': ' 01', 'code': ' {}[]()<>/\\|=+*', 'waves': '·≈≋▒▓█'}
RAMP = P.get('rampCustom') or RAMPS.get(P['ramp'], RAMPS['classic'])
DIRS = ('─','╱','│','╲')
def hsl(h, l):
    h = (h % 360) / 360.0
    import colorsys
    r, g, b = colorsys.hls_to_rgb(h, max(0.0, min(1.0, l)), 0.85)
    return (r*255, g*255, b*255)
def hex2rgb(hx):
    hx = hx.lstrip('#')
    return tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
def paint(rgb, L):
    r, g, b = rgb
    gray = 0.299*r + 0.587*g + 0.114*b
    s = P.get('sat', 100)/100.0
    r, g, b = gray+(r-gray)*s, gray+(g-gray)*s, gray+(b-gray)*s
    t = P.get('temp', 0) * 0.35
    r, b = min(255, r+t), max(0, b-t)
    m = P['colMode']
    if m == 'phosphor': return hsl(P.get('hue', 120), 0.04 + L*0.85)
    if m == 'duotone':
        a, c = hex2rgb(P.get('shadowCol', '#0a1030')), hex2rgb(P.get('highCol', '#ffd166'))
        return tuple(a[i] + (c[i]-a[i])*max(0.0, min(1.0, L/255.0)) for i in range(3))
    if m == 'heatmap': return hsl((300 - L/255.0*300) % 360, 0.2 + L*0.25)
    if m == 'ink':
        v = 255 - L
        return (v, v, v)
    return (r, g, b)
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('no camera found'); return
    sys.stdout.write(ESC + '[?25l' + ESC + '[2J')
    ok, frame = cap.read()
    fh, fw = frame.shape[:2]
    cols = P['density']
    rows = max(2, int(cols * fh / fw * 0.5))
    try:
        while True:
            ok, frame = cap.read()
            if not ok: break
            if P.get('mirror', True): frame = cv2.flip(frame, 1)
            small = cv2.resize(frame, (cols, rows))
            lum = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY).astype(np.float32)
            con = P['contrast']/25.0
            lum = np.clip((lum - 128.0) * con + 128.0 + P['brightness']*2.2, 0, 255)
            lum = 255.0 * np.power(np.clip(lum/255.0, 0, 1), P['gamma']/100.0)
            lum = np.clip((lum - P['blackPt']) / max(1, P['whitePt'] - P['blackPt']) * 255.0, 0, 255)
            if P.get('invert'): lum = 255.0 - lum
            if P.get('posterize', 0) > 1:
                lv = P['posterize'] - 1
                lum = np.round(lum/255.0*lv)/lv*255.0
            gx = cv2.Sobel(lum, cv2.CV_32F, 1, 0, ksize=3)
            gy = cv2.Sobel(lum, cv2.CV_32F, 0, 1, ksize=3)
            mag = np.sqrt(gx*gx + gy*gy) / 1020.0
            lines = []
            if P['engine'] == 'pixel':
                small2 = cv2.resize(frame, (cols, rows*2))
                for y in range(rows):
                    row = ''
                    for x in range(cols):
                        pt = small2[y*2, x][::-1]; pb = small2[y*2+1, x][::-1]
                        Lt = float(lum[y, x]); Lb = float(lum[min(rows-1, y+1), x])
                        ct, cb2 = paint(pt, Lt), paint(pb, Lb)
                        row += fg(*cb2) + ESC + '[48;2;' + str(int(ct[0])) + ';' + str(int(ct[1])) + ';' + str(int(ct[2])) + 'm' + '▀'
                    lines.append(row + RESET)
            else:
                rl = len(RAMP)
                tm, em = P.get('toneAmt', 100)/100.0, P.get('edgeAmt', 0)/100.0
                thr = P.get('edgeThresh', 4)/100.0
                for y in range(rows):
                    row = ''
                    for x in range(cols):
                        L = float(lum[y, x])
                        rgb = small[y, x][::-1]
                        m2 = float(mag[y, x])
                        ch = None
                        if em > 0 and m2 > thr:
                            ang = math.degrees(math.atan2(float(gy[y, x]), float(gx[y, x]))) % 180
                            fam = 0
                            if 22.5 <= ang < 67.5: fam = 1
                            elif 67.5 <= ang < 112.5: fam = 2
                            elif 112.5 <= ang < 157.5: fam = 3
                            ch = DIRS[fam]
                        if ch is None and tm > 0.05:
                            ch = RAMP[min(rl-1, int((1.0 - L/255.0) * rl))]
                            if ch == ' ': ch = None
                        if ch is None:
                            row += ' '
                        else:
                            cr, cg, cb3 = paint(rgb, L)
                            row += fg(cr, cg, cb3) + ch
                    lines.append(row + RESET)
            sys.stdout.write(ESC + '[H' + chr(10).join(lines))
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        sys.stdout.write(RESET + ESC + '[?25h' + chr(10))
if __name__ == '__main__':
    main()
