#!/usr/bin/env python3
"""Ensambla las páginas del sitio: head + header + contenido (src/*.html) + footer."""
import re, pathlib, json
ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
# versión de CSS/JS para que el navegador no use una copia vieja guardada
import hashlib
VER = hashlib.md5((ROOT/'assets/css/styles.css').read_bytes()+(ROOT/'assets/js/main.js').read_bytes()).hexdigest()[:8]

# === Contacto y redes: se editan solo aquí ===
# Lo que quede vacío ("") no aparece en el sitio.
SITE = {
  "email": "fundacionsevenfold@gmail.com",
  "phone": "+57 304 674 2005",
  "whatsapp": "573046742005",                                  # solo números, con indicativo 57
  "instagram": "https://www.instagram.com/fundacion_sevenfold/",
  "instagram_seven": "https://www.instagram.com/futbol7colombia_/",  # Seven Colombia
  "facebook": "", "youtube": "", "tiktok": "", "linkedin": "",
}

PAGES = [
  # archivo, título, descripción, clave del menú
  ("index.html", "Fundación Sevenfold Colombia | Fútbol 7, educación y oportunidades",
   "Fundación Sevenfold Colombia: llevamos el fútbol 7, la educación y oportunidades reales a niños y jóvenes de Bogotá, Vaupés y Chocó.", "inicio"),
  ("nosotros.html", "Nosotros | Fundación Sevenfold Colombia",
   "Equipo, propósito, misión, visión, valores, historia y hacia dónde va la Fundación Sevenfold Colombia.", "nosotros"),
  ("seven-colombia.html", "Seven Colombia · Fútbol 7 | Fundación Sevenfold",
   "Seven Colombia, avalada por la FIF7: Seven Bogotá F.C., Seven Vaupés F.C. y Seven Chocó. Categorías, palmarés, Kings League y temporada 2026.", "seven"),
  ("educacion.html", "Educación | Fundación Sevenfold Colombia",
   "La línea de educación de la Fundación Sevenfold: kits escolares, calzado y formación para niños y jóvenes de Vaupés y otros territorios.", "educacion"),
  ("ambiente.html", "Ambiente y desarrollo sostenible | Fundación Sevenfold Colombia",
   "Ambiente y desarrollo sostenible: iniciativas de conservación de la biodiversidad y cuidado del territorio de la Fundación Sevenfold.", "ambiente"),
  ("impacto.html", "Impacto e historias | Fundación Sevenfold Colombia",
   "Resultados 2025-2026, historias de jóvenes que llegaron lejos y la bitácora de acciones en Bogotá, Vaupés y Chocó.", "impacto"),
  ("aliados.html", "Aliados | Fundación Sevenfold Colombia",
   "La FIF7, la Asociación Colombiana de Fútbol 7, Nestlé y las marcas y organizaciones que juegan con la Fundación Sevenfold.", "aliados"),
  ("apoya.html", "Súmate: dona, apadrina o patrocina | Fundación Sevenfold Colombia",
   "Dona, apadrina un talento, dona en especie o patrocina. Escríbenos desde aquí: las donaciones reciben certificado y pueden dar lugar a beneficios tributarios.", "apoya"),
]

# Páginas que ya no existen: llevan a donde quedó su contenido (enlaces viejos o compartidos)
REDIRECTS = {
  "contacto.html": "apoya.html#formulario",
  "kings-league.html": "seven-colombia.html#kings",
  "merida-2025.html": "seven-colombia.html#palmares",
}

# Menú: una pestaña = una página. Sin desplegables ni pestañas intermedias.
NAV = [
  ("index.html", "Inicio", "inicio"),
  ("nosotros.html", "Nosotros", "nosotros"),
  ("seven-colombia.html", "Seven Colombia", "seven"),
  ("educacion.html", "Educación", "educacion"),
  ("ambiente.html", "Ambiente", "ambiente"),
  ("impacto.html", "Impacto", "impacto"),
  ("aliados.html", "Aliados", "aliados"),
  ("apoya.html", "Súmate", "apoya"),
]

# Versión en inglés: mismas páginas, textos en src/en/*.html, salida en /en/
PAGES_EN = {
  "index.html": ("Fundación Sevenfold Colombia | 7-a-side football, education and opportunities", "Fundación Sevenfold Colombia brings 7-a-side football, education and real opportunities to children and young people in Bogotá, Vaupés and Chocó."),
  "nosotros.html": ("About us | Fundación Sevenfold Colombia", "Team, purpose, mission, vision, values, history and annual reports of Fundación Sevenfold Colombia."),
  "seven-colombia.html": ("Seven Colombia · 7-a-side football | Fundación Sevenfold", "Seven Colombia, endorsed by the FIF7: our clubs, categories, track record, Kings League and 2026 season."),
  "educacion.html": ("Education | Fundación Sevenfold Colombia", "Our education line: school kits, shoes, scholarships and training for children and young people."),
  "ambiente.html": ("Environment and sustainable development | Fundación Sevenfold Colombia", "Conservation, biodiversity and sustainable development initiatives in the Colombian Pacific and Amazon."),
  "impacto.html": ("Impact and stories | Fundación Sevenfold Colombia", "Our progress since 2025, stories of young people who went far, and a log of every activity."),
  "aliados.html": ("Partners | Fundación Sevenfold Colombia", "The brands and organizations that play alongside Fundación Sevenfold Colombia."),
  "apoya.html": ("Get involved: donate, sponsor or volunteer | Fundación Sevenfold Colombia", "Donate, sponsor a talent, give in kind or partner with us. Donations receive a certificate and may qualify for tax benefits in Colombia."),
}
NAV_EN = {"inicio": "Home", "nosotros": "About us", "seven": "Seven Colombia", "educacion": "Education",
          "ambiente": "Environment", "impacto": "Impact", "aliados": "Partners", "apoya": "Get involved"}

# Textos fijos (menú, pie, formulario, ventanas) en cada idioma
T = {
 "es": dict(skip="Saltar al contenido", home_label="Fundación Sevenfold Colombia, inicio", logo_alt="Fundación Sevenfold · Creemos en el futuro",
   nav="Principal", open_menu="Abrir menú", close="Cerrar", prev="Anterior", next="Siguiente", viewer="Visor de fotos", story="Historia",
   switch_label="English version", switch="EN", locale="es_CO", lang="es-CO",
   foot_about="Entidad sin ánimo de lucro que transforma la vida de niños, niñas y jóvenes de Colombia a través del deporte, la educación y el desarrollo sostenible.",
   explore="Explora", join="Súmate", contact="Contacto",
   f_links=[("nosotros.html","Nosotros"),("seven-colombia.html","Seven Colombia"),("educacion.html","Educación"),("ambiente.html","Ambiente"),("impacto.html","Impacto e historias"),("aliados.html","Aliados")],
   f_join=[("donar","Donar"),("apadrinar","Apadrinar un talento"),("especie","Donar en especie"),("patrocinar","Patrocinar"),("voluntariado","Voluntariado")],
   tax="Beneficio tributario", legal="Régimen Tributario Especial · ESAL.", made="Hecho en Bogotá con el corazón en la cancha.",
   ig_fund="Instagram de la Fundación",
   form_q="¿Cómo quieres participar?", form_opts=["Quiero donar","Quiero apadrinar un talento","Soy empresa y quiero patrocinar","Quiero donar en especie","Quiero proponer una alianza","Quiero ser voluntario","Quiero inscribir a un niño o joven","Prensa y medios","Otro tema"],
   name="Nombre completo", org="Empresa u organización", optional="Opcional", email="Correo", phone="Teléfono", interest="Me interesa apoyar en",
   interests=["Seven Colombia","Educación","Ambiente","Bogotá","Vaupés","Chocó","Viajes y torneos"], msg="Mensaje", msg_ph="Cuéntanos un poco más",
   send="Enviar mensaje", note="Se abrirá tu correo con el mensaje listo para", ok="Abrimos tu aplicación de correo con el mensaje listo. Si no se abrió, escríbenos directamente a",
   direct="¿Prefieres escribir directo?", dlg_eyebrow="Súmate", dlg_title="Hablemos", dlg_text="Cuéntanos cómo quieres participar y te respondemos con una propuesta clara.",
   read_story="Leer historia", read_the_story="Leer la historia", see_photos="Ver fotos", pending="Pendiente", photos="Fotos", stories="Historias", palmares="Palmarés",
   report_title="Informe de gestión y resultados"),
 "en": dict(skip="Skip to content", home_label="Fundación Sevenfold Colombia, home", logo_alt="Fundación Sevenfold · We believe in the future",
   nav="Main", open_menu="Open menu", close="Close", prev="Previous", next="Next", viewer="Photo viewer", story="Story",
   switch_label="Versión en español", switch="ES", locale="en_US", lang="en",
   foot_about="A non-profit organization that transforms the lives of children and young people in Colombia through sport, education and sustainable development.",
   explore="Explore", join="Get involved", contact="Contact",
   f_links=[("nosotros.html","About us"),("seven-colombia.html","Seven Colombia"),("educacion.html","Education"),("ambiente.html","Environment"),("impacto.html","Impact and stories"),("aliados.html","Partners")],
   f_join=[("donar","Donate"),("apadrinar","Sponsor a talent"),("especie","Donate in kind"),("patrocinar","Become a sponsor"),("voluntariado","Volunteer")],
   tax="Tax benefits", legal="Special Tax Regime · non-profit (ESAL).", made="Made in Bogotá with our hearts on the pitch.",
   ig_fund="Foundation on Instagram",
   form_q="How would you like to take part?", form_opts=["I want to donate","I want to sponsor a talent","I represent a company and want to sponsor","I want to donate in kind","I want to propose a partnership","I want to volunteer","I want to sign up a child or young person","Press and media","Other"],
   name="Full name", org="Company or organization", optional="Optional", email="Email", phone="Phone", interest="I'm interested in supporting",
   interests=["Seven Colombia","Education","Environment","Bogotá","Vaupés","Chocó","Trips and tournaments"], msg="Message", msg_ph="Tell us a bit more",
   send="Send message", note="Your email app will open with the message ready for", ok="We opened your email app with the message ready. If it didn't open, write to us directly at",
   direct="Prefer to write directly?", dlg_eyebrow="Get involved", dlg_title="Let's talk", dlg_text="Tell us how you'd like to take part and we'll reply with a clear proposal.",
   read_story="Read story", read_the_story="Read the story", see_photos="See photos", pending="Pending", photos="Photos", stories="Stories", palmares="Track record",
   report_title="Management and results report"),
}
FORM_VALUES = ["Donación","Apadrinar un talento","Patrocinio","Donación en especie","Alianza","Voluntariado","Inscripción de un deportista","Prensa","Otro"]
INTEREST_VALUES = ["Seven Colombia","Educación","Ambiente","Bogotá","Vaupés","Chocó","Delegaciones internacionales"]

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
 "download":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>',
 "cert":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 14l2 2 4-4"/></svg>',
 "shield":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>',
 "mail":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 "phone":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
 "pin":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "id":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M6 16c.6-1.5 1.7-2.2 3-2.2s2.4.7 3 2.2M15 10h3M15 13h3"/></svg>',
 "chat":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M20 12a8 8 0 0 1-11.6 7.1L4 20l1-4.1A8 8 0 1 1 20 12z"/></svg>',
 "play":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.9l10.4-6.5a1 1 0 0 0 0-1.8L9.5 4.6A1 1 0 0 0 8 5.5z"/></svg>',
 "wa":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3a.5.5 0 0 0 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.7 11.7 0 0 0 4.5 4c1.7.7 2.3.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.5-.3z"/></svg>',
 "ig":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 "fb":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8.5c0-.3.2-.5.5-.5z"/></svg>',
 "yt":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12a31 31 0 0 0 .4 3.8 3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-3.8 31 31 0 0 0-.4-3.8zM10 15.1V8.9l5.2 3.1z"/></svg>',
 "tt":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.2v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.6a5.9 5.9 0 1 0 5 5.8V9.1a7.4 7.4 0 0 0 4.3 1.4V7.3a4.3 4.3 0 0 1-3.2-1.5z"/></svg>',
 "in":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4v11H3zM9.5 9.5h3.8v1.6c.6-1 1.9-1.9 3.8-1.9 4 0 4.9 2.5 4.9 5.8v5.5h-4v-4.9c0-1.2 0-2.7-1.7-2.7s-1.9 1.3-1.9 2.6v5h-4z"/></svg>',
}

L = "es"  # idioma de la página que se está armando ("es" o "en")
def t(k): return T[L][k]

WA = f"https://wa.me/{SITE['whatsapp']}" if SITE["whatsapp"] else ""
TEL = "tel:" + re.sub(r"[^\d+]", "", SITE["phone"]) if SITE["phone"] else ""
def handle(url):  # "https://www.instagram.com/fundacion_sevenfold/" -> "@fundacion_sevenfold"
    return "@" + url.rstrip("/").rsplit("/", 1)[-1]

def social():
    items = [("instagram","ig",t("ig_fund")),("facebook","fb","Facebook"),("youtube","yt","YouTube"),("tiktok","tt","TikTok"),("linkedin","in","LinkedIn")]
    links = "".join(f'<a href="{SITE[k]}" target="_blank" rel="noopener" aria-label="{n}">{ICONS[i]}</a>' for k,i,n in items if SITE[k])
    if WA: links += f'<a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICONS["wa"]}</a>'
    return f'<div class="social">{links}</div>' if links else ""

def sumate(tipo):
    """Atributos de un botón de apoyo: abre el formulario ahí mismo (sin cambiar de página).
    Sin JavaScript, lleva al formulario de Súmate con la opción ya elegida."""
    return f'href="apoya.html?tipo={tipo}#formulario" data-form="{tipo}"'

def nav_item(page, text, key, active):
    cur = ' aria-current="page"' if key == active else ""
    soft = " nav-soft" if key == "apoya" else ""
    return f'<div class="nav-item{soft}"><div class="nav-top"><a href="{page}"{cur}>{text}</a></div></div>'

def header(active, fn):
    links = "".join(nav_item(page, NAV_EN[key] if L == "en" else text, key, active) for page, text, key in NAV)
    other = f"../{fn}" if L == "en" else f"en/{fn}"
    olang = "es" if L == "en" else "en"
    switch = f'<a class="lang-switch" href="{other}" hreflang="{olang}" lang="{olang}" aria-label="{t("switch_label")}">{t("switch")}</a>'
    return f'''<a class="skip" href="#main">{t("skip")}</a>
<header class="site-head">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="{t("home_label")}"><img src="assets/logo-white.png" alt="{t("logo_alt")}" width="409" height="161"></a>
    <nav class="nav" id="nav" aria-label="{t("nav")}">{links}</nav>
    {switch}
    <button class="menu-btn" aria-label="{t("open_menu")}" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  </div>
</header>'''

# Formulario único: va dentro de Súmate (apoya.html) y, en las demás páginas, en una ventana que se abre ahí mismo.
def form():
    opts = "".join(f'\n      <option value="{v}">{x}</option>' for v, x in zip(FORM_VALUES, t("form_opts")))
    ints = "".join(f'\n      <label><input type="checkbox" name="interes" value="{v}">{x}</label>' for v, x in zip(INTEREST_VALUES, t("interests")))
    return f'''<form class="form" novalidate>
  <label class="full">{t("form_q")}
    <select name="tipo" required>{opts}
    </select>
  </label>
  <label>{t("name")}<input name="nombre" required autocomplete="name"></label>
  <label>{t("org")}<input name="empresa" autocomplete="organization" placeholder="{t("optional")}"></label>
  <label>{t("email")}<input type="email" name="correo" required autocomplete="email"></label>
  <label>{t("phone")}<input type="tel" name="telefono" autocomplete="tel" placeholder="{t("optional")}"></label>
  <fieldset class="full">
    <legend>{t("interest")}</legend>
    <div class="interest">{ints}
    </div>
  </fieldset>
  <label class="full">{t("msg")}<textarea name="mensaje" placeholder="{t("msg_ph")}"></textarea></label>
  <div class="full row-cta"><button class="btn dark-btn" type="submit">{t("send")} {ICONS["arrow"]}</button><span class="note">{t("note")} {SITE["email"]}.</span></div>
  <p class="ok" hidden>{t("ok")} {SITE["email"]}.</p>
</form>'''

def contact_alt():
    wa = f' · <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a>' if WA else ""
    return f'<p class="sheet-alt">{t("direct")} <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>{wa}</p>'

# Ventanas que se abren sobre la página: el formulario y las historias.
# La X va fuera de .sheet-in para quedarse fija en la esquina mientras el contenido se desplaza.
def dialogs():
    return f'''<dialog class="sheet sheet-form" id="dlg-form" aria-labelledby="dlg-form-t">
  <button class="sheet-x" type="button" data-close aria-label="{t("close")}" autofocus>×</button>
  <div class="sheet-in">
    <div class="sheet-head"><span class="eyebrow">{t("dlg_eyebrow")}</span><h2 class="h-md" id="dlg-form-t" data-form-title>{t("dlg_title")}</h2><p>{t("dlg_text")}</p></div>
    {form()}
    {contact_alt()}
  </div>
</dialog>
<dialog class="sheet sheet-story" id="dlg-story" aria-label="{t("story")}">
  <button class="sheet-x" type="button" data-close aria-label="{t("close")}" autofocus>×</button>
  <div class="sheet-in">
    <div class="sheet-body"></div>
  </div>
</dialog>'''

def footer(fn):
    ig = f'<li><a href="{SITE["instagram"]}" target="_blank" rel="noopener">Instagram {handle(SITE["instagram"])}</a></li>' if SITE["instagram"] else ""
    ig7 = f'<li><a href="{SITE["instagram_seven"]}" target="_blank" rel="noopener">Seven Colombia {handle(SITE["instagram_seven"])}</a></li>' if SITE["instagram_seven"] else ""
    tel = f'<li><a href="{TEL}">{SITE["phone"]}</a></li>' if TEL else ""
    wa = f'<li><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></li>' if WA else ""
    explore = "".join(f'<li><a href="{h}">{x}</a></li>' for h, x in t("f_links"))
    join = "".join(f'<li><a {sumate(k)}>{x}</a></li>' for k, x in t("f_join"))
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="grid">
      <div>
        <img class="logo" src="assets/logo-white.png" alt="{t("logo_alt")}" width="409" height="161" loading="lazy">
        <p>{t("foot_about")}</p>
        {social()}
      </div>
      <div>
        <h4>{t("explore")}</h4>
        <ul>{explore}</ul>
      </div>
      <div>
        <h4>{t("join")}</h4>
        <ul>{join}<li><a href="apoya.html#beneficio">{t("tax")}</a></li></ul>
      </div>
      <div>
        <h4>{t("contact")}</h4>
        <ul>
          <li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
          {tel}{wa}{ig}{ig7}
          <li>Carrera 51 # 24-35, Bogotá D.C.</li>
          <li>NIT 901.965.467-5</li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>© <span data-year>2026</span> Fundación Sevenfold Colombia (FUNSEVEN). {t("legal")}</span>
      <span>{t("made")}</span>
    </div>
  </div>
</footer>
<div class="tricolor" aria-hidden="true"></div>
<div class="lb" hidden role="dialog" aria-modal="true" aria-label="{t("viewer")}">
  <button class="x" aria-label="{t("close")}">×</button><button class="pv" aria-label="{t("prev")}">‹</button><button class="nx" aria-label="{t("next")}">›</button>
  <figure style="margin:0"><img src="" alt=""><figcaption class="lb-cap" hidden></figcaption></figure>
  <span class="lb-count" aria-live="polite"></span>
</div>
{dialogs()}
<script>window.SITE={json.dumps({"email": SITE["email"], "instagram": SITE["instagram"]})}</script>
<script src="assets/js/main.js?v={VER}"></script>'''

FAVICON = "data:image/svg+xml," + ("%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230B1320'/%3E"
  "%3Cpath d='M50 20A22 22 0 1 0 52 40' fill='none' stroke='%231E7A4B' stroke-width='7' stroke-linecap='round'/%3E"
  "%3Cpath d='M44 13A22 22 0 0 1 53 27' fill='none' stroke='%23F2C40F' stroke-width='7' stroke-linecap='round'/%3E"
  "%3Ctext x='32' y='42' font-family='Arial Black,Arial' font-weight='900' font-size='26' text-anchor='middle' fill='%23fff'%3E7%3C/text%3E%3C/svg%3E")

def head(title, desc, fn):
    es, en = (f"../{fn}", fn) if L == "en" else (fn, f"en/{fn}")
    extra = f'\n<link rel="alternate" hreflang="es" href="{es}">\n<link rel="alternate" hreflang="en" href="{en}">'
    return f'''<!doctype html>
<html lang="{t("lang")}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0B1320">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/img/hero-seleccion.webp">
<meta property="og:locale" content="{t("locale")}">
<link rel="icon" href="{FAVICON}">{extra}
<link rel="preload" href="assets/fonts/big-shoulders-display-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/figtree-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/styles.css?v={VER}">
</head>
<body>'''

OPT = json.loads((ROOT/"assets/img/opt/manifest.json").read_text()) if (ROOT/"assets/img/opt/manifest.json").exists() else {}

def images(html):
    """srcset con las versiones optimizadas (assets/img/opt, generadas aparte) y carga diferida.
    La primera imagen de cada página (fondo del encabezado) carga de inmediato."""
    first = [True]
    def fix(m):
        tag = m.group(0)
        src = re.search(r'(data-src|src)="assets/img/([\w\-]+)\.webp"', tag)
        if src and src.group(2) in OPT and "srcset" not in tag:
            o = OPT[src.group(2)]
            cands = ", ".join(f"assets/img/opt/{src.group(2)}-{w}.webp {w}w" for w in o["v"]) + f", assets/img/{src.group(2)}.webp {o['w']}w"
            full = 'alt=""' in tag or "fetchpriority" in tag
            sizes = "100vw" if full else "(max-width: 760px) 100vw, 50vw"
            attr = "data-srcset" if src.group(1) == "data-src" else "srcset"
            tag = tag.replace("<img ", f'<img {attr}="{cands}" sizes="{sizes}" ', 1)
        if first[0]:
            first[0] = False
        elif "loading=" not in tag and "fetchpriority" not in tag and "data-src" not in tag:
            tag = tag.replace("<img ", '<img loading="lazy" ', 1)
        return tag
    return re.sub(r"<img [^>]*>", fix, html)

# === Contenido tipo blog: un archivo por historia (content/historias) y por resultado (content/palmares) ===
# Todos tienen la misma estructura; se editan a mano o desde el gestor de contenidos (.pages.yml).
from html import escape as esc
def load(folder):
    items = [json.loads(f.read_text()) for f in sorted((ROOT/"content"/folder).glob("*.json"))]
    return sorted([i for i in items if i.get("publicada", True)], key=lambda i: (i.get("orden", 99), i["id"]))
HISTORIAS = {h["id"]: h for h in load("historias")}
PALMARES = load("palmares")

def tr(item):
    """Versión del elemento en el idioma actual: en inglés, los campos de "en" reemplazan a los de español."""
    if L != "en" or not item.get("en"): return item
    out = dict(item); en = item["en"]
    for k, v in en.items():
        if k in ("fotos",) and isinstance(v, list):  # solo textos alternativos, en el mismo orden
            out[k] = [dict(f, alt=a) for f, a in zip(item[k], v)]
        elif k in ("portada", "foto") and isinstance(v, str):
            out[k] = dict(item[k], alt=v)
        else:
            out[k] = v
    return out

def img(f, extra=""):
    pos = f' style="object-position:{esc(f["pos"])}"' if f.get("pos") else ""
    return f'<img src="{esc(f["src"])}" alt="{esc(f.get("alt",""))}"{pos}{extra}>'

def pendiente(texto):
    return f'<p class="pendiente">{t("pending")}: {esc(texto)}</p>' if texto else ""

def story_card(h):
    h = tr(h)
    return (f'<a class="story" href="#historia-{h["id"]}" data-story="{h["id"]}">{img(h["portada"])}'
            f'<div class="in"><span class="kicker">{esc(h["etiqueta"])}</span><h3>{esc(h["titulo"])}</h3>'
            f'<p>{esc(h["resumen"])}</p><span class="go">{t("read_story")} <i>{ICONS["arrow"]}</i></span></div></a>')

def story_cards(linea=""):
    hs = [h for h in HISTORIAS.values() if not linea or h["linea"] in linea.split("+")]
    return f'<div class="stories rail" data-carousel aria-label="{t("stories")}">{"".join(story_card(h) for h in hs)}</div>'

def story_sheet(h):
    h = tr(h)
    k = h["id"]
    fotos = "".join(f'<figure class="pc-slide">{img(f)}</figure>' for f in h["fotos"])
    podios = ""
    if h.get("podios"):
        podios = '<ul class="tally">' + "".join(f'<li{" class=\"gold\"" if x.get("oro") else ""}>{esc(x["categoria"])} <b>{esc(x["resultado"])}</b></li>' for x in h["podios"]) + "</ul>"
    texto = "".join(f"<p>{esc(t)}</p>" for t in h["texto"])
    cita = f'<blockquote>“{esc(h["cita"]["texto"])}”<small>{esc(h["cita"]["fuente"])}</small></blockquote>' if h.get("cita") else ""
    cifras = ('<div class="stat-row">' + "".join(f'<div><b>{esc(c["valor"])}</b><span>{esc(c["texto"])}</span></div>' for c in h["cifras"]) + "</div>") if h.get("cifras") else ""
    ln = {"educacion": " ln-edu", "ambiente": " ln-amb"}.get(h["linea"], "")
    return (f'<template id="story-{k}">\n<article class="story-sheet{ln}">\n'
            f'  <div class="pc" data-pc aria-label="{t("photos")}: {esc(h["titulo"])}"><div class="pc-track">{fotos}</div></div>\n'
            f'  <div class="story-txt"><span class="eyebrow">{esc(h["etiqueta"])} · {esc(h["fecha"])}</span>'
            f'<h2 class="h-lg" id="st-{k}">{esc(h["titulo"])}</h2>{podios}<div class="prose">{texto}</div>{cita}{cifras}{pendiente(h.get("pendiente",""))}</div>\n'
            f'</article>\n</template>')

def stories_for(html):
    """Agrega a la página las historias que abre (data-story="x"): se leen en una ventana, sin salir de la página."""
    keys = list(dict.fromkeys(re.findall(r'data-story="([\w-]+)"', html)))
    for k in keys:
        if k not in HISTORIAS: raise SystemExit(f"falta la historia '{k}' en content/historias")
    return "\n".join(story_sheet(HISTORIAS[k]) for k in keys)

# Informes de gestión para descargar (assets/docs). Para sumar un año, agrega una fila.
INFORMES = [
  ("2025", "Informe de gestión y resultados", [("Español", "assets/docs/informe-gestion-2025-es.pdf"), ("English", "assets/docs/management-report-2025-en.pdf")]),
]
def informes():
    cards = []
    for year, title, files in INFORMES:
        title = t("report_title")
        if L == "en": files = files[::-1]
        links = "".join(f'<a class="btn{" ghost-dark" if i else ""}" href="{f}" download>{ICONS["download"]} {lang} · PDF</a>' for i, (lang, f) in enumerate(files))
        size = " · ".join(f'{lang}: {round((ROOT/f).stat().st_size/1048576,1)} MB' for lang, f in files)
        cards.append(f'<article class="report"><span class="report-year">{year}</span><div><h3>{title} {year}</h3><p>Fundación Sevenfold Colombia · {size}</p><div class="row-cta">{links}</div></div></article>')
    return '<div class="reports">' + "".join(cards) + "</div>"

COLOR = {"oro": "", "azul": " blue", "plata": " silver", "bronce": " bronze"}
def palmares():
    out = []
    for r in map(tr, PALMARES):
        if r.get("historia"): tag, attrs, go = "a", f' href="#historia-{r["historia"]}" data-story="{r["historia"]}"', t("read_the_story")
        elif r.get("album"): tag, attrs, go = "a", f' href="#galeria" data-album="{r["album"]}"', t("see_photos")
        else: tag, attrs, go = "article", "", ""
        go = f'<span class="go">{go} <i>{ICONS["arrow"]}</i></span>' if go else ""
        out.append(f'<{tag} class="result"{attrs}><div class="ph">{img(r["foto"])}<span class="medal{COLOR.get(r.get("color","oro"),"")}">{esc(r["medalla"])}</span></div>'
                   f'<div class="body"><div class="meta"><span>{esc(r["lugar"])}</span><span>{esc(r["fecha"])}</span></div><h3>{esc(r["titulo"])}</h3><p>{esc(r["texto"])}</p>{go}</div></{tag}>')
    return f'<div class="results rail" data-carousel aria-label="{t("palmares")}">{"".join(out)}</div>'

def reels(html):
    """Videos: cada uno lleva a su post de Instagram (data-ig="enlace del post"); vacío = perfil de la Fundación."""
    return re.sub(r'<figure class="reel" data-ig="([^"]*)">.*?</figure>',
                  lambda m: m.group(0).replace("{{ig-url}}", m.group(1) or SITE["instagram"]), html, flags=re.S)

def expand(html):
    html = re.sub(r"\{\{include:([\w\-]+\.html)\}\}", lambda m: (SRC/m.group(1)).read_text(), html)
    html = re.sub(r"\{\{historias(?::([\w+]+))?\}\}", lambda m: story_cards(m.group(1) or ""), html)
    html = html.replace("{{palmares}}", palmares()).replace("{{informes}}", informes())
    html += "\n" + stories_for(html)
    html = reels(html)
    html = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: ICONS[m.group(1)], html)
    html = re.sub(r"\{\{sumate:(\w+)\}\}", lambda m: sumate(m.group(1)), html)
    svg = (SRC/"_map.svg").read_text()
    if L == "en": svg = svg.replace("Mapa de Colombia con los territorios donde trabaja la Fundación Sevenfold: Chocó, Bogotá y Vaupés", "Map of Colombia showing where Fundación Sevenfold works: Chocó, Bogotá and Vaupés")
    html = html.replace("{{map}}", svg)
    html = html.replace("{{form}}", form()).replace("{{contact-alt}}", contact_alt())
    for k in ("instagram", "instagram_seven"):
        html = html.replace("{{%s-handle}}" % k, handle(SITE[k])).replace("{{%s}}" % k, SITE[k])
    html = html.replace("{{email}}", SITE["email"]).replace("{{phone}}", SITE["phone"]).replace("{{tel}}", TEL).replace("{{wa}}", WA)
    return images(html)

LINE = {"seven-colombia.html": "ln-dep", "educacion.html": "ln-edu", "ambiente.html": "ln-amb"}

def relocate(html):
    """Páginas en /en/: las rutas a assets/ suben un nivel."""
    return re.sub(r'((?:src|href|srcset|data-src|data-srcset|poster|content)="|, )assets/', r'\1../assets/', html)

for L in ("es", "en"):
    src, outdir = (SRC, ROOT) if L == "es" else (SRC/"en", ROOT/"en")
    if not src.exists(): continue
    outdir.mkdir(exist_ok=True)
    for fn, title, desc, key in PAGES:
        if L == "en": title, desc = PAGES_EN[fn]
        if not (src/fn).exists(): print("falta", src/fn); continue
        body = expand((src/fn).read_text())
        if "{{" in body: raise SystemExit(f"{L}/{fn}: marcador sin reemplazar: " + re.search(r"\{\{[^}]*\}\}", body).group(0))
        # color de la línea (deporte / educación / ambiente) para las páginas de cada línea
        line = LINE.get(fn, "")
        main_open = f'\n<main id="main" class="{line}">\n' if line else '\n<main id="main">\n'
        out = head(title, desc, fn) + "\n" + header(key, fn) + main_open + body + "\n</main>\n" + footer(fn) + "\n</body>\n</html>\n"
        if L == "en": out = relocate(out)
        (outdir/fn).write_text(out)
        print("ok", L, fn, len(out))
L = "es"

for fn, to in REDIRECTS.items():
    out = f'''<!doctype html>
<html lang="es-CO"><head><meta charset="utf-8"><title>Fundación Sevenfold Colombia</title>
<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={to}">
<script>location.replace("{to.split('#')[0]}" + location.search + "#{to.split('#')[1]}")</script></head>
<body><p><a href="{to}">Continuar</a></p></body></html>
'''
    (ROOT/fn).write_text(out)
    print("ok", fn, "→", to)

# Vista previa del sitio completo en docs/preview (fundacionsevenfold.com/preview/) mientras
# la portada del dominio muestra "en construcción". No se indexa en buscadores.
import shutil
PREVIEW = ROOT / "docs" / "preview"
if PREVIEW.exists():
    shutil.rmtree(PREVIEW)
PREVIEW.mkdir(parents=True)
shutil.copytree(ROOT / "assets", PREVIEW / "assets")
(PREVIEW / "en").mkdir()
for page in [*ROOT.glob("*.html"), *(ROOT/"en").glob("*.html")]:
    html = page.read_text()
    if 'name="robots"' not in html:
        html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
    (PREVIEW / page.relative_to(ROOT)).write_text(html)
(PREVIEW / ".nojekyll").write_text("")
print("ok vista previa en docs/preview")
