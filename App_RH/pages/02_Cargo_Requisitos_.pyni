import streamlit as st
from utils import sidebar_global, formatar_moeda, gerar_pdf_cargo
st.set_page_config(page_title="Cargo Requisitos RH Unique", page_icon="📋", layout="wide")
cargos_df, maturidade_df, skills_df, pdi_df, avaliacoes_df, filtro, cargo_selecionado = sidebar_global()
st.title("📋 Cargo e Requisitos")
detalhe = cargos_df[cargos_df["Cargo"] == cargo_selecionado]
if not detalhe.empty:
    d = detalhe.iloc[0]
    st.download_button("Exportar cargo em PDF", data=gerar_pdf_cargo(d), file_name=f"cargo_{str(d['Cargo']).replace(' ','_')}.pdf", mime="application/pdf")
    st.write(f"**Cargo:** {d['Cargo']}")
    st.write(f"**Área:** {d['Área']}")
    st.write(f"**Família:** {d['Família']}")
    st.write(f"**Nível:** {d['Nível']}")
    st.write(f"**Grade:** {d['Grade']}")
    st.write(f"**Faixa média:** {formatar_moeda(d['Faixa Salarial Média'])}")
    st.info(str(d["Descrição Resumida"]))
    st.write("### Atividades do cargo")
    st.write(str(d["Atividades do Cargo"]))
    st.write("### Pré-requisitos obrigatórios")
    st.write(str(d["Pré-requisitos Obrigatórios"]))
    st.write("### Pré-requisitos desejáveis")
    st.write(str(d["Pré-requisitos Desejáveis"]))
