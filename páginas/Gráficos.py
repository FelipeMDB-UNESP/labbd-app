import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

st.header("Alguns gráficos")

def load_escolas():
	conn = mysql.connector.connect(host=st.secrets["DB_HOST"]
                               , user=st.secrets["DB_USERNAME"], password=st.secrets["DB_PASSWORD"]
                               , port=st.secrets["DB_PORT"], db=st.secrets["DB_NAME"]
                               , auth_plugin='mysql_native_password')
	cursor = conn.cursor()
	cursor.execute("select * from escolas_view;")
	res = cursor.fetchall()
	df = pd.DataFrame(res, columns=cursor.column_names)
	return df

df = load_escolas()

# Exibe um gráfico de barras
st.bar_chart(df, x="NO_ENTIDADE", y="NU_COMPUTADOR", x_label="Escola", y_label="Total de computadores")

# Exibe um gráfico de linhas com os mesmos dados
st.line_chart(df, x="NO_ENTIDADE", y="NU_COMPUTADOR")

# Exibe um gráfico de dispersão
st.scatter_chart(df, x="NU_SALAS_EXISTENTES", y="NU_COMPUTADOR", x_label="Núm de salas", y_label="Total de computadores")

# Exibe dados para mapa
df = pd.DataFrame(
		np.random.randn(100,2) / [50,50] + [-22.4094224,-47.5632023],
		columns = ["lat", "lon"]
	)
st.map(df)