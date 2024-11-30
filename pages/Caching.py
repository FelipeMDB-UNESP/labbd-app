import streamlit as st
import pandas as pd
import mysql.connector

# Usa o padrão decorator para registrar a assinatura a ser armazenada em cache
# ttl = duração (em segundos) da persistência em cache
# max_entries = total de objetos carregados no cache
# show_spinner = mostra widget de carregamente de dados, que desaparecerá ao final do carregamento
@st.cache_data(ttl=10, show_spinner="Fetching data from API...")
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

# Teste novamente depois do tempo definido no parâmetro ttl para ver a diferença
st.button("Rerun")