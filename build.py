#!/usr/bin/env python3
"""Ensambla las páginas del sitio: head + header + contenido (src/*.html) + footer."""
import re, pathlib
ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"

PAGES = [
  # archivo, título, descripción, clave nav
  ("index.html", "Fundación Sevenfold Colombia | Fútbol 7, educación y oportunidades",
   "Fundación Sevenfold Colombia: llevamos el fútbol 7, la educación y oportunidades reales a niños y jóvenes de Bogotá, Huila, Vaupés y Chocó.", "inicio"),
  ("nosotros.html", "Nosotros | Fundación Sevenfold Colombia",
   "Propósito, misión y visión, equipo, historia, casos y hacia dónde va la Fundación Sevenfold Colombia.", "nosotros"),
  ("seven-colombia.html", "Seven Colombia · Fútbol 7 | Fundación Sevenfold",
   "Seven Colombia: la línea deportiva de la Fundación Sevenfold, avalada por la FIF7. Categorías, palmarés internacional, Kings League y temporada 2026.", "lineas"),
  ("educacion.html", "Educación | Fundación Sevenfold Colombia",
   "La línea de educación de la Fundación Sevenfold: kits escolares, calzado y formación para niños y jóvenes de Vaupés y otros territorios.", "lineas"),
  ("ambiente.html", "Ambiente y desarrollo sostenible | Fundación Sevenfold Colombia",
   "Ambiente y desarrollo sostenible: iniciativas de conservación de la biodiversidad y cuidado del territorio de la Fundación Sevenfold.", "lineas"),
  ("impacto.html", "Impacto e historias | Fundación Sevenfold Colombia",
   "Resultados 2025-2026, historias de jóvenes que llegaron lejos y la bitácora de acciones en Bogotá, Huila, Vaupés y Chocó.", "lineas"),
  ("apoya.html", "Apoya y patrocina | Fundación Sevenfold Colombia",
   "Dona, apadrina un talento, dona en especie o patrocina. Las donaciones reciben certificado y pueden dar lugar a beneficios tributarios.", "apoya"),
  ("contacto.html", "Contacto | Fundación Sevenfold Colombia",
   "Escríbenos para donar, patrocinar, hacer alianzas o sumarte como voluntario a la Fundación Sevenfold Colombia.", "contacto"),
  ("kings-league.html", "Kings League | Seven Colombia · Fundación Sevenfold",
   "Jugadores formados en Seven Colombia que llegaron a la Kings League Américas: el camino del barrio a las grandes vitrinas del fútbol 7.", "lineas"),
  ("merida-2025.html", "Campeones en Mérida 2025 | Fundación Sevenfold Colombia",
   "Tres títulos, un subcampeonato y un tercer lugar: la delegación de Seven Colombia en el Torneo Internacional de Fútbol 7 de Mérida, México.", "lineas"),
]

# Menú principal: página, texto, clave y desplegable.
# Pestañas sin desplegable llevan directo a su página. "Qué hacemos" no es una página:
# solo abre el desplegable con las tres líneas y el impacto (nada lleva a una pestaña intermedia).
NAV = [
  ("index.html", "Inicio", "inicio", []),
  ("nosotros.html", "Nosotros", "nosotros", []),
  (None, "Qué hacemos", "lineas", [
    ("seven-colombia.html", "Deporte · Seven Colombia"), ("educacion.html", "Educación"),
    ("ambiente.html", "Ambiente y desarrollo sostenible"), ("impacto.html", "Impacto e historias")]),
  ("contacto.html", "Contacto", "contacto", []),
  ("apoya.html", "Súmate", "apoya", []),
]

ICONS = {
 "arrow":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "chev":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>',
 "ball":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7.5l4.2 3-1.6 5h-5.2l-1.6-5z"/><path d="M12 3v4.5M20.4 9.6l-4.2 1M17.5 19.5l-2.9-4M6.5 19.5l2.9-4M3.6 9.6l4.2 1"/></svg>',
 "book":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/></svg>',
 "heart":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 20s-7.5-4.6-9.3-9.4C1.4 7 3.6 4 6.8 4c2 0 3.6 1.1 4.2 2.7h2C13.6 5.1 15.2 4 17.2 4c3.2 0 5.4 3 4.1 6.6C19.5 15.4 12 20 12 20z"/></svg>',
 "globe":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>',
 "leaf":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-8 5-14 15-15-1 10-7 15-15 15z"/><path d="M5 19l8-8"/></svg>',
 "gift":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="8" width="18" height="5" rx="1"/><path d="M5 13v8h14v-8M12 8v13M12 8S10.5 3.5 8 4s-1.5 4 4 4zm0 0s1.5-4.5 4-4 1.5 4-4 4z"/></svg>',
 "star":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg>',
 "brief":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/></svg>',
 "hands":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 11l3-3 2 2 3-3 5 5-6 6-3-3"/><path d="M3 12l5-5 3 3M3 12l5 5 2-2"/></svg>',
 "cert":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 14l2 2 4-4"/></svg>',
 "mail":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 "pin":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "id":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M6 16c.6-1.5 1.7-2.2 3-2.2s2.4.7 3 2.2M15 10h3M15 13h3"/></svg>',
 "wa":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3a.5.5 0 0 0 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.7 11.7 0 0 0 4.5 4c1.7.7 2.3.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.5-.3z"/></svg>',
 "ig":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 "fb":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8.5c0-.3.2-.5.5-.5z"/></svg>',
 "yt":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12a31 31 0 0 0 .4 3.8 3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-3.8 31 31 0 0 0-.4-3.8zM10 15.1V8.9l5.2 3.1z"/></svg>',
 "tt":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.2v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.6a5.9 5.9 0 1 0 5 5.8V9.1a7.4 7.4 0 0 0 4.3 1.4V7.3a4.3 4.3 0 0 1-3.2-1.5z"/></svg>',
 "in":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4v11H3zM9.5 9.5h3.8v1.6c.6-1 1.9-1.9 3.8-1.9 4 0 4.9 2.5 4.9 5.8v5.5h-4v-4.9c0-1.2 0-2.7-1.7-2.7s-1.9 1.3-1.9 2.6v5h-4z"/></svg>',
}

def social():
    items = [("instagram","ig","Instagram"),("facebook","fb","Facebook"),("youtube","yt","YouTube"),("tiktok","tt","TikTok"),("linkedin","in","LinkedIn")]
    return '<div class="social">' + "".join(f'<a data-social="{k}" href="#" target="_blank" rel="noopener" aria-label="{n}">{ICONS[i]}</a>' for k,i,n in items) + "</div>"

def nav_item(page, text, key, subs, active):
    cur = ' aria-current="page"' if key == active else ""
    soft = " nav-soft" if key == "apoya" else ""
    if not subs:
        return f'<div class="nav-item{soft}"><div class="nav-top"><a href="{page}"{cur}>{text}</a></div></div>'
    items = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in subs)
    current = " current" if key == active else ""
    return (f'<div class="nav-item group"><div class="nav-top"><button class="sub-btn group-btn{current}" aria-expanded="false" aria-controls="sub-{key}">{text}{ICONS["chev"]}</button></div>'
            f'<div class="sub" id="sub-{key}"><ul>{items}</ul></div></div>')

def header(active, solid):
    links = "".join(nav_item(*n, active) for n in NAV)
    return f'''<a class="skip" href="#main">Saltar al contenido</a>
<header class="site-head{' always' if solid else ''}">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="Fundación Sevenfold Colombia, inicio"><img src="assets/logo-white.png" alt="Fundación Sevenfold · Creemos en el futuro" width="409" height="161"></a>
    <nav class="nav" id="nav" aria-label="Principal">{links}</nav>
    <button class="menu-btn" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  </div>
</header>'''

FOOTER = f'''<footer class="foot">
  <div class="wrap">
    <div class="grid">
      <div>
        <img class="logo" src="assets/logo-white.png" alt="Fundación Sevenfold · Creemos en el futuro" width="409" height="161" loading="lazy">
        <p>Entidad sin ánimo de lucro que transforma la vida de niños, niñas y jóvenes de Colombia a través del deporte, la educación y el desarrollo sostenible.</p>
        {social()}
      </div>
      <div>
        <h4>Explora</h4>
        <ul><li><a href="nosotros.html">Nosotros</a></li><li><a href="seven-colombia.html">Deporte · Seven Colombia</a></li><li><a href="educacion.html">Educación</a></li><li><a href="ambiente.html">Ambiente</a></li><li><a href="impacto.html">Impacto e historias</a></li><li><a href="impacto.html#bitacora">Bitácora</a></li></ul>
      </div>
      <div>
        <h4>Súmate</h4>
        <ul><li><a href="contacto.html?tipo=donar#formulario">Donar</a></li><li><a href="contacto.html?tipo=apadrinar#formulario">Apadrinar un talento</a></li><li><a href="contacto.html?tipo=especie#formulario">Donar en especie</a></li><li><a href="apoya.html#patrocinio">Patrocinar</a></li><li><a href="apoya.html#beneficio">Beneficio tributario</a></li><li><a href="contacto.html">Voluntariado</a></li></ul>
      </div>
      <div>
        <h4>Contacto</h4>
        <ul>
          <li><a href="mailto:fundacionsevenfold@gmail.com">fundacionsevenfold@gmail.com</a></li>
          <li>Carrera 51 # 24-35, Bogotá D.C.</li>
          <li>NIT 901.965.467-5</li>
          <li><a data-wa href="#" target="_blank" rel="noopener">WhatsApp</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>© <span data-year>2026</span> Fundación Sevenfold Colombia (FUNSEVEN). Régimen Tributario Especial · ESAL.</span>
      <span>Hecho en Bogotá con el corazón en la cancha.</span>
    </div>
  </div>
</footer>
<div class="tricolor" aria-hidden="true"></div>
<div class="lb" hidden role="dialog" aria-modal="true" aria-label="Visor de fotos">
  <button class="x" aria-label="Cerrar">×</button><button class="pv" aria-label="Anterior">‹</button><button class="nx" aria-label="Siguiente">›</button>
  <figure style="margin:0"><img src="" alt=""><p></p></figure>
</div>
<script src="assets/js/main.js"></script>'''

FAVICON = "data:image/svg+xml," + ("%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230B1320'/%3E"
  "%3Cpath d='M50 20A22 22 0 1 0 52 40' fill='none' stroke='%231E7A4B' stroke-width='7' stroke-linecap='round'/%3E"
  "%3Cpath d='M44 13A22 22 0 0 1 53 27' fill='none' stroke='%23F2C40F' stroke-width='7' stroke-linecap='round'/%3E"
  "%3Ctext x='32' y='42' font-family='Arial Black,Arial' font-weight='900' font-size='26' text-anchor='middle' fill='%23fff'%3E7%3C/text%3E%3C/svg%3E")

def head(title, desc):
    return f'''<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0B1320">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/img/hero-seleccion.webp">
<meta property="og:locale" content="es_CO">
<link rel="icon" href="{FAVICON}">
<link rel="preload" href="assets/fonts/big-shoulders-display-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/figtree-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>'''

def expand(html):
    html = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: ICONS[m.group(1)], html)
    html = html.replace("{{map}}", (ROOT/"src/_map.svg").read_text())
    return html

LINE = {"seven-colombia.html": "ln-dep", "kings-league.html": "ln-dep", "merida-2025.html": "ln-dep",
        "educacion.html": "ln-edu", "ambiente.html": "ln-amb"}

for fn, title, desc, key in PAGES:
    body = expand((SRC/fn).read_text())
    solid = key == "contacto"
    # color de la línea (deporte / educación / ambiente) para las páginas de cada línea
    line = LINE.get(fn, "")
    main_open = f'\n<main id="main" class="{line}">\n' if line else '\n<main id="main">\n'
    out = head(title, desc) + "\n" + header(key, False) + main_open + body + "\n</main>\n" + FOOTER + "\n</body>\n</html>\n"
    (ROOT/fn).write_text(out)
    print("ok", fn, len(out))
