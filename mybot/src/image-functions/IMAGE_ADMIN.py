from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

class IMAGE_admin:
    def __init__(self):
        pass

    def draw_menu(self, avatar_url, username):
        # Carrega a imagem de fundo localmente
        background_path = os.path.join(os.path.dirname(__file__), 'welcome_bg.png')
        if not os.path.exists(background_path):
            raise FileNotFoundError(f"A imagem de fundo '{background_path}' não foi encontrada.")
        
        background_image = Image.open(background_path)
        background_width, background_height = background_image.size  # Editando imagem de fundo

        # Carrega a imagem do avatar e dimensiona para 450x450 pixels (aumentado em 150 pixels)
        response = requests.get(avatar_url)
        avatar_image = Image.open(BytesIO(response.content))
        avatar_image = avatar_image.resize((450, 450))

        mask = Image.new("L", (450, 450), 0)
        draw = ImageDraw.Draw(mask)  # Máscara na imagem
        draw.ellipse((0, 0, 450, 450), fill=255)  # Circular
        avatar_image.putalpha(mask)  # Tira o fundo da área circular ao redor

        # Centralizando imagens
        avatar_x = (background_width - 450) // 2
        avatar_y = (background_height - 790) // 2

        # Cola a imagem do avatar usando os parâmetros de localização
        background_image.paste(avatar_image, (avatar_x, avatar_y), avatar_image)

        # Verifica se o arquivo de fonte existe
        caminho_fonte = os.path.join(os.path.dirname(__file__), 'arial-unicode-ms.ttf')
        if not os.path.exists(caminho_fonte):
            raise FileNotFoundError(f"O arquivo de fonte '{caminho_fonte}' não foi encontrado.")

        fontDaMensagem = ImageFont.truetype(caminho_fonte, 86)  # Tamanho da fonte aumentado para 64

        draw = ImageDraw.Draw(background_image)

        text = username  # Pode ser f"Texto sla {username}"
        text_width = draw.textlength(text, font=fontDaMensagem)

        text_x = (background_width - text_width) // 2  # Meio da tela
        text_y = avatar_y + 450 + 230 # Coloquei 120 pixels de distância do centro

        # Finalmente desenha o texto em cima da imagem
        draw.text((text_x, text_y), text, font=fontDaMensagem, fill="white")  # White é a cor

        return background_image

# Exemplo de uso
if __name__ == "__main__":
    avatar_url = "https://example.com/path/to/avatar.jpg"
    username = "User123"
    img_admin = IMAGE_admin()
    try:
        result_image = img_admin.draw_menu(avatar_url, username)
        result_image.show()  # Mostra a imagem resultante
        result_image.save("output.png")  # Salva a imagem resultante
    except FileNotFoundError as e:
        print(e)
