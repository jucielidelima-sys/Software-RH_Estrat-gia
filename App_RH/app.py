import streamlit as st
from utils import sidebar_global, formatar_moeda, carregar_logo

st.set_page_config(page_title="Home RH Industrial 4.0", page_icon="🏭", layout="wide")
cargos_df, maturidade_df, skills_df, pdi_df, filtro, cargo_selecionado = sidebar_global()
logo_path = carregar_logo()
c1, c2 = st.columns([0.12, 0.88])
with c1:
    if logo_path:
        st.image(logo_path, width=120)
with c2:
    st.markdown("""
    <div class="hero-panel">
        <div class="hero-title">RH Estratégico Industrial 4.0</div>
        <p class="hero-sub"></p>
    </div>
    """, unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Cargos", int(filtro["Cargo"].nunique()) if not filtro.empty else 0)
k2.metric("Áreas", int(filtro["Área"].nunique()) if not filtro.empty else 0)
k3.metric("Headcount", int(filtro["Colaboradores"].sum()) if not filtro.empty else 0)
k4.metric("Salário Médio", formatar_moeda(float(filtro["Faixa Salarial Média"].mean()) if not filtro.empty else 0))
k5.metric("Maior Grade", str(filtro["Grade"].sort_values().iloc[-1]) if not filtro.empty else "-")
