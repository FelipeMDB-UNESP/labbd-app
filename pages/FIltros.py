import streamlit as st
import pandas as pd
import mysql.connector

st.header("Aula de laboratório de banco de dados")

conn = mysql.connector.connect(
    host=st.secrets["DB_HOST"],
    user=st.secrets["DB_USERNAME"],
    password=st.secrets["DB_PASSWORD"],
    port=st.secrets["DB_PORT"],
    db=st.secrets["DB_NAME"],
    auth_plugin='mysql_native_password'
)

cursor = conn.cursor()

# Modificando a consulta para utilizar a view
cursor.execute("SELECT * FROM filtros_view;")
res = cursor.fetchall()
df = pd.DataFrame(res, columns=cursor.column_names)

with st.sidebar:
    st.header("Selecione:")    
    dpa = st.multiselect("Dependência administrativa", df['TP_DEPENDENCIA'].unique())
    lc = st.radio("Localização", df['TP_LOCALIZACAO'].unique())

# Aplica o filtro de acordo com as seleções no sidebar
st.write(df[
    (df["TP_LOCALIZACAO"] == lc) & 
    (df["TP_DEPENDENCIA"].isin(dpa))
])
