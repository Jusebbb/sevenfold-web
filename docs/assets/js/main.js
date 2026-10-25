/* Fundación Sevenfold Colombia — interacciones del sitio
   Contacto y redes se editan en build.py (bloque SITE); aquí llegan como window.SITE. */
const SITE = window.SITE || { email: "fundacionsevenfold@gmail.com" };
document.documentElement.classList.add("js");
// Textos de la interfaz en el idioma de la página (<html lang="...">)
const EN = document.documentElement.lang.startsWith("en");
const TX = EN ? {
  closeMenu: "Close menu", openMenu: "Open menu", pick: "Choose item", goTo: (i, n) => `Go to ${i} of ${n}`,
  talk: "Let's talk", copied: "Copied", copy: "Copy", none: "Not specified", web: "Website (English)", contact: "Contact",
  name: "Name", org: "Company / organization", email: "Email", phone: "Phone", interest: "Interested in", prevPhoto: "Previous photo", nextPhoto: "Next photo", prev: "Previous", next: "Next",
  sending: "Sending…", sent: "Message sent! Thank you for writing to us. We'll get back to you soon by email.", kind: "Type of support", msg: "Message", page: "Page"
} : {
  closeMenu: "Cerrar menú", openMenu: "Abrir menú", pick: "Elegir elemento", goTo: (i, n) => `Ir al ${i} de ${n}`,
  talk: "Hablemos", copied: "Copiado", copy: "Copiar", none: "No especificado", web: "Sitio web", contact: "Contacto",
  name: "Nombre", org: "Empresa / organización", email: "Correo", phone: "Teléfono", interest: "Me interesa", prevPhoto: "Foto anterior", nextPhoto: "Foto siguiente", prev: "Anterior", next: "Siguiente",
  sending: "Enviando…", sent: "¡Mensaje enviado! Gracias por escribirnos. Te responderemos pronto a tu correo.", kind: "Tipo de apoyo", msg: "Mensaje", page: "Página"
};
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const ARROW = d => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${d}"/></svg>`;
const LEFT = ARROW("M15 6l-6 6 6 6"), RIGHT = ARROW("M9 6l6 6-6 6");
const button = (cls, label, html) => { const b = document.createElement("button"); b.type = "button"; b.className = cls; b.setAttribute("aria-label", label); b.innerHTML = html; return b; };

/* Header sólido al hacer scroll */
const head = document.querySelector(".site-head");
const onScroll = () => { if (head) head.classList.toggle("solid", window.scrollY > 40); };
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

/* Menú móvil */
const menuBtn = document.querySelector(".menu-btn");
if (menuBtn) {
  const setMenu = open => {
    document.body.classList.toggle("menu-open", open);
    menuBtn.setAttribute("aria-expanded", open);
    menuBtn.setAttribute("aria-label", open ? TX.closeMenu : TX.openMenu);
  };
  menuBtn.addEventListener("click", () => setMenu(!document.body.classList.contains("menu-open")));
  document.querySelectorAll(".nav a").forEach(a => a.addEventListener("click", () => setMenu(false)));
  document.addEventListener("keydown", e => { if (e.key === "Escape" && document.body.classList.contains("menu-open")) { setMenu(false); menuBtn.focus(); } });
}

/* Hero: fotos que rotan. Cada foto (data-src) se descarga un turno antes de que le toque
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

/* Visor de fotos (lightbox): se abre al tocar una foto de un carrusel.
   Cerrar con X, Esc o clic fuera; flechas y teclado; deslizar en móvil; contador 3/12; foco atrapado. */
let openLB = () => {};
const lb = document.querySelector(".lb");
if (lb) {
  const lbImg = lb.querySelector("img"), lbCap = lb.querySelector(".lb-cap"), lbCount = lb.querySelector(".lb-count");
  const btns = [...lb.querySelectorAll("button")];
  let group = [], idx = 0, lastFocus = null;
  const show = () => {
    const im = group[idx];
    lbImg.removeAttribute("style");
    // en grande va la foto original (src), no la versión reducida que eligió el carrusel
    lbImg.src = im.dataset.full || im.getAttribute("src") || im.currentSrc; lbImg.alt = im.alt;
    // nunca más grande que su tamaño real
    const fit = () => { if (lbImg.naturalWidth) lbImg.style.maxWidth = `min(${lbImg.naturalWidth}px, 100%)`; };
    lbImg.complete ? fit() : lbImg.addEventListener("load", fit, { once: true });
    const cap = (im.closest("figure")?.querySelector("figcaption")?.textContent || "").trim();
    lbCap.textContent = cap; lbCap.hidden = !cap;
    lbCount.textContent = group.length > 1 ? `${idx + 1} / ${group.length}` : "";
    lb.querySelector(".pv").hidden = lb.querySelector(".nx").hidden = group.length < 2;
  };
  const step = d => { idx = (idx + d + group.length) % group.length; show(); };
  openLB = (imgs, i, from) => {
    group = imgs; idx = i; lastFocus = from; show(); lb.hidden = false;
    document.documentElement.classList.add("lb-open"); lb.querySelector(".x").focus();
  };
  const close = () => { lb.hidden = true; document.documentElement.classList.remove("lb-open"); lastFocus && lastFocus.focus({ preventScroll: true }); };
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

/* Carrusel de fotos: una foto a la vez, flechas a los lados, contador, deslizar con el dedo y teclado.
   Las fotos cercanas se descargan solo cuando el carrusel está cerca de la pantalla.
   .fit = foto completa sobre un fondo difuminado (fotos verticales y horizontales mezcladas).
   data-autoplay="6000" = avanza solo hasta que la persona lo toca. */
const nearIO = "IntersectionObserver" in window ? new IntersectionObserver(es => es.forEach(e => {
  const api = e.target._pc; if (!api) return; api.near = e.isIntersecting; if (e.isIntersecting) api.refresh();
}), { rootMargin: "400px 0px" }) : null;
function initPC(pc) {
  if (pc._pc) return pc._pc;
  const track = pc.querySelector(".pc-track");
  const slidesEl = [...track.children], imgs = slidesEl.map(s => s.querySelector("img")), n = slidesEl.length;
  const api = { near: !nearIO };
  pc._pc = api;
  track.tabIndex = 0;
  track.setAttribute("role", "region");
  track.setAttribute("aria-roledescription", "carrusel");
  if (pc.getAttribute("aria-label")) track.setAttribute("aria-label", pc.getAttribute("aria-label"));
  let prev, next, count, auto = null;
  if (n > 1) {
    prev = button("pc-btn pc-prev", TX.prevPhoto, LEFT);
    next = button("pc-btn pc-next", TX.nextPhoto, RIGHT);
    count = document.createElement("span"); count.className = "pc-count"; count.setAttribute("aria-hidden", "true");
    pc.append(prev, next, count);
  }
  const w = () => track.clientWidth || 1;
  const cur = () => Math.min(n - 1, Math.max(0, Math.round(track.scrollLeft / w())));
  const go = i => { const j = ((i % n) + n) % n; track.scrollTo({ left: j * w(), behavior: reduced ? "auto" : "smooth" }); };
  const warm = c => [c - 1, c, c + 1].forEach(k => { const im = imgs[(k + n) % n]; if (im && im.loading === "lazy") im.loading = "eager"; });
  api.refresh = () => {
    const c = cur();
    if (count) count.textContent = `${c + 1} / ${n}`;
    slidesEl.forEach((s, k) => s.setAttribute("aria-hidden", String(k !== c)));
    if (api.near) warm(c);
  };
  api.go = go;
  const stop = () => { if (auto) { clearInterval(auto); auto = null; } };
  if (n > 1) {
    prev.addEventListener("click", () => { stop(); go(cur() - 1); });
    next.addEventListener("click", () => { stop(); go(cur() + 1); });
  }
  let raf; track.addEventListener("scroll", () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(api.refresh); }, { passive: true });
  track.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") { e.preventDefault(); stop(); go(cur() + 1); }
    if (e.key === "ArrowLeft") { e.preventDefault(); stop(); go(cur() - 1); }
    if (e.key === "Enter" && !pc.closest("dialog")) openLB(imgs, cur(), track);
  });
  track.addEventListener("pointerdown", stop, { passive: true });
  // tocar la foto la abre en grande (dentro de una historia ya se ve grande)
  imgs.forEach((im, i) => im.addEventListener("click", () => { if (!pc.closest("dialog")) openLB(imgs, i, track); }));
  if (pc.classList.contains("fit")) slidesEl.forEach((s, k) => {
    const im = imgs[k], set = () => s.style.setProperty("--bg", `url("${im.currentSrc || im.src}")`);
    im.complete && im.naturalWidth ? set() : im.addEventListener("load", set, { once: true });
  });
  const ms = +pc.dataset.autoplay;
  if (ms && n > 1 && !reduced) {
    auto = setInterval(() => {
      if (!api.near || document.hidden || pc.matches(":hover") || pc.contains(document.activeElement)) return;
      go(cur() + 1);
    }, ms);
  }
  addEventListener("resize", () => api.refresh());
  nearIO ? nearIO.observe(pc) : api.refresh();
  api.refresh();
  return api;
}
document.querySelectorAll("[data-pc]").forEach(initPC);
const refreshIn = el => el && el.querySelectorAll("[data-pc]").forEach(pc => pc._pc && pc._pc.refresh());

/* Carruseles de tarjetas: flechas a los lados, puntos debajo, teclado y arrastre con el dedo (scroll nativo). */
document.querySelectorAll("[data-carousel]").forEach(track => {
  const items = [...track.children];
  // .car-wrap = carrusel + puntos (ocupan un solo lugar en la cuadrícula de la sección)
  const outer = document.createElement("div"), box = document.createElement("div");
  outer.className = "car-wrap"; box.className = "car";
  track.before(outer); outer.append(box); box.append(track);
  track.tabIndex = 0;
  track.setAttribute("role", "region");
  track.setAttribute("aria-roledescription", "carrusel");
  const pv = button("car-btn car-prev", TX.prev, LEFT), nx = button("car-btn car-next", TX.next, RIGHT);
  box.append(pv, nx);
  const dotsBox = document.createElement("div");
  dotsBox.className = "car-dots";
  dotsBox.setAttribute("role", "group"); dotsBox.setAttribute("aria-label", TX.pick);
  dotsBox.innerHTML = items.map((_, i) => `<button type="button" aria-label="${TX.goTo(i + 1, items.length)}"></button>`).join("");
  box.after(dotsBox);
  const dots = [...dotsBox.children];
  // solo cuentan las tarjetas visibles (la bitácora se filtra ocultando tarjetas)
  const shown = () => items.filter(it => !it.hidden);
  const x0 = () => (shown()[0] || items[0]).offsetLeft;
  const go = i => { const s = shown(), it = s[Math.max(0, Math.min(s.length - 1, i))]; if (it) track.scrollTo({ left: it.offsetLeft - x0(), behavior: reduced ? "auto" : "smooth" }); };
  const current = () => { const s = shown(), x = track.scrollLeft; let best = 0; s.forEach((it, i) => { if (Math.abs(it.offsetLeft - x0() - x) < Math.abs(s[best].offsetLeft - x0() - x)) best = i; }); return best; };
  const update = () => {
    const scrollable = track.scrollWidth > track.clientWidth + 4;
    box.classList.toggle("scrollable", scrollable);
    dotsBox.hidden = !scrollable;
    dots.forEach((d, i) => d.hidden = items[i].hidden);
    const vis = dots.filter(d => !d.hidden), c = current(), end = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
    vis.forEach((d, i) => d.setAttribute("aria-current", String(end ? i === vis.length - 1 : i === c)));
    pv.disabled = track.scrollLeft <= 4; nx.disabled = end;
  };
  track._refresh = () => { track.scrollLeft = 0; update(); };
  dots.forEach((d, i) => d.addEventListener("click", () => go(shown().indexOf(items[i]))));
  pv.addEventListener("click", () => go(current() - 1));
  nx.addEventListener("click", () => go(current() + 1));
  track.addEventListener("keydown", e => {
    if (e.target !== track) return;
    if (e.key === "ArrowRight") { e.preventDefault(); go(current() + 1); }
    if (e.key === "ArrowLeft") { e.preventDefault(); go(current() - 1); }
  });
  let t; track.addEventListener("scroll", () => { cancelAnimationFrame(t); t = requestAnimationFrame(update); }, { passive: true });
  addEventListener("resize", update);
  update();
});

/* Territorios: pestañas + mapa */
const tabs = document.querySelectorAll(".terr-tabs [role=tab]");
function selectTerr(key) {
  tabs.forEach(t => t.setAttribute("aria-selected", t.dataset.k === key));
  document.querySelectorAll(".terr-panel").forEach(p => { p.hidden = p.dataset.k !== key; if (!p.hidden) refreshIn(p); });
  document.querySelectorAll(".map-box path[data-dep]").forEach(p => p.classList.toggle("dim", p.dataset.dep !== key));
}
tabs.forEach(t => t.addEventListener("click", () => selectTerr(t.dataset.k)));
document.querySelectorAll(".map-box [data-dep], .map-box .pin").forEach(el =>
  el.addEventListener("click", () => selectTerr(el.dataset.dep || el.dataset.k)));

/* Pestañas (clubes, álbumes de fotos): todo se muestra en el mismo lugar, sin cambiar de página */
document.querySelectorAll("[data-tabs]").forEach(list => {
  const tbs = [...list.querySelectorAll("[role=tab]")];
  const select = (t, focus) => {
    tbs.forEach(x => {
      const on = x === t;
      x.setAttribute("aria-selected", String(on)); x.tabIndex = on ? 0 : -1;
      const p = document.getElementById(x.getAttribute("aria-controls"));
      if (p) p.hidden = !on;
    });
    refreshIn(document.getElementById(t.getAttribute("aria-controls")));
    if (focus) t.focus();
  };
  tbs.forEach((t, i) => {
    t.addEventListener("click", () => select(t));
    t.addEventListener("keydown", e => {
      const j = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tbs.length - 1 }[e.key];
      if (j === undefined) return;
      e.preventDefault(); select(tbs[(j + tbs.length) % tbs.length], true);
    });
  });
  list._select = select;
});
// enlaces que abren un álbum de la galería (data-album="roma")
document.querySelectorAll("[data-album]").forEach(a => a.addEventListener("click", () => {
  const t = document.getElementById("a-" + a.dataset.album), list = t && t.closest("[data-tabs]");
  if (list && list._select) list._select(t);
}));

/* Ventanas sobre la página (historias y formulario). El botón "atrás" del celular las cierra. */
const dlgForm = document.getElementById("dlg-form"), dlgStory = document.getElementById("dlg-story");
let lastTrigger = null;
function openSheet(dlg, hash) {
  if (!dlg || typeof dlg.showModal !== "function") return false;
  if (!dlg.open) {
    lastTrigger = document.activeElement;
    dlg.showModal();
    if (hash) history.pushState({ sheet: dlg.id }, "", hash);
  }
  dlg.querySelector(".sheet-in").scrollTop = 0;
  return true;
}
function closeSheet(dlg) {
  if (!dlg.open) return;
  if (history.state && history.state.sheet === dlg.id) history.back();
  else { dlg.close(); if (/^#(historia-|escribenos)/.test(location.hash)) history.replaceState(null, "", location.pathname + location.search); }
}
addEventListener("popstate", () => document.querySelectorAll("dialog.sheet[open]").forEach(d => d.close()));
document.querySelectorAll("dialog.sheet").forEach(dlg => {
  dlg.addEventListener("click", e => { if (e.target === dlg || e.target.closest("[data-close]")) closeSheet(dlg); });
  dlg.addEventListener("cancel", e => { e.preventDefault(); closeSheet(dlg); });
  dlg.addEventListener("close", () => { if (lastTrigger && document.contains(lastTrigger)) lastTrigger.focus({ preventScroll: true }); });
});

// Historias: "Leer más" abre la historia completa aquí mismo
function openStory(key, push = true) {
  const tpl = document.getElementById("story-" + key);
  if (!tpl || !dlgStory) return false;
  const body = dlgStory.querySelector(".sheet-body");
  body.replaceChildren(tpl.content.cloneNode(true));
  const h = body.querySelector("h2[id]");
  if (h) dlgStory.setAttribute("aria-labelledby", h.id);
  if (!openSheet(dlgStory, push ? "#historia-" + key : null)) return false;
  body.querySelectorAll("[data-pc]").forEach(pc => { initPC(pc).near = true; pc._pc.refresh(); });
  return true;
}
document.querySelectorAll("[data-story]").forEach(a => a.addEventListener("click", e => {
  if (!openStory(a.dataset.story)) return;
  e.preventDefault();
  // data-to: dentro de la historia, baja hasta esa parte (p. ej. la historia de un jugador)
  const to = a.dataset.to && dlgStory.querySelector("#" + a.dataset.to);
  if (to) requestAnimationFrame(() => {
    const box = dlgStory.querySelector(".sheet-in");
    box.scrollTop = to.getBoundingClientRect().top - box.getBoundingClientRect().top + box.scrollTop - 16;
    to.classList.add("hi"); setTimeout(() => to.classList.remove("hi"), 1800);
  });
}));

// Formulario: donar, apadrinar, patrocinar... se abre aquí mismo con la opción ya elegida
const TIPOS = {
  donar: ["Donación", "Quiero donar"], apadrinar: ["Apadrinar un talento", "Apadrina un talento"],
  patrocinar: ["Patrocinio", "Patrocina con tu marca"], especie: ["Donación en especie", "Dona en especie"],
  voluntariado: ["Voluntariado", "Sé voluntario"], alianza: ["Alianza", "Construyamos juntos"],
  inscripcion: ["Inscripción de un deportista", "Inscribe a tu hijo"], prensa: ["Prensa", "Prensa y medios"]
};
if (EN) Object.entries({ donar: "I want to donate", apadrinar: "Sponsor a talent", patrocinar: "Sponsor with your brand", especie: "Donate in kind",
  voluntariado: "Volunteer with us", alianza: "Let's build together", inscripcion: "Sign up your child", prensa: "Press and media" })
  .forEach(([k, v]) => TIPOS[k][1] = v);
function openForm(tipo) {
  if (!dlgForm) return false;
  const t = TIPOS[tipo], form = dlgForm.querySelector("form");
  if (t) form.elements.tipo.value = t[0];
  dlgForm.querySelector("[data-form-title]").textContent = t ? t[1] : TX.talk;
  form.querySelector(".ok").hidden = true;
  return openSheet(dlgForm, "#escribenos");
}
document.querySelectorAll("[data-form]").forEach(a => a.addEventListener("click", e => { if (openForm(a.dataset.form)) e.preventDefault(); }));

// enlaces compartidos: …#historia-mitu o …#escribenos abren su ventana al cargar
const deep = location.hash.match(/^#historia-([\w-]+)$/);
if (deep) openStory(deep[1], false);
else if (location.hash === "#escribenos") openForm();

/* Preselección del formulario desde el enlace (apoya.html?tipo=donar#formulario) */
try {
  const t = TIPOS[new URLSearchParams(location.search).get("tipo")];
  if (t) document.querySelectorAll("#formulario select[name=tipo]").forEach(s => s.value = t[0]);
} catch {}

/* Formulario: envía el mensaje directo al correo de la Fundación (SITE.form, servicio FormSubmit).
   Si el envío falla, o si SITE.form está vacío, abre la aplicación de correo del visitante con el mensaje listo. */
document.querySelectorAll("form.form").forEach(form => {
  const ok = form.querySelector(".ok"), btn = form.querySelector("button[type=submit]");
  const mailText = ok ? ok.textContent : "";
  form.addEventListener("submit", async e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const d = new FormData(form);
    if (d.get("_honey")) return;  // campo oculto: solo lo llenan los robots
    const intereses = d.getAll("interes").join(", ") || TX.none;
    const asunto = `${TX.web} · ${d.get("tipo") || TX.contact} · ${d.get("nombre")}`;
    const show = text => { if (ok) { ok.textContent = text; ok.hidden = false; } };
    const mailto = () => {
      const cuerpo = [
        `${TX.name}: ${d.get("nombre")}`,
        d.get("empresa") ? `${TX.org}: ${d.get("empresa")}` : "",
        `${TX.email}: ${d.get("correo")}`,
        d.get("telefono") ? `${TX.phone}: ${d.get("telefono")}` : "",
        `${TX.interest}: ${intereses}`,
        "", d.get("mensaje") || ""
      ].filter(Boolean).join("\n");
      show(mailText);
      window.location.href = `mailto:${SITE.email}?subject=${encodeURIComponent(asunto)}&body=${encodeURIComponent(cuerpo)}`;
    };
    if (!SITE.form) return mailto();
    const label = btn ? btn.innerHTML : "";
    if (btn) { btn.disabled = true; btn.textContent = TX.sending; }
    try {
      const r = await fetch(SITE.form, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          _subject: asunto, _template: "table", _captcha: "false", _replyto: d.get("correo"), email: d.get("correo"),
          [TX.name]: d.get("nombre"), [TX.org]: d.get("empresa") || "—", [TX.phone]: d.get("telefono") || "—",
          [TX.kind]: d.get("tipo"), [TX.interest]: intereses, [TX.msg]: d.get("mensaje") || "—", [TX.page]: location.href
        })
      });
      const j = await r.json().catch(() => ({}));
      if (!r.ok || String(j.success) !== "true") throw new Error(j.message || r.status);
      form.reset();
      show(TX.sent);
    } catch {
      mailto();
    } finally {
      if (btn) { btn.disabled = false; btn.innerHTML = label; }
    }
  });
});

/* Copiar correo */
document.querySelectorAll("[data-copy]").forEach(b => b.addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(b.dataset.copy); b.textContent = TX.copied; }
  catch { const r = document.createRange(); r.selectNodeContents(b.previousElementSibling); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }
  setTimeout(() => b.textContent = TX.copy, 1800);
}));

/* Videos: se reproducen solo cuando están en pantalla (al tocarlos se abre Instagram) */
const vids = document.querySelectorAll(".reel video");
if ("IntersectionObserver" in window && vids.length) {
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) e.target.play().catch(() => {}); else e.target.pause();
  }), { threshold: .4 });
  vids.forEach(v => io.observe(v));
}

/* Aliados: franja de logos en movimiento (la lista se duplica para que el giro no tenga cortes) */
document.querySelectorAll("[data-marquee] .marquee-track").forEach(ul => {
  if (reduced) return;
  [...ul.children].forEach(li => { const c = li.cloneNode(true); c.setAttribute("aria-hidden", "true"); c.querySelectorAll("img").forEach(i => i.alt = ""); ul.append(c); });
  ul.classList.add("moving");
});

/* Bitácora: filtros (y preselección desde el enlace: impacto.html?f=educacion#bitacora) */
const fbtns = document.querySelectorAll(".filters button");
fbtns.forEach(b => b.addEventListener("click", () => {
  fbtns.forEach(x => x.setAttribute("aria-pressed", x === b));
  const f = b.dataset.f;
  document.querySelectorAll(".evc").forEach(ev => { ev.hidden = f !== "all" && !ev.dataset.tags.split(" ").includes(f); });
  const log = document.querySelector(".log2");
  if (log && log._refresh) log._refresh();
}));
/* Bitácora: la foto de cada jornada abre todas sus fotos en el visor */
document.querySelectorAll(".evc-ph[type=button]").forEach(b => b.addEventListener("click", () => {
  const imgs = [...b.parentElement.querySelectorAll(".evc-photos img")];
  if (imgs.length) openLB(imgs, 0, b);
}));
try { const f = new URLSearchParams(location.search).get("f"); const b = f && [...fbtns].find(x => x.dataset.f === f); if (b) b.click(); } catch {}

/* Recorrido de la página (Seven Colombia): marca la sección en la que vas */
const pnav = document.querySelector(".page-nav");
if (pnav && "IntersectionObserver" in window) {
  const links = [...pnav.querySelectorAll("a")], secs = links.map(a => document.querySelector(a.getAttribute("href"))).filter(Boolean);
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    const a = links.find(l => l.getAttribute("href") === "#" + e.target.id);
    links.forEach(l => l.toggleAttribute("aria-current", l === a));
    if (a) { const w = pnav.querySelector(".wrap"); w.scrollTo({ left: a.offsetLeft - 16, behavior: reduced ? "auto" : "smooth" }); }
  }), { rootMargin: "-45% 0px -50% 0px" });
  secs.forEach(s => io.observe(s));
}

/* Aparición suave al hacer scroll: encabezados y tarjetas entran en escalonado */
if ("IntersectionObserver" in window && !reduced) {
  const sel = ".sec-head, .problem > *, .lines > *, .s7 > *, .territory > *, .car-wrap, .cta-band .in, .feature > *, .duo > *, .goals > *, .gives, .sponsor, .gways > *, .tax-note, .steps > *, .tl-item, .aval > li, .aval-why, .club-tabs, .club-panel, .backers > *, .logos > *, .orgs > *, .contact > *, .next-note, .mv > *, .values > li, .goals4 > li, .focus-strip, .kings > *";
  const els = [...document.querySelectorAll(sel)].filter(el => !el.closest("dialog, template") && el.getBoundingClientRect().top > innerHeight);
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

/* Año actual */
document.querySelectorAll("[data-year]").forEach(s => s.textContent = new Date().getFullYear());

/* Cifras como contador: al aparecer en pantalla suben desde 0 hasta su valor (data-count) */
const counters = document.querySelectorAll("[data-count]");
if (counters.length) {
  const fmt = n => n.toLocaleString("es-CO");
  const run = el => {
    const to = +el.dataset.count, suf = el.dataset.suffix || "", t0 = performance.now(), dur = 1600;
    const tick = t => { const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(Math.round(to * e)) + (k === 1 ? suf : ""); if (k < 1) requestAnimationFrame(tick); };
    requestAnimationFrame(tick);
  };
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if ("IntersectionObserver" in window && !reducedMotion) {
    counters.forEach(el => { el.textContent = "0"; });
    const cio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { run(e.target); cio.unobserve(e.target); } }), { threshold: .4 });
    counters.forEach(el => cio.observe(el));
  }
}
