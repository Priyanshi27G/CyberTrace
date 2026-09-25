import streamlit as st
import streamlit.components.v1 as components

st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/daisyui@4.10.2/dist/full.min.css" rel="stylesheet" type="text/css" />
<script src="https://cdn.tailwindcss.com"></script>
""", unsafe_allow_html=True)

st.markdown("""
<div class="navbar bg-base-100 shadow-xl mb-8">
  <div class="flex-1">
    <a class="btn btn-ghost text-xl">CyberTrace</a>
  </div>
  <div class="flex-none">
    <ul class="menu menu-horizontal px-1">
      <li>
        <details>
          <summary>Theme</summary>
          <ul class="p-2 bg-base-100 rounded-t-none">
            <li><a class="theme-btn" data-theme="corporate">Corporate</a></li>
            <li><a class="theme-btn" data-theme="sunset">Sunset</a></li>
          </ul>
        </details>
      </li>
    </ul>
  </div>
</div>
<div class="card w-96 bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Hello World</h2>
    <p>Test</p>
  </div>
</div>
""", unsafe_allow_html=True)

components.html("""
<script>
const parentDoc = window.parent.document;
function setTheme(theme) {
    parentDoc.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}
let saved = localStorage.getItem('theme') || 'corporate';
setTheme(saved);

setInterval(() => {
    const btns = parentDoc.querySelectorAll('.theme-btn:not(.bound)');
    btns.forEach(btn => {
        btn.classList.add('bound');
        btn.addEventListener('click', (e) => {
            setTheme(e.target.getAttribute('data-theme'));
        });
    });
}, 500);
</script>
""", height=0, width=0)
