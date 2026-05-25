const btn = document.getElementById('toggle-furigana');
let visible = true;
btn.addEventListener('click', () => {
  visible = !visible;
  document.querySelectorAll('rt').forEach(rt => rt.style.display = visible ? '' : 'none');
  btn.textContent = visible ? 'Hide furigana' : 'Show furigana';
});
