import os

def get_svg(index, title):
    # Color Palettes (Rich, Epic colors)
    palettes = [
        {"name": "Royal", "bg": ["#2d0b00", "#5d1a1a"], "accent": "#ffd700", "sec": "#ff8c00"},
        {"name": "Forest", "bg": ["#0b3300", "#1a5d00"], "accent": "#a2d149", "sec": "#ffd700"},
        {"name": "Divine", "bg": ["#001a33", "#003366"], "accent": "#80d8ff", "sec": "#ffffff"},
        {"name": "Conflict", "bg": ["#330000", "#800000"], "accent": "#ff4444", "sec": "#ffd700"},
        {"name": "Mystical", "bg": ["#1a0033", "#4a154b"], "accent": "#e040fb", "sec": "#ffd700"},
    ]
    
    p = palettes[0]
    if index in [5, 6, 7, 8, 21, 25, 26, 27, 28, 29, 32, 33]: p = palettes[1] # Forest
    if index in [1, 2, 8, 11, 20, 34, 38, 39]: p = palettes[2] # Divine
    if index in [15, 16, 22, 28, 30, 31, 37]: p = palettes[3] # Conflict
    if index in [9, 10, 13, 35, 36]: p = palettes[4] # Mystical

    bg1, bg2 = p["bg"]
    accent = p["accent"]
    sec = p["sec"]

    # Reusable components
    def person(x, y, scale=1, color="#ffcc99", crown=False, bow=False, staff=False, hair=True, sari=False):
        res = f'<g transform="translate({x},{y}) scale({scale})">'
        # Aura / Divine halo
        res += f'<circle cx="0" cy="-5" r="35" fill="{accent}" opacity="0.12" filter="url(#glow)"/>'
        # Detailed Head & Crown
        if hair:
            res += f'<path d="M -15 -18 C -15 -35 15 -35 15 -18 C 18 -10 15 5 15 5 L -15 5 C -15 5 -18 -10 -15 -18 Z" fill="#2b1810"/>'
        res += f'<circle cx="0" cy="0" r="18" fill="{color}" stroke="{accent}" stroke-width="0.8"/>'
        # Facial details
        res += f'<circle cx="-5" cy="-2" r="2" fill="#333"/><circle cx="5" cy="-2" r="2" fill="#333"/><path d="M -3 5 Q 0 8 3 5" fill="none" stroke="#333" stroke-width="1.2"/>'
        if crown:
            res += f'<path d="M -16 -14 L -20 -35 L -8 -22 L 0 -42 L 8 -22 L 20 -35 L 16 -14 Z" fill="url(#goldGrad)" filter="url(#glow)" stroke="#b38f00" stroke-width="1"/>'
            res += f'<circle cx="0" cy="-30" r="4" fill="#ff3333"/><circle cx="-12" cy="-25" r="2.5" fill="#33ff33"/><circle cx="12" cy="-25" r="2.5" fill="#3333ff"/>'
        # Detailed Robe / Attire
        body_color = "#ff8c00" if not sari else "#e63946"
        res += f'<path d="M -22 18 Q 0 15 22 18 L 35 85 L 18 90 L 0 75 L -18 90 L -35 85 Z" fill="{body_color}" stroke="{accent}" stroke-width="1.5"/>'
        res += f'<path d="M -15 18 L 15 18 L 22 55 L -22 55 Z" fill="#ffd700" opacity="0.25"/>' # Sash
        # Jewelry / Mala
        res += f'<path d="M -10 20 Q 0 35 10 20" fill="none" stroke="{accent}" stroke-width="2.5"/>'
        res += f'<circle cx="0" cy="30" r="3" fill="#ff4444"/>'
        if bow:
            res += f'<path d="M 28 -40 Q 80 25 28 90" fill="none" stroke="url(#goldGrad)" stroke-width="4.5" stroke-linecap="round"/>'
            res += f'<line x1="28" y1="-40" x2="28" y2="90" stroke="#fff" stroke-width="1.2"/>'
            res += f'<path d="M 24 15 L 35 25 L 24 35" fill="none" stroke="{accent}" stroke-width="2"/>' # Arrow
        if staff:
            res += f'<line x1="-30" y1="-50" x2="-30" y2="95" stroke="#8b4513" stroke-width="6" stroke-linecap="round"/>'
            res += f'<circle cx="-30" cy="-52" r="6" fill="url(#goldGrad)"/>'
        res += '</g>'
        return res

    def tree(x, y, scale=1):
        return f'''<g transform="translate({x},{y}) scale({scale})">
            <path d="M -6 50 L 6 50 L 8 -10 L -8 -10 Z" fill="#5c3a21"/>
            <circle cx="0" cy="-20" r="45" fill="#1b4d1b" opacity="0.9"/>
            <circle cx="-25" cy="-5" r="30" fill="#2d6a2d" opacity="0.85"/>
            <circle cx="25" cy="-5" r="30" fill="#2d6a2d" opacity="0.85"/>
            <circle cx="0" cy="-50" r="35" fill="#388e3c" opacity="0.9"/>
        </g>'''

    def mountain(x, y, w, h, color="#37474f"):
        return f'''<g transform="translate({x},{y})">
            <path d="M 0 0 L {w/2} {-h} L {w} 0 Z" fill="{color}" opacity="0.75"/>
            <path d="M {w/4} {-h/2} L {w/2} {-h} L {w*0.75} {-h/2} Z" fill="#ffffff" opacity="0.25"/> <!-- Snow cap -->
        </g>'''

    def sun(x, y, r, color="#ffeb3b"):
        res = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" filter="url(#glow)"/>'
        for i in range(16):
            angle = i * 22.5
            res += f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y-r-25}" stroke="{color}" stroke-width="3" stroke-linecap="round" transform="rotate({angle}, {x}, {y})" opacity="0.7"/>'
        return res

    def palace(x, y, scale=1):
        return f'''<g transform="translate({x},{y}) scale({scale})">
            <rect x="-120" y="0" width="240" height="150" fill="#fff3e0" stroke="#b38f00" stroke-width="2"/>
            <path d="M -140 0 L 140 0 L 120 -25 L -120 -25 Z" fill="#ff8c00"/>
            <!-- Domes -->
            <path d="M -70 0 Q -70 -90 0 -110 Q 70 -90 70 0 Z" fill="url(#goldGrad)" filter="url(#glow)"/>
            <path d="M -110 0 Q -110 -60 -80 -70 Q -50 -60 -50 0 Z" fill="url(#goldGrad)"/>
            <path d="M 50 0 Q 50 -60 80 -70 Q 110 -60 110 0 Z" fill="url(#goldGrad)"/>
            <!-- Pillars & Entrance -->
            <rect x="-30" y="40" width="60" height="110" rx="30" fill="#3e2723"/>
            <line x1="-15" y1="40" x2="-15" y2="150" stroke="{accent}" stroke-width="4"/>
            <line x1="15" y1="40" x2="15" y2="150" stroke="{accent}" stroke-width="4"/>
        </g>'''

    # Background elements based on palette
    bg_elements = sun(700, 80, 40, accent)
    if p["name"] == "Forest":
        bg_elements += mountain(0, 400, 400, 200, "#0b3300") + mountain(300, 400, 500, 250, "#0b3300")
        bg_elements += tree(100, 350, 1.2) + tree(700, 360, 1) + tree(200, 370, 0.8)
    elif p["name"] == "Royal":
        bg_elements += f'<rect x="0" y="300" width="800" height="100" fill="#3d1212" opacity="0.3"/>'
        bg_elements += f'<path d="M 0 300 L 800 300" stroke="{accent}" stroke-width="2" stroke-dasharray="10,10"/>'
    elif p["name"] == "Divine":
        bg_elements += f'<circle cx="400" cy="150" r="100" fill="white" opacity="0.05" filter="url(#glow)"/>'
        bg_elements += f'<path d="M 0 400 Q 400 450 800 400 L 800 500 L 0 500 Z" fill="#003366" opacity="0.6"/>'

    # Unique Drawing Logic for each of the 40 chapters
    drawings = [
        # 1. Dasharatha's Sorrow
        person(400, 200, 1.5, crown=True) + f'<path d="M 380 230 Q 400 260 420 230" fill="none" stroke="{accent}" opacity="0.6"/>',
        # 2. The Putrakameshti Yagna
        f'<path d="M 300 400 L 500 400 L 450 450 L 350 450 Z" fill="#4a154b"/><path d="M 400 400 L 320 250 Q 400 100 480 250 Z" fill="#ff6600" filter="url(#glow)"/>',
        # 3. Birth of the Divine Princes
        f'<g transform="translate(400,250)">' + "".join([f'<circle cx="{x}" cy="{y}" r="25" fill="#ffcc99" stroke="{accent}" filter="url(#glow)"/>' for x,y in [(-60,-40), (60,-40), (-60,60), (60,60)]]) + '</g>',
        # 4. Education and Training
        person(300, 250, 0.8, crown=True) + person(500, 250, 1.2, staff=True, hair=True),
        # 5. Vishwamitra's Arrival
        person(300, 250, 1.2, staff=True) + person(550, 250, 1, crown=True),
        # 6. Departure with the Sage
        person(200, 300, 1, staff=True) + person(400, 300, 1, crown=True, bow=True) + person(600, 300, 1, crown=True, bow=True),
        # 7. Slaying of Tataka
        f'<path d="M 500 400 L 700 400 L 650 100 L 550 100 Z" fill="#1a1a1a" stroke="red"/>' + person(250, 300, 1, crown=True, bow=True),
        # 8. Protection of the Sacrifice
        f'<path d="M 350 400 L 450 400 L 400 250 Z" fill="#ff4400" filter="url(#glow)"/>' + person(200, 300, 1, crown=True, bow=True) + person(600, 300, 1, crown=True, bow=True),
        # 9. Redemption of Ahalya
        f'<path d="M 300 400 L 500 400 L 480 380 L 320 380 Z" fill="#666"/>' + person(400, 250, 1, color="#fff", hair=False) + f'<path d="M 400 250 Q 450 150 400 50" fill="none" stroke="white" opacity="0.5" filter="url(#glow)"/>',
        # 10. Arrival in Mithila
        f'<path d="M 100 400 L 350 400 L 225 50 Z" fill="#432818" stroke="{accent}" stroke-width="4"/>' + person(550, 300, 1, crown=True),
        # 11. The Challenge of Shiva's Bow
        f'<path d="M 150 350 Q 400 -50 650 350" fill="none" stroke="{accent}" stroke-width="15" filter="url(#glow)"/>' + person(400, 300, 1, crown=True),
        # 12. Rama Breaks the Bow
        f'<path d="M 200 300 Q 350 100 390 280" fill="none" stroke="{accent}" stroke-width="10"/><path d="M 410 280 Q 450 100 600 300" fill="none" stroke="{accent}" stroke-width="10"/><circle cx="400" cy="250" r="30" fill="white" filter="url(#glow)"/>',
        # 13. The Grand Wedding
        person(350, 250, 1, crown=True) + person(450, 250, 1, color="#ffcc99", sari=True) + f'<path d="M 300 400 L 500 400 L 400 300 Z" fill="#ff4400" opacity="0.4"/>',
        # 14. Encounter with Parashurama
        person(300, 250, 1.2, staff=True) + person(550, 250, 1, crown=True, bow=True),
        # 15. Plans for Coronation
        f'<path d="M 200 400 L 600 400 L 400 50 Z" fill="{accent}" opacity="0.2"/>' + person(400, 250, 1.3, crown=True),
        # 16. Manthara's Poison
        person(350, 250, 1, color="#333") + person(500, 250, 1, crown=True),
        # 17. The Two Boons
        person(300, 250, 1, crown=True) + person(550, 250, 1, crown=True) + f'<rect x="350" y="300" width="100" height="10" fill="{accent}"/>',
        # 18. Rama's Acceptance
        person(400, 250, 1.2, crown=True) + f'<path d="M 350 350 L 450 350" stroke="white" stroke-width="2" opacity="0.5"/>',
        # 19. Sita and Lakshmana's Resolve
        person(250, 300, 1, crown=True) + person(400, 300, 1, color="#ffcc99", sari=True) + person(550, 300, 1, crown=True, bow=True),
        # 20. Departure from Ayodhya
        f'<rect x="200" y="350" width="400" height="60" fill="#8b4513" stroke="{accent}"/>' + person(400, 280, 1, crown=True),
        # 21. Crossing the Ganges
        f'<path d="M 0 400 Q 400 480 800 400 L 800 500 L 0 500 Z" fill="#00b0ff" opacity="0.4"/>' + person(400, 320, 1, crown=True),
        # 22. Arrival at Chitrakoot
        f'<path d="M 0 400 Q 400 300 800 400" fill="#1a5d00" opacity="0.5"/>' + person(400, 320, 1, crown=True),
        # 23. Dasharatha's Passing
        person(400, 250, 1.2, crown=True) + f'<circle cx="400" cy="250" r="150" fill="none" stroke="white" stroke-dasharray="20,10" opacity="0.2"/>',
        # 24. Bharata's Return
        person(400, 250, 1.2, crown=True) + f'<path d="M 300 400 L 500 400" stroke="red" stroke-width="8" opacity="0.6"/>',
        # 25. The Paduka Rajyabhisheka
        f'<rect x="350" y="380" width="100" height="30" fill="{accent}" stroke="#8b4513"/>' + person(400, 250, 1, crown=True),
        # 26. Into the Dandaka Forest
        f'<path d="M 0 500 L 300 100 L 600 500" fill="#0b3300" opacity="0.3"/>' + person(400, 350, 1, crown=True, bow=True),
        # 27. Meeting Sage Agastya
        person(300, 300, 1.2, staff=True) + person(550, 300, 1, crown=True, bow=True),
        # 28. Shurpanakha's Encounter
        person(350, 250, 1, color="#ffcc99", sari=True) + person(550, 250, 1.2, color="#1a1a1a"),
        # 29. Battle with Khara and Dushana
        person(300, 300, 1, crown=True, bow=True) + f'<path d="M 500 300 L 700 300" stroke="red" stroke-width="10" stroke-dasharray="5,5"/>',
        # 30. The Golden Deer Plot
        f'<path d="M 550 350 L 650 350 L 600 280 Z" fill="{accent}" filter="url(#glow)"/>' + person(300, 300, 1, crown=True, bow=True),
        # 31. The Abduction of Sita
        f'<path d="M 200 250 Q 400 50 600 250" fill="#4a154b" opacity="0.6"/>' + person(400, 180, 1, color="#ffcc99", sari=True),
        # 32. Jatayu's Sacrifice
        f'<path d="M 150 350 L 400 250 L 650 350 L 400 450 Z" fill="#432818" stroke="red"/>' + person(400, 200, 1, color="#333"),
        # 33. Rama's Grief and Search
        person(400, 250, 1.2, crown=True, bow=True) + f'<path d="M 380 280 Q 400 350 420 280" fill="none" stroke="#80d8ff" stroke-width="3"/>',
        # 34. Meeting Shabari
        person(300, 300, 1, color="#666", hair=False) + person(550, 300, 1, crown=True),
        # 35. Meeting Hanuman
        person(300, 250, 1.2, crown=True) + person(550, 250, 1.2, color="#ff9933", hair=True),
        # 36. Alliance with Sugriva
        person(350, 300, 1, color="#ff9933") + person(500, 300, 1, crown=True) + f'<path d="M 400 350 L 450 350" stroke="{accent}" stroke-width="5"/>',
        # 37. Hanuman in Lanka
        f'<rect x="250" y="150" width="300" height="300" fill="#1a1a1a" stroke="{accent}"/>' + person(400, 300, 1, color="#ff9933"),
        # 38. The Burning of Lanka
        f'<rect x="150" y="250" width="500" height="200" fill="#333"/><path d="M 150 250 L 650 250 L 400 0 Z" fill="#ff4400" filter="url(#glow)" opacity="0.8"/>',
        # 39. Building the Rama Setu
        f'<path d="M 0 400 Q 400 480 800 400 L 800 500 L 0 500 Z" fill="#00b0ff" opacity="0.5"/><rect x="150" y="380" width="500" height="40" fill="#666" stroke="{accent}"/>',
        # 40. Victory and Coronation
        f'<circle cx="400" cy="200" r="150" fill="url(#goldGrad)" filter="url(#glow)"/>' + person(400, 250, 1.8, crown=True),
    ]

    drawing = drawings[index] if index < len(drawings) else drawings[-1]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" height="100%">
  <defs>
    <linearGradient id="bg{index+1}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffe066"/>
      <stop offset="50%" stop-color="#ffd700"/>
      <stop offset="100%" stop-color="#b38f00"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" stroke-width="0.5" opacity="0.1"/>
    </pattern>
  </defs>
  <rect width="800" height="500" fill="url(#bg{index+1})"/>
  <rect width="800" height="500" fill="url(#grid)"/>
  
  {bg_elements}

  <!-- Decorative Border -->
  <rect x="15" y="15" width="770" height="470" rx="15" fill="none" stroke="url(#goldGrad)" stroke-width="6"/>
  <rect x="30" y="30" width="740" height="440" rx="10" fill="none" stroke="url(#goldGrad)" stroke-width="1" stroke-dasharray="15,10" opacity="0.5"/>

  <!-- Main Illustration -->
  <g transform="translate(0, -20)">
    {drawing}
  </g>

  <!-- Title Plate -->
  <g transform="translate(400, 440)">
    <rect x="-320" y="-35" width="640" height="70" rx="20" fill="black" fill-opacity="0.8" stroke="url(#goldGrad)" stroke-width="3"/>
    <text y="10" font-family="'Playfair Display', serif" font-size="28" font-weight="bold" fill="#ffd700" text-anchor="middle">{title.upper()}</text>
  </g>
</svg>"""

titles = [
    "1. Dasharatha's Sorrow", "2. The Putrakameshti Yagna", "3. Birth of the Divine Princes",
    "4. Education and Training", "5. Vishwamitra's Arrival", "6. Departure with the Sage",
    "7. Slaying of Tataka", "8. Protection of the Sacrifice", "9. Redemption of Ahalya",
    "10. Arrival in Mithila", "11. The Challenge of Shiva's Bow", "12. Rama Breaks the Bow",
    "13. The Grand Wedding", "14. Encounter with Parashurama", "15. Plans for Coronation",
    "16. Manthara's Poison", "17. The Two Boons", "18. Rama's Acceptance",
    "19. Sita and Lakshmana's Resolve", "20. Departure from Ayodhya", "21. Crossing the Ganges",
    "22. Arrival at Chitrakoot", "23. Dasharatha's Passing", "24. Bharata's Return",
    "25. The Paduka Rajyabhisheka", "26. Into the Dandaka Forest", "27. Meeting Sage Agastya",
    "28. Shurpanakha's Encounter", "29. Battle with Khara and Dushana", "30. The Golden Deer Plot",
    "31. The Abduction of Sita", "32. Jatayu's Sacrifice", "33. Rama's Grief and Search",
    "34. Meeting Shabari", "35. Meeting Hanuman", "36. Alliance with Sugriva",
    "37. Hanuman in Lanka", "38. The Burning of Lanka", "39. Building the Rama Setu",
    "40. Victory and Coronation"
]

if not os.path.exists("images"): os.makedirs("images")
for i, title in enumerate(titles):
    with open(f"images/frame-{i+1}.svg", "w", encoding="utf-8") as f:
        f.write(get_svg(i, title))
print("Generated 40 unique SVGs.")
