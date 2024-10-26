import streamlit as st
import pandas as pd
import mysql.connector

st.header("Aula de laboratório de banco de dados")

conn = mysql.connector.connect(host="localhost"
                               , user="root", password="aluno"
                               , port=3306, db="labbd"
                               , auth_plugin='mysql_native_password')

cursor = conn.cursor()

cursor.execute("select * from vw_escola;")
res = cursor.fetchall()
df = pd.DataFrame(res, columns=cursor.column_names)

with st.sidebar:
    st.header("Selecione:")    
	# Objeto df contém a estrutura tabular retornada, em formato Pandas DataFrame
	# 	podemos acessar o conteúdo da coluna por seu nome, ex: df['nome_coluna']
	#	algumas operações podem ser aplicadas sobre essa estrutura, similar às do SQL (ex: unique = DISTINCT)
	# Nos exemplos abaixo, os widgets recebem os valores únicos dos campos
    dpa = st.multiselect("Dependência administrativa", df['TP_DEPENDENCIA'].unique())
    lc = st.radio("Localização", df['TP_LOCALIZACAO'].unique())

# Escreve na página o resultado da consulta, conforme os valores selecionados em ambos os filtros (lc e dpa, definidos acima)
st.write(df[
    	(df["TP_LOCALIZACAO"]==lc) & 
        (df["TP_DEPENDENCIA"].isin(dpa))
        ])