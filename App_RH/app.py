import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import sidebar_global, formatar_moeda, carregar_logo

st.set_page_config(page_title="Home RH Industrial 4.0", page_icon="🏭", layout="wide")
cargos_df, maturidade_df, skills_df, pdi_df, avaliacoes_df, filtro, cargo_selecionado = sidebar_global()
logo_path = carregar_logo()

top1, top2 = st.columns([0.12, 0.88])
with top1:
    if logo_path:
        st.image(logo_path, width=120)
with top2:
    st.markdown("""
    <div class="hero-panel">
        <div class="hero-title">RH Estratégico Industrial 4.0</div>
        <p class="hero-sub"></p>
    </div>
    """, unsafe_allow_html=True)

headcount = int(filtro["Colaboradores"].sum()) if not filtro.empty else 0
salario_medio = float(filtro["Faixa Salarial Média"].mean()) if not filtro.empty else 0
merit_media = float(avaliacoes_df["Nota Meritocracia"].mean()) if not avaliacoes_df.empty else 0
tempo_medio = float(avaliacoes_df["Tempo de Casa (anos)"].mean()) if not avaliacoes_df.empty else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Cargos", int(filtro["Cargo"].nunique()) if not filtro.empty else 0)
k2.metric("Áreas", int(filtro["Área"].nunique()) if not filtro.empty else 0)
k3.metric("Headcount", headcount)
k4.metric("Salário Médio", formatar_moeda(salario_medio))
k5.metric("Meritocracia Média", f"{merit_media:.1f}")

st.markdown("### Painel interativo do app")
c_filtro1, c_filtro2, c_filtro3 = st.columns(3)
with c_filtro1:
    area_merito = st.selectbox("Área para análise rápida", ["Todas"] + sorted(avaliacoes_df["Área"].dropna().astype(str).unique().tolist()))
with c_filtro2:
    sexo_view = st.selectbox("Sexo", ["Todos"] + sorted(avaliacoes_df["Sexo"].dropna().astype(str).unique().tolist()))
with c_filtro3:
    cargo_view = st.selectbox("Cargo na visão do app", ["Todos"] + sorted(avaliacoes_df["Cargo"].dropna().astype(str).unique().tolist()))

av = avaliacoes_df.copy()
if area_merito != "Todas":
    av = av[av["Área"] == area_merito]
if sexo_view != "Todos":
    av = av[av["Sexo"] == sexo_view]
if cargo_view != "Todos":
    av = av[av["Cargo"] == cargo_view]

g1, g2 = st.columns(2)
with g1:
    st.markdown("#### Avaliações por meritocracia")
    if not av.empty:
        merit = av.groupby("Cargo", as_index=False)["Nota Meritocracia"].mean().sort_values("Nota Meritocracia", ascending=True)
        fig = px.bar(merit, x="Nota Meritocracia", y="Cargo", orientation="h", text="Nota Meritocracia")
        fig.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f3f4f6"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem dados para esse filtro.")

with g2:
    st.markdown("#### Tempo de casa")
    if not av.empty:
        fig2 = px.scatter(
            av, x="Tempo de Casa (anos)", y="Nota Meritocracia",
            color="Área", size="Nota Meritocracia", hover_name="Colaborador",
            hover_data=["Cargo", "Sexo", "Performance", "Potencial"], size_max=28
        )
        fig2.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f3f4f6"))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sem dados para esse filtro.")

g3, g4 = st.columns(2)
with g3:
    st.markdown("#### Distribuição de headcount por sexo")
    if not av.empty:
        sexo_df = av.groupby("Sexo", as_index=False)["Colaborador"].count().rename(columns={"Colaborador":"Quantidade"})
        fig3 = px.pie(sexo_df, values="Quantidade", names="Sexo", hole=0.55)
        fig3.update_traces(textinfo="percent+label")
        fig3.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f3f4f6"))
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Sem dados para esse filtro.")

with g4:
    st.markdown("#### Matriz de competências")
    if not maturidade_df.empty:
        pivot = maturidade_df.pivot_table(index="Cargo", columns="Competência", values="Nível de Maturidade", aggfunc="mean")
        fig4 = px.imshow(
            pivot, text_auto=True, aspect="auto",
            color_continuous_scale=[[0.0, "#0f172a"], [0.25, "#1d4ed8"], [0.5, "#06b6d4"], [0.75, "#22c55e"], [1.0, "#f59e0b"]],
        )
        fig4.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f3f4f6"))
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Sem dados de competências.")

g5, g6 = st.columns(2)
with g5:
    st.markdown("#### Ranking individual de meritocracia")
    if not av.empty:
        rank = av.sort_values("Nota Meritocracia", ascending=True)
        fig5 = px.bar(rank, x="Nota Meritocracia", y="Colaborador", orientation="h", color="Área", text="Nota Meritocracia")
        fig5.update_layout(height=460, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f3f4f6"))
        st.plotly_chart(fig5, use_container_width=True)


# cálculo seguro da maior média de mérito
if not av.empty:
    maior_merito = av.groupby('Cargo')['Nota Meritocracia'].mean().max()
else:
    maior_merito = 0

with g6:
    st.markdown("#### Resumo rápido")
    st.markdown(f"""
    <div class="metal-card">
        <b>Tempo médio de casa:</b> {tempo_medio:.1f} anos<br><br>
        <b>Maior nota média de mérito:</b> {maior_merito:.1f}<br><br>
        <b>Colaboradores avaliados:</b> {len(av)}<br><br>
        <b>Cargo selecionado no painel:</b> {cargo_selecionado}
    </div>
    """, unsafe_allow_html=True)

with st.expander("Ver base de avaliações de mérito, tempo de casa e headcount"):
    st.dataframe(av, use_container_width=True, hide_index=True)

st.info("Além desta tela interativa, o menu lateral continua com páginas separadas para cargos, famílias, skills, radar/PDI, exportações e base de dados.")
