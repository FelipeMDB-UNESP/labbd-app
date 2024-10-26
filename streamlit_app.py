import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

st.header("Aula de laboratório de banco de dados")
st.title("Título")

st.sidebar.header("Cabeçalho sidebar")
st.sidebar.radio("radiobutton", [1,2])

conn = mysql.connector.connect(host="localhost"
                               , user="root", password="batata123"
                               , port=3306, db="censo_escolar"
                               , auth_plugin='mysql_native_password')

cursor = conn.cursor()

cursor.execute("select * from escola;")
res = cursor.fetchall()
df = pd.DataFrame(res, columns=cursor.column_names)

st.write(df)