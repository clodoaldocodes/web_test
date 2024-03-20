import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

#######################
# Page configuration
st.set_page_config(
    page_title="NDVI Viewer",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded")

# Enable dark theme for Altair
alt.themes.enable("dark")

def plot_ndvi(df):
    # Plotar o gráfico usando Plotly Express
    fig = px.line(df, x='Datetime', y='Mean', title='Normalized Difference Vegetation Index (NDVI)')
    st.plotly_chart(fig)

def main():
    st.title('Visualizador de NDVI')
    
    # Upload do arquivo CSV
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Ler o arquivo CSV
            df = pd.read_csv(uploaded_file)
            
            # Verificar se as colunas 'data' e 'ndvi' estão presentes
            if 'Datetime' in df.columns and 'Mean' in df.columns:
                # Plotar o gráfico
                plot_ndvi(df)
            else:
                st.error("O arquivo CSV não contém as colunas 'Datetime' e 'Mean'.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    main()
