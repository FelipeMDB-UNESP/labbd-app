import streamlit as st
import mysql.connector
import datetime
import pandas as pd

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "new_usuario" not in st.session_state:
    st.session_state.new_usuario = ""

if "new_senha" not in st.session_state:
    st.session_state.new_senha = ""

def submitted():
    st.session_state.submitted = True
def reset():
    st.session_state.submitted = False

def existe(nome_usuario, senha):

    # Configurações de conexão com o MySQL
    conn = mysql.connector.connect(host=st.secrets["DB_HOST"]
                            , user=st.secrets["DB_USERNAME"], password=st.secrets["DB_PASSWORD"]
                            , port=st.secrets["DB_PORT"], db=st.secrets["DB_NAME"]
                            , auth_plugin='mysql_native_password')
    cursor = conn.cursor()

    sql_command = f"""SELECT * FROM usuario WHERE usuario.nomeUsuario = '{nome_usuario}' AND usuario.senha = '{senha}';"""
    cursor.execute(sql_command)

    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)

    cursor.close()
    conn.close()
    return not df.empty

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
        VALUES ('{nome}', '{email}', '{nome_usuario}', '{tipoPerfil}', '{senha}', '{dt_nasc}')
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


def set_login():
    left, right = st.columns([0.12,0.88])

    if left.button("Sign in"):
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
            print(submit)
            if submit:
                print("é:" + nome_usuario)
                print("Deu quase certo")
                if validar(nome, email, nome_usuario, senha, dt_nasc, tipoPerfil):

                    # Se o formulário for submetido e os dados estiverem válidos
                    cadastra_usuario(nome, email, nome_usuario, senha, dt_nasc, tipoPerfil)
                    print("Deu certo")
                    st.session_state.logged_in = True
                    st.rerun()
    
    if right.button("Log in", on_click=reset):
        reset()
        with st.form("login"):
            st.title('Login:')
            st.text_input('Usuário:', key= 'new_usuario')
            st.text_input('Senha:', type="password", key='new_senha')
            st.form_submit_button("Continuar", on_click=submitted)
        
        if 'submitted' in st.session_state:
            if st.session_state.submitted == True:
                print("é:" + st.session_state.new_usuario)
                print("Deu quase bom")
                nome_usuario = st.session_state.new_usuario
                senha = st.session_state.new_senha
                if existe(nome_usuario,senha):
                    print("Deu bom")
                    st.session_state.logged_in = True
                    reset()
                    st.rerun()
                        

# def login():
#     left, right = st.columns([0.12,0.88])
    
#     if left.button("Sign in"):
#         st.session_state.logged_in = True
#         st.rerun()
#     if right.button("Log in"):
#         st.session_state.logged_in = True
#         st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(set_login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

inicio = st.Page(
    "trabalho/inicio.py", title="Início", icon=":material/dashboard:", default=True
)

cadastro = st.Page(
    "trabalho/Cadastro.py", title="Cadastro", icon=":material/dashboard:"
)

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Dashboards": [inicio],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()