import pandas as pd
import streamlit as st
from utils import sidebar_global, radar_fig, salvar_pdi
st.set_page_config(page_title="Radar PDI RH Unique", page_icon="🎯", layout="wide")
cargos_df, maturidade_df, skills_df, pdi_df, avaliacoes_df, filtro, cargo_selecionado = sidebar_global()
st.title("🎯 Radar e PDI")
cargo_radar = st.selectbox("Cargo para radar", sorted(skills_df["Cargo"].dropna().astype(str).unique().tolist()))
df_radar = skills_df[skills_df["Cargo"] == cargo_radar]
st.plotly_chart(radar_fig(df_radar[df_radar["Tipo Skill"] == "Hard Skill"], "Hard Skills"), use_container_width=True)
st.dataframe(pdi_df, use_container_width=True, hide_index=True)
novo_colaborador = st.text_input("Colaborador")
novo_cargo = st.text_input("Cargo")
novo_objetivo = st.text_area("Objetivo de desenvolvimento")
nova_acao = st.text_area("Ação de desenvolvimento")
novo_prazo = st.text_input("Prazo")
novo_status = st.selectbox("Status", ["Planejado","Em andamento","Concluído"])
if st.button("Salvar PDI em arquivo"):
    if novo_colaborador and novo_cargo and novo_objetivo and nova_acao and novo_prazo:
        novo = pd.DataFrame([{
            "Colaborador": novo_colaborador, "Cargo": novo_cargo,
            "Objetivo de Desenvolvimento": novo_objetivo, "Ação de Desenvolvimento": nova_acao,
            "Prazo": novo_prazo, "Status": novo_status
        }])
        pdi_df = pd.concat([pdi_df, novo], ignore_index=True)
        st.session_state["dados_carregados"]["pdi"] = pdi_df
        salvar_pdi(pdi_df)
        st.success("PDI salvo.")
