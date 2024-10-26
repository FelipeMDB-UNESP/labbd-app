import streamlit as st



with st.form("cadastro"):
	st.title('Cadastro de usuários')
	nome = st.text_input('Nome:')
	email = st.text_input('Email:')
	senha = st.text_input('Senha:', type="password")
	submit = st.form_submit_button("Enviar")
	
if submit:
	st.write("Form submetido")