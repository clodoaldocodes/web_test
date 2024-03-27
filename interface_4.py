import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import scipy.stats as stats
import plotly.graph_objs as go
from scipy.stats import trim_mean, hmean, iqr, skew, kurtosis

def ccdf(data):
    sorted_data = np.sort(data)
    ccdf = 1.0 - np.arange(len(sorted_data)) / float(len(sorted_data))
    return sorted_data, ccdf

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Análise Estatística de Dados",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Análise Estatística de Dados")

    # Carregar o arquivo CSV
    file = st.file_uploader("Carregar arquivo CSV", type=["csv"])
    if file is not None:
        df = pd.read_csv(file)

        # Organizando a tela
        col1, col2 = st.columns([2, 1])  # 2/3 e 1/3

        # Visualização dos dados
        with col1:
            st.write("Visualização dos dados:")
            st.write(df)
        
        # Resumo Estatístico
        with col2:
            # Calcular as estatísticas de variância e desvio padrão
            variance = df.var().rename('var')

            # Criar uma lista contendo os DataFrames para concatenar
            dataframes_to_concat = [df.describe(), variance.to_frame().T]

            # Concatenar os DataFrames
            summary_stats = pd.concat(dataframes_to_concat)

            # Interface Streamlit
            st.write("Resumo Estatístico:")
            st.write(summary_stats)

        # Organizando os gráficos lado a lado
        col3, col4 = st.columns(2)

        # Boxplot
        with col3:
            # Adicionando a opção de "Todas as variáveis"
            df_columns = df.columns.tolist()
            df_columns.insert(0, "Todas as variáveis")

            # Interface Streamlit
            st.write("Boxplot:")
            selected_column_boxplot = st.selectbox("Selecione a coluna para visualizar o boxplot", df_columns)

            fig = go.Figure()

            if selected_column_boxplot == "Todas as variáveis":
                for column in df.columns:
                    fig.add_trace(go.Box(y=df[column], name=f'{column}'))
            else:
                fig.add_trace(go.Box(y=df[selected_column_boxplot], name=selected_column_boxplot))

            fig.update_layout(title="Boxplot")

            st.plotly_chart(fig, use_container_width=True)

        # CCDF
        with col4:
            df_columns = df.columns.tolist()
            df_columns.insert(0, "Todas as variáveis")

            # Interface Streamlit
            st.write("CCDF:")
            selected_column_ccdf = st.selectbox("Selecione a coluna para visualizar o CCDF", df_columns)
            fig = go.Figure()

            if selected_column_ccdf == "Todas as variáveis":
                for column in df.columns:
                    sorted_data, ccdf_values = ccdf(df[column])
                    fig.add_trace(go.Scatter(x=sorted_data, y=ccdf_values, mode='lines', name=f'CCDF - {column}'))
            else:
                sorted_data, ccdf_values = ccdf(df[selected_column_ccdf])
                fig.add_trace(go.Scatter(x=sorted_data, y=ccdf_values, mode='lines', name='CCDF'))

            fig.update_layout(title="Complementary Cumulative Distribution Function (CCDF)",
                            xaxis_title="Valores ordenados",
                            yaxis_title="CCDF",
                            yaxis_type="log",
                            yaxis_range=[-3, 0])

            st.plotly_chart(fig, use_container_width=True)

        # Organizando os gráficos lado a lado
        col5, col6 = st.columns(2)

        with col5:
            st.write("Gráfico de Correlação:")
            corr_matrix = df.corr()
            fig_corr = px.imshow(corr_matrix, labels=dict(color="Correlation"), x=corr_matrix.index, y=corr_matrix.columns, 
                                    color_continuous_scale='RdBu')
            for i in range(len(corr_matrix.index)):
                for j in range(len(corr_matrix.columns)):
                    fig_corr.add_trace(
                        dict(
                            type='scatter',
                            x=[corr_matrix.columns[j]],
                            y=[corr_matrix.index[i]],
                            text=[corr_matrix.values[i, j].round(2)],
                            mode='text',
                            showlegend=False
                        )
                    )
            fig_corr.update_traces(textfont=dict(size=8))
            st.plotly_chart(fig_corr)

        with col6:
            st.write("Distribuição dos Dados e Função Normal Ajustada:")
            selected_column = st.selectbox("Selecione a coluna para visualizar a distribuição", df.columns)
            ignore_percentile = st.slider("Percentil a ser ignorado", min_value=0, max_value=100, value=0, step=1)
            # Ignorar o percentil selecionado
            ignored_value = np.percentile(df[selected_column], ignore_percentile)
            filtered_data = df[df[selected_column] < ignored_value][selected_column]
            # Plotando a distribuição dos dados
            fig = px.histogram(filtered_data, x=selected_column, nbins=30, histnorm='probability density', 
                               title='Distribuição dos Dados (Ignorando {}º Percentil)'.format(ignore_percentile))
            # Ajustando a função normal
            mean = filtered_data.mean()
            std = filtered_data.std()
            x = np.linspace(mean - 4*std, mean + 4*std, 1000)
            y = stats.norm.pdf(x, mean, std)
            fig.add_scatter(x=x, y=y, mode='lines', name='Função Normal Ajustada')
            st.plotly_chart(fig)
        
        col7, col8 = st.columns(2)

        with col7:
            # Interface Streamlit
            st.write("Gráfico de Correlação (Scatter Plot):")
            selected_columns = st.multiselect("Selecione duas colunas para visualizar a correlação", df.columns)

            if len(selected_columns) == 2:
                corr_matrix = df[selected_columns].corr()
                fig = px.imshow(corr_matrix,
                                labels=dict(color="Correlação"),
                                color_continuous_scale='RdBu_r',
                                zmin=-1, zmax=1)
                
                for i in range(len(corr_matrix)):
                    for j in range(len(corr_matrix)):
                        fig.add_annotation(x=i, y=j, text=str(round(corr_matrix.iloc[i, j], 2)),
                                        showarrow=False, font=dict(color='black' if abs(corr_matrix.iloc[i, j]) < 0.5 else 'white'))
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Selecione exatamente duas colunas.")

if __name__ == "__main__":
    main()
