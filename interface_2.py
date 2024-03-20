import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_ndvi(df):
    # Converter a coluna 'data' para o tipo datetime
    df['data'] = pd.to_datetime(df['Datetime'])
    
    # Plotar o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df['data'], df['Mean'], marker='o', linestyle='-')
    plt.title('Índice de Vegetação por Diferença Normalizada (NDVI)')
    plt.xlabel('Data')
    plt.ylabel('NDVI')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

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
