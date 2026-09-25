import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/daisyui@4.10.2/dist/full.min.css" rel="stylesheet" type="text/css" />
<script src="https://cdn.tailwindcss.com"></script>
<script>
    // Ensure parent document gets the theme
    window.parent.document.documentElement.setAttribute('data-theme', 'sunset');
</script>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card w-96 bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">DaisyUI Works!</h2>
    <p>If a dog chews shoes whose shoes does he choose?</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Buy Now</button>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
