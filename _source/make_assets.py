#!/usr/bin/env python3
"""Make checklist PDFs (EN/FR) and the social preview image into the site folder."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import CHECK_EN, CHECK_FR
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

OUT = sys.argv[1]
GREEN, AMBER, INK, MUTED = HexColor("#173a31"), HexColor("#e0954a"), HexColor("#14201c"), HexColor("#4a5852")


def mark(c, x, y, s):
    k = s / 96.0
    c.setFillColor(GREEN); c.roundRect(x, y, s, s, 20 * k, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#ffffff")); c.setLineWidth(5 * k); c.setLineCap(1)
    Y = lambda v: y + s - v * k
    X = lambda v: x + v * k
    p = c.beginPath(); p.moveTo(X(22), Y(28)); p.curveTo(X(40), Y(28), X(40), Y(48), X(56), Y(48)); c.drawPath(p, stroke=1, fill=0)
    c.line(X(22), Y(48), X(64), Y(48))
    p = c.beginPath(); p.moveTo(X(22), Y(68)); p.curveTo(X(40), Y(68), X(40), Y(48), X(56), Y(48)); c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(AMBER); c.circle(X(73), Y(48), 12 * k, stroke=0, fill=1)
    c.setStrokeColor(GREEN); c.setLineWidth(3.6 * k)
    p = c.beginPath(); p.moveTo(X(67.5), Y(48.5)); p.lineTo(X(71.5), Y(52.5)); p.lineTo(X(79), Y(44)); c.drawPath(p, stroke=1, fill=0)


def pdf(path, title, sub, items, foot, lang):
    c = canvas.Canvas(path, pagesize=letter)
    c.setTitle(title); c.setAuthor("BAS Digital Solutions"); c.setSubject(sub)
    W, H = letter
    mark(c, 54, H - 96, 42)
    c.setFillColor(INK); c.setFont("Times-Bold", 15); c.drawString(106, H - 70, "BAS Digital Solutions")
    c.setFont("Times-Bold", 26); c.drawString(54, H - 150, title)
    c.setFillColor(MUTED); c.setFont("Helvetica", 12); c.drawString(54, H - 172, sub)
    y = H - 220
    for i, it in enumerate(items, 1):
        c.setStrokeColor(GREEN); c.setLineWidth(1.4); c.rect(54, y - 4, 14, 14, stroke=1, fill=0)
        c.setFillColor(INK); c.setFont("Helvetica", 13); c.drawString(80, y, it.replace(" ", " "))
        c.setStrokeColor(HexColor("#d6dcd6")); c.setLineWidth(.6); c.line(54, y - 14, W - 54, y - 14)
        y -= 38
    c.setFillColor(MUTED); c.setFont("Helvetica", 10)
    c.drawString(54, 60, foot)
    c.drawString(54, 46, "basdigitalsolutions.ca  ·  info@basdigitalsolutions.ca")
    c.save()


pdf(os.path.join(OUT, "rfq-checklist-en.pdf"), "RFQ readiness checklist", "A starting point for your free 30-minute call.",
    CHECK_EN, "Book a call: basdigitalsolutions.ca/#contact", "en")
pdf(os.path.join(OUT, "rfq-checklist-fr.pdf"), "Liste de préparation aux demandes de prix",
    "Un point de départ pour votre appel gratuit de 30 minutes.", CHECK_FR,
    "Réserver un appel : basdigitalsolutions.ca/fr.html#contact", "fr")

# Social preview image (1200x630) rendered with Playwright from HTML
html = open(os.path.join(OUT, "favicon.svg")).read()
og = f"""<html><body style="margin:0;width:1200px;height:630px;background:#173a31;display:flex;flex-direction:column;justify-content:center;padding:0 90px;box-sizing:border-box;font-family:Georgia,serif;color:#fff">
<div style="display:flex;align-items:center;gap:22px;margin-bottom:46px"><div style="width:96px;height:96px;outline:2px solid rgba(255,255,255,.25);border-radius:20px">{html}</div>
<div style="font-size:44px;font-weight:700">BAS Digital Solutions</div></div>
<div style="font-size:60px;font-weight:700;line-height:1.1;max-width:960px">RFQ and workflow automation for industrial companies</div>
<div style="font-family:system-ui,Arial,sans-serif;font-size:28px;color:#e0954a;margin-top:28px">Montreal · Quebec · Human approval on every quote</div>
</body></html>"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(og)
    pg.screenshot(path=os.path.join(OUT, "og-image.png"))
    b.close()
print("assets ok")
