import streamlit as st

st.header("Localização da Escolas")

st.markdown(
    """
    <style>
        .responsive-iframe-container {
            position: relative;
            width: 100%;
            height: 0;
            padding-bottom: 56.25%; /* Proporção 16:9 */
            overflow: hidden;
        }
        .responsive-iframe-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }
        /* Ajuste para telas menores */
        @media (max-width: 600px) {
            .responsive-iframe-container {
                padding-bottom: 150%; /* Ajusta a proporção para telas menores */
            }
        }
        /* Ajuste para telas maiores */
        @media (min-width: 1200px) {
            .responsive-iframe-container {
                padding-bottom: 75%; /* Aumenta a altura para telas maiores */
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Exemplo de como adicionar o iframe
tableau_url = "https://public.tableau.com/views/SchoolsGeolocationRioClaro-SPBrazil/Geoloc?:embed=y&:showVizHome=no&:host_url=https%3A%2F%2Fpublic.tableau.com%2F&:embed_code_version=3&:tabs=no&:toolbar=yes&:animate_transition=yes&:display_static_image=no&:display_spinner=no&:display_overlay=yes&:display_count=yes&:language=en-US&:tooltip=no&:showShareOptions=false&publish=yes&:loadOrderID=0"  # Substitua pela URL do seu iframe
st.markdown(
    f"""
    <div class="responsive-iframe-container">
        <iframe src="{tableau_url}" frameborder="0" allowfullscreen></iframe>
    </div>
    """,
    unsafe_allow_html=True
)