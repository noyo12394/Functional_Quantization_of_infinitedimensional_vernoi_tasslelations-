// ============================================================
//  app.js — hand-rolled, dependency-free SVG charts + UI
// ============================================================
const SVGNS = "http://www.w3.org/2000/svg";
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const el = (tag, attrs = {}, kids = []) => {
  const n = document.createElementNS(SVGNS, tag);
  for (const k in attrs) n.setAttribute(k, attrs[k]);
  (Array.isArray(kids) ? kids : [kids]).forEach(c =>
    n.appendChild(typeof c === "string" ? document.createTextNode(c) : c));
  return n;
};
const fmt = (v, d = 3) => (+v).toFixed(d);
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

// ---- tooltip ----
let TIP;
function tip() {
  if (!TIP) { TIP = document.createElement("div"); TIP.className = "tooltip"; document.body.appendChild(TIP); }
  return TIP;
}
function showTip(html, e) {
  const t = tip(); t.innerHTML = html; t.style.opacity = 1;
  const pad = 14;
  t.style.left = Math.min(e.clientX + pad, innerWidth - t.offsetWidth - 8) + "px";
  t.style.top = (e.clientY + pad) + "px";
}
function hideTip() { if (TIP) TIP.style.opacity = 0; }

// ============================================================
//  Horizontal bar chart (composite leaderboard)
// ============================================================
function barChart(mount, data, opts = {}) {
  const host = typeof mount === "string" ? $(mount) : mount;
  if (!host) return;
  const W = host.clientWidth || 760, rowH = opts.rowH || 34, padL = opts.padL || 132,
        padR = 56, padT = 8, padB = 8;
  const H = padT + padB + data.length * rowH;
  const max = Math.max(...data.map(d => d.value)) * 1.08;
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%", height: H, class: "chart" });
  data.forEach((d, i) => {
    const y = padT + i * rowH;
    const bw = (W - padL - padR) * (d.value / max);
    const g = el("g", { class: "barrow" });
    g.appendChild(el("text", { x: padL - 10, y: y + rowH / 2 + 4, "text-anchor": "end", class: "lbl" }, d.label));
    const track = el("rect", { x: padL, y: y + 6, width: W - padL - padR, height: rowH - 14, rx: 6, class: "track" });
    const bar = el("rect", { x: padL, y: y + 6, width: 0, height: rowH - 14, rx: 6, fill: d.color || css("--accent") });
    const val = el("text", { x: padL + bw + 8, y: y + rowH / 2 + 4, class: "val", opacity: 0 }, opts.valFmt ? opts.valFmt(d.value) : fmt(d.value));
    g.append(track, bar, val);
    g.addEventListener("mousemove", e => showTip(`<b>${d.full || d.label}</b><br>${opts.tipLabel || "value"}: <b>${opts.valFmt ? opts.valFmt(d.value) : d.value}</b>${d.extra ? "<br>" + d.extra : ""}`, e));
    g.addEventListener("mouseleave", hideTip);
    svg.appendChild(g);
    requestAnimationFrame(() => {
      setTimeout(() => {
        bar.style.transition = "width .9s cubic-bezier(.2,.7,.2,1)";
        bar.setAttribute("width", bw);
        val.style.transition = "opacity .6s ease .5s"; val.setAttribute("opacity", 1);
      }, 60 + i * 45);
    });
  });
  host.innerHTML = ""; host.appendChild(svg);
}

// ============================================================
//  Multi-series line chart (log-log timing vs R)
// ============================================================
function lineChart(mount, opts) {
  const host = typeof mount === "string" ? $(mount) : mount;
  if (!host) return;
  const series = opts.series;
  const W = host.clientWidth || 760, H = opts.height || 440;
  const padL = 64, padR = 18, padT = 18, padB = 46;
  const xs = opts.x, logY = opts.logY;
  const allY = series.flatMap(s => s.y);
  const yMin = logY ? Math.max(1e-4, Math.min(...allY)) : 0;
  const yMax = Math.max(...allY);
  const xMin = Math.min(...xs), xMax = Math.max(...xs);
  const lx = v => Math.log10(v);
  const X = v => padL + (W - padL - padR) * (lx(v) - lx(xMin)) / (lx(xMax) - lx(xMin));
  const Y = v => {
    if (logY) return padT + (H - padT - padB) * (1 - (lx(v) - lx(yMin)) / (lx(yMax) - lx(yMin)));
    return padT + (H - padT - padB) * (1 - (v - yMin) / (yMax - yMin));
  };
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%", height: H, class: "chart" });
  // gridlines
  const yticks = logY ? [0.001, 0.01, 0.1, 1, 10, 100] : niceTicks(yMin, yMax, 5);
  yticks.filter(t => t >= yMin && t <= yMax).forEach(t => {
    svg.appendChild(el("line", { x1: padL, x2: W - padR, y1: Y(t), y2: Y(t), class: "grid" }));
    svg.appendChild(el("text", { x: padL - 8, y: Y(t) + 3, "text-anchor": "end", class: "axis" }, logY ? (t < 1 ? t.toString() : t + "") : fmt(t, 2)));
  });
  xs.forEach(t => {
    svg.appendChild(el("text", { x: X(t), y: H - padB + 18, "text-anchor": "middle", class: "axis" }, t.toString()));
  });
  svg.appendChild(el("text", { x: (W) / 2, y: H - 6, "text-anchor": "middle", class: "axis-title" }, opts.xlabel || ""));
  svg.appendChild(el("text", { x: 16, y: H / 2, "text-anchor": "middle", class: "axis-title", transform: `rotate(-90 16 ${H / 2})` }, opts.ylabel || ""));
  // series
  series.forEach((s, si) => {
    const d = xs.map((xv, i) => `${i ? "L" : "M"}${X(xv)},${Y(s.y[i])}`).join(" ");
    const path = el("path", { d, fill: "none", stroke: s.color, "stroke-width": s.width || 2.4, "stroke-linejoin": "round", class: "spark", "data-len": 1 });
    svg.appendChild(path);
    const len = path.getTotalLength ? 1 : 1;
    path.style.strokeDasharray = "2000"; path.style.strokeDashoffset = "2000";
    requestAnimationFrame(() => { path.style.transition = `stroke-dashoffset 1.1s ease ${si * 0.08}s`; path.style.strokeDashoffset = "0"; });
    xs.forEach((xv, i) => {
      const c = el("circle", { cx: X(xv), cy: Y(s.y[i]), r: 3.4, fill: s.color, class: "dot" });
      c.addEventListener("mousemove", e => showTip(`<b>${s.name}</b><br>R = ${xv}<br>time: <b>${fmt(s.y[i], 4)} s</b>`, e));
      c.addEventListener("mouseleave", hideTip);
      svg.appendChild(c);
    });
  });
  host.innerHTML = ""; host.appendChild(svg);
}
function niceTicks(min, max, n) {
  const step = (max - min) / n, out = [];
  for (let i = 0; i <= n; i++) out.push(min + step * i);
  return out;
}

// ============================================================
//  Scatter (time vs quality Pareto)
// ============================================================
function scatter(mount, pts, opts = {}) {
  const host = typeof mount === "string" ? $(mount) : mount;
  if (!host) return;
  const W = host.clientWidth || 760, H = opts.height || 440;
  const padL = 60, padR = 20, padT = 18, padB = 48;
  const xMax = Math.max(...pts.map(p => p.x)) * 1.1;
  const yMax = Math.max(...pts.map(p => p.y)) * 1.12;
  const X = v => padL + (W - padL - padR) * (v / xMax);
  const Y = v => padT + (H - padT - padB) * (1 - v / yMax);
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%", height: H, class: "chart" });
  niceTicks(0, yMax, 5).forEach(t => {
    svg.appendChild(el("line", { x1: padL, x2: W - padR, y1: Y(t), y2: Y(t), class: "grid" }));
    svg.appendChild(el("text", { x: padL - 8, y: Y(t) + 3, "text-anchor": "end", class: "axis" }, fmt(t, 2)));
  });
  niceTicks(0, xMax, 5).forEach(t => svg.appendChild(el("text", { x: X(t), y: H - padB + 18, "text-anchor": "middle", class: "axis" }, fmt(t, 1))));
  svg.appendChild(el("text", { x: W / 2, y: H - 6, "text-anchor": "middle", class: "axis-title" }, opts.xlabel || ""));
  svg.appendChild(el("text", { x: 14, y: H / 2, "text-anchor": "middle", class: "axis-title", transform: `rotate(-90 14 ${H / 2})` }, opts.ylabel || ""));
  pts.forEach((p, i) => {
    const g = el("g");
    const c = el("circle", { cx: X(p.x), cy: Y(p.y), r: 0, fill: p.color, "fill-opacity": 0.85, stroke: "#0b0f17", "stroke-width": 1 });
    const lab = el("text", { x: X(p.x) + 9, y: Y(p.y) + 4, class: "scatlbl" }, p.code);
    g.append(c, lab);
    g.addEventListener("mousemove", e => showTip(`<b>${p.code}</b><br>mean time: <b>${fmt(p.x, 3)} s</b><br>composite: <b>${fmt(p.y, 3)}</b>`, e));
    g.addEventListener("mouseleave", hideTip);
    svg.appendChild(g);
    requestAnimationFrame(() => { setTimeout(() => { c.style.transition = "r .5s ease"; c.setAttribute("r", p.r || 7); }, i * 40); });
  });
  host.innerHTML = ""; host.appendChild(svg);
}

// ============================================================
//  Heatmap (timing matrix, log-scaled colour)
// ============================================================
function heatmap(mount, rows, cols, matrix, opts = {}) {
  const host = typeof mount === "string" ? $(mount) : mount;
  if (!host) return;
  const W = host.clientWidth || 760;
  const padL = 96, padT = 28, padB = 8, cell = (W - padL) / cols.length;
  const H = padT + padB + rows.length * cell;
  const vals = matrix.flat();
  const lmin = Math.log10(Math.min(...vals)), lmax = Math.log10(Math.max(...vals));
  const color = v => {
    const t = (Math.log10(v) - lmin) / (lmax - lmin);
    // green -> yellow -> red
    const stops = [[47,208,127],[255,212,59],[214,34,70]];
    const seg = t < 0.5 ? 0 : 1, lt = t < 0.5 ? t * 2 : (t - 0.5) * 2;
    const a = stops[seg], b = stops[seg + 1];
    return `rgb(${a.map((c, i) => Math.round(c + (b[i] - c) * lt)).join(",")})`;
  };
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%", height: H, class: "chart" });
  cols.forEach((c, j) => svg.appendChild(el("text", { x: padL + j * cell + cell / 2, y: padT - 10, "text-anchor": "middle", class: "axis" }, c)));
  rows.forEach((rname, i) => {
    svg.appendChild(el("text", { x: padL - 8, y: padT + i * cell + cell / 2 + 3, "text-anchor": "end", class: "lbl" }, rname));
    cols.forEach((c, j) => {
      const v = matrix[i][j];
      const rect = el("rect", { x: padL + j * cell + 1, y: padT + i * cell + 1, width: cell - 2, height: cell - 2, rx: 3, fill: color(v), opacity: 0 });
      rect.addEventListener("mousemove", e => showTip(`<b>${rname}</b> @ R=${c}<br>time: <b>${fmt(v, 4)} s</b>`, e));
      rect.addEventListener("mouseleave", hideTip);
      svg.appendChild(rect);
      requestAnimationFrame(() => setTimeout(() => { rect.style.transition = "opacity .4s"; rect.setAttribute("opacity", 1); }, (i + j) * 18));
    });
  });
  host.innerHTML = ""; host.appendChild(svg);
}

// ============================================================
//  Scroll reveal + nav
// ============================================================
function initReveal() {
  const io = new IntersectionObserver((es) => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  }), { threshold: 0.12 });
  $$(".reveal").forEach(n => io.observe(n));
}
function initCounters() {
  const io = new IntersectionObserver((es) => es.forEach(e => {
    if (!e.isIntersecting) return;
    const n = e.target, end = parseFloat(n.dataset.count), dec = (n.dataset.dec | 0), suf = n.dataset.suf || "";
    let t0 = null, dur = 1100;
    const tick = ts => { if (!t0) t0 = ts; const p = Math.min(1, (ts - t0) / dur); n.textContent = (end * (1 - Math.pow(1 - p, 3))).toFixed(dec) + suf; if (p < 1) requestAnimationFrame(tick); };
    requestAnimationFrame(tick); io.unobserve(n);
  }), { threshold: 0.6 });
  $$("[data-count]").forEach(n => io.observe(n));
}
function initMenu() {
  const btn = $(".menu-btn"); if (!btn) return;
  btn.addEventListener("click", () => $(".links").classList.toggle("open"));
}

window.FQ = { barChart, lineChart, scatter, heatmap };
document.addEventListener("DOMContentLoaded", () => { initReveal(); initCounters(); initMenu(); });
window.addEventListener("resize", () => { clearTimeout(window.__rz); window.__rz = setTimeout(() => document.dispatchEvent(new Event("fq:redraw")), 200); });
