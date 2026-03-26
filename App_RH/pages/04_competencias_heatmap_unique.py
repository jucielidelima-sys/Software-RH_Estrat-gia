import plotly.express as px
import streamlit as st
from utils import sidebar_global
st.set_page_config(page_title="Competencias Heatmap RH Unique", page_icon="🧭", layout="wide")
cargos_df, maturidade_df, skills_df, pdi_df, filtro, cargo_selecionado = sidebar_global()
st.title("🧭 Heatmap de Competências")
mat = maturidade_df[maturidade_df["Cargo"].isin(filtro["Cargo"].unique())]
if not mat.empty:
    pivot = mat.pivot_table(index="Cargo", columns="Competência", values="Nível de Maturidade", aggfunc="mean")
    fig_heat = px.imshow(pivot, text_auto=True, aspect="auto",
                         color_continuous_scale=[[0.0, "#0f172a"], [0.25, "#1d4ed8"], [0.5, "#06b6d4"], [0.75, "#22c55e"], [1.0, "#f59e0b"]])
    fig_heat.update_layout(height=540, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f3f4f6"))
    st.plotly_chart(fig_heat, use_container_width=True)
else:
    st.info("Sem dados de maturidade.")
