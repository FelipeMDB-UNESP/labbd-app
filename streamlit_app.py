import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "signed_in" not in st.session_state:
    st.session_state.signed_in = False

if "logging_in" not in st.session_state:
    st.session_state.logging_in = False

def login():

    st.set_page_config(layout="centered")
        
    st.title("Bem vindo à Central")
    left, right = st.columns([0.12,0.88])
    
    if left.button("Sign in"):
        st.session_state.signed_in = True
        st.session_state.reload = True
        st.rerun()
    if right.button("Log in"):
        st.session_state.logging_in = True
        st.session_state.reload = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

def logar():
    import streamlit as st
    import mysql.connector

    st.header("Dashboard com informações escolares")

    def existencia(nome_usuario, senha):

        # Configurações de conexão com o MySQL
        conn = mysql.connector.connect(host=st.secrets["DB_HOST"]
                                , user=st.secrets["DB_USERNAME"], password=st.secrets["DB_PASSWORD"]
                                , port=st.secrets["DB_PORT"], db=st.secrets["DB_NAME"]
                                , auth_plugin='mysql_native_password')
        cursor = conn.cursor()

        sql_command = f"""SELECT * FROM usuario WHERE nomeUsuario = '{nome_usuario}' and senha = SHA('{senha}');"""
        cursor.execute(sql_command)
        res = cursor.fetchall()

        if res == []:
            cursor.close()
            conn.close()
            return False
        
        cursor.close()
        conn.close()
        return True
    
    with st.form("login"):
        st.title('Login de Usuário')
        nome_usuario = st.text_input('Nome de usuário:')
        senha = st.text_input('Senha:', type="password")
        submit = st.form_submit_button("Enviar")

    if submit and existencia(nome_usuario, senha):
        # Se o formulário for submetido e os dados estiverem válidos
        st.session_state.logging_in = False
        st.session_state.logged_in = True
        st.rerun()
    elif submit:
        
        # Se o formulário for submetido mas com dados inválidos
        st.warning("Dados inválidos")

    if st.button("Voltar"):
        st.session_state.logging_in = False
        st.rerun()

def cadastrar():
    import streamlit as st
    import mysql.connector
    import datetime

    st.header("Dashboard com informações escolares")

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
            VALUES ('{nome}', '{email}', '{nome_usuario}', '{tipoPerfil}', SHA1('{senha}'), '{dt_nasc}')
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
        st.title('Cadastro de Usuário')
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
        st.session_state.signed_in = False
        st.session_state.logged_in = True
        st.rerun()
    elif submit:
        # Se o formulário for submetido mas com dados inválidos
        st.warning("Dados inválidos")

    if st.button("Voltar"):
        st.session_state.signed_in = False
        st.rerun()


login_page = st.Page(login, title="Log in", icon=":material/login:")
logging_page = st.Page(logar, title="Logging in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

inicio = st.Page(
    "feito/Inicio.py", title="Início", icon=":material/dashboard:", default=True
)

cadastro = st.Page(
    cadastrar, title="Cadastro de Usuário", icon=":material/dashboard:"
)

escolas = st.Page(
    "feito/Escolas.py", title="Escolas", icon=":material/school:"
)

graficos = st.Page(
    "feito/Gráficos.py", title="Gráficos", icon=":material/bar_chart:"
)

geolocalizacao = st.Page(
    "feito/Geolocalização.py", title="Localizações", icon=":material/map:"
)

favoritos = st.Page(
    "feito/Favoritos.py", title="Favoritos", icon=":material/star:"
)

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Dashboards": [inicio, escolas, graficos, geolocalizacao, favoritos],
        }
    )

elif st.session_state.signed_in:
    pg = st.navigation([cadastro])

elif st.session_state.logging_in:
    pg = st.navigation([logging_page])

else:
    pg = st.navigation([login_page])

pg.run()