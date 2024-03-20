import streamlit as st
import pandas as pd
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="NDVI Viewer",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded")

def plot_ndvi(df, x_variable, y_variable, title):
    # Plotar o gráfico usando Plotly Express
    fig = px.line(df, x=x_variable, y=y_variable, title=title)
    fig.update_layout(xaxis_title=x_variable, yaxis_title=y_variable)
    fig.update_yaxes(range=[0, 1])
    st.plotly_chart(fig)

def main():
    st.title('NDVI Viewer')
    
    # Upload dos arquivos CSV
    uploaded_files = st.file_uploader("Escolha dois arquivos CSV", type=["csv"], accept_multiple_files=True)
    
    if uploaded_files is not None and len(uploaded_files) == 2:
        try:
            # Ler os arquivos CSV
            dfs = [pd.read_csv(file) for file in uploaded_files]
            
            # Verificar se as colunas 'Datetime' e 'ndvi' estão presentes em ambos os DataFrames
            if all('Datetime' in df.columns and 'Mean' in df.columns for df in dfs):
                # Selecionar variáveis para os eixos x e y usando menu suspenso
                y_variable = st.selectbox("Selecione a variável para o eixo y:", ['Mean'] + dfs[0].columns.tolist(), key="y_variable")
                
                # Plotar gráficos separados
                st.subheader("Gráficos Separados:")
                for i, df in enumerate(dfs):
                    x_variable = st.selectbox(f"Selecione a variável x para o gráfico {i+1}:", ['Datetime'] + df.columns.tolist(), key=f"x_variable_{i}")
                    plot_ndvi(df, x_variable, y_variable, f"Gráfico {i+1}")
                
                # Plotar gráfico combinado
                st.subheader("Gráfico Combinado:")
                combined_df = pd.concat(dfs)
                x_variable_combined = st.selectbox("Selecione a variável x para o gráfico combinado:", ['Datetime'] + combined_df.columns.tolist(), key="x_variable_combined")
                plot_ndvi(combined_df, x_variable_combined, y_variable, "Gráfico Combinado")
                
            else:
                st.error("Os arquivos CSV devem conter as colunas 'Datetime' e 'ndvi'.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
    elif uploaded_files is not None:
        st.error("Por favor, selecione dois arquivos CSV.")

if __name__ == "__main__":
    main()