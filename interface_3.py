import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    fig.update_layout(xaxis_title=x_variable, yaxis_title=y_variable, title_x=0.5)  # Centralizar o título
    fig.update_yaxes(range=[0, 1])
    st.plotly_chart(fig, use_container_width=True)  # Usando a largura total da tela

def plot_ndvi_2(df1, df2, x_variable, y_variable1, y_variable2, title):
    # Adicionar caixas de texto para personalizar as legendas
    col1, col2 = st.columns(2)
    with col1:
        custom_legend1 = st.text_input("Legenda DataFrame 1:", value='DataFrame 1')
    with col2:
        custom_legend2 = st.text_input("Legenda DataFrame 2:", value='DataFrame 2')

    # Criar uma figura com dois subplots
    fig = go.Figure()

    # Adicionar o primeiro conjunto de dados ao primeiro subplot
    fig.add_trace(go.Scatter(x=df1[x_variable], y=df1[y_variable1], mode='lines', name=custom_legend1))

    # Adicionar o segundo conjunto de dados ao segundo subplot
    fig.add_trace(go.Scatter(x=df2[x_variable], y=df2[y_variable2], mode='lines', name=custom_legend2))

    # Atualizar o layout da figura
    fig.update_layout(title=title, xaxis_title=x_variable, yaxis_title='NDVI', title_x=0.5)  # Centralizar o título
    fig.update_yaxes(range=[0, 1])
    st.plotly_chart(fig, use_container_width=True)  # Usando a largura total da tela

def main():
    st.title('NDVI Viewer')
    
    # Upload dos arquivos CSV
    uploaded_files = st.file_uploader("Escolha dois arquivos CSV", type=["csv"], accept_multiple_files=True)
    
    if uploaded_files is not None and len(uploaded_files) == 2:
        try:
            # Ler os arquivos CSV
            dfs = [pd.read_csv(file) for file in uploaded_files]
            
            # Verificar se as colunas 'Datetime' e 'ndvi' estão presentes em ambos os DataFrames
            if all(('datetime' in map(str.lower, df.columns)) and ('mean' in map(str.lower, df.columns)) for df in dfs):
                # Selecionar variável para o eixo y usando menu suspenso
                y_variable_options = ['Mean'] + dfs[0].columns.tolist()
                
                # Plotar gráficos separados
                st.subheader("Gráficos Separados:")
                for i, df in enumerate(dfs):
                    x_variable = 'Datetime'  # Manter a mesma variável x para todos os gráficos
                    csv_name = uploaded_files[i].name
                    y_variable = st.selectbox(f"Selecione a variável y para o gráfico {i+1} ({csv_name}):", y_variable_options, key=f"y_variable_{i+1}_{csv_name}")  # Chave única
                    title = st.text_input(f"Digite o título do gráfico {i+1} ({csv_name}):", f"Gráfico {i+1}")
                    plot_ndvi(df, x_variable, y_variable, title)

                # Plotar gráficos sobrepostos
                st.subheader("Gráficos Sobrepostos:")
                x_variable = 'Datetime'  # Manter a mesma variável x para todos os gráficos
                csv_name1 = uploaded_files[0].name
                csv_name2 = uploaded_files[1].name
                col1, col2 = st.columns(2)
                with col1:
                    y_variable1 = st.selectbox(f"Selecione a variável y para o gráfico DataFrame 1 ({csv_name1}):", y_variable_options, key="y_variable_1")  # Chave única

                with col2:
                    y_variable2 = st.selectbox(f"Selecione a variável y para o gráfico DataFrame 2 ({csv_name2}):", y_variable_options, key="y_variable_2")  # Chave única
                title = st.text_input("Digite o título para os gráficos sobrepostos:", "Gráficos Sobrepostos")
                plot_ndvi_2(dfs[0], dfs[1], x_variable, y_variable1, y_variable2, title)
                
            else:
                st.error("Os arquivos CSV devem conter as colunas 'Datetime' e 'Mean'.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
    elif uploaded_files is not None:
        st.error("Por favor, selecione dois arquivos CSV.")

if __name__ == "__main__":
    main()