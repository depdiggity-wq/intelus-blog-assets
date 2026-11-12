"""Branded blog cover generator for The IT Wake-Up Call (Intelus Technology Group).
Usage: python3 cover.py "<title>" <area> <out.png>
area: security | voip | camera | access
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 800
F = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
AREAS = {
    "security": ("CYBERSECURITY", (56, 189, 248)),
    "voip": ("BUSINESS PHONES", (52, 211, 153)),
    "camera": ("VIDEO SURVEILLANCE", (251, 146, 60)),
    "access": ("ACCESS CONTROL", (167, 139, 250)),
}

def font(w, s):
    try:
        return ImageFont.truetype(F.format(w), s)
    except OSError:
        return ImageFont.load_default(s)

def icon(d, area, cx, cy, c, s=1.0):
    lw = int(14 * s)
    if area == "security":  # shield with check
        pts = [(cx, cy - 150*s), (cx + 125*s, cy - 100*s), (cx + 115*s, cy + 40*s),
               (cx, cy + 160*s), (cx - 115*s, cy + 40*s), (cx - 125*s, cy - 100*s)]
        d.line(pts + [pts[0]], fill=c, width=lw, joint="curve")
        d.line([(cx - 50*s, cy), (cx - 10*s, cy + 45*s), (cx + 60*s, cy - 50*s)], fill=c, width=lw, joint="curve")
    elif area == "voip":  # desk phone handset + signal arcs
        d.rounded_rectangle([cx - 120*s, cy - 20*s, cx + 120*s, cy + 130*s], 28*s, outline=c, width=lw)
        d.rounded_rectangle([cx - 140*s, cy - 110*s, cx + 140*s, cy - 50*s], 30*s, outline=c, width=lw)
        for i in range(3):
            for j in range(3):
                d.ellipse([cx - 70*s + i*55*s - 9*s, cy + 20*s + j*35*s - 9*s,
                           cx - 70*s + i*55*s + 9*s, cy + 20*s + j*35*s + 9*s], fill=c)
    elif area == "camera":  # bullet camera on mount
        d.rounded_rectangle([cx - 130*s, cy - 90*s, cx + 90*s, cy + 10*s], 30*s, outline=c, width=lw)
        d.ellipse([cx + 60*s, cy - 75*s, cx + 140*s, cy - 5*s], outline=c, width=lw)
        d.line([(cx - 40*s, cy + 10*s), (cx - 40*s, cy + 110*s), (cx - 130*s, cy + 110*s)], fill=c, width=lw)
        d.ellipse([cx - 100*s, cy - 55*s, cx - 70*s, cy - 25*s], fill=c)
    else:  # access: keycard reader + card
        d.rounded_rectangle([cx - 80*s, cy - 150*s, cx + 80*s, cy + 150*s], 26*s, outline=c, width=lw)
        d.ellipse([cx - 22*s, cy - 110*s, cx + 22*s, cy - 66*s], fill=c)
        for r in (20, 40, 60):
            d.arc([cx - r*s, cy - r*s + 70*s, cx + r*s, cy + r*s + 70*s], 220, 320, fill=c, width=int(9*s))

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines

def make(title, area, out):
    label, accent = AREAS[area]
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):  # navy diagonal gradient
        for x in range(0, W):
            t = (x / W * 0.4 + y / H * 0.6)
            px[x, y] = (int(11 + 10*t), int(22 + 18*t), int(48 + 30*t))
    d = ImageDraw.Draw(img)
    # subtle grid
    for gx in range(0, W, 60):
        d.line([(gx, 0), (gx, H)], fill=(255, 255, 255, 0) if False else (24, 40, 74), width=1)
    for gy in range(0, H, 60):
        d.line([(0, gy), (W, gy)], fill=(24, 40, 74), width=1)
    # icon panel on right
    d.ellipse([820, 200, 1160, 540], fill=(20, 36, 70), outline=accent, width=4)
    icon(d, area, 990, 370, accent, 0.95)
    # accent bar + label pill
    d.rectangle([0, 0, W, 10], fill=accent)
    lf = font("Bold", 24)
    tw = d.textlength(label, font=lf)
    d.rounded_rectangle([70, 80, 70 + tw + 40, 128], 24, fill=accent)
    d.text((90, 104), label, font=lf, fill=(11, 22, 48), anchor="lm")
    # title (auto-shrink)
    for size in (72, 64, 58, 52, 46):
        tf = font("ExtraBold", size)
        lines = wrap(d, title, tf, 690)
        if len(lines) <= 4:
            break
    y = 175
    for ln in lines:
        d.text((70, y), ln, font=tf, fill="white")
        y += int(size * 1.18)
    # footer
    d.line([(70, 680), (1130, 680)], fill=(44, 64, 104), width=2)
    d.text((70, 720), "THE IT WAKE-UP CALL", font=font("Bold", 26), fill=accent, anchor="lm")
    d.text((1130, 720), "Intelus Technology Group  ·  Tucson, AZ", font=font("Medium", 26),
           fill=(190, 200, 220), anchor="rm")
    img.save(out, "PNG", optimize=True)

if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2], sys.argv[3])
