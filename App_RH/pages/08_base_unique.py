import streamlit as st
from utils import sidebar_global
st.set_page_config(page_title="Base RH Unique", page_icon="🗂️", layout="wide")
cargos_df, maturidade_df, skills_df, pdi_df, filtro, cargo_selecionado = sidebar_global()
st.title("🗂️ Base de Dados")
t1, t2, t3, t4 = st.tabs(["Cargos","Matriz","Skills","PDI"])
with t1: st.dataframe(cargos_df, use_container_width=True, hide_index=True)
with t2: st.dataframe(maturidade_df, use_container_width=True, hide_index=True)
with t3: st.dataframe(skills_df, use_container_width=True, hide_index=True)
with t4: st.dataframe(pdi_df, use_container_width=True, hide_index=True)
