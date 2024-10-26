import streamlit as st
import pandas as pd
import mysql.connector

# Necessário criar um arquivo 'secrets.toml' em um diretório '.streamlit' no mesmo 
#	diretório do arquivo da aplicação principal
# Ele deve conter o seguinte texto (sem os comentários):
# DB_USERNAME="bruno"
# DB_PASSWORD="1234"
# DB_HOST="localhost"
# DB_PORT="3306"
# DB_NAME="labbd"

st.header("Aula de laboratório de banco de dados")

# Os secrets podem ser acessados de duas maneiras:
# i) pelo nome definido no arquivo 'secrets.toml': st.secrets.DB_HOST
# ii) pelo seu nome de índice: st.secrets['DB_HOST']
conn = mysql.connector.connect(host=st.secrets.DB_HOST
                               , user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD
                               , port=3306, db=st.secrets['DB_NAME']
                               , auth_plugin='mysql_native_password')

cursor = conn.cursor()
