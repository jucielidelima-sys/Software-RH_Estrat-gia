import plotly.express as px
import streamlit as st
from utils import sidebar_global
st.set_page_config(page_title="Skills RH Unique", page_icon="🛠️", layout="wide")
cargos_df, maturidade_df, skills_df, pdi_df, filtro, cargo_selecionado = sidebar_global()
st.title("🛠️ Hard e Soft Skills")
cargo_skill = st.selectbox("Selecione o cargo", sorted(skills_df["Cargo"].dropna().astype(str).unique().tolist()))
df_skill = skills_df[skills_df["Cargo"] == cargo_skill]
c1, c2 = st.columns(2)
with c1:
    hard = df_skill[df_skill["Tipo Skill"] == "Hard Skill"].sort_values("Nível", ascending=True)
    if not hard.empty:
        fig = px.bar(hard, x="Nível", y="Skill", orientation="h", text="Nível")
        fig.update_layout(height=420, xaxis_range=[0, 5.5], paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f3f4f6"))
        st.plotly_chart(fig, use_container_width=True)
with c2:
    soft = df_skill[df_skill["Tipo Skill"] == "Soft Skill"].sort_values("Nível", ascending=True)
    if not soft.empty:
        fig = px.bar(soft, x="Nível", y="Skill", orientation="h", text="Nível")
        fig.update_layout(height=420, xaxis_range=[0, 5.5], paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f3f4f6"))
        st.plotly_chart(fig, use_container_width=True)
