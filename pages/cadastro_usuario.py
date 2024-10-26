import streamlit as st
import mysql.connector
import datetime

st.header("Aula de laboratório de banco de dados")
st.write("**Conceitos Streamlit**")

def validar(nome, email, nome_usuario, senha, dt_nasc, tipoPerfil):
    if nome == "" or email == "" or nome_usuario == "" or senha == "" or dt_nasc == "" or tipoPerfil == "":
        return False
    return True

def cadastra_usuario(nome, email, nome_usuario, senha, dt_nasc, tipoPerfil):
    # Configurações de conexão com o MySQL
    conn = mysql.connector.connect(
        host='localhost', user='root', password='batata123',
        port=3306, db='censo_escolar', auth_plugin='mysql_native_password'
    )
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

with st.form("cadastro"):
    st.title('Cadastro de usuários')
    nome = st.text_input('Nome:')
    email = st.text_input('Email:')
    nome_usuario = st.text_input('Nome de usuário:')
    senha = st.text_input('Senha:', type="password")
    dt_nasc = st.date_input(
        'Data de nascimento:',
        min_value=datetime.date(1924, 1, 1),
        max_value=datetime.date(2024, 1, 1),
        format="DD/MM/YYYY"
    )
    tipoPerfil = st.selectbox("Tipo de perfil:", ["Gerencial", "Aberto"])
    submit = st.form_submit_button("Enviar")

if submit and validar(nome, email, nome_usuario, senha, dt_nasc, tipoPerfil):
    # Se o formulário for submetido e os dados estiverem válidos
    cadastra_usuario(nome, email, nome_usuario, senha, dt_nasc, tipoPerfil)
elif submit:
    # Se o formulário for submetido mas com dados inválidos
    st.warning("Dados inválidos")
