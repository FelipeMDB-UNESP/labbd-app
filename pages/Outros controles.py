import time
import streamlit as st

########################################################################################
# Insere uma imagem de logo no sidebar
st.logo("https://igce.rc.unesp.br/images/unesp.svg")

# Insere uma imagem no corpo da página, ajustando sua dimensão e adicionando legenda
st.image("https://igce.rc.unesp.br/Home/DiretoriaTecnicaAcademica/staepe/brasaoigce.gif", caption="IGCE/Unesp", width=150)

# Embute vídeos de diferentes fontes, como do Youtube
st.video("https://www.youtube.com/watch?v=KmcoofohV64")

########################################################################################
# Exibe formatação para diferentes tipos de mensagens de feedback ao usuário
st.success("Sucesso", icon="✅")
st.info("Informação", icon="ℹ️")
st.warning("Aviso", icon="⚠️")
st.error("Erro", icon="⛔")

########################################################################################
# Widgets para indicar o processamento ou carregamento de dados
with st.spinner("Aguarde..."):
	time.sleep(5)
	st.write("Conteúdo carregado")

with st.status("Fazendo download dos dados...", expanded=True) as status:
	st.write("Buscando dados..")
	time.sleep(2)
	st.write("URL encontrada")
	time.sleep(1)
	st.write("Fazendo download dos dados")
	time.sleep(1)
	status.update(label="Download completo", state="complete", expanded=False)

progress_text = "Aguarde. Processando..."
my_bar = st.progress(0, text=progress_text)
for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
#my_bar.empty()

st.button("Reexecute a barra de progresso")

########################################################################################

if st.button("Diga!"):
	st.toast("Hip")
	time.sleep(0.5)
	st.toast("Hip")
	time.sleep(0.5)
	st.toast("Hooray")

if st.button("Clique aqui para nevar"):
	st.snow()

if st.button("Clique aqui para soltar balões"):
	st.balloons()
