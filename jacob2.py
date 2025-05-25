import streamlit as st
import numpy as np

# CSS direto aplicado ao campo input
st.markdown("""
    <style>
    .matrix-input input {
        width: 55px !important;
        text-align: center;
        padding: 2px 4px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

st.subheader("🧶 Teste de interface de matriz compacta")

n = st.number_input("Tamanho da matriz:", min_value=2, max_value=6, value=3)
A = np.zeros((n, n))
b = np.zeros(n)

st.markdown("### Matriz A (visual tipo matriz):")
for i in range(n):
    cols = st.columns(n)
    for j in range(n):
        with cols[j]:
            st.markdown('<div class="matrix-input">', unsafe_allow_html=True)
            val = st.text_input(f"A{i}{j}", value="0", key=f"A_{i}_{j}", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
            try:
                A[i][j] = float(val.replace(",", "."))
            except:
                A[i][j] = 0.0

st.markdown("### Vetor b:")
cols_b = st.columns(n)
for i in range(n):
    with cols_b[i]:
        st.markdown('<div class="matrix-input">', unsafe_allow_html=True)
        val = st.text_input(f"b{i}", value="0", key=f"b_{i}", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        try:
            b[i] = float(val.replace(",", "."))
        except:
            b[i] = 0.0

st.write("Matriz A:", A)
st.write("Vetor b:", b)
