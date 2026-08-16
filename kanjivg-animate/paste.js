/*
 * Written using Claude.
 *
 * Glue for paste.html: work out how this platform pastes, capture the pasted
 * text and, if it's a single kanji, render it with kanjivg-animate.js and play
 * the stroke order animation immediately.
 *
 * Anything that isn't a single kanji (and any kanji that KanjiVG has no stroke
 * data for) gets the blank marker below instead, with no animation.
 */
(() => {
  const CMD = '⌘'; // The macOS command key glyph.

  // A stand-in for "nothing to draw here", modelled on 〼 (U+303C, the masu
  // mark) because it looks like a stop sign. Drawn rather than set as text so
  // it doesn't depend on a Japanese font being installed, and so it sits in the
  // same 109x109 viewBox as the KanjiVG glyphs it replaces.
  const BLANK = `
    <svg viewBox="0 0 109 109" xmlns="http://www.w3.org/2000/svg" aria-label="not a kanji" role="img">
      <g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round">
        <rect x="16" y="16" width="77" height="77"/>
        <line x1="16" y1="93" x2="93" y2="16"/>
      </g>
    </svg>
  `;

  // A single Han character - i.e. a kanji, rather than kana, punctuation etc.
  const KANJI = /^\p{Script=Han}$/u;

  const stage = document.querySelector('.stage');
  const box = stage.querySelector('.kanjivg-animate');
  const hint = document.querySelector('.hint');
  const controls = document.querySelector('.controls');
  const status = document.querySelector('.status');

  const say = message => { status.textContent = message; };

  function showBlank(message) {
    box.classList.add('blank');
    box.innerHTML = BLANK;
    say(message);
  }

  async function render(text) {
    const chars = [...text.replace(/\s+/g, '')];
    if (chars.length !== 1 || !KANJI.test(chars[0])) {
      const quoted = text.trim().slice(0, 16);
      showBlank(quoted ? `“${quoted}” isn't a single kanji.` : 'Nothing was pasted.');
      return;
    }
    const char = chars[0];

    box.classList.remove('blank');
    box.textContent = char;
    say('');

    const [handle] = await window.kanjivgAnimate({ root: stage });
    if (!handle) {
      showBlank(`KanjiVG has no stroke data for ${char}.`);
      return;
    }
    handle.play();
  }

  document.addEventListener('paste', event => {
    event.preventDefault();
    render(event.clipboardData ? event.clipboardData.getData('text') : '');
  });

  function platform() {
    const ua = navigator.userAgent;
    // Chromium's client hints, where available, otherwise sniff the UA string.
    const hinted = (navigator.userAgentData && navigator.userAgentData.platform || '').toLowerCase();
    // Android UA strings also contain "Linux", so check for it first.
    if (hinted === 'android' || /Android/.test(ua)) return 'android';
    if (/iPhone|iPod|iPad/.test(ua)) return 'ios';
    const mac = hinted === 'macos' || /Mac/.test(ua);
    // iPadOS 13+ claims to be a Mac - the touchscreen gives it away.
    if (mac) return navigator.maxTouchPoints > 1 ? 'ios' : 'macos';
    if (hinted === 'windows' || /Windows/.test(ua)) return 'windows';
    if (hinted === 'linux' || /Linux|X11|CrOS/.test(ua)) return 'linux';
    return 'unknown';
  }

  const SHORTCUT = {
    macos: `<kbd>${CMD}</kbd><kbd>V</kbd>`,
    windows: '<kbd>Ctrl</kbd><kbd>V</kbd>',
    linux: '<kbd>Ctrl</kbd><kbd>V</kbd>',
    unknown: `<kbd>Ctrl</kbd><kbd>V</kbd> (or <kbd>${CMD}</kbd><kbd>V</kbd> on a Mac)`,
  };

  const shortcut = SHORTCUT[platform()];
  const canRead = !!(navigator.clipboard && navigator.clipboard.readText);

  if (shortcut) {
    hint.innerHTML = `Copy a single kanji from anywhere and press ${shortcut} to paste it here and see`
      + ' it animated in the correct stroke order.';
  } else if (!canRead) {
    // A touch platform, but one that won't let us read the clipboard.
    hint.textContent = 'Copy a single kanji from anywhere and paste it here to see it animated in the'
      + ' correct stroke order.';
  } else {
    // Touch platforms have no paste shortcut and won't deliver a paste event
    // without an editable element in focus, so offer a button that reads the
    // clipboard itself.
    hint.textContent = 'Copy a single kanji from anywhere, then tap Paste to see it animated in the'
      + ' correct stroke order.';

    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = 'Paste';
    button.addEventListener('click', async () => {
      let text;
      try {
        text = await navigator.clipboard.readText();
      } catch {
        say("Couldn't read the clipboard - permission denied?");
        return;
      }
      render(text);
    });
    controls.replaceChildren(button);
  }
})();
