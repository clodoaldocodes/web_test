import streamlit as st
import pandas as pd

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

        # Outras análises estatísticas podem ser adicionadas aqui, conforme necessário

if __name__ == "__main__":
    main()
