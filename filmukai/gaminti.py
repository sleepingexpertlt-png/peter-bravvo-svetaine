# OG paveikslėliai (1200x630, 9 šventės x 4 kalbos) ir vertikalūs filmukai 1080x1920 (LT + PL)
import sys, os, json, subprocess, glob, re
sys.path.insert(0, '/home/user/peter-bravvo-svetaine/src')
from turinys import S, ISIV, SUKIS, SEGS
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
FD = '/home/user/peter-bravo/fontai/'
UNB, MAN, COR = FD + 'Unbounded.ttf', FD + 'Manrope.ttf', FD + 'Cormorant.ttf'
ORIG = {int(re.findall(r'\d+', os.path.basename(p))[0]): p for p in glob.glob('/home/user/peter-bravo/foto/orig/*.jpg')}
FJ = json.load(open('/home/user/peter-bravvo-svetaine/src/foto/foto.json'))
COL = {"home": ("#16110d", "#f3ece2", "#e3a54a"), "vestuves": ("#1d1812", "#f6f1e8", "#d9b26a"), "imones": ("#0d1624", "#e9eef6", "#7cc8e0"),
       "parodos": ("#0d1624", "#e9eef6", "#7cc8e0"), "jubiliejai": ("#2a0f17", "#f8ebe6", "#f0c987"), "seimos": ("#16231c", "#f2f5f0", "#f0a69c"),
       "jaunimas": ("#0b0b11", "#f4f4f7", "#ff4f9e"), "miestas": ("#090c13", "#f1f3f7", "#ffb547"), "balsas": ("#141414", "#f0eee9", "#ff7a59")}
ROLE = {"lt": "Renginių vedėjas", "pl": "Wodzirej", "ru": "Ведущий", "en": "Event host"}
LINKB = {"lt": "Nuoroda profilyje", "pl": "Link w profilu", "ru": "Ссылка в профиле", "en": "Link in bio"}
LANGS = "LT · PL · RU · EN"
cache = {}
def img(n):
    if n not in cache: cache[n] = ImageOps.exif_transpose(Image.open(ORIG[n])).convert('RGB')
    return cache[n]
def F(path, size): return ImageFont.truetype(path, size)
def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines
def hexrgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
def chip(k, L): return ROLE[L] if k == 'home' else S[k][L]['chip']

def og(k, L):
    bg, ink, acc = COL[k]; W, H = 1200, 630
    base = Image.new('RGB', (W, H), bg)
    ph = ImageOps.fit(img(FJ['hero'][k]), (640, H), centering=(0.5, 0.2))
    mask = Image.linear_gradient('L').rotate(90).resize((640, H))  # kairė juoda -> dešinė balta
    mask = mask.point(lambda v: min(255, int(v * 1.8)))
    base.paste(ph, (W - 640, 0), mask)
    d = ImageDraw.Draw(base)
    d.text((64, 70), chip(k, L).upper(), font=F(MAN, 26), fill=acc)
    d.text((64, 112), "Peter", font=F(UNB, 78), fill=ink); d.text((64, 200), "Bravvo", font=F(UNB, 78), fill=acc)
    y = 318
    for ln in wrap(d, SUKIS[k][L], F(COR, 44), 600)[:3]:
        d.text((64, y), ln, font=F(COR, 44), fill=ink); y += 50
    d.text((64, 548), LANGS + "   ·   peterbravvo.lt", font=F(MAN, 26), fill=ink)
    out = f'/home/user/peter-bravvo-svetaine/src/foto/og/{k}-{L}.jpg'; base.save(out, quality=84)

def render_video(k, L, pics):
    bg, ink, acc = COL[k]; W, H, FPS = 1080, 1920, 30
    scenes = [(pics[0], 5.5), (pics[1], 5.5), (pics[2], 7.0)]; total = sum(d for _, d in scenes)
    hook = ISIV[k][L][1][0] if k in ISIV else chip(k, L)
    texts = [("hook", hook), ("sukis", SUKIS[k][L]), ("end", None)]
    out = f'/home/user/peter-bravo/video/{k}_{L}.mp4'
    pr = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    prepared = []
    for n, d in scenes:
        im = img(n); s = max(W / im.width, H / im.height) * 1.14
        big = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS); prepared.append(big)
    fH, fS, fE, fM = F(COR, 92), F(COR, 86), F(UNB, 110), F(MAN, 50)
    t0 = 0
    for si, ((n, d), big) in enumerate(zip(scenes, prepared)):
        nf = int(d * FPS)
        for f in range(nf):
            p = f / nf
            fmax = min(big.width / W, big.height / H); fz = 1.0 + (min(fmax, 1.13) - 1.0) * p  # lėtas atitolinimas
            ww, hh = int(W * fz), int(H * fz)
            x = (big.width - ww) // 2; y = int((big.height - hh) * 0.3)
            fr = big.crop((x, y, x + ww, y + hh)).resize((W, H), Image.BILINEAR)
            # tamsinimas apačioje ir viršuje tekstui
            ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            r, g, b = hexrgb(bg)
            BH = 1150 if si == 2 else 900
            for yy in range(0, BH, 6): od.rectangle((0, H - BH + yy, W, H - BH + yy + 6), fill=(r, g, b, int((250 if si == 2 else 235) * min(1, yy / BH * 1.3))))
            for yy in range(0, 420, 6): od.rectangle((0, yy, W, yy + 6), fill=(r, g, b, int(170 * (1 - yy / 420))))
            fr = Image.alpha_composite(fr.convert('RGBA'), ov)
            d2 = ImageDraw.Draw(fr)
            # viršus: vardas visada
            d2.text((80, 150), "Peter Bravvo", font=F(UNB, 54), fill=ink)
            d2.text((80, 225), chip(k, L).upper() + "  ·  " + LANGS, font=F(MAN, 30), fill=acc)
            a = min(1, f / (0.6 * FPS)) if si == 0 or True else 1
            kind, txt = texts[si]
            col = lambda c: tuple(int(v * a + bb * (1 - a)) for v, bb in zip(hexrgb(c), (r, g, b)))
            if kind in ("hook", "sukis"):
                font = fH if kind == "hook" else fS
                lines = wrap(d2, txt, font, 840)
                yb = H - 340 - len(lines) * 100
                for ln in lines: d2.text((80, yb), ln, font=font, fill=col(ink if kind == "hook" else acc)); yb += 100
            else:
                d2.text((80, 1100), "Peter", font=fE, fill=col(ink)); d2.text((80, 1230), "Bravvo", font=fE, fill=col(acc))
                d2.text((80, 1390), "+370 607 03318", font=fM, fill=col(ink))
                d2.text((80, 1460), "peterbravvo.lt  ·  " + LINKB[L], font=F(MAN, 36), fill=col(acc))
            # perėjimas: paskutinės 0,5 s -> tamsėja į kitą
            if si < 2 and f > nf - 15:
                fr = Image.blend(fr, Image.new('RGBA', (W, H), (r, g, b, 255)), (f - (nf - 15)) / 15 * 0.8)
            if si > 0 and f < 15:
                fr = Image.blend(fr, Image.new('RGBA', (W, H), (r, g, b, 255)), (1 - f / 15) * 0.8)
            pr.stdin.write(fr.convert('RGB').tobytes())
    pr.stdin.close(); pr.wait(); return out

if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'og':
        for k in ["home"] + SEGS:
            for L in ("lt", "pl", "ru", "en"): og(k, L)
        print('og ok')
    else:
        k, L = sys.argv[2], sys.argv[3]
        PICS = {"home": [19, 32, 39], "vestuves": [33, 26, 29], "imones": [47, 51, 54], "parodos": [48, 50, 53], "jubiliejai": [39, 38, 43],
                "seimos": [18, 19, 32], "jaunimas": [41, 46, 45], "miestas": [44, 38, 40], "balsas": [54, 14, 53]}
        print(render_video(k, L, PICS[k]))
