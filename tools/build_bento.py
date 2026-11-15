"""Generates the SVG bento tiles (electric-blue storm theme) for the N-AVTEJ profile README.
Run:  python tools/build_bento.py   (writes to ./assets). Edit PROJECTS / HERO text below, re-run."""
import os, textwrap
from xml.sax.saxutils import escape as esc

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

BG, STROKE = "#080d1a", "#17264c"
TXT, MUTED, BODY = "#EAF4FF", "#7F93B5", "#B5C6E3"
ACC, CORE = "#3FA9FF", "#D6EEFF"          # electric blue, bolt core
CHIP, CHIPS = "#0f1830", "#24396e"
MONO = "'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace"
SANS = "'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif"

CSS = f"""
text{{font-family:{SANS}}} .m{{font-family:{MONO}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
@keyframes strike{{0%,86%,100%{{opacity:.14}}87%{{opacity:1}}88%{{opacity:.25}}89%{{opacity:1}}90%{{opacity:.5}}91%{{opacity:1}}95%{{opacity:.14}}}}
@keyframes flash{{0%,86%,100%{{opacity:0}}87%{{opacity:.20}}88%{{opacity:.04}}89%{{opacity:.26}}90%{{opacity:.08}}91%{{opacity:.18}}95%{{opacity:0}}}}
@keyframes drift{{from{{transform:translateX(-40px)}}to{{transform:translateX(40px)}}}}
.cur{{animation:blink 1s steps(1) infinite}} .dot{{animation:pulse 1.6s ease-in-out infinite}}
.bolt{{opacity:.14;animation:strike 6s linear infinite}} .flash{{opacity:0;animation:flash 6s linear infinite}}
.cloud{{animation:drift 9s ease-in-out infinite alternate}}
"""

DEFS = f"""<defs>
<pattern id="g" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#14214a"/></pattern>
<radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{ACC}" stop-opacity=".22"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></radialGradient>
<radialGradient id="cloud" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#2a4fb0" stop-opacity=".55"/><stop offset="1" stop-color="#2a4fb0" stop-opacity="0"/></radialGradient>
<filter id="bg" x="-80%" y="-30%" width="260%" height="160%"><feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"""

def svg(w, h, body):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<style>{CSS}</style>{DEFS}{body}</svg>')

BOLT = "M22,0 L8,40 L23,43 L5,84 L17,87 L0,130"
FORK = "M23,43 L38,66 L29,68 L42,92"

def bolt(x, y, s=1.0, delay=0.0, flip=False):
    """Lightning bolt: blue glow + white-hot core, flickers like a strike."""
    sx = -s if flip else s
    return (f'<g transform="translate({x},{y}) scale({sx},{s})" class="bolt" style="animation-delay:{delay}s" filter="url(#bg)">'
            f'<path d="{BOLT}" fill="none" stroke="{ACC}" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{FORK}" fill="none" stroke="{ACC}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{BOLT}" fill="none" stroke="{CORE}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{FORK}" fill="none" stroke="{CORE}" stroke-width="1" stroke-linejoin="round" stroke-linecap="round"/></g>')

def tile(x, y, w, h, glow=True, grid=False, clipid=None, flash_delay=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{BG}" stroke="{STROKE}"/>'
    if grid: s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="url(#g)"/>'
    if glow: s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="url(#glow)"/>'
    if flash_delay is not None:
        s += (f'<rect class="flash" style="animation-delay:{flash_delay}s" x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{ACC}"/>')
    return s

def t(x, y, s, size=14, fill=TXT, weight=400, mono=False, anchor="start", extra=""):
    cls = ' class="m"' if mono else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{cls} {extra}>{esc(s)}</text>'

def chips(x, y, items, maxw, size=11, cw=6.6, pad=16, h=22, gap=8):
    s, cx, cy = "", x, y
    for it in items:
        w = len(it) * cw + pad
        if cx + w > x + maxw:
            cx, cy = x, cy + h + 10
        s += f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{CHIP}" stroke="{CHIPS}"/>'
        s += t(cx + w / 2, cy + h / 2 + 4, it, size, TXT, 500, True, "middle")
        cx += w + gap
    return s

# ---------- HERO (1000 x 452) ----------
def hero():
    b = tile(0, 0, 600, 270, grid=True, flash_delay=0)
    b += '<clipPath id="c"><rect x="0" y="0" width="600" height="270" rx="20"/></clipPath>'
    b += f'<g clip-path="url(#c)"><ellipse class="cloud" cx="430" cy="0" rx="260" ry="70" fill="url(#cloud)"/><ellipse class="cloud" cx="560" cy="10" rx="160" ry="50" fill="url(#cloud)" style="animation-delay:-4s"/></g>'
    b += bolt(520, 0, 1.55, 0)
    b += bolt(448, 0, 0.9, 0.35, flip=True)
    b += t(36, 38, "~/navtej $ ship --solo", 13, MUTED, 400, True)
    b += f'<rect class="cur" x="190" y="27" width="8" height="14" fill="{ACC}"/>'
    b += t(36, 112, "NAVTEJ", 70, TXT, 800, extra='textLength="300" lengthAdjust="spacingAndGlyphs"')
    b += t(36, 184, "MADIPADIGA", 70, "none", 800, extra=f'textLength="510" lengthAdjust="spacingAndGlyphs" stroke="{ACC}" stroke-width="1.6"')
    b += t(36, 216, "Full-stack developer · AI product builder", 17, MUTED, 400, True)
    b += f'<rect x="36" y="230" width="236" height="26" rx="13" fill="{ACC}" fill-opacity=".12" stroke="{ACC}" stroke-opacity=".6"/>'
    b += f'<circle class="dot" cx="54" cy="243" r="4" fill="{ACC}"/>'
    b += t(66, 247, "OPEN TO INTERNSHIPS", 12, ACC, 600, True)

    b += tile(612, 0, 388, 130, glow=False)
    b += t(640, 34, "BASE", 11, MUTED, 400, True)
    b += t(640, 80, "Hyderabad, IN", 32, TXT, 700)
    b += t(640, 108, "Aurora University · B.Tech CS '28", 14, MUTED, 400)

    b += tile(612, 142, 388, 128, flash_delay=0.35)
    b += bolt(958, 148, 0.62, 0.35)
    b += t(640, 176, "BEST FINISH", 11, MUTED, 400, True)
    b += t(640, 244, "2nd", 62, ACC, 800)
    b += t(772, 214, "AVISHKRUTI", 24, TXT, 700)
    b += t(772, 238, "Build-a-Thon · 50+ teams", 14, MUTED, 400)

    b += tile(0, 282, 300, 170, glow=False)
    b += t(28, 316, "ALSO", 11, MUTED, 400, True)
    for i, (k, v) in enumerate([("Finalist", "IIT Hyderabad"), ("Finalist", "IIT Madras"), ("Top 1000", "Vibe Hacks")]):
        y = 354 + i * 30
        b += f'<text x="28" y="{y}" font-size="16" class="m"><tspan fill="{ACC}" font-weight="600">{k}</tspan><tspan fill="{TXT}" dx="10">{esc(v)}</tspan></text>'

    b += tile(312, 282, 400, 170, glow=False)
    b += t(340, 316, "STACK", 11, MUTED, 400, True)
    b += chips(340, 332, ["Next.js", "React Native", "TypeScript", "Python", "Three.js", "Gemini", "Claude", "Supabase"], 344)

    b += tile(724, 282, 276, 170, flash_delay=0.7)
    b += bolt(962, 292, 0.55, 0.7)
    b += f'<circle class="dot" cx="752" cy="312" r="4" fill="{ACC}"/>'
    b += t(764, 316, "NOW BUILDING", 11, MUTED, 400, True)
    for i, s in enumerate(["PromptForge", "DevLens v2", "VelvetCycle health"]):
        y = 358 + i * 30
        b += f'<text x="752" y="{y}" font-size="16" class="m"><tspan fill="{ACC}">›</tspan><tspan fill="{TXT}" dx="8">{esc(s)}</tspan></text>'
    return svg(1000, 452, b)

# ---------- PROJECT TILES (490 x 250) ----------
PROJECTS = [
    ("devlens", "01", "DevLens AI", "REPO ↗",
     "Career intelligence for developers. Scans a GitHub profile, scores it on 6 dimensions, builds a month-by-month roadmap.",
     "Honest Roast Mode: brutal, specific feedback on your repos.",
     ["Next.js 15", "React 19", "Gemini", "Three.js", "Recharts"]),
    ("buildmate", "02", "BuildMate", "LIVE ↗  ·  REPO ↗",
     "Marketplace for student academic projects. Quotation, locked scope, payment, then delivery unlock.",
     "Server-authoritative: payments, deadlines and delivery gating are never trusted from the client.",
     ["Razorpay", "Google OAuth", "RBAC", "Vercel"]),
    ("batsense", "03", "BATsense", "REPO ↗",
     "Cricket game where your phone is the bat. Gyroscope and accelerometer decide swing speed and shot direction.",
     "Deterministic swing-to-shot mapping, zero RNG. Your real swing is the game.",
     ["JavaScript", "Gyro", "Three.js (WIP)", "Web Audio"]),
    ("velvetcycle", "04", "VelvetCycle", "REPO ↗",
     "Privacy-first period tracker built for India. Open source, no subscription.",
     "Calculator-disguise lock, PIN + biometric, Hindi and Telugu, quick-commerce reminders.",
     ["React Native", "Expo", "SecureStore"]),
    ("autodoc", "05", "AutoDoc AI", "REPO ↗",
     "Generates code documentation and detects doc drift when the code changes but the docs don't.",
     "Multi-provider LLMs (Gemini, Anthropic, OpenAI) with a free tier.",
     ["Vercel KV", "Gemini", "Claude", "OpenAI"]),
    ("apex", "06", "Apex Moto Speedo", "REPO ↗",
     "Open-source GPS speedometer PWA for motorcycles. MIT licensed.",
     "Kalman-filtered speed, GPS jump rejection, dropout watchdog, superbike TFT UI.",
     ["React", "Vite", "PWA", "Geolocation"]),
]

def project(i, num, name, links, desc, standout, stack):
    d = round(i * 0.9, 2)
    b = tile(0, 0, 490, 250, flash_delay=d)
    b += f'<clipPath id="pc"><rect width="490" height="250" rx="20"/></clipPath><g clip-path="url(#pc)"><ellipse class="cloud" cx="440" cy="0" rx="150" ry="46" fill="url(#cloud)"/></g>'
    b += bolt(452, 0, 0.8, d)
    b += t(28, 36, num, 12, ACC, 600, True)
    b += t(420, 36, links, 12, MUTED, 400, True, "end")
    b += t(28, 80, name, 30, TXT, 800)
    y = 110
    for ln in textwrap.wrap(desc, 56)[:3]:
        b += t(28, y, ln, 14, BODY); y += 20
    y += 6
    for k, ln in enumerate(textwrap.wrap(standout, 56)[:2]):
        if k == 0:
            b += f'<path transform="translate(28,{y-11})" d="M6,0 L0,7 L4,7 L2,13 L9,5 L5,5 Z" fill="{ACC}"/>'
        b += t(46, y, ln, 13, ACC, 500); y += 18
    b += chips(28, 212, stack, 434)
    return svg(490, 250, b)

# ---------- CONTACT (1000 x 120) ----------
def contact():
    b = tile(0, 0, 1000, 120, grid=True, flash_delay=0.5)
    b += bolt(640, 0, 0.9, 0.5)
    b += bolt(520, 0, 0.6, 1.1, flip=True)
    b += t(32, 62, "Ship fast. Learn faster. Build smarter.", 28, TXT, 800, extra='textLength="560" lengthAdjust="spacingAndGlyphs"')
    b += f'<rect class="cur" x="602" y="40" width="12" height="26" fill="{ACC}"/>'
    b += t(32, 94, "Open to internships · collaborations · hackathon teams", 13, MUTED, 400, True)
    b += t(968, 58, "madipadiganavtej@gmail.com", 17, ACC, 600, True, "end")
    b += t(968, 88, "github.com/N-AVTEJ", 14, MUTED, 400, True, "end")
    return svg(1000, 120, b)

def write(name, s):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f: f.write(s)

write("hero.svg", hero())
for i, (slug, *rest) in enumerate(PROJECTS): write(f"p-{slug}.svg", project(i, *rest))
write("contact.svg", contact())
print("ok")
