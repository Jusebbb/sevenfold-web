/* Fundación Sevenfold Colombia — interacciones del sitio */

/* === CONFIGURACIÓN EDITABLE ===
   Completa aquí los enlaces reales de redes y el WhatsApp. Los que queden vacíos se ocultan solos. */
const SITE = {
  email: "fundacionsevenfold@gmail.com",
  whatsapp: "",            // ej: "573001234567" (solo números, con indicativo 57)
  social: {
    instagram: "",         // ej: "https://instagram.com/usuario"
    facebook: "",
    youtube: "",
    tiktok: "",
    linkedin: ""
  }
};

document.documentElement.classList.add("js");

/* Header sólido al hacer scroll */
const head = document.querySelector(".site-head");
const onScroll = () => {
  if (head && !head.classList.contains("always")) head.classList.toggle("solid", window.scrollY > 40);
};
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

/* Menú móvil */
const menuBtn = document.querySelector(".menu-btn");
if (menuBtn) {
  menuBtn.addEventListener("click", () => {
    const open = document.body.classList.toggle("menu-open");
    menuBtn.setAttribute("aria-expanded", open);
  });
  document.querySelectorAll(".nav a").forEach(a => a.addEventListener("click", () => {
    document.body.classList.remove("menu-open");
    menuBtn.setAttribute("aria-expanded", "false");
  }));
}

/* Menú: desplegables con lo que hay en cada pestaña.
   Con mouse se abren al pasar por encima (CSS); la flechita los abre con clic, toque o teclado. */
const subBtns = document.querySelectorAll(".sub-btn");
const closeSubs = (except) => subBtns.forEach(b => {
  if (b === except) return;
  b.setAttribute("aria-expanded", "false");
  b.closest(".nav-item").classList.remove("open");
});
subBtns.forEach(b => b.addEventListener("click", () => {
  const open = b.getAttribute("aria-expanded") !== "true";
  closeSubs(b);
  b.setAttribute("aria-expanded", open);
  b.closest(".nav-item").classList.toggle("open", open);
}));
document.querySelectorAll(".nav-item").forEach(item => item.addEventListener("focusout", e => {
  if (!item.contains(e.relatedTarget) && !matchMedia("(max-width:1020px)").matches) closeSubs();
}));
// al elegir una sección de la misma página, el desplegable se cierra aunque el mouse siga encima
document.querySelectorAll(".sub a").forEach(a => a.addEventListener("click", () => {
  closeSubs();
  const item = a.closest(".nav-item");
  item.classList.add("hush");
  item.addEventListener("mouseleave", () => item.classList.remove("hush"), { once: true });
}));
document.addEventListener("click", e => { if (!e.target.closest(".nav-item")) closeSubs(); });
document.addEventListener("keydown", e => {
  const b = document.querySelector('.sub-btn[aria-expanded="true"]');
  if (e.key === "Escape" && b) { closeSubs(); b.focus(); }
});

/* Hero: carrusel de fotos. Cada foto (data-src) se descarga un turno antes de que le toque
   y solo entra cuando ya cargó; si la conexión va lenta, la foto actual espera. */
const slides = document.querySelectorAll(".hero-slides img");
if (slides.length > 1) {
  let i = 0;
  const load = n => { const im = slides[n]; if (im.dataset.src) { if (im.dataset.srcset) { im.srcset = im.dataset.srcset; im.removeAttribute("data-srcset"); } im.src = im.dataset.src; im.removeAttribute("data-src"); } };
  slides[0].classList.add("on");
  slides[0].parentElement.classList.add("ready");
  load(1);
  setInterval(() => {
    const n = (i + 1) % slides.length;
    if (!slides[n].complete || !slides[n].naturalWidth) return;
    slides[i].classList.remove("on");
    slides[n].classList.add("on");
    i = n;
    load((i + 1) % slides.length);
  }, 7000);
}

/* Territorios: pestañas + mapa */
const tabs = document.querySelectorAll(".terr-tabs [role=tab]");
function selectTerr(key) {
  tabs.forEach(t => t.setAttribute("aria-selected", t.dataset.k === key));
  document.querySelectorAll(".terr-panel").forEach(p => p.hidden = p.dataset.k !== key);
  document.querySelectorAll(".map-box path[data-dep]").forEach(p => p.classList.toggle("dim", p.dataset.dep !== key));
}
tabs.forEach(t => t.addEventListener("click", () => selectTerr(t.dataset.k)));
document.querySelectorAll(".map-box [data-dep], .map-box .pin").forEach(el =>
  el.addEventListener("click", () => selectTerr(el.dataset.dep || el.dataset.k)));

/* Galerías con visor (lightbox).
   Pie de foto solo si el botón trae data-caption con texto real (el alt no se muestra).
   Cerrar con X, Esc o clic fuera; flechas y teclado; deslizar en móvil; contador 3/12; foco atrapado. */
const lb = document.querySelector(".lb");
if (lb) {
  const lbImg = lb.querySelector("img"), lbCap = lb.querySelector(".lb-cap"), lbCount = lb.querySelector(".lb-count");
  const btns = [...lb.querySelectorAll("button")];
  let group = [], idx = 0, lastFocus = null;
  const show = () => {
    const b = group[idx], im = b.querySelector("img");
    lbImg.removeAttribute("style");
    lbImg.src = im.dataset.full || im.currentSrc || im.src; lbImg.alt = im.alt;
    // nunca más grande que su tamaño real
    const fit = () => { if (lbImg.naturalWidth) lbImg.style.maxWidth = `min(${lbImg.naturalWidth}px, 100%)`; };
    lbImg.complete ? fit() : lbImg.addEventListener("load", fit, { once: true });
    const cap = (b.dataset.caption || "").trim();
    lbCap.textContent = cap; lbCap.hidden = !cap;
    lbCount.textContent = group.length > 1 ? `${idx + 1} / ${group.length}` : "";
    lb.querySelector(".pv").hidden = lb.querySelector(".nx").hidden = group.length < 2;
  };
  const step = d => { idx = (idx + d + group.length) % group.length; show(); };
  document.querySelectorAll("[data-lb]").forEach(b => b.addEventListener("click", () => {
    group = [...document.querySelectorAll(`[data-lb="${b.dataset.lb}"]`)];
    idx = group.indexOf(b); lastFocus = b; show(); lb.hidden = false;
    document.body.style.overflow = "hidden"; lb.querySelector(".x").focus();
  }));
  const close = () => { lb.hidden = true; document.body.style.overflow = ""; lastFocus && lastFocus.focus(); };
  lb.querySelector(".x").addEventListener("click", close);
  lb.querySelector(".pv").addEventListener("click", () => step(-1));
  lb.querySelector(".nx").addEventListener("click", () => step(1));
  lb.addEventListener("click", e => { if (e.target === lb || e.target.tagName === "FIGURE") close(); });
  document.addEventListener("keydown", e => {
    if (lb.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowRight") step(1);
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "Tab") { // foco atrapado dentro del visor
      const vis = btns.filter(x => !x.hidden), i = vis.indexOf(document.activeElement);
      e.preventDefault(); vis[(i + (e.shiftKey ? -1 : 1) + vis.length) % vis.length].focus();
    }
  });
  let x0 = null;
  lb.addEventListener("touchstart", e => { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", e => {
    if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 45 && group.length > 1) step(dx < 0 ? 1 : -1);
  });
}

/* Reels: se reproducen solo cuando están en pantalla */
const vids = document.querySelectorAll(".reel video");
if ("IntersectionObserver" in window && vids.length) {
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) e.target.play().catch(() => {}); else e.target.pause();
  }), { threshold: .4 });
  vids.forEach(v => io.observe(v));
}

/* Bitácora: filtros (y preselección desde el enlace: impacto.html?f=educacion#bitacora) */
const fbtns = document.querySelectorAll(".filters button");
fbtns.forEach(b => b.addEventListener("click", () => {
  fbtns.forEach(x => x.setAttribute("aria-pressed", x === b));
  const f = b.dataset.f;
  document.querySelectorAll(".ev").forEach(ev => ev.hidden = f !== "all" && !ev.dataset.tags.includes(f));
}));
try { const f = new URLSearchParams(location.search).get("f"); const b = f && [...fbtns].find(x => x.dataset.f === f); if (b) b.click(); } catch {}

/* Aparición suave al hacer scroll: encabezados y tarjetas entran en escalonado */
if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const sel = ".sec-head, .problem > *, .lines > *, .results > *, .stories > *, .territory > *, .reels, .allies, .cta-band .in, .feature > *, .duo > *, .cats > *, .model > *, .team > *, .goals > *, .ways > *, .gives > *, .sponsor, .gways > *, .tax-note, .packs > *, .steps > *, .tl-item, .ev";
  const els = [...document.querySelectorAll(sel)].filter(el => el.getBoundingClientRect().top > innerHeight);
  const reveal = el => {
    if (!el.classList.contains("pre")) return;
    el.classList.remove("pre"); ro.unobserve(el);
    // al terminar, devuelve el elemento a sus transiciones propias (hover de tarjetas)
    setTimeout(() => { el.classList.remove("rv"); el.style.transitionDelay = ""; }, 1300);
  };
  const ro = new IntersectionObserver(es => es.forEach(e => e.isIntersecting && reveal(e.target)), { rootMargin: "0px 0px -8% 0px" });
  // respaldo: si se baja muy rápido (tecla Fin, anclas), nada queda oculto por encima de la pantalla
  let tick = 0;
  addEventListener("scroll", () => { if (tick) return; tick = setTimeout(() => {
    tick = 0; document.querySelectorAll(".rv.pre").forEach(el => { if (el.getBoundingClientRect().top < innerHeight) reveal(el); });
  }, 150); }, { passive: true });
  els.forEach(el => {
    const sibs = [...el.parentElement.children].filter(c => c.classList.contains("rv") || els.includes(c));
    el.style.transitionDelay = Math.min(sibs.indexOf(el), 5) * 70 + "ms";
    el.classList.add("rv", "pre"); ro.observe(el);
  });
}

/* Formulario: arma un correo con la información (sitio informativo, sin servidor) */
document.querySelectorAll("form.form").forEach(form => {
  form.addEventListener("submit", e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const d = new FormData(form);
    const intereses = d.getAll("interes").join(", ") || "No especificado";
    const asunto = `Sitio web · ${d.get("tipo") || "Contacto"} · ${d.get("nombre")}`;
    const cuerpo = [
      `Nombre: ${d.get("nombre")}`,
      d.get("empresa") ? `Empresa / organización: ${d.get("empresa")}` : "",
      `Correo: ${d.get("correo")}`,
      d.get("telefono") ? `Teléfono: ${d.get("telefono")}` : "",
      `Me interesa: ${intereses}`,
      "", d.get("mensaje") || ""
    ].filter(Boolean).join("\n");
    const ok = form.querySelector(".ok");
    if (ok) { ok.hidden = false; }
    window.location.href = `mailto:${SITE.email}?subject=${encodeURIComponent(asunto)}&body=${encodeURIComponent(cuerpo)}`;
  });
});

/* Copiar correo */
document.querySelectorAll("[data-copy]").forEach(b => b.addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(b.dataset.copy); b.textContent = "Copiado"; }
  catch { const r = document.createRange(); r.selectNodeContents(b.previousElementSibling); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }
  setTimeout(() => b.textContent = "Copiar", 1800);
}));

/* Redes y WhatsApp desde la configuración */
document.querySelectorAll("[data-social]").forEach(a => {
  const url = SITE.social[a.dataset.social];
  if (url) a.href = url; else a.remove();
});
document.querySelectorAll(".social").forEach(s => { if (!s.children.length) s.remove(); });
document.querySelectorAll("[data-wa]").forEach(a => {
  if (SITE.whatsapp) a.href = `https://wa.me/${SITE.whatsapp}`; else a.remove();
});

if (!SITE.whatsapp) document.querySelectorAll("[data-wa-row]").forEach(r => r.remove());

/* Preselección del formulario desde el enlace (contacto.html?tipo=donar) */
const tipoSel = document.getElementById("f-tipo");
if (tipoSel) {
  const map = { donar: "Donación", apadrinar: "Apadrinar un talento", patrocinar: "Patrocinio", especie: "Donación en especie", voluntariado: "Voluntariado", alianza: "Alianza", inscripcion: "Inscripción de un deportista", prensa: "Prensa" };
  try { const t = new URLSearchParams(location.search).get("tipo"); if (t && map[t]) tipoSel.value = map[t]; } catch {}
}

/* Año actual */
document.querySelectorAll("[data-year]").forEach(s => s.textContent = new Date().getFullYear());

/* Carruseles: puntos, flechas (escritorio), teclado y arrastre con el dedo (scroll nativo con snap). */
document.querySelectorAll("[data-carousel]").forEach((track, n) => {
  const items = [...track.children];
  track.tabIndex = 0;
  track.setAttribute("role", "region");
  track.setAttribute("aria-roledescription", "carrusel");
  const arrow = d => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${d}"/></svg>`;
  const ui = document.createElement("div");
  ui.className = "car-ui";
  ui.innerHTML = `<div class="car-dots" role="group" aria-label="Elegir elemento">${items.map((_, i) => `<button type="button" aria-label="Ir al ${i + 1} de ${items.length}"></button>`).join("")}</div>
    <div class="car-arrows"><button type="button" class="pv" aria-label="Anterior">${arrow("M15 6l-6 6 6 6")}</button><button type="button" class="nx" aria-label="Siguiente">${arrow("M9 6l6 6-6 6")}</button></div>`;
  track.after(ui);
  const dots = [...ui.querySelectorAll(".car-dots button")];
  const pv = ui.querySelector(".pv"), nx = ui.querySelector(".nx");
  const go = i => { const it = items[Math.max(0, Math.min(items.length - 1, i))]; track.scrollTo({ left: it.offsetLeft - items[0].offsetLeft, behavior: "smooth" }); };
  const current = () => { const x = track.scrollLeft; let best = 0; items.forEach((it, i) => { if (Math.abs(it.offsetLeft - items[0].offsetLeft - x) < Math.abs(items[best].offsetLeft - items[0].offsetLeft - x)) best = i; }); return best; };
  const update = () => {
    const scrollable = track.scrollWidth > track.clientWidth + 4;
    ui.hidden = !scrollable;
    const c = current(), end = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
    dots.forEach((d, i) => d.setAttribute("aria-current", String(end ? i === items.length - 1 : i === c)));
    pv.disabled = track.scrollLeft <= 4; nx.disabled = end;
  };
  dots.forEach((d, i) => d.addEventListener("click", () => go(i)));
  pv.addEventListener("click", () => go(current() - 1));
  nx.addEventListener("click", () => go(current() + 1));
  track.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") { e.preventDefault(); go(current() + 1); }
    if (e.key === "ArrowLeft") { e.preventDefault(); go(current() - 1); }
  });
  let t; track.addEventListener("scroll", () => { cancelAnimationFrame(t); t = requestAnimationFrame(update); }, { passive: true });
  addEventListener("resize", update);
  update();
});
