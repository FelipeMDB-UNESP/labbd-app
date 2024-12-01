import streamlit as st
import pandas as pd
import mysql.connector

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
    cursor.execute("SELECT * FROM V_Escola_Turmas;")
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



botao_listar_escolas = st.button("Listar Escolas")
botao_totais_escolas = st.button("Mostrar Totais por Escola")
botao_ordenar_escolas = st.button("Ordenar Escolas por Número de Alunos")
botao_listar_turmas = st.button("Ver Escolas e suas turmas")
botao_professores_alunos = st.button("Ver Professores e Alunos por Escola")
botao_nivel_ensino = st.button("Ver Alunos por Nível de Ensino")



if botao_listar_escolas:
    st.subheader("Lista de Escolas")
    df_escolas = load_escolas()
    st.write(df_escolas)
    if botao_listar_escolas:
        botao_listar_escolas = False


if botao_totais_escolas:
    st.subheader("Totais por Escola")
    df_totals = load_totals()
    st.write(df_totals)

if botao_ordenar_escolas:
    st.subheader("Escolas Ordenadas por Número de Alunos")
    df_totals = load_totals()
    df_sorted = df_totals.sort_values(by="TOTAL_ALUNOS", ascending=False)
    st.write(df_sorted)

if botao_listar_turmas:
    st.subheader("Escola e suas turmas")
    df_uma_escola = load_escola_turmas()
    st.write(df_uma_escola)

if botao_professores_alunos:
    st.subheader("Professores e Alunos por Escola")
    df_professores_alunos = load_professores_alunos()
    st.write(df_professores_alunos)

if botao_nivel_ensino:
    st.subheader("Alunos por Nível de Ensino")
    df_alunos_por_nivel = load_alunos_por_nivel()
    st.write(df_alunos_por_nivel)

cursor.close()
conn.close()