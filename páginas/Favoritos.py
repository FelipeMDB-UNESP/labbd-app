import streamlit as st
import pandas as pd
import mysql.connector

st.header("Gerenciamento de Escolas Favoritas")

conn = mysql.connector.connect(
    host=st.secrets["DB_HOST"],
    user=st.secrets["DB_USERNAME"],
    password=st.secrets["DB_PASSWORD"],
    port=st.secrets["DB_PORT"],
    db=st.secrets["DB_NAME"],
    auth_plugin='mysql_native_password'
)

cursor = conn.cursor()

def load_favorite_schools(user_id):
    query = """
    SELECT e.CO_ENTIDADE, e.NO_ENTIDADE
    FROM bookmark b
    JOIN escola e ON b.CO_ENTIDADE = e.CO_ENTIDADE
    WHERE b.id_usuario = %s;
    """
    cursor.execute(query, (user_id,))
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=["CO_ENTIDADE", "NO_ENTIDADE"])
    return df

def load_all_schools():
    query = "SELECT CO_ENTIDADE, NO_ENTIDADE FROM escola;"
    cursor.execute(query)
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=["CO_ENTIDADE", "NO_ENTIDADE"])
    return df

def add_favorite_school(user_id, school_id):
    query = "INSERT INTO bookmark (id_usuario, co_entidade) VALUES (%s, %s);"
    cursor.execute(query, (user_id, school_id))
    conn.commit()

def is_school_favorite(user_id, school_id):
    query = "SELECT 1 FROM bookmark WHERE id_usuario = %s AND co_entidade = %s LIMIT 1;"
    cursor.execute(query, (user_id, school_id))
    return cursor.fetchone() is not None

def remove_favorite_school(user_id, school_id):
    query = "DELETE FROM bookmark WHERE id_usuario = %s AND co_entidade = %s;"
    cursor.execute(query, (user_id, school_id))
    conn.commit()

user_id = st.session_state.get('user_id')

if "update_favorites" not in st.session_state:
    st.session_state.update_favorites = False

st.subheader("Adicionar Nova Escola aos Favoritos")
df_all_schools = load_all_schools()

school_choice = st.selectbox(
    "Selecione uma escola para adicionar aos favoritos:",
    df_all_schools['NO_ENTIDADE']
)

if school_choice:
    selected_school_id = int(df_all_schools[df_all_schools['NO_ENTIDADE'] == school_choice].iloc[0]['CO_ENTIDADE'])

    if is_school_favorite(user_id, selected_school_id):
        st.warning(f"A escola '{school_choice}' já está nos seus favoritos.")
    else:
        if st.button("Adicionar Escola aos Favoritos"):
            add_favorite_school(user_id, selected_school_id)
            st.session_state.update_favorites = True
            st.success(f"Escola '{school_choice}' adicionada aos favoritos!")

st.subheader("Suas Escolas Favoritas")

df_favorites = load_favorite_schools(user_id)

if not df_favorites.empty:
    for index, row in df_favorites.iterrows():
        col1, col2 = st.columns([3, 1])
        col1.write(row["NO_ENTIDADE"])
        if col2.button("Remover", key=f"remove_{row['CO_ENTIDADE']}"):
            remove_favorite_school(user_id, row["CO_ENTIDADE"])
            st.success(f"Escola '{row['NO_ENTIDADE']}' removida dos favoritos!")
            st.session_state.update_favorites = False
            st.rerun()
else:
    st.info("Você ainda não possui escolas favoritas.")

cursor.close()
conn.close()
