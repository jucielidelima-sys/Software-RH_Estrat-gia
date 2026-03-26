import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import sidebar_global
st.set_page_config(page_title="Painel Executivo RH Unique", page_icon="📊", layout="wide")
cargos_df, maturidade_df, skills_df, pdi_df, avaliacoes_df, filtro, cargo_selecionado = sidebar_global()
st.title("📊 Painel Executivo RH")
c1, c2 = st.columns([1.25, 1])
with c1:
    st.subheader("Faixa salarial por cargo")
    if not filtro.empty:
        df_plot = filtro.sort_values("Faixa Salarial Média", ascending=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_plot["Faixa Salarial Mín"], y=df_plot["Cargo"], orientation="h", name="Mínimo", marker_color="#475569"))
        fig.add_trace(go.Bar(x=df_plot["Faixa Salarial Média"], y=df_plot["Cargo"], orientation="h", name="Média", marker_color="#00e5ff"))
        fig.add_trace(go.Bar(x=df_plot["Faixa Salarial Máx"], y=df_plot["Cargo"], orientation="h", name="Máximo", marker_color="#38bdf8"))
        fig.update_layout(barmode="group", height=520, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f3f4f6"))
        st.plotly_chart(fig, use_container_width=True)
with c2:
    st.subheader("Distribuição por área")
    if not filtro.empty:
        area_df = filtro.groupby("Área", as_index=False)["Cargo"].count().rename(columns={"Cargo":"Quantidade"})
        fig2 = px.pie(area_df, values="Quantidade", names="Área", hole=0.55)
        fig2.update_traces(textinfo="percent+label")
        fig2.update_layout(height=520, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f3f4f6"))
        st.plotly_chart(fig2, use_container_width=True)
