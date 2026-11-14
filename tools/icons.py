"""Generate every Neon Focus icon, splash and store graphic from code.

Usage: python3 tools/icons.py [--android DIR] [--ios DIR] [--store DIR]
  --android  path to android/app/src/main/res   (mipmaps + splash)
  --ios      path to ios/App/App/Assets.xcassets (AppIcon + Splash)
  --store    output folder for store graphics (icon-512, icon-1024, feature graphic)
"""
import argparse, json, os
from PIL import Image, ImageDraw, ImageFilter

BG = (7, 2, 15)
PINK = (255, 61, 242, 255)
CYAN = (34, 230, 255, 255)
GOLD = (255, 210, 61, 255)


def gradient(w, h):
    im = Image.new('RGB', (w, h), BG)
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=(int(7 + 35 * t), int(2 + 6 * t), int(15 + 41 * t)))
    return im


def glow_layer(size, draw_fn):
    g = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(g), size)
    return g


def emblem(d, S):
    c = S // 2
    r = int(S * 0.30)
    d.ellipse([c - r, c - r, c + r, c + r], outline=PINK, width=max(2, S // 18))
    tr = int(r * 0.55)
    d.polygon([(c, c - tr), (c + tr, c + int(tr * .7)), (c - tr, c + int(tr * .7))], fill=CYAN)


def icon(size, bg=True):
    """Square app icon. bg=False gives a transparent emblem (adaptive foreground)."""
    S = size * 4
    base = gradient(S, S).convert('RGBA') if bg else Image.new('RGBA', (S, S), (0, 0, 0, 0))
    g = glow_layer(S, emblem)
    base = Image.alpha_composite(base, g.filter(ImageFilter.GaussianBlur(S // 30)))
    base = Image.alpha_composite(base, g)
    return base.resize((size, size), Image.LANCZOS)


def splash(w, h):
    im = gradient(w, h).convert('RGBA')
    s = int(min(w, h) * 0.42)
    em = icon(s, bg=False)
    im.alpha_composite(em, ((w - s) // 2, (h - s) // 2))
    return im.convert('RGB')


def feature_graphic(path):
    W, H = 1024, 500
    im = gradient(W, H).convert('RGBA')
    d = ImageDraw.Draw(im)
    # falling shapes
    shapes = [(120, 90, 'c', PINK), (240, 330, 't', CYAN), (860, 120, 's', GOLD),
              (930, 360, 'c', CYAN), (70, 390, 's', PINK), (780, 420, 't', PINK)]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for x, y, k, col in shapes:
        r = 26
        if k == 'c':
            ld.ellipse([x - r, y - r, x + r, y + r], fill=col)
        elif k == 's':
            ld.rectangle([x - r, y - r, x + r, y + r], fill=col)
        else:
            ld.polygon([(x, y - r), (x + r, y + r), (x - r, y + r)], fill=col)
    im = Image.alpha_composite(im, lay.filter(ImageFilter.GaussianBlur(10)))
    im = Image.alpha_composite(im, lay)
    em = icon(300, bg=False)
    im.alpha_composite(em, ((W - 300) // 2, (H - 300) // 2))
    im.convert('RGB').save(path)


def android(res):
    src = icon(1024)
    fg = icon(1024, bg=False)
    for k, s in {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}.items():
        dd = f'{res}/mipmap-{k}'
        os.makedirs(dd, exist_ok=True)
        for n in ['ic_launcher.png', 'ic_launcher_round.png']:
            src.resize((s, s), Image.LANCZOS).save(f'{dd}/{n}')
        F = int(s * 2.25)
        cv = Image.new('RGBA', (F, F), (0, 0, 0, 0))
        i = int(F * 0.62)
        cv.paste(fg.resize((i, i), Image.LANCZOS), ((F - i) // 2,) * 2)
        cv.save(f'{dd}/ic_launcher_foreground.png')
    # replace every Capacitor splash image (drawable*/splash.png)
    for root, _, files in os.walk(res):
        for f in files:
            if f == 'splash.png':
                p = os.path.join(root, f)
                w, h = Image.open(p).size
                splash(w, h).save(p)
    bgx = f'{res}/values/ic_launcher_background.xml'
    if os.path.exists(bgx):
        open(bgx, 'w').write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
                             '    <color name="ic_launcher_background">#07020F</color>\n</resources>\n')


def ios(assets):
    ai = f'{assets}/AppIcon.appiconset'
    os.makedirs(ai, exist_ok=True)
    for f in os.listdir(ai):
        if f.endswith('.png'):
            os.remove(os.path.join(ai, f))
    icon(1024).convert('RGB').save(f'{ai}/AppIcon-512@2x.png')  # no alpha for Apple
    json.dump({'images': [{'filename': 'AppIcon-512@2x.png', 'idiom': 'universal',
                           'platform': 'ios', 'size': '1024x1024'}],
               'info': {'author': 'xcode', 'version': 1}}, open(f'{ai}/Contents.json', 'w'), indent=2)
    sp = f'{assets}/Splash.imageset'
    if os.path.isdir(sp):
        for f in os.listdir(sp):
            if f.endswith('.png'):
                p = os.path.join(sp, f)
                w, h = Image.open(p).size
                splash(w, h).save(p)


def store(out):
    os.makedirs(out, exist_ok=True)
    icon(512).convert('RGB').save(f'{out}/icon-512.png')
    icon(1024).convert('RGB').save(f'{out}/icon-1024.png')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--android')
    ap.add_argument('--ios')
    ap.add_argument('--store')
    a = ap.parse_args()
    if a.android:
        android(a.android)
    if a.ios:
        ios(a.ios)
    if a.store:
        store(a.store)
