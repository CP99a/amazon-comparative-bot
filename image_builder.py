from PIL import Image
import requests
from io import BytesIO

def generate_comparative_image(image_urls, output_path):
    assert len(image_urls) == 8, "Servono 8 immagini"
    grid_size = (4, 2)
    cell_size = (500, 500)
    final_size = (grid_size[0] * cell_size[0], grid_size[1] * cell_size[1])
    collage = Image.new("RGB", final_size, "white")

    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            img.thumbnail(cell_size, Image.ANTIALIAS)
            x = (idx % 4) * cell_size[0]
            y = (idx // 4) * cell_size[1]
            offset = ((cell_size[0] - img.width) // 2, (cell_size[1] - img.height) // 2)
            collage.paste(img, (x + offset[0], y + offset[1]))
        except Exception as e:
            print(f"Errore con l'immagine {url}: {e}")

    collage.save(output_path)
