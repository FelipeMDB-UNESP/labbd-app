import streamlit as st
import mysql.connector
import datetime
import pandas as pd

st.header("Dashboard com informações escolares")

def existencia(nome_usuario, senha):

    # Configurações de conexão com o MySQL
    conn = mysql.connector.connect(host=st.secrets["DB_HOST"]
                            , user=st.secrets["DB_USERNAME"], password=st.secrets["DB_PASSWORD"]
                            , port=st.secrets["DB_PORT"], db=st.secrets["DB_NAME"]
                            , auth_plugin='mysql_native_password')
    cursor = conn.cursor()

    sql_command = f"""SELECT * FROM usuario where nomeUsuario = '{nome_usuario}' and senha = '{senha}');"""
    cursor.execute(sql_command)

    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)

    cursor.close()
    conn.close()
    return (not df.empty)

def validar(nome, email, nome_usuario, senha, dt_nasc, tipoPerfil):
    if nome == "" or email == "" or nome_usuario == "" or senha == "" or dt_nasc == "" or tipoPerfil == "":
        return False
    return True

def cadastra_usuario(nome, email, nome_usuario, senha, dt_nasc, tipoPerfil):
    # Configurações de conexão com o MySQL
    conn = mysql.connector.connect(host=st.secrets["DB_HOST"]
                            , user=st.secrets["DB_USERNAME"], password=st.secrets["DB_PASSWORD"]
                            , port=st.secrets["DB_PORT"], db=st.secrets["DB_NAME"]
                            , auth_plugin='mysql_native_password')
    cursor = conn.cursor()

    # Comando de inserção com o campo nomeUsuario incluído
    inp = f"""
        INSERT INTO usuario (nome, email, nomeUsuario, tipoPerfil, senha, dataNascimento)
        VALUES ('{nome}', '{email}', '{nome_usuario}', '{tipoPerfil}', SHA('{senha}'), '{dt_nasc}')
    """
    try:
        cursor.execute(inp)
        conn.commit()
        st.success("Usuário cadastrado com sucesso.")
    except Exception as e:
        conn.rollback()
        st.error(f"Erro ao cadastrar o usuário: {e}")
    finally:
        cursor.close()
        conn.close()

with st.form("login"):
    st.title('Login de Usuário')
    nome_usuario = st.text_input('Nome de usuário:')
    senha = st.text_input('Senha:', type="password")
    submit = st.form_submit_button("Enviar")

if submit and existencia(nome_usuario, senha):
    # Se o formulário for submetido e os dados estiverem válidos
    cadastra_usuario(nome, email, nome_usuario, senha, dt_nasc, tipoPerfil)
elif submit:
    # Se o formulário for submetido mas com dados inválidos
    st.warning("Dados inválidos")
