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
const floatCta = document.querySelector(".float-cta");
const onScroll = () => {
  const y = window.scrollY;
  if (head && !head.classList.contains("always")) head.classList.toggle("solid", y > 40);
  if (floatCta) floatCta.classList.toggle("show", y > 700);
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

/* Hero: carrusel de fotos */
const slides = document.querySelectorAll(".hero-slides img");
if (slides.length > 1) {
  let i = 0;
  slides[0].classList.add("on");
  slides[0].parentElement.classList.add("ready");
  setInterval(() => {
    slides[i].classList.remove("on");
    i = (i + 1) % slides.length;
    slides[i].classList.add("on");
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

/* Galerías con visor (lightbox) */
const lb = document.querySelector(".lb");
if (lb) {
  const lbImg = lb.querySelector("img"), lbCap = lb.querySelector("p");
  let group = [], idx = 0, lastFocus = null;
  const show = () => { const b = group[idx]; const im = b.querySelector("img"); lbImg.src = im.currentSrc || im.src; lbImg.alt = im.alt; lbCap.textContent = im.alt; };
  document.querySelectorAll("[data-lb]").forEach(b => b.addEventListener("click", () => {
    group = [...document.querySelectorAll(`[data-lb="${b.dataset.lb}"]`)];
    idx = group.indexOf(b); lastFocus = b; show(); lb.hidden = false; lb.querySelector(".x").focus();
  }));
  const close = () => { lb.hidden = true; lastFocus && lastFocus.focus(); };
  lb.querySelector(".x").addEventListener("click", close);
  lb.querySelector(".pv").addEventListener("click", () => { idx = (idx - 1 + group.length) % group.length; show(); });
  lb.querySelector(".nx").addEventListener("click", () => { idx = (idx + 1) % group.length; show(); });
  lb.addEventListener("click", e => { if (e.target === lb) close(); });
  document.addEventListener("keydown", e => {
    if (lb.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowRight") lb.querySelector(".nx").click();
    if (e.key === "ArrowLeft") lb.querySelector(".pv").click();
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

/* Bitácora: filtros */
const fbtns = document.querySelectorAll(".filters button");
fbtns.forEach(b => b.addEventListener("click", () => {
  fbtns.forEach(x => x.setAttribute("aria-pressed", x === b));
  const f = b.dataset.f;
  document.querySelectorAll(".ev").forEach(ev => ev.hidden = f !== "all" && !ev.dataset.tags.includes(f));
}));

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
  const map = { donar: "Donación", apadrinar: "Apadrinar un talento", patrocinar: "Patrocinio", especie: "Donación en especie", voluntariado: "Voluntariado", alianza: "Alianza" };
  try { const t = new URLSearchParams(location.search).get("tipo"); if (t && map[t]) tipoSel.value = map[t]; } catch {}
}

/* Año actual */
document.querySelectorAll("[data-year]").forEach(s => s.textContent = new Date().getFullYear());
