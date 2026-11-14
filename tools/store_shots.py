"""Make captioned store screenshots of Neon Focus with Playwright.

Usage: python3 tools/store_shots.py www store/screenshots
Serves the www folder locally, plays the real game in a phone-sized browser,
then frames each capture with a caption at the exact store sizes:
  apple-6.9/  1320x2868 (iPhone 6.9" display, required by App Store Connect)
  play/       1080x1920 (Google Play phone screenshots)
"""
import base64, functools, http.server, os, sys, threading, time
from playwright.sync_api import sync_playwright

WWW, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])

SHOTS = [
    ('1-play', 'One rule. Sixty seconds.', 'Catch only what the rule says'),
    ('2-flip', 'The rule keeps flipping', 'Switch fast. Stay sharp.'),
    ('3-handsoff', 'HANDS OFF', 'Hold back. Dodge everything.'),
    ('4-results', 'See your focus skills', 'Accuracy, switching and self-control'),
    ('5-stats', 'Track your progress', 'Every run, charted'),
    ('6-menu', 'No ads. No subscription.', 'Daily challenge, Zen mode and more'),
]
LAUNCH = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
FONTS = dict(fo=base64.b64encode(open(f'{WWW}/fonts/orbitron-latin-900-normal.woff2','rb').read()).decode(),
             fi=base64.b64encode(open(f'{WWW}/fonts/inter-latin-600-normal.woff2','rb').read()).decode())
SIZES = {'apple-6.9': (1320, 2868), 'play': (1080, 1920)}


def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    h = functools.partial(Q, directory=WWW)
    s = http.server.ThreadingHTTPServer(('127.0.0.1', 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]


def drag(page, xs):
    for x in xs:
        page.mouse.move(x, 700)
        page.wait_for_timeout(90)


def capture(pw, port):
    raw = {}
    b = pw.chromium.launch(**LAUNCH)
    ctx = b.new_context(viewport={'width': 440, 'height': 880}, device_scale_factor=3,
                        is_mobile=True, has_touch=True)
    page = ctx.new_page()
    # seed a returning player so menu/stats look lived-in
    page.add_init_script("""
      try{if(!localStorage.getItem('neonfocus.v2')){
        const hist=[];let s=820;for(let i=0;i<14;i++){s+=Math.round(40+Math.random()*110);const d=new Date(Date.now()-(14-i)*864e5).toISOString().slice(0,10);hist.push({d,s,a:Math.min(97,74+i*1.6|0),sc:80})}
        localStorage.setItem('neonfocus.v2',JSON.stringify({best:s,runs:31,xp:5400,peak:6,streak:6,last:new Date().toISOString().slice(0,10),tutDone:true,hist,set:{sound:false,music:false,haptics:false}}))}}catch(e){}
    """)
    page.goto(f'http://127.0.0.1:{port}/index.html')
    page.wait_for_timeout(1500)
    raw['6-menu'] = page.screenshot()

    page.evaluate("__NF.start('classic')")
    page.mouse.move(220, 700)
    page.wait_for_timeout(3800)          # countdown
    drag(page, [120, 200, 300, 340, 260, 180, 140, 220, 300, 260, 200, 160])
    page.evaluate("Object.assign(__NF.G,{score:640,combo:9,mult:2,hits:21,misses:2})")
    page.wait_for_timeout(120)
    raw['1-play'] = page.screenshot()

    page.evaluate("__NF.G.nextRule=__NF.G.elapsed+0.02;__NF.G.warned=true")
    page.wait_for_timeout(300)
    raw['2-flip'] = page.screenshot()
    page.wait_for_timeout(1400)

    page.evaluate("__NF.G.nextStop=__NF.G.elapsed+0.05")
    page.wait_for_timeout(500)
    drag(page, [200, 210])
    raw['3-handsoff'] = page.screenshot()

    drag(page, [150, 250, 330, 230, 130] * 3)
    page.evaluate("Object.assign(__NF.G,{score:1840,hits:52,misses:5,topCombo:23,stopsDone:2,stopsClean:2,swHit:9,swTot:10,flips:4,topDiff:5.8,time:0})")
    page.evaluate("__NF.end(false)")
    page.wait_for_timeout(1800)
    raw['4-results'] = page.screenshot()

    page.evaluate("document.getElementById('home').click()")
    page.wait_for_timeout(500)
    page.evaluate("document.getElementById('statsBtn').click()")
    page.wait_for_timeout(900)
    raw['5-stats'] = page.screenshot()
    b.close()
    return raw, b


FRAME = """<!doctype html><html><head><style>
@font-face{font-family:O;font-weight:900;src:url(data:font/woff2;base64,%(fo)s)}
@font-face{font-family:I;font-weight:600;src:url(data:font/woff2;base64,%(fi)s)}
html,body{margin:0;width:%(w)dpx;height:%(h)dpx;overflow:hidden;background:#07020f}
body{background:radial-gradient(ellipse at 50%% 8%%,rgba(255,61,242,.35),transparent 55%%),radial-gradient(ellipse at 50%% 100%%,rgba(34,230,255,.22),transparent 55%%),#07020f;
display:flex;flex-direction:column;align-items:center;font-family:I,sans-serif;color:#fff}
h1{font-family:O,sans-serif;font-weight:900;font-size:%(f1)dpx;line-height:1.08;margin:%(top)dpx %(pad)dpx 0;text-align:center;
background:linear-gradient(90deg,#22e6ff,#ff3df2);-webkit-background-clip:text;color:transparent}
p{font-size:%(f2)dpx;margin:%(gap)dpx %(pad)dpx 0;color:#d9d0ec;text-align:center}
.ph{margin-top:%(gap2)dpx;width:%(pw)dpx;height:%(ph)dpx;border-radius:%(rad)dpx;overflow:hidden;
box-shadow:0 0 0 %(bd)dpx rgba(255,255,255,.14),0 0 80px rgba(255,61,242,.35)}
.ph img{width:100%%;height:100%%;object-fit:cover;object-position:top;display:block}
</style></head><body><h1>%(t)s</h1><p>%(s)s</p><div class="ph"><img src="data:image/png;base64,%(img)s"></div></body></html>"""


def frame(pw, port, raw):
    b = pw.chromium.launch(**LAUNCH)
    for key, (w, h) in SIZES.items():
        os.makedirs(f'{OUT}/{key}', exist_ok=True)
        page = b.new_page(viewport={'width': w, 'height': h})
        u = w / 1320
        pw_ = int(w * 0.80)
        ph_ = int(pw_ * 2.0)
        top = int(h * 0.055)
        f1 = int(92 * u)
        f2 = int(46 * u)
        avail = h - (top + f1 * 1.1 + 24 * u + f2 * 1.3 + 50 * u)
        if ph_ > avail:  # shorter Play canvas: shrink phone to fit
            ph_ = int(avail)
            pw_ = int(ph_ / 2.0)
        for name, t, s in SHOTS:
            html = FRAME % dict(**FONTS, port=port, w=w, h=h, f1=f1, f2=f2, top=top, pad=int(60 * u),
                                gap=int(24 * u), gap2=int(50 * u), pw=pw_, ph=ph_, rad=int(70 * u),
                                bd=int(6 * u), t=t, s=s, img=base64.b64encode(raw[name]).decode())
            page.set_content(html)
            page.evaluate("Promise.all([document.fonts.load('900 40px O'),document.fonts.load('600 20px I')]).then(()=>document.fonts.ready)")
            page.wait_for_timeout(300)
            page.screenshot(path=f'{OUT}/{key}/{name}.png')
        page.close()
    b.close()


FEATURE = """<!doctype html><html><head><style>
@font-face{font-family:O;font-weight:900;src:url(data:font/woff2;base64,%(fo)s)}
@font-face{font-family:I;font-weight:600;src:url(data:font/woff2;base64,%(fi)s)}
html,body{margin:0;width:1024px;height:500px;overflow:hidden}
body{background:radial-gradient(ellipse at 30%% 40%%,rgba(255,61,242,.35),transparent 60%%),radial-gradient(ellipse at 85%% 90%%,rgba(34,230,255,.25),transparent 55%%),linear-gradient(#07020f,#2a0838);
display:flex;align-items:center;gap:44px;padding:0 70px;box-sizing:border-box;color:#fff;font-family:I,sans-serif}
svg{flex:none;filter:drop-shadow(0 0 18px #ff3df2)}
h1{font-family:O;font-weight:900;font-size:84px;line-height:.95;margin:0;background:linear-gradient(90deg,#22e6ff,#ff3df2);-webkit-background-clip:text;color:transparent}
p{font-size:30px;margin:18px 0 0;color:#e6dcf5}
.s{position:absolute;filter:drop-shadow(0 0 10px currentColor)}
</style></head><body>
<svg width="230" height="230" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="none" stroke="#ff3df2" stroke-width="7"/><polygon points="50,28 72,63 28,63" fill="#22e6ff"/></svg>
<div><h1>NEON<br>FOCUS</h1><p>60-second focus runs.<br>The rule keeps flipping.</p></div>
<svg class="s" style="left:930px;top:60px;color:#ffd23d" width="40" height="40"><rect width="40" height="40" fill="#ffd23d"/></svg>
<svg class="s" style="left:860px;top:400px;color:#22e6ff" width="44" height="44"><circle cx="22" cy="22" r="22" fill="#22e6ff"/></svg>
<svg class="s" style="left:40px;top:30px;color:#ff3df2" width="36" height="36"><polygon points="18,0 36,36 0,36" fill="#ff3df2"/></svg>
</body></html>"""


def feature(pw, port):
    b = pw.chromium.launch(**LAUNCH)
    page = b.new_page(viewport={'width': 1024, 'height': 500})
    page.set_content(FEATURE % dict(**FONTS, port=port))
    page.evaluate("Promise.all([document.fonts.load('900 84px O'),document.fonts.load('600 30px I')]).then(()=>document.fonts.ready)")
    page.wait_for_timeout(300)
    page.screenshot(path=f'{OUT}/feature-graphic-1024x500.png')
    b.close()


if __name__ == '__main__':
    port = serve()
    with sync_playwright() as pw:
        raw, _ = capture(pw, port)
        frame(pw, port, raw)
        feature(pw, port)
    print('screenshots written to', OUT)
