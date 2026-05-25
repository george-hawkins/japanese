/*
 * Written using Claude.
 *
 * Draw KanjiVG SVGs stroke by stroke (with the stroke numbers drawn in
 * after the last stroke is drawn).
 *
 * Usage:
 *   <script src="kanjivg-animate.js"></script>
 *   <span class="kanjivg-animate">日</span>
 *
 * The KanjiVG SVG (with stroke numbers) appears fully drawn by default.
 * Clicking it causes it to be redrawn stroke by stroke.
 *
 * By default the KanjiVG SVGs are assumed to be in the same directory
 * as this script. Add the attribute data-base-path="..." to the script
 * tag to point to the SVGs if they're elsewhere.
 *
 * Other optional attributes that can be used with the script tag:
 * - data-pace-ms          ms per sqrt(path-unit), larger = slower (default 60)
 * - data-min-stroke-ms    floor per stroke for tiny strokes (default 240)
 * - data-filename-format  'char' (食.svg) or 'hex' (098df.svg) (default 'char')
 * - data-filename-prefix  prepended to the filename, '' for none (default '_kanjivg-')
 *
 * Filename is built as `<basePath>/<prefix><stem>.svg`, where <stem> is either
 * the kanji itself or its zero-padded hex codepoint.
 */
(() => {
  const SCRIPT = document.currentScript;
  const SELECTOR = '.kanjivg-animate';

  const DEFAULTS = {
    basePath: '',
    filenameFormat: 'char',
    filenamePrefix: '_kanjivg-',
    paceMs: 60,
    minStrokeMs: 240,
  };

  function fromScriptAttrs() {
    if (!SCRIPT) return {};
    const out = {};
    const { basePath, filenameFormat, filenamePrefix, paceMs, minStrokeMs } = SCRIPT.dataset;
    if (basePath !== undefined) out.basePath = basePath;
    if (filenameFormat !== undefined) out.filenameFormat = filenameFormat;
    if (filenamePrefix !== undefined) out.filenamePrefix = filenamePrefix;
    if (paceMs !== undefined) out.paceMs = +paceMs;
    if (minStrokeMs !== undefined) out.minStrokeMs = +minStrokeMs;
    return out;
  }

  const STYLE = `
    ${SELECTOR} svg { cursor: pointer; touch-action: manipulation; display: inline-block; vertical-align: middle; }
    ${SELECTOR} svg [id^="kvg:StrokeNumbers"] { transition: opacity 0.25s ease; }
  `;

  let styleInjected = false;
  const svgCache = new Map();

  function injectStyle() {
    if (styleInjected) return;
    const s = document.createElement('style');
    s.textContent = STYLE;
    document.head.appendChild(s);
    styleInjected = true;
  }

  async function fetchSvg(opts, char) {
    const stem = opts.filenameFormat === 'hex'
      ? char.codePointAt(0).toString(16).padStart(5, '0')
      : char;
    const filename = `${opts.filenamePrefix}${stem}.svg`;
    const url = opts.basePath ? `${opts.basePath.replace(/\/$/, '')}/${filename}` : filename;
    if (!svgCache.has(url)) {
      svgCache.set(url, fetch(url).then(r => {
        if (!r.ok) throw new Error(`KanjiVG ${char} (${url}) → HTTP ${r.status}`);
        return r.text();
      }));
    }
    return svgCache.get(url);
  }

  function parseSvg(text) {
    const doc = new DOMParser().parseFromString(text, 'image/svg+xml');
    const svg = doc.documentElement;
    svg.removeAttribute('width');
    svg.removeAttribute('height');
    return svg;
  }

  async function animate(paths, numbers, opts) {
    if (numbers) numbers.style.opacity = '0';

    for (const p of paths) {
      const len = p.getTotalLength();
      p.style.strokeDasharray = len;
      p.style.strokeDashoffset = len;
    }

    for (const p of paths) {
      const len = p.getTotalLength();
      const duration = Math.max(opts.minStrokeMs, opts.paceMs * Math.sqrt(len));
      const naturalStroke = getComputedStyle(p).stroke;
      p.style.stroke = 'red';
      const draw = p.animate(
        { strokeDashoffset: [len, 0] },
        { duration, easing: 'linear', fill: 'forwards' }
      );
      await draw.finished;
      try { draw.commitStyles(); } catch {}
      draw.cancel();

      const fade = p.animate(
        { stroke: ['red', naturalStroke] },
        { duration: 150, easing: 'ease-out', fill: 'forwards' }
      );
      await fade.finished;
      try { fade.commitStyles(); } catch {}
      fade.cancel();
      p.style.stroke = '';
    }

    if (numbers) numbers.style.opacity = '1';
  }

  async function mount(el, opts) {
    const char = el.textContent.trim();
    if (!char) return;
    let svg;
    try {
      svg = parseSvg(await fetchSvg(opts, char));
    } catch (e) {
      console.error(e);
      return;
    }
    el.replaceChildren(svg);

    const paths = [...svg.querySelectorAll('[id^="kvg:StrokePaths"] path')];
    const numbers = svg.querySelector('[id^="kvg:StrokeNumbers"]');
    if (!paths.length) return;

    let playing = false;
    svg.addEventListener('click', async () => {
      if (playing) return;
      playing = true;
      try { await animate(paths, numbers, opts); }
      finally { playing = false; }
    });
  }

  function kanjivgAnimate(userOpts = {}) {
    const opts = { ...DEFAULTS, ...fromScriptAttrs(), ...userOpts };
    injectStyle();
    const root = opts.root || document;
    root.querySelectorAll(SELECTOR).forEach(el => mount(el, opts));
  }

  window.kanjivgAnimate = kanjivgAnimate;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => kanjivgAnimate());
  } else {
    kanjivgAnimate();
  }
})();
