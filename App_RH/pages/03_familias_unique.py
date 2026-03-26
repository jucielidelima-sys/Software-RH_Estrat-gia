import streamlit as st
from utils import sidebar_global
st.set_page_config(page_title="Familias RH Unique", page_icon="🏷️", layout="wide")
cargos_df, maturidade_df, skills_df, pdi_df, filtro, cargo_selecionado = sidebar_global()
st.title("🏷️ Famílias de Cargos")
familias = sorted(cargos_df["Família"].dropna().astype(str).unique().tolist())
familia_sel = st.selectbox("Selecione a família", familias)
df_fam = cargos_df[cargos_df["Família"] == familia_sel].sort_values(["Grade","Cargo"])
st.dataframe(df_fam[["Cargo","Área","Nível","Grade","Gestor","Descrição Resumida","Trilha de Carreira"]], use_container_width=True, hide_index=True)
