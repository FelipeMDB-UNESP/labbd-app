import streamlit as st
import pandas as pd
import mysql.connector

if "botao1" not in st.session_state:
    st.session_state.botao1 = True

if "botao2" not in st.session_state:
    st.session_state.botao2 = True

if "botao3" not in st.session_state:
    st.session_state.botao3 = True

if "botao4" not in st.session_state:
    st.session_state.botao4 = True

if "botao5" not in st.session_state:
    st.session_state.botao5 = True

if "botao6" not in st.session_state:
    st.session_state.botao6 = True

st.header("Gerenciamento de Escolas")

conn = mysql.connector.connect(host=st.secrets["DB_HOST"],
                               user=st.secrets["DB_USERNAME"], password=st.secrets["DB_PASSWORD"],
                               port=st.secrets["DB_PORT"], db=st.secrets["DB_NAME"],
                               auth_plugin='mysql_native_password')

cursor = conn.cursor()

def load_escolas():
    cursor.execute("SELECT NO_ENTIDADE, TP_SITUACAO_FUNCIONAMENTO, CO_MUNICIPIO, TP_LOCALIZACAO, TP_DEPENDENCIA, IN_COMUM_FUND_AI, IN_COMUM_FUND_AF, IN_COMUM_MEDIO_MEDIO, IN_COMUM_MEDIO_NORMAL, IN_COMUM_EJA_FUND, IN_COMUM_EJA_MEDIO, IN_COMUM_EJA_PROF, IN_COMUM_PROF FROM escola;")
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)
    return df

def load_totals():
    cursor.execute("SELECT * FROM resumo_escolas;")
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)
    return df

def load_escola_turmas():
    cursor.execute("SELECT * FROM v_escola_turmas;")
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)
    return df

def load_professores_alunos():
    cursor.execute("SELECT * FROM vw_professores_alunos_por_escola;")
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)
    return df

def load_alunos_por_nivel():
    cursor.execute("SELECT * FROM vw_alunos_por_nivel_ensino;")
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)
    return df

if st.button("Listar Escolas"):
    if st.session_state.botao1:
        st.subheader("Lista de Escolas")
        st.session_state.botao1 = False
        st.session_state.botao2 = True
        st.session_state.botao3 = True
        st.session_state.botao4 = True
        st.session_state.botao5 = True
        st.session_state.botao6 = True
        df_escolas = load_escolas()
        st.write(df_escolas)
    else:
        st.session_state.botao1 = True

if st.button("Mostrar Totais por Escola"):
    if st.session_state.botao2:
        st.subheader("Totais por Escola")
        st.session_state.botao1 = True
        st.session_state.botao2 = False
        st.session_state.botao3 = True
        st.session_state.botao4 = True
        st.session_state.botao5 = True
        st.session_state.botao6 = True
        df_totals = load_totals()
        st.write(df_totals)
    else:
        st.session_state.botao2 = True

if st.button("Ordenar Escolas por Número de Alunos"):
    if st.session_state.botao3:
        st.subheader("Escolas Ordenadas por Número de Alunos")
        st.session_state.botao1 = True
        st.session_state.botao2 = True
        st.session_state.botao3 = False
        st.session_state.botao4 = True
        st.session_state.botao5 = True
        st.session_state.botao6 = True
        df_totals = load_totals()
        df_sorted = df_totals.sort_values(by="TOTAL_ALUNOS", ascending=False)
        st.write(df_sorted)
    else:
        st.session_state.botao3 = True

if st.button("Ver Escolas e suas turmas"):
    if st.session_state.botao4:
        st.subheader("Escola e suas turmas")
        st.session_state.botao1 = True
        st.session_state.botao2 = True
        st.session_state.botao3 = True
        st.session_state.botao4 = False
        st.session_state.botao5 = True
        st.session_state.botao6 = True
        df_uma_escola = load_escola_turmas()
        st.write(df_uma_escola)
    else:
        st.session_state.botao4 = True

if st.button("Ver Professores e Alunos por Escola"):
    if st.session_state.botao5:
        st.subheader("Professores e Alunos por Escola")
        st.session_state.botao1 = True
        st.session_state.botao2 = True
        st.session_state.botao3 = True
        st.session_state.botao4 = True
        st.session_state.botao5 = False
        st.session_state.botao6 = True
        df_professores_alunos = load_professores_alunos()
        st.write(df_professores_alunos)
    else:
        st.session_state.botao5 = True

if st.button("Ver Alunos por Nível de Ensino"):
    if st.session_state.botao6:
        st.subheader("Alunos por Nível de Ensino")
        st.session_state.botao1 = True
        st.session_state.botao2 = True
        st.session_state.botao3 = True
        st.session_state.botao4 = True
        st.session_state.botao5 = True
        st.session_state.botao6 = False
        df_alunos_por_nivel = load_alunos_por_nivel()
        st.write(df_alunos_por_nivel)
    else:
        st.session_state.botao6 = True

cursor.close()
conn.close()