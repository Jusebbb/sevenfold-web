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
   "Fundación Sevenfold Colombia: llevamos el fútbol 7, la educación y oportunidades reales a niños y jóvenes de Bogotá, Huila, Vaupés y Chocó.", "inicio"),
  ("nosotros.html", "Nosotros | Fundación Sevenfold Colombia",
   "Equipo, propósito, misión, visión, valores, historia y hacia dónde va la Fundación Sevenfold Colombia.", "nosotros"),
  ("seven-colombia.html", "Seven Colombia · Fútbol 7 | Fundación Sevenfold",
   "Seven Colombia, avalada por la FIF7: Seven Bogotá F.C., Seven Vaupés F.C. y Seven Chocó. Categorías, palmarés, Kings League y temporada 2026.", "seven"),
  ("educacion.html", "Educación | Fundación Sevenfold Colombia",
   "La línea de educación de la Fundación Sevenfold: kits escolares, calzado y formación para niños y jóvenes de Vaupés y otros territorios.", "educacion"),
  ("ambiente.html", "Ambiente y desarrollo sostenible | Fundación Sevenfold Colombia",
   "Ambiente y desarrollo sostenible: iniciativas de conservación de la biodiversidad y cuidado del territorio de la Fundación Sevenfold.", "ambiente"),
  ("impacto.html", "Impacto e historias | Fundación Sevenfold Colombia",
   "Resultados 2025-2026, historias de jóvenes que llegaron lejos y la bitácora de acciones en Bogotá, Huila, Vaupés y Chocó.", "impacto"),
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

WA = f"https://wa.me/{SITE['whatsapp']}" if SITE["whatsapp"] else ""
TEL = "tel:" + re.sub(r"[^\d+]", "", SITE["phone"]) if SITE["phone"] else ""
def handle(url):  # "https://www.instagram.com/fundacion_sevenfold/" -> "@fundacion_sevenfold"
    return "@" + url.rstrip("/").rsplit("/", 1)[-1]

def social():
    items = [("instagram","ig","Instagram de la Fundación"),("facebook","fb","Facebook"),("youtube","yt","YouTube"),("tiktok","tt","TikTok"),("linkedin","in","LinkedIn")]
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

def header(active):
    links = "".join(nav_item(*n, active) for n in NAV)
    return f'''<a class="skip" href="#main">Saltar al contenido</a>
<header class="site-head">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="Fundación Sevenfold Colombia, inicio"><img src="assets/logo-white.png" alt="Fundación Sevenfold · Creemos en el futuro" width="409" height="161"></a>
    <nav class="nav" id="nav" aria-label="Principal">{links}</nav>
    <button class="menu-btn" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  </div>
</header>'''

# Formulario único: va dentro de Súmate (apoya.html) y, en las demás páginas, en una ventana que se abre ahí mismo.
FORM = f'''<form class="form" novalidate>
  <label class="full">¿Cómo quieres participar?
    <select name="tipo" required>
      <option value="Donación">Quiero donar</option>
      <option value="Apadrinar un talento">Quiero apadrinar un talento</option>
      <option value="Patrocinio">Soy empresa y quiero patrocinar</option>
      <option value="Donación en especie">Quiero donar en especie</option>
      <option value="Alianza">Quiero proponer una alianza</option>
      <option value="Voluntariado">Quiero ser voluntario</option>
      <option value="Inscripción de un deportista">Quiero inscribir a un niño o joven</option>
      <option value="Prensa">Prensa y medios</option>
      <option value="Otro">Otro tema</option>
    </select>
  </label>
  <label>Nombre completo<input name="nombre" required autocomplete="name"></label>
  <label>Empresa u organización<input name="empresa" autocomplete="organization" placeholder="Opcional"></label>
  <label>Correo<input type="email" name="correo" required autocomplete="email"></label>
  <label>Teléfono<input type="tel" name="telefono" autocomplete="tel" placeholder="Opcional"></label>
  <fieldset class="full">
    <legend>Me interesa apoyar en</legend>
    <div class="interest">
      <label><input type="checkbox" name="interes" value="Seven Colombia">Seven Colombia</label>
      <label><input type="checkbox" name="interes" value="Educación">Educación</label>
      <label><input type="checkbox" name="interes" value="Ambiente">Ambiente</label>
      <label><input type="checkbox" name="interes" value="Bogotá">Bogotá</label>
      <label><input type="checkbox" name="interes" value="Vaupés">Vaupés</label>
      <label><input type="checkbox" name="interes" value="Chocó">Chocó</label>
      <label><input type="checkbox" name="interes" value="Delegaciones internacionales">Viajes y torneos</label>
    </div>
  </fieldset>
  <label class="full">Mensaje<textarea name="mensaje" placeholder="Cuéntanos un poco más"></textarea></label>
  <div class="full row-cta"><button class="btn dark-btn" type="submit">Enviar mensaje {ICONS["arrow"]}</button><span class="note">Se abrirá tu correo con el mensaje listo para {SITE["email"]}.</span></div>
  <p class="ok" hidden>Abrimos tu aplicación de correo con el mensaje listo. Si no se abrió, escríbenos directamente a {SITE["email"]}.</p>
</form>'''

def contact_alt():
    wa = f' · <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a>' if WA else ""
    return f'<p class="sheet-alt">¿Prefieres escribir directo? <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>{wa}</p>'

# Ventanas que se abren sobre la página: el formulario y las historias.
# La X va fuera de .sheet-in para quedarse fija en la esquina mientras el contenido se desplaza.
FORM_DIALOG = f'''<dialog class="sheet sheet-form" id="dlg-form" aria-labelledby="dlg-form-t">
  <button class="sheet-x" type="button" data-close aria-label="Cerrar" autofocus>×</button>
  <div class="sheet-in">
    <div class="sheet-head"><span class="eyebrow">Súmate</span><h2 class="h-md" id="dlg-form-t" data-form-title>Hablemos</h2><p>Cuéntanos cómo quieres participar y te respondemos con una propuesta clara.</p></div>
    {FORM}
    {contact_alt()}
  </div>
</dialog>'''

STORY_DIALOG = '''<dialog class="sheet sheet-story" id="dlg-story" aria-label="Historia">
  <button class="sheet-x" type="button" data-close aria-label="Cerrar" autofocus>×</button>
  <div class="sheet-in">
    <div class="sheet-body"></div>
  </div>
</dialog>'''

def footer(fn):
    ig = f'<li><a href="{SITE["instagram"]}" target="_blank" rel="noopener">Instagram {handle(SITE["instagram"])}</a></li>' if SITE["instagram"] else ""
    ig7 = f'<li><a href="{SITE["instagram_seven"]}" target="_blank" rel="noopener">Seven Colombia {handle(SITE["instagram_seven"])}</a></li>' if SITE["instagram_seven"] else ""
    tel = f'<li><a href="{TEL}">{SITE["phone"]}</a></li>' if TEL else ""
    wa = f'<li><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></li>' if WA else ""
    dialogs = FORM_DIALOG + "\n" + STORY_DIALOG
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="grid">
      <div>
        <img class="logo" src="assets/logo-white.png" alt="Fundación Sevenfold · Creemos en el futuro" width="409" height="161" loading="lazy">
        <p>Entidad sin ánimo de lucro que transforma la vida de niños, niñas y jóvenes de Colombia a través del deporte, la educación y el desarrollo sostenible.</p>
        {social()}
      </div>
      <div>
        <h4>Explora</h4>
        <ul><li><a href="nosotros.html">Nosotros</a></li><li><a href="seven-colombia.html">Seven Colombia</a></li><li><a href="educacion.html">Educación</a></li><li><a href="ambiente.html">Ambiente</a></li><li><a href="impacto.html">Impacto e historias</a></li><li><a href="aliados.html">Aliados</a></li></ul>
      </div>
      <div>
        <h4>Súmate</h4>
        <ul><li><a {sumate("donar")}>Donar</a></li><li><a {sumate("apadrinar")}>Apadrinar un talento</a></li><li><a {sumate("especie")}>Donar en especie</a></li><li><a {sumate("patrocinar")}>Patrocinar</a></li><li><a {sumate("voluntariado")}>Voluntariado</a></li><li><a href="apoya.html#beneficio">Beneficio tributario</a></li></ul>
      </div>
      <div>
        <h4>Contacto</h4>
        <ul>
          <li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
          {tel}{wa}{ig}{ig7}
          <li>Carrera 51 # 24-35, Bogotá D.C.</li>
          <li>NIT 901.965.467-5</li>
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
  <figure style="margin:0"><img src="" alt=""><figcaption class="lb-cap" hidden></figcaption></figure>
  <span class="lb-count" aria-live="polite"></span>
</div>
{dialogs}
<script>window.SITE={json.dumps({"email": SITE["email"], "instagram": SITE["instagram"]})}</script>
<script src="assets/js/main.js?v={VER}"></script>'''

FAVICON = "data:image/svg+xml," + ("%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230B1320'/%3E"
  "%3Cpath d='M50 20A22 22 0 1 0 52 40' fill='none' stroke='%231E7A4B' stroke-width='7' stroke-linecap='round'/%3E"
  "%3Cpath d='M44 13A22 22 0 0 1 53 27' fill='none' stroke='%23F2C40F' stroke-width='7' stroke-linecap='round'/%3E"
  "%3Ctext x='32' y='42' font-family='Arial Black,Arial' font-weight='900' font-size='26' text-anchor='middle' fill='%23fff'%3E7%3C/text%3E%3C/svg%3E")

def head(title, desc, extra=""):
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

STORIES = (SRC/"_stories.html").read_text()

def stories_for(html):
    """Agrega a la página las historias que abre (data-story="x"): se leen en una ventana, sin salir de la página."""
    keys = list(dict.fromkeys(re.findall(r'data-story="([\w-]+)"', html)))
    out = []
    for k in keys:
        m = re.search(rf'<template id="story-{k}">.*?</template>', STORIES, re.S)
        if not m: raise SystemExit(f"falta la historia '{k}' en src/_stories.html")
        out.append(m.group(0))
    return "\n".join(out)

def reels(html):
    """Videos: cada uno lleva a su post de Instagram (data-ig="enlace del post"); vacío = perfil de la Fundación."""
    return re.sub(r'<figure class="reel" data-ig="([^"]*)">.*?</figure>',
                  lambda m: m.group(0).replace("{{ig-url}}", m.group(1) or SITE["instagram"]), html, flags=re.S)

def expand(html):
    html = re.sub(r"\{\{include:([\w\-]+\.html)\}\}", lambda m: (SRC/m.group(1)).read_text(), html)
    html += "\n" + stories_for(html)
    html = reels(html)
    html = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: ICONS[m.group(1)], html)
    html = re.sub(r"\{\{sumate:(\w+)\}\}", lambda m: sumate(m.group(1)), html)
    html = html.replace("{{map}}", (SRC/"_map.svg").read_text())
    html = html.replace("{{form}}", FORM).replace("{{contact-alt}}", contact_alt())
    for k in ("instagram", "instagram_seven"):
        html = html.replace("{{%s-handle}}" % k, handle(SITE[k])).replace("{{%s}}" % k, SITE[k])
    html = html.replace("{{email}}", SITE["email"]).replace("{{phone}}", SITE["phone"]).replace("{{tel}}", TEL).replace("{{wa}}", WA)
    return images(html)

LINE = {"seven-colombia.html": "ln-dep", "educacion.html": "ln-edu", "ambiente.html": "ln-amb"}

for fn, title, desc, key in PAGES:
    body = expand((SRC/fn).read_text())
    if "{{" in body: raise SystemExit(f"{fn}: marcador sin reemplazar: " + re.search(r"\{\{[^}]*\}\}", body).group(0))
    # color de la línea (deporte / educación / ambiente) para las páginas de cada línea
    line = LINE.get(fn, "")
    main_open = f'\n<main id="main" class="{line}">\n' if line else '\n<main id="main">\n'
    out = head(title, desc) + "\n" + header(key) + main_open + body + "\n</main>\n" + footer(fn) + "\n</body>\n</html>\n"
    (ROOT/fn).write_text(out)
    print("ok", fn, len(out))

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
for page in ROOT.glob("*.html"):
    html = page.read_text()
    if 'name="robots"' not in html:
        html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
    (PREVIEW / page.name).write_text(html)
(PREVIEW / ".nojekyll").write_text("")
print("ok vista previa en docs/preview")
