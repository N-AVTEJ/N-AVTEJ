"""Generates the SVG bento tiles for the N-AVTEJ profile README.
Run:  python tools/build_bento.py   (writes to ./assets). Edit PROJECTS / HERO text below, re-run."""
import os, textwrap
from xml.sax.saxutils import escape as esc

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

BG, STROKE = "#0e110e", "#232b23"
TXT, MUTED, LIME = "#ECF1E6", "#8A9587", "#C8FF00"
MONO = "'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace"
SANS = "'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif"

CSS = f"""
text{{font-family:{SANS}}} .m{{font-family:{MONO}}}
@keyframes blink{{50%{{opacity:0}}}} @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
@keyframes scan{{from{{transform:translateX(-160px)}}to{{transform:translateX(780px)}}}}
.cur{{animation:blink 1s steps(1) infinite}} .dot{{animation:pulse 1.6s ease-in-out infinite}}
.scan{{animation:scan 5s linear infinite}}
"""

def svg(w, h, body):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<style>{CSS}</style>'
            f'<defs><pattern id="g" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#1d241d"/></pattern>'
            f'<radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{LIME}" stop-opacity=".16"/><stop offset="1" stop-color="{LIME}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="sc" x1="0" x2="1"><stop offset="0" stop-color="{LIME}" stop-opacity="0"/><stop offset=".5" stop-color="{LIME}" stop-opacity=".10"/><stop offset="1" stop-color="{LIME}" stop-opacity="0"/></linearGradient></defs>'
            f'{body}</svg>')

def tile(x, y, w, h, glow=True, grid=False):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{BG}" stroke="{STROKE}"/>'
    if grid: s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="url(#g)"/>'
    if glow: s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="url(#glow)"/>'
    return s

def t(x, y, s, size=14, fill=TXT, weight=400, mono=False, anchor="start", extra=""):
    cls = ' class="m"' if mono else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{cls} {extra}>{esc(s)}</text>'

def chips(x, y, items, maxw, size=11, cw=6.6, pad=16, h=22, gap=8, maxrows=9):
    s, cx, cy, rows = "", x, y, 1
    for it in items:
        w = len(it) * cw + pad
        if cx + w > x + maxw:
            cx, cy, rows = x, cy + h + 10, rows + 1
        s += f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="#171c17" stroke="#2a342a"/>'
        s += t(cx + w / 2, cy + h / 2 + 4, it, size, TXT, 500, True, "middle")
        cx += w + gap
    return s

# ---------- HERO (1000 x 452) ----------
def hero():
    b = tile(0, 0, 600, 270, grid=True)
    b += '<clipPath id="c"><rect x="0" y="0" width="600" height="270" rx="20"/></clipPath>'
    b += '<g clip-path="url(#c)"><rect class="scan" x="0" y="0" width="160" height="270" fill="url(#sc)"/></g>'
    b += t(36, 38, "~/navtej $ ship --solo", 13, MUTED, 400, True)
    b += f'<rect class="cur" x="190" y="27" width="8" height="14" fill="{LIME}"/>'
    b += t(36, 112, "NAVTEJ", 70, TXT, 800, extra='textLength="300" lengthAdjust="spacingAndGlyphs"')
    b += t(36, 184, "MADIPADIGA", 70, "none", 800, extra=f'textLength="510" lengthAdjust="spacingAndGlyphs" stroke="{LIME}" stroke-width="1.6"')
    b += t(36, 216, "Full-stack developer · AI product builder", 17, MUTED, 400, True)
    b += f'<rect x="36" y="230" width="236" height="26" rx="13" fill="{LIME}" fill-opacity=".1" stroke="{LIME}" stroke-opacity=".5"/>'
    b += f'<circle class="dot" cx="54" cy="243" r="4" fill="{LIME}"/>'
    b += t(66, 247, "OPEN TO INTERNSHIPS", 12, LIME, 600, True)

    b += tile(612, 0, 388, 130, glow=False)
    b += t(28 + 612, 34, "BASE", 11, MUTED, 400, True)
    b += t(28 + 612, 80, "Hyderabad, IN", 32, TXT, 700)
    b += t(28 + 612, 108, "Aurora University · B.Tech CS '28", 14, MUTED, 400)

    b += tile(612, 142, 388, 128)
    b += t(28 + 612, 176, "BEST FINISH", 11, MUTED, 400, True)
    b += t(28 + 612, 244, "2nd", 62, LIME, 800)
    b += t(160 + 612, 214, "AVISHKRUTI", 24, TXT, 700)
    b += t(160 + 612, 238, "Build-a-Thon · 50+ teams", 14, MUTED, 400)

    b += tile(0, 282, 300, 170, glow=False)
    b += t(28, 316, "ALSO", 11, MUTED, 400, True)
    for i, (k, v) in enumerate([("Finalist", "IIT Hyderabad"), ("Finalist", "IIT Madras"), ("Top 1000", "Vibe Hacks")]):
        y = 354 + i * 30
        b += f'<text x="28" y="{y}" font-size="16" class="m"><tspan fill="{LIME}" font-weight="600">{k}</tspan><tspan fill="{TXT}" dx="10">{esc(v)}</tspan></text>'

    b += tile(312, 282, 400, 170, glow=False)
    b += t(340, 316, "STACK", 11, MUTED, 400, True)
    b += chips(340, 332, ["Next.js", "React Native", "TypeScript", "Python", "Three.js", "Gemini", "Claude", "Supabase"], 344)

    b += tile(724, 282, 276, 170)
    b += f'<circle class="dot" cx="752" cy="312" r="4" fill="{LIME}"/>'
    b += t(764, 316, "NOW BUILDING", 11, MUTED, 400, True)
    for i, s in enumerate(["PromptForge", "DevLens v2", "VelvetCycle health"]):
        y = 358 + i * 30
        b += f'<text x="752" y="{y}" font-size="16" class="m"><tspan fill="{LIME}">›</tspan><tspan fill="{TXT}" dx="8">{esc(s)}</tspan></text>'
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
    ("docdrift", "05", "DocDrift AI", "REPO ↗",
     "Generates code documentation and detects doc drift when the code changes but the docs don't.",
     "Multi-provider LLMs (Gemini, Anthropic, OpenAI) with a free tier.",
     ["Vercel KV", "Gemini", "Claude", "OpenAI"]),
    ("apex", "06", "Apex Moto Speedo", "REPO ↗",
     "Open-source GPS speedometer PWA for motorcycles. MIT licensed.",
     "Kalman-filtered speed, GPS jump rejection, dropout watchdog, superbike TFT UI.",
     ["React", "Vite", "PWA", "Geolocation"]),
]

def project(num, name, links, desc, standout, stack):
    b = tile(0, 0, 490, 250)
    b += t(28, 36, num, 12, LIME, 600, True)
    b += t(462, 36, links, 12, MUTED, 400, True, "end")
    b += t(28, 80, name, 30, TXT, 800)
    y = 110
    for ln in textwrap.wrap(desc, 56)[:3]:
        b += t(28, y, ln, 14, "#B5BFB1"); y += 20
    y += 6
    for i, ln in enumerate(textwrap.wrap(standout, 58)[:2]):
        pre = "★ " if i == 0 else "   "
        b += t(28, y, pre + ln, 13, LIME, 500); y += 18
    b += chips(28, 212, stack, 434)
    return svg(490, 250, b)

# ---------- CONTACT (1000 x 120) ----------
def contact():
    b = tile(0, 0, 1000, 120, grid=True)
    b += t(32, 62, "Ship fast. Learn faster. Build smarter.", 28, TXT, 800, extra='textLength="560" lengthAdjust="spacingAndGlyphs"')
    b += f'<rect class="cur" x="602" y="40" width="12" height="26" fill="{LIME}"/>'
    b += t(32, 94, "Open to internships · collaborations · hackathon teams", 13, MUTED, 400, True)
    b += t(968, 58, "madipadiganavtej@gmail.com", 17, LIME, 600, True, "end")
    b += t(968, 88, "github.com/N-AVTEJ", 14, MUTED, 400, True, "end")
    return svg(1000, 120, b)

def write(name, s):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f: f.write(s)

write("hero.svg", hero())
for slug, *rest in PROJECTS: write(f"p-{slug}.svg", project(*rest))
write("contact.svg", contact())
print("ok")
