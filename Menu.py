import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

st.set_page_config(page_title="Laboratório de Banco de Dados", layout="wide")

st.title("Bem-vindo ao Sistema de Gerenciamento Escolar")

st.sidebar.header("Navegação")
page = st.sidebar.radio("Ir para", ["Visão Geral", "Análise de Dados", "Configurações"])

conn = mysql.connector.connect(host=st.secrets.DB_HOST,
                               user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD,
                               port=st.secrets.DB_PORT, db=st.secrets.DB_NAME,
                               auth_plugin='mysql_native_password')

cursor = conn.cursor()

if page == "Visão Geral":
    st.subheader("Visão Geral dos Dados")
    cursor.execute("select * from escola;")
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)
    st.write(df)

elif page == "Análise de Dados":
    st.subheader("Análise de Dados")
    cursor.execute("select * from escola;")
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)
    
    # Limit the number of schools for better readability
    df_limited = df.head(20)
    
    st.write("Número de Salas Utilizadas por Escola")
    fig, ax = plt.subplots()
    df_limited.plot(kind='scatter', x='NO_ENTIDADE', y='NU_SALAS_UTILIZADAS', ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

elif page == "Configurações":
    st.subheader("Configurações")
    st.write("Configurações da aplicação")

cursor.close()
conn.close()