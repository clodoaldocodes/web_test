import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

def ccdf(data):
    sorted_data = np.sort(data)
    ccdf = 1.0 - np.arange(len(sorted_data)) / float(len(sorted_data))
    return sorted_data, ccdf

def main():
    st.title("Análise Estatística de Dados")

    # Carregar o arquivo CSV
    file = st.file_uploader("Carregar arquivo CSV", type=["csv"])
    if file is not None:
        df = pd.read_csv(file)

        st.write("Visualização dos dados:")
        st.write(df)
        
        # Análise estatística básica
        st.write("Resumo Estatístico:")
        st.write(df.describe())

        # Boxplot
        st.write("Boxplot:")
        selected_column = st.selectbox("Selecione a coluna para visualizar o boxplot", df.columns)
        fig = px.box(df, y=selected_column)
        st.plotly_chart(fig)

        # CCDF
        st.write("CCDF:")
        selected_column_ccdf = st.selectbox("Selecione a coluna para visualizar o CCDF", df.columns)
        sorted_data, ccdf_values = ccdf(df[selected_column_ccdf])
        fig_ccdf = px.line(x=sorted_data, y=ccdf_values, labels={'x': 'Valores ordenados', 'y': 'CCDF'})
        fig_ccdf.update_layout(title="Complementary Cumulative Distribution Function (CCDF)")
        fig_ccdf.update_yaxes(type="log", range=[-3, 0])  # Definindo o intervalo de -3 a 0 (ou 1 a 10^-3)
        st.plotly_chart(fig_ccdf)

if __name__ == "__main__":
    main()
