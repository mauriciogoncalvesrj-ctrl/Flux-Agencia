#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Template: Programmatic Instagram Carousel SVG Generation
Usage: Adapt this script for each carousel project.
"""

import os

def wrap_text(text, max_chars=22):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = cur + " " + w if cur else w
        if len(test) <= max_chars:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def create_slide(title, subtitle="", body="", slide_num=0, total=1,
                 highlight_words=[], icon="", badge="", cta="", footer="",
                 numbers=None, alert_box=""):
    W, H = 1080, 1350
    GOLD, WHITE, GRAY, RED = "#D4AF37", "#FFFFFF", "#888888", "#DC5046"
    
    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    svg.append('<defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#000"/><stop offset="100%" stop-color="#0a0a0a"/></linearGradient></defs>')
    svg.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    svg.append(f'<circle cx="950" cy="150" r="280" fill="none" stroke="{GOLD}" stroke-width="0.5" opacity="0.06"/>')
    svg.append(f'<circle cx="150" cy="1200" r="220" fill="none" stroke="{GOLD}" stroke-width="0.5" opacity="0.06"/>')
    
    if slide_num > 0:
        svg.append(f'<text x="{W-50}" y="50" font-size="20" font-weight="bold" text-anchor="end" fill="#333">{slide_num}/{total}</text>')
    
    if badge:
        bw = len(badge) * 14 + 30
        svg.append(f'<rect x="50" y="35" width="{bw}" height="32" rx="16" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
        svg.append(f'<text x="{50+bw//2}" y="58" font-size="14" font-weight="bold" text-anchor="middle" fill="{GOLD}">{badge}</text>')
    
    y = 170
    
    if icon:
        svg.append(f'<text x="{W//2}" y="{y+70}" font-size="85" text-anchor="middle">{icon}</text>')
        y += 110
    
    for line in wrap_text(title.upper(), 22):
        color = GOLD if any(hw.upper() in line for hw in highlight_words) else WHITE
        svg.append(f'<text x="{W//2}" y="{y}" font-family="Arial Black, Arial" font-size="48" font-weight="900" text-anchor="middle" fill="{color}">{line}</text>')
        y += 64
    
    y += 18
    
    if alert_box:
        alines = wrap_text(alert_box, 50)
        bh = len(alines) * 30 + 24
        svg.append(f'<rect x="80" y="{y}" width="{W-160}" height="{bh}" rx="10" fill="rgba(220,80,70,0.08)" stroke="{RED}" stroke-width="2"/>')
        ay = y + 28
        for al in alines:
            svg.append(f'<text x="{W//2}" y="{ay}" font-size="20" text-anchor="middle" fill="#f5f5f5">{al}</text>')
            ay += 30
        y += bh + 20
    
    if subtitle:
        for sl in wrap_text(subtitle, 48):
            svg.append(f'<text x="{W//2}" y="{y}" font-size="26" text-anchor="middle" fill="{GRAY}">{sl}</text>')
            y += 40
    
    y += 12
    
    if body:
        for bline in body.split('\n'):
            if not bline.strip():
                y += 12
                continue
            if bline.startswith('-'):
                svg.append(f'<text x="100" y="{y}" font-size="22" fill="{GOLD}">→</text>')
                svg.append(f'<text x="130" y="{y}" font-size="20" fill="#ccc">{bline[1:].strip()}</text>')
            else:
                for bl in wrap_text(bline, 50):
                    svg.append(f'<text x="{W//2}" y="{y}" font-size="20" text-anchor="middle" fill="#ccc">{bl}</text>')
                    y += 34
            y += 34
    
    if numbers:
        y += 25
        for num, label in numbers:
            svg.append(f'<text x="{W//2}" y="{y}" font-family="Arial Black" font-size="70" font-weight="900" text-anchor="middle" fill="{GOLD}">{num}</text>')
            y += 46
            svg.append(f'<text x="{W//2}" y="{y}" font-size="18" text-anchor="middle" fill="#666">{label}</text>')
            y += 34
    
    if cta:
        y += 25
        clines = wrap_text(cta, 48)
        bh = len(clines) * 32 + 32
        svg.append(f'<rect x="70" y="{y}" width="{W-140}" height="{bh}" rx="14" fill="#0d0d0d" stroke="{GOLD}" stroke-width="2"/>')
        cy = y + 28
        for cl in clines:
            svg.append(f'<text x="{W//2}" y="{cy}" font-size="20" font-weight="bold" text-anchor="middle" fill="{GOLD}">{cl}</text>')
            cy += 32
    
    if footer:
        svg.append(f'<text x="{W//2}" y="{H-55}" font-size="16" text-anchor="middle" fill="#444">{footer}</text>')
    
    svg.append(f'<rect x="50" y="{H-25}" width="{W-100}" height="3" rx="2" fill="{GOLD}"/>')
    svg.append('</svg>')
    return '\n'.join(svg)


# Example usage
if __name__ == "__main__":
    output_dir = "/opt/data/carrosseis"
    os.makedirs(output_dir, exist_ok=True)
    
    slides = [
        {"title": "TÍTULO PRINCIPAL", "subtitle": "Subtítulo descritivo", "slide_num": 1, "total": 5, "icon": "🚀"},
        {"title": "DESTAQUE EM DOURADO", "subtitle": "Exemplo de slide", "slide_num": 2, "total": 5, "highlight_words": ["DOURADO"], "body": "- Bullet 1\n- Bullet 2"},
        {"title": "SLIDE COM NÚMEROS", "slide_num": 3, "total": 5, "numbers": [("80%", "Estatística"), ("R$35K", "Resultado")]},
        {"title": "ALERTA VERMELHO", "slide_num": 4, "total": 5, "alert_box": "Esta é uma mensagem de alerta."},
        {"title": "CHAMADA PARA AÇÃO", "slide_num": 5, "total": 5, "cta": "Comenta 'SIM' para saber mais!", "footer": "Sua Marca · Posicionamento"},
    ]
    
    for s in slides:
        svg = create_slide(**s)
        path = os.path.join(output_dir, f"slide{s['slide_num']:02d}.svg")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f"✅ {path}")
    
    print(f"\n🎉 {len(slides)} slides gerados em {output_dir}")
