# Fundación Sevenfold Colombia · Sitio web

Sitio institucional de la Fundación Sevenfold Colombia (FUNSEVEN): deporte, educación y ambiente para niños y jóvenes de Bogotá, Huila, Vaupés y Chocó.

## Páginas
- `index.html` · Inicio
- `nosotros.html` · Propósito, historia, modelo, equipo y transparencia
- `seven-colombia.html` · Fútbol 7, categorías, palmarés y agenda 2026
- `impacto.html` · Cifras, historias y bitácora de actividades
- `apoya.html` · Donaciones, padrinazgo, patrocinio y beneficio tributario
- `contacto.html` · Formulario y datos de contacto
- `kings-league.html` · Historia dedicada: del barrio a la Kings League
- `merida-2025.html` · Historia dedicada: campeones en Mérida 2025

## Cómo editar
El sitio es 100 % estático (HTML, CSS y JS, sin dependencias).

- Textos de cada página: `src/*.html`
- Menú, pie de página y `<head>`: `build.py`
- Regenerar las páginas: `python3 build.py`
- Redes sociales y WhatsApp: bloque `SITE` al inicio de `assets/js/main.js`

## Publicar
Funciona en GitHub Pages, Netlify, Vercel o cualquier hosting estático.
En GitHub Pages: *Settings → Pages → Deploy from a branch → main / (root)*.

Pendientes de contenido: ver `LEEME.txt`.
