import io
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

THEME_CSS = """
<style>
.stApp {
    background:
        radial-gradient(circle at top right, rgba(0,255,255,0.08), transparent 28%),
        radial-gradient(circle at top left, rgba(0,140,255,0.08), transparent 22%),
        linear-gradient(135deg, #0a0f14 0%, #0f1720 38%, #111827 70%, #0a0f14 100%);
}
.block-container { padding-top: 0.8rem; padding-bottom: 1.2rem; max-width: 1600px; }
h1,h2,h3,h4,h5,h6,p,div,span,label { color: #f3f4f6 !important; }
div[data-testid="metric-container"] {
    background: linear-gradient(180deg, rgba(40,48,64,0.95), rgba(22,28,39,0.90));
    border: 1px solid rgba(148,163,184,0.22);
    border-radius: 18px;
    padding: 14px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 12px 30px rgba(0,0,0,0.28);
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #dde3eb 0%, #d1d9e4 100%) !important;
    border-right: 1px solid rgba(0,0,0,0.08);
}
section[data-testid="stSidebar"] * { color: #111111 !important; }
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #ffffff !important; color: #111111 !important;
    border: 1px solid #8a94a6 !important; border-radius: 10px !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] span,
section[data-testid="stSidebar"] div[data-baseweb="select"] input {
    color: #111111 !important; -webkit-text-fill-color: #111111 !important;
}
div[data-baseweb="popover"], div[data-baseweb="popover"] * { color: #111111 !important; }
div[role="listbox"], div[role="option"], ul[role="listbox"] li, ul[role="listbox"] li * {
    background: #ffffff !important; color: #111111 !important; -webkit-text-fill-color: #111111 !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.82); border: 1px solid #b5becb; border-radius: 14px; padding: 10px;
}
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important; border: 2px dashed #97a3b6 !important; border-radius: 12px !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] *,
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
    color: #111111 !important; fill: #111111 !important; -webkit-text-fill-color: #111111 !important;
}
.hero-panel {
    background:
        linear-gradient(90deg, rgba(10,15,20,0.96), rgba(17,24,39,0.90)),
        repeating-linear-gradient(45deg, rgba(255,255,255,0.03) 0px, rgba(255,255,255,0.03) 8px, rgba(255,255,255,0.01) 8px, rgba(255,255,255,0.01) 16px);
    border: 1px solid rgba(0,255,255,0.12); border-radius: 24px; padding: 20px 24px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.35); margin-bottom: 12px;
}
.metal-card {
    background: linear-gradient(180deg, rgba(57,65,80,0.95) 0%, rgba(28,35,48,0.92) 100%);
    border: 1px solid rgba(148,163,184,0.22); border-radius: 20px; padding: 18px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 14px 36px rgba(0,0,0,0.24); margin-bottom: 12px;
}
.hero-title { font-size: 1.8rem; font-weight: 800; color: #e5f9ff !important; margin-bottom: 4px; }
.hero-sub { color: #b6c2d1 !important; font-size: 0.96rem; margin-bottom: 0; }
.small-note { color: #cbd5e1 !important; font-size: 0.88rem; }
</style>
"""

CARGOS_COLS = [
    "ID Cargo","Cargo","Área","Família","Nível","Grade","Faixa Salarial Mín","Faixa Salarial Média","Faixa Salarial Máx",
    "Colaboradores","Gestor","Descrição Resumida","Atividades do Cargo","Pré-requisitos Obrigatórios",
    "Pré-requisitos Desejáveis","Escolaridade","Experiência","Trilha de Carreira"
]
MATURIDADE_COLS = ["Cargo","Competência","Nível de Maturidade"]
SKILLS_COLS = ["Cargo","Tipo Skill","Skill","Nível"]
PDI_COLS = ["Colaborador","Cargo","Objetivo de Desenvolvimento","Ação de Desenvolvimento","Prazo","Status"]
AVALIACOES_COLS = ["Colaborador","Cargo","Área","Sexo","Tempo de Casa (anos)","Nota Meritocracia","Performance","Potencial"]

def aplicar_tema():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

def formatar_moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def to_excel_bytes(df, sheet_name="dados"):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()

def criar_bases():
    cargos = pd.DataFrame([
        [1,"Analista de Processos Jr","Engenharia","Processos","Júnior","G07",3500,4200,5000,3,"Coordenador de Engenharia","Mapear processos, apoiar melhorias e analisar indicadores operacionais.","Cronoanálise; levantamento de fluxos; padronização; análise de perdas; atualização de indicadores; apoio a kaizens.","Graduação em andamento ou completa; Excel intermediário; noções de processos industriais.","Power BI; Lean; experiência em metalurgia/linha branca.","Superior em andamento/completo em Engenharia, Administração ou afins","Vivência inicial com processos industriais","Analista de Processos Jr > Pl > Sr > Especialista/Coordenação"],
        [2,"Analista de Processos Pl","Engenharia","Processos","Pleno","G09",5000,6200,7500,4,"Coordenador de Engenharia","Conduzir projetos de melhoria e produtividade.","Balanceamento; VSM; kaizen; estudos de layout; dashboards; gestão de projetos de melhoria.","Superior completo; Excel avançado; experiência com processos industriais.","Power BI; Green Belt; vivência com slitter, prensas ou laser.","Superior completo em Engenharia ou áreas correlatas","Experiência com Lean, indicadores e melhoria contínua","Analista de Processos Jr > Pl > Sr > Especialista/Coordenação"],
        [3,"Analista de PCP","PCP","Planejamento","Pleno","G09",4800,5900,7000,2,"Coordenador de PCP","Planejar produção, capacidade e sequenciamento.","MRP; programação; follow-up; análise de estoque; aderência ao plano; reuniões com produção.","Superior completo; Excel avançado; experiência em PCP.","Conhecimento em ERP; Power BI; experiência em manufatura seriada.","Superior completo em Administração, Engenharia ou Logística","Vivência com MRP, Excel e rotinas de planejamento","Assistente PCP > Analista PCP > Coordenador PCP"],
        [4,"Supervisor de Produção","Produção","Liderança","Sênior","G12",7000,8500,10500,2,"Gerente Industrial","Supervisionar equipe, segurança, qualidade e metas.","Gestão de equipe; DDS; acompanhamento de indicadores; tratativa de desvios; plano de ação; gestão do turno.","Superior completo; experiência em liderança industrial; gestão de indicadores.","Lean; formação em gestão de pessoas; experiência em metalúrgica.","Superior completo","Experiência em liderança industrial","Líder > Supervisor > Coordenador > Gerente"],
        [5,"Operador de Slitter","Produção","Operação","Operacional","G05",2600,3100,3800,8,"Supervisor de Produção","Operar slitter, preparar setup e monitorar qualidade.","Setup; operação da máquina; controle visual; apontamentos; segurança; limpeza do posto.","Ensino médio completo; experiência com operação industrial.","Experiência com slitter; leitura de OP; ponte rolante.","Ensino médio completo","Vivência em corte longitudinal é diferencial","Operador I > Operador II > Preparador > Líder"],
        [6,"Técnico de Qualidade","Qualidade","Qualidade","Técnico","G07",3200,4100,5200,3,"Coordenador da Qualidade","Executar inspeções, auditorias e tratativas de NC.","Inspeções; auditorias; RNC; metrologia; laudos; suporte às áreas produtivas.","Técnico completo; leitura e interpretação de desenho; metrologia.","Auditoria interna; CEP; MASP/8D.","Técnico completo","Vivência com instrumentos de medição","Inspetor > Técnico > Analista > Coordenação"],
    ], columns=CARGOS_COLS)

    maturidade = pd.DataFrame([
        ["Analista de Processos Jr","Mapeamento de Processos",2],
        ["Analista de Processos Jr","Lean Manufacturing",2],
        ["Analista de Processos Jr","Power BI",1],
        ["Analista de Processos Pl","Mapeamento de Processos",4],
        ["Analista de Processos Pl","Lean Manufacturing",4],
        ["Analista de Processos Pl","Power BI",3],
        ["Analista de PCP","Planejamento",4],
        ["Analista de PCP","MRP",4],
        ["Supervisor de Produção","Liderança",5],
        ["Supervisor de Produção","Gestão de Indicadores",4],
        ["Operador de Slitter","Setup",4],
        ["Operador de Slitter","Qualidade no Processo",3],
        ["Técnico de Qualidade","Metrologia",4],
        ["Técnico de Qualidade","Análise de Não Conformidade",4],
    ], columns=MATURIDADE_COLS)

    skills = pd.DataFrame([
        ["Analista de Processos Jr","Hard Skill","Excel",3],
        ["Analista de Processos Jr","Hard Skill","Cronoanálise",2],
        ["Analista de Processos Jr","Soft Skill","Comunicação",3],
        ["Analista de Processos Jr","Soft Skill","Organização",4],
        ["Analista de Processos Pl","Hard Skill","Lean",4],
        ["Analista de Processos Pl","Hard Skill","Power BI",3],
        ["Analista de Processos Pl","Soft Skill","Protagonismo",4],
        ["Analista de Processos Pl","Soft Skill","Trabalho em Equipe",4],
        ["Analista de PCP","Hard Skill","MRP",4],
        ["Analista de PCP","Hard Skill","Excel Avançado",4],
        ["Analista de PCP","Soft Skill","Planejamento",4],
        ["Analista de PCP","Soft Skill","Senso de Prioridade",4],
        ["Supervisor de Produção","Hard Skill","Gestão de KPIs",4],
        ["Supervisor de Produção","Hard Skill","Gestão de Pessoas",5],
        ["Supervisor de Produção","Soft Skill","Liderança",5],
        ["Supervisor de Produção","Soft Skill","Tomada de Decisão",4],
        ["Operador de Slitter","Hard Skill","Operação de Slitter",4],
        ["Operador de Slitter","Hard Skill","Leitura de OP",3],
        ["Operador de Slitter","Soft Skill","Disciplina",4],
        ["Operador de Slitter","Soft Skill","Atenção",4],
        ["Técnico de Qualidade","Hard Skill","Metrologia",4],
        ["Técnico de Qualidade","Hard Skill","Auditoria",3],
        ["Técnico de Qualidade","Soft Skill","Análise Crítica",4],
        ["Técnico de Qualidade","Soft Skill","Relacionamento Interpessoal",3],
    ], columns=SKILLS_COLS)

    pdi = pd.DataFrame([
        ["Ana","Analista de Processos Jr","Melhorar Power BI","Treinamento interno + projeto prático","30/06/2026","Em andamento"],
        ["Bruno","Analista de Processos Pl","Desenvolver gestão de projetos","Curso + liderar kaizen","30/07/2026","Planejado"],
        ["Carla","Analista de PCP","Fortalecer S&OP","Mentoria com coordenação","15/08/2026","Planejado"],
        ["Diego","Supervisor de Produção","Aprimorar liderança","Treinamento de feedback e rotina","20/06/2026","Em andamento"],
    ], columns=PDI_COLS)

    avaliacoes = pd.DataFrame([
        ["Ana","Analista de Processos Jr","Engenharia","Feminino",1.2,7.8,"Média","Alta"],
        ["Bruno","Analista de Processos Pl","Engenharia","Masculino",3.5,8.9,"Alta","Alta"],
        ["Carla","Analista de PCP","PCP","Feminino",2.8,8.1,"Alta","Média"],
        ["Diego","Supervisor de Produção","Produção","Masculino",5.7,9.2,"Alta","Alta"],
        ["Elisa","Operador de Slitter","Produção","Feminino",2.0,7.4,"Média","Média"],
        ["Fabio","Operador de Slitter","Produção","Masculino",1.6,6.8,"Média","Média"],
        ["Gabriela","Técnico de Qualidade","Qualidade","Feminino",4.1,8.5,"Alta","Alta"],
        ["Henrique","Operador de Slitter","Produção","Masculino",6.3,7.2,"Média","Média"],
        ["Isabela","Analista de Processos Pl","Engenharia","Feminino",4.8,9.0,"Alta","Alta"],
        ["João","Analista de PCP","PCP","Masculino",2.1,7.9,"Média","Alta"],
        ["Karen","Técnico de Qualidade","Qualidade","Feminino",3.3,8.7,"Alta","Alta"],
        ["Lucas","Supervisor de Produção","Produção","Masculino",7.0,8.8,"Alta","Alta"],
    ], columns=AVALIACOES_COLS)

    return cargos, maturidade, skills, pdi, avaliacoes

def garantir_estrutura():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    pdi_path = data_dir / "pdi_registros.xlsx"
    if not pdi_path.exists():
        _, _, _, pdi, _ = criar_bases()
        pdi.to_excel(pdi_path, index=False)

def carregar_dados_iniciais():
    cargos, maturidade, skills, pdi, avaliacoes = criar_bases()
    garantir_estrutura()
    pdi_path = Path("data") / "pdi_registros.xlsx"
    if pdi_path.exists():
        try:
            pdi = pd.read_excel(pdi_path)
        except Exception:
            pass
    return cargos, maturidade, skills, pdi, avaliacoes

def salvar_pdi(df):
    garantir_estrutura()
    df.to_excel(Path("data") / "pdi_registros.xlsx", index=False)

def gerar_excel_export(cargos_df, maturidade_df, skills_df, pdi_df, avaliacoes_df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        cargos_df.to_excel(writer, index=False, sheet_name="Cargos")
        maturidade_df.to_excel(writer, index=False, sheet_name="Competencias_Matriz")
        skills_df.to_excel(writer, index=False, sheet_name="Skills")
        pdi_df.to_excel(writer, index=False, sheet_name="PDI")
        avaliacoes_df.to_excel(writer, index=False, sheet_name="Meritocracia_Headcount")
    output.seek(0)
    return output.getvalue()

def gerar_pdf_cargo(detalhe):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#22d3ee"))
    c.setLineWidth(1)
    c.rect(10*mm, 10*mm, width-20*mm, height-20*mm, fill=0, stroke=1)
    c.setFillColor(colors.HexColor("#e5f9ff"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(18*mm, height-20*mm, "Relatório de Cargo - RH Estratégico Industrial 4.0")
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(18*mm, height-33*mm, str(detalhe["Cargo"]))
    y = height - 45*mm
    c.setFont("Helvetica", 10)
    linhas = [
        f"Área: {detalhe['Área']}",
        f"Família: {detalhe['Família']}",
        f"Nível: {detalhe['Nível']}",
        f"Grade: {detalhe['Grade']}",
        f"Gestor: {detalhe['Gestor']}",
        f"Faixa Mínima: {formatar_moeda(float(detalhe['Faixa Salarial Mín']))}",
        f"Faixa Média: {formatar_moeda(float(detalhe['Faixa Salarial Média']))}",
        f"Faixa Máxima: {formatar_moeda(float(detalhe['Faixa Salarial Máx']))}",
        f"Descrição: {detalhe['Descrição Resumida']}",
        f"Atividades: {detalhe['Atividades do Cargo']}",
        f"Pré-requisitos Obrigatórios: {detalhe['Pré-requisitos Obrigatórios']}",
        f"Pré-requisitos Desejáveis: {detalhe['Pré-requisitos Desejáveis']}",
        f"Escolaridade: {detalhe['Escolaridade']}",
        f"Experiência: {detalhe['Experiência']}",
        f"Trilha de Carreira: {detalhe['Trilha de Carreira']}",
    ]
    def quebrar(texto, limite=115):
        partes = []
        while len(texto) > limite:
            corte = texto.rfind(" ", 0, limite)
            if corte <= 0:
                corte = limite
            partes.append(texto[:corte])
            texto = texto[corte:].strip()
        partes.append(texto)
        return partes
    for linha in linhas:
        for sub in quebrar(linha):
            c.drawString(18*mm, y, sub)
            y -= 6*mm
            if y < 20*mm:
                c.showPage()
                c.setFillColor(colors.HexColor("#0f172a"))
                c.rect(0, 0, width, height, fill=1, stroke=0)
                c.setFillColor(colors.white)
                c.setFont("Helvetica", 10)
                y = height - 20*mm
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.setFont("Helvetica-Oblique", 9)
    c.drawRightString(width-18*mm, 12*mm, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def radar_fig(df_plot, titulo):
    categorias = df_plot["Skill"].tolist()
    valores = df_plot["Nível"].tolist()
    if not categorias:
        categorias = ["Sem dados"]
        valores = [0]
    categorias = categorias + [categorias[0]]
    valores = valores + [valores[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=valores, theta=categorias, fill="toself", name=titulo,
                                  line=dict(width=3, color="#00e5ff"), fillcolor="rgba(0,229,255,0.22)"))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5], color="#dbeafe"),
                   angularaxis=dict(color="#dbeafe"), bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f3f4f6"), showlegend=False, height=440,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def carregar_logo():
    path = Path("assets/logo_rh_industrial.png")
    return str(path) if path.exists() else None

def sidebar_global():
    aplicar_tema()
    if "dados_carregados" not in st.session_state:
        cargos_df, maturidade_df, skills_df, pdi_df, avaliacoes_df = carregar_dados_iniciais()
        st.session_state["dados_carregados"] = {
            "cargos": cargos_df, "maturidade": maturidade_df, "skills": skills_df,
            "pdi": pdi_df, "avaliacoes": avaliacoes_df
        }
    dados = st.session_state["dados_carregados"]

    st.sidebar.title("⚙️ Painel de Controle")
    fonte = st.sidebar.radio("Fonte de dados", ["Base de exemplo", "Upload de planilhas"], key="fonte_global")

    if fonte == "Upload de planilhas":
        arq_cargos = st.sidebar.file_uploader("Planilha cargos e salários", type=["xlsx"], key="uploader_cargos")
        arq_maturidade = st.sidebar.file_uploader("Planilha maturidade", type=["xlsx"], key="uploader_maturidade")
        arq_skills = st.sidebar.file_uploader("Planilha hard e soft skills", type=["xlsx"], key="uploader_skills")
        arq_pdi = st.sidebar.file_uploader("Planilha PDI", type=["xlsx"], key="uploader_pdi")
        arq_avaliacoes = st.sidebar.file_uploader("Planilha avaliações e headcount", type=["xlsx"], key="uploader_avaliacoes")
        if arq_cargos is not None: dados["cargos"] = pd.read_excel(arq_cargos)
        if arq_maturidade is not None: dados["maturidade"] = pd.read_excel(arq_maturidade)
        if arq_skills is not None: dados["skills"] = pd.read_excel(arq_skills)
        if arq_pdi is not None:
            dados["pdi"] = pd.read_excel(arq_pdi)
            salvar_pdi(dados["pdi"])
        if arq_avaliacoes is not None: dados["avaliacoes"] = pd.read_excel(arq_avaliacoes)

    cargos_df = dados["cargos"].copy()
    maturidade_df = dados["maturidade"].copy()
    skills_df = dados["skills"].copy()
    pdi_df = dados["pdi"].copy()
    avaliacoes_df = dados["avaliacoes"].copy()

    for col in ["Faixa Salarial Mín","Faixa Salarial Média","Faixa Salarial Máx","Colaboradores"]:
        cargos_df[col] = pd.to_numeric(cargos_df[col], errors="coerce").fillna(0)
    skills_df["Nível"] = pd.to_numeric(skills_df["Nível"], errors="coerce").fillna(0)
    maturidade_df["Nível de Maturidade"] = pd.to_numeric(maturidade_df["Nível de Maturidade"], errors="coerce").fillna(0)
    if "Nota Meritocracia" in avaliacoes_df.columns:
        avaliacoes_df["Nota Meritocracia"] = pd.to_numeric(avaliacoes_df["Nota Meritocracia"], errors="coerce").fillna(0)
    if "Tempo de Casa (anos)" in avaliacoes_df.columns:
        avaliacoes_df["Tempo de Casa (anos)"] = pd.to_numeric(avaliacoes_df["Tempo de Casa (anos)"], errors="coerce").fillna(0)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔎 Filtros")
    areas = ["Todas"] + sorted(cargos_df["Área"].dropna().astype(str).unique().tolist())
    niveis = ["Todos"] + sorted(cargos_df["Nível"].dropna().astype(str).unique().tolist())
    familias = ["Todas"] + sorted(cargos_df["Família"].dropna().astype(str).unique().tolist())

    f_area = st.sidebar.selectbox("Área", areas, key="f_area")
    f_nivel = st.sidebar.selectbox("Nível", niveis, key="f_nivel")
    f_familia = st.sidebar.selectbox("Família", familias, key="f_familia")

    filtro = cargos_df.copy()
    if f_area != "Todas": filtro = filtro[filtro["Área"] == f_area]
    if f_nivel != "Todos": filtro = filtro[filtro["Nível"] == f_nivel]
    if f_familia != "Todas": filtro = filtro[filtro["Família"] == f_familia]

    lista_cargos = sorted(filtro["Cargo"].dropna().astype(str).unique().tolist())
    cargo_selecionado = st.sidebar.selectbox("Cargo para detalhamento", lista_cargos if lista_cargos else ["Sem dados"], key="cargo_det")

    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Templates")
    base_cargos, base_maturidade, base_skills, base_pdi, base_avaliacoes = criar_bases()
    st.sidebar.download_button("Template cargos e salários", to_excel_bytes(base_cargos, "cargos_salarios"), "template_cargos_salarios.xlsx")
    st.sidebar.download_button("Template maturidade", to_excel_bytes(base_maturidade, "maturidade_base"), "template_maturidade.xlsx")
    st.sidebar.download_button("Template skills", to_excel_bytes(base_skills, "skills_base"), "template_skills.xlsx")
    st.sidebar.download_button("Template PDI", to_excel_bytes(base_pdi, "pdi_base"), "template_pdi.xlsx")
    st.sidebar.download_button("Template avaliações e headcount", to_excel_bytes(base_avaliacoes, "avaliacoes_headcount"), "template_avaliacoes_headcount.xlsx")

    return cargos_df, maturidade_df, skills_df, pdi_df, avaliacoes_df, filtro, cargo_selecionado
