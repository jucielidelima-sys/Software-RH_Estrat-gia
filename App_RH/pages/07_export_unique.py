import streamlit as st
from utils import sidebar_global, gerar_excel_export, gerar_pdf_cargo
st.set_page_config(page_title="Export RH Unique", page_icon="📤", layout="wide")
cargos_df, maturidade_df, skills_df, pdi_df, filtro, cargo_selecionado = sidebar_global()
st.title("📤 Exportações")
st.download_button("Exportar base completa em Excel", data=gerar_excel_export(cargos_df, maturidade_df, skills_df, pdi_df), file_name="rh_estrategico_industrial.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
detalhe = cargos_df[cargos_df["Cargo"] == cargo_selecionado]
if not detalhe.empty:
    st.download_button("Exportar cargo selecionado em PDF", data=gerar_pdf_cargo(detalhe.iloc[0]), file_name=f"cargo_{cargo_selecionado.replace(' ','_')}.pdf", mime="application/pdf")
