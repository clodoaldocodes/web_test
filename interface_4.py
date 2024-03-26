import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

        # Gráfico de percentil
        st.write("Gráfico de Percentil:")
        column_name = st.selectbox("Selecione a coluna para visualizar o gráfico de percentil", df.columns)
        fig, ax = plt.subplots()
        sns.histplot(df[column_name], kde=True, ax=ax)
        ax.set_title("Distribuição dos Dados")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
