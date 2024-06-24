import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.title("Criar Polígono a partir de Cliques em uma Imagem")

    st.write("Faça o upload de uma imagem:")
    uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.write("Imagem carregada com sucesso!")
        image = Image.open(uploaded_file)
        st.image(image, caption='Imagem carregada', use_column_width=True)

        st.write("Clique na imagem para marcar os pontos do polígono:")
        image_clickable = st.image(image, use_column_width=True, clamp=True)

        clicked_coordinates = []

        while st.button("Finalizar Polígono") == False:
            clicked_coordinates = get_mouse_click_coordinates(image_clickable, clicked_coordinates)
            if clicked_coordinates:
                draw_polygon(image, clicked_coordinates)

        save_coordinates(clicked_coordinates)

def get_mouse_click_coordinates(image, coordinates):
    drawn_image = image.copy()
    draw = ImageDraw.Draw(drawn_image)
    coordinates_new = coordinates.copy()
    if st.pydeck_chart(image):
        x, y = st.pydeck_chart(image)
        coordinates_new.append((x, y))
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill="green", outline="green")
        for i in range(len(coordinates_new) - 1):
            draw.line([coordinates_new[i], coordinates_new[i + 1]], fill="green", width=2)
        st.image(drawn_image, use_column_width=True)

    return coordinates_new

def draw_polygon(image, coordinates):
    image_np = np.array(image)
    plt.imshow(image_np)
    plt.plot([x for x, y in coordinates], [y for x, y in coordinates], 'r-')
    plt.title('Polígono')
    plt.axis('off')
    st.pyplot()

def save_coordinates(coordinates):
    with open("coordenadas.txt", "w") as file:
        for coord in coordinates:
            file.write(f"{coord}\n")

if __name__ == "__main__":
    main()
