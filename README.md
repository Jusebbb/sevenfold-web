# Fundación Sevenfold Colombia · Sitio web

Sitio institucional de la Fundación Sevenfold Colombia (FUNSEVEN): deporte, educación y ambiente para niños y jóvenes de Bogotá, Huila, Vaupés y Chocó.

## Páginas (una pestaña del menú = una página)
- `index.html` · Inicio
- `nosotros.html` · Equipo, propósito, misión, visión, valores, historia y proyección
- `seven-colombia.html` · El aval (FIF7), clubes (Seven Bogotá F.C., Seven Vaupés F.C., Seven Chocó), categorías, palmarés, Kings League, temporada 2026 y galería
- `educacion.html` · Línea de educación
- `ambiente.html` · Línea de ambiente y desarrollo sostenible
- `impacto.html` · Cifras, historias y bitácora
- `aliados.html` · Respaldo institucional, marcas y organizaciones aliadas
- `apoya.html` · Súmate: formas de apoyar, patrocinio, beneficio tributario, preguntas y formulario de contacto

`contacto.html`, `kings-league.html` y `merida-2025.html` ya no son páginas: redirigen a donde quedó su contenido.

## Cómo funciona la navegación
- Las historias ("Leer historia") se abren en una ventana sobre la misma página (`src/_stories.html`).
- Los botones de donar, apadrinar, patrocinar, etc. abren el formulario ahí mismo (`{{sumate:tipo}}` en `src`).
- Las fotos van en carruseles con flechas a los lados (`class="pc" data-pc`).

## Cómo editar
El sitio es 100 % estático (HTML, CSS y JS, sin dependencias).

- Textos de cada página: `src/*.html`
- Historias que se abren en ventana: `src/_stories.html`
- Menú, pie de página, formulario, correo, teléfono, WhatsApp e Instagram: `build.py` (bloque `SITE`)
- Regenerar las páginas: `python3 build.py`

## Publicar
Funciona en GitHub Pages, Netlify, Vercel o cualquier hosting estático.
En GitHub Pages: *Settings → Pages → Deploy from a branch → main / (root)*.

Pendientes de contenido: ver `LEEME.txt`.
