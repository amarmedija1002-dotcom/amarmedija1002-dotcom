#!/usr/bin/env python3
"""Erzeugt die animierten Matrix-SVGs fuer das GitHub-Profil.

Aufruf:  python3 tools/gen_matrix.py
Ergebnis: assets/matrix-header.svg, assets/matrix-footer.svg, assets/terminal.svg

GitHub fuehrt in READMEs kein JavaScript aus. Die Animation laeuft deshalb
rein ueber CSS-Keyframes innerhalb der SVG-Dateien.
"""
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
GLYPHS = "0123456789" * 3 + "01010101" + "<>/{}[]#$%&=+*"
GREEN = "#00ff66"
HEAD = "#eafff0"


def rain(width, height, seed, cell=20, step=18, min_len=8, max_len=22, streams=2):
    """Fallende Zeichenspalten. Jede Spalte ist ein <text> mit eigener Dauer."""
    rnd = random.Random(seed)
    cols = width // cell
    out = []
    for c in range(cols):
        x = c * cell + cell // 2
        for _ in range(streams):
            n = rnd.randint(min_len, max_len)
            dur = rnd.uniform(4.5, 11.0)
            delay = -rnd.uniform(0, dur)
            length = n * step
            spans = []
            for i in range(n):
                ch = rnd.choice(GLYPHS)
                ch = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}.get(ch, ch)
                if i == n - 1:
                    spans.append(f'<tspan x="{x}" dy="{step}" fill="{HEAD}">{ch}</tspan>')
                else:
                    op = round(0.08 + 0.92 * (i / (n - 1)) ** 1.6, 2)
                    spans.append(f'<tspan x="{x}" dy="{step}" fill-opacity="{op}">{ch}</tspan>')
            out.append(
                f'<text class="r" y="0" style="--a:{-length - step}px;--b:{height + step}px;'
                f'animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s">{"".join(spans)}</text>'
            )
    return "\n".join(out)


def frame(width, height, body, extra_css="", extra_defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="KRYPT0R">
<defs>
<clipPath id="card"><rect width="{width}" height="{height}" rx="16"/></clipPath>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".35"/></pattern>
<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
{extra_defs}
</defs>
<style>
.r{{font:16px {FONT};fill:{GREEN};text-anchor:middle;animation:fall linear infinite;transform:translateY(var(--a))}}
@keyframes fall{{from{{transform:translateY(var(--a))}}to{{transform:translateY(var(--b))}}}}
{extra_css}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.r{{transform:translateY(40px)}}}}
</style>
<g clip-path="url(#card)">
<rect width="{width}" height="{height}" fill="#020a05"/>
{body}
<rect width="{width}" height="{height}" fill="url(#scan)"/>
</g>
<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="15" fill="none" stroke="{GREEN}" stroke-opacity=".35" stroke-width="2"/>
</svg>
'''


def header():
    w, h = 1200, 440
    cx, cy = w // 2, 218
    title = "KRYPT0R"
    tattr = f'x="{cx}" y="{cy}" text-anchor="middle" textLength="640" lengthAdjust="spacingAndGlyphs"'
    sub = "&gt; IT-Systemtechniker · Full-Stack · Self-Hosting · Lokale KI"
    body = f'''{rain(w, h, seed=1337)}
<rect width="{w}" height="{h}" fill="url(#vig)"/>
<g class="t">
<text class="g1" {tattr}>{title}</text>
<text class="g2" {tattr}>{title}</text>
<text class="main" {tattr} filter="url(#glow)">{title}</text>
</g>
<rect class="line" x="{cx - 330}" y="{cy + 34}" width="660" height="2" fill="{GREEN}"/>
<g clip-path="url(#type)"><text class="sub" x="{cx}" y="{cy + 80}" text-anchor="middle" textLength="640" lengthAdjust="spacingAndGlyphs">{sub}</text></g>
<rect class="cur" x="{cx + 328}" y="{cy + 60}" width="13" height="25" fill="{GREEN}"/>
<text class="tag" x="28" y="34">[ SYSTEM ONLINE ]</text>
<text class="tag" x="{w - 28}" y="34" text-anchor="end">ACCESS GRANTED</text>
<text class="tag" x="28" y="{h - 20}">0x4B 0x52 0x59 0x50 0x54 0x30 0x52</text>
<text class="tag" x="{w - 28}" y="{h - 20}" text-anchor="end">NODE: CH · STATUS: BUILDING</text>'''
    css = f'''.t text{{font:800 124px {FONT}}}
.main{{fill:{GREEN}}}
.g1{{fill:#ff2a6d;opacity:0;animation:g1 5.5s steps(1) infinite}}
.g2{{fill:#05d9e8;opacity:0;animation:g2 5.5s steps(1) infinite}}
.t{{animation:shake 5.5s steps(1) infinite}}
@keyframes g1{{0%,91%,100%{{opacity:0;transform:none}}92%{{opacity:.85;transform:translate(-9px,2px)}}94%{{opacity:.85;transform:translate(7px,-3px)}}96%{{opacity:.6;transform:translate(-4px,0)}}98%{{opacity:0}}}}
@keyframes g2{{0%,91%,100%{{opacity:0;transform:none}}92%{{opacity:.85;transform:translate(9px,-2px)}}94%{{opacity:.85;transform:translate(-7px,3px)}}96%{{opacity:.6;transform:translate(4px,0)}}98%{{opacity:0}}}}
@keyframes shake{{0%,91%,98%,100%{{transform:none}}93%{{transform:translate(3px,0) skewX(-4deg)}}95%{{transform:translate(-3px,0) skewX(3deg)}}}}
.line{{opacity:.55;transform-origin:{cx}px 0;animation:grow 1.4s ease-out both}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
.sub{{font:500 22px {FONT};fill:#b6ffcf}}
#type rect{{animation:type 3.2s steps(46) .9s both}}
@keyframes type{{from{{width:0}}to{{width:680px}}}}
.cur{{opacity:0;animation:blink 1s steps(1) 4.1s infinite}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.tag{{font:13px {FONT};fill:{GREEN};opacity:.9;letter-spacing:2px;stroke:#020a05;stroke-width:7px;paint-order:stroke}}'''
    defs = f'''<radialGradient id="vig" cx="50%" cy="52%" r="62%"><stop offset="0" stop-color="#020a05" stop-opacity=".96"/><stop offset=".42" stop-color="#020a05" stop-opacity=".86"/><stop offset="1" stop-color="#020a05" stop-opacity=".1"/></radialGradient>
<clipPath id="type"><rect x="{cx - 340}" y="{cy + 50}" width="680" height="44"/></clipPath>'''
    return frame(w, h, body, css, defs)


def footer():
    w, h = 1200, 110
    body = f'''{rain(w, h, seed=4242, min_len=4, max_len=9, streams=2)}
<rect width="{w}" height="{h}" fill="#020a05" opacity=".55"/>
<text class="f" x="{w // 2}" y="{h // 2 + 8}" text-anchor="middle" filter="url(#glow)">// END OF TRANSMISSION</text>'''
    css = f'.f{{font:700 24px {FONT};fill:{GREEN};letter-spacing:6px;animation:pulse 3s ease-in-out infinite}}@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.45}}}}'
    return frame(w, h, body, css)


def terminal():
    """Terminal-Karte, deren Zeilen nacheinander getippt werden."""
    w, lh, top = 860, 30, 78
    lines = [
        ("p", "kryptor@matrix:~$ whoami"),
        ("o", "Amar · IT-Systemtechniker in Ausbildung · Schweiz"),
        ("p", "kryptor@matrix:~$ cat mission.txt"),
        ("o", "Ich baue echte Produkte, kein Tutorial-Code."),
        ("p", "kryptor@matrix:~$ ls ~/projects"),
        ("o", "secret-calc/  homelab/  local-ai/"),
        ("p", "kryptor@matrix:~$ uptime"),
        ("o", "always shipping"),
    ]
    h = top + len(lines) * lh + 22
    clips, texts, css, t = [], [], [], 0.4
    for i, (kind, txt) in enumerate(lines):
        y = top + i * lh
        esc = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        clips.append(f'<clipPath id="l{i}"><rect class="c{i}" x="28" y="{y - 22}" width="{w - 56}" height="{lh}"/></clipPath>')
        texts.append(f'<g clip-path="url(#l{i})"><text class="{kind}" x="30" y="{y}" xml:space="preserve">{esc}</text></g>')
        if kind == "p":
            dur = 0.035 * len(txt)
            css.append(f'.c{i}{{animation:w {dur:.2f}s steps({len(txt)}) {t:.2f}s both}}')
            t += dur + 0.25
        else:
            css.append(f'.c{i}{{animation:w .01s linear {t:.2f}s both}}')
            t += 0.45
    cy = top + len(lines) * lh
    body = f'''<rect width="{w}" height="40" fill="#06180d"/>
<circle cx="26" cy="20" r="6.5" fill="#ff5f57"/><circle cx="48" cy="20" r="6.5" fill="#febc2e"/><circle cx="70" cy="20" r="6.5" fill="#28c840"/>
<text class="bar" x="{w // 2}" y="25" text-anchor="middle">kryptor@matrix: ~</text>
{"".join(texts)}
<g class="last"><text class="p" x="30" y="{cy}">kryptor@matrix:~$</text><rect class="cur" x="222" y="{cy - 18}" width="11" height="22" fill="{GREEN}"/></g>'''
    style = f'''.p,.o,.bar{{font:17px {FONT}}}
.p{{fill:{GREEN}}}.o{{fill:#c9ffdb}}.bar{{fill:{GREEN};opacity:.6;font-size:13px}}
@keyframes w{{from{{width:0}}to{{width:{w - 56}px}}}}
{"".join(css)}
.last{{opacity:0;animation:show .01s linear {t:.2f}s both}}
@keyframes show{{to{{opacity:1}}}}
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}'''
    return frame(w, h, body, style, "".join(clips))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, svg in (("matrix-header", header()), ("matrix-footer", footer()), ("terminal", terminal())):
        p = OUT / f"{name}.svg"
        p.write_text(svg, encoding="utf-8")
        print(f"{p.name}: {len(svg) / 1024:.0f} KB")
