import streamlit as st
import pandas as pd
import mysql.connector

# Inicializa a variável na Session
if 'escolas' not in st.session_state:
    st.session_state['escolas'] = []

# Gera um dataframe
def load_escolas():
	conn = mysql.connector.connect(host=st.secrets["DB_HOST"]
                               , user=st.secrets["DB_USERNAME"], password=st.secrets["DB_PASSWORD"]
                               , port=st.secrets["DB_PORT"], db=st.secrets["DB_NAME"]
                               , auth_plugin='mysql_native_password')
	cursor = conn.cursor()
	cursor.execute("select * from vw_escola;")
	res = cursor.fetchall()
	df = pd.DataFrame(res, columns=cursor.column_names)
	return df

# Carrega o valor na Session
st.session_state['escolas'] = load_escolas()

# Escreve o valor armazenado na Session
# Esta mesma variável pode ser usada em outras páginas ou na mesma, desde que a aba não seja fechada nem o servidor reiniciado
st.write(st.session_state['escolas'])
