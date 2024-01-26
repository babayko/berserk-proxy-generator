import os
import uuid

from PIL import (
    Image,
    ImageOps,
)
from fpdf import (
    FPDF,
)

from constants import (
    CARD_HEIGHT,
    CARD_WIDTH,
    SETS,
    SHORTS,
)


def concat_images(image_paths, width, height, shape):
    # Открываем изображения и изменяем размер
    images = map(Image.open, image_paths)
    images = [ImageOps.fit(image, (width - 10, height - 10), Image.LANCZOS) for image in images]

    # Создаем холст и преобразуем к нужному размеру
    image_size = (width * shape[1], height * shape[0])
    image = Image.new('RGB', image_size)

    # Добавляем изображения на холст
    for row in range(shape[0]):
        for col in range(shape[1]):
            offset = width * col, height * row
            idx = row * shape[1] + col
            image.paste(images[idx], offset)

    return image


def batch(iterable, n):
    l = len(iterable)

    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def generate(card_per_page=3):

    for release in SETS:
        folder = SHORTS[release]
        image_paths = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.jpg')])
        grouped_paths = batch(image_paths, card_per_page)
        pdf = FPDF()

        for group in grouped_paths:
            filepath = str(uuid.uuid4()) + '.jpg'
            card_counts = len(group)

            image = concat_images(group * card_per_page, CARD_WIDTH, CARD_HEIGHT, (card_per_page, card_counts))
            image.save(filepath, 'JPEG')

            pdf.add_page()
            pdf.image(filepath, x=0, y=0, w=int(210 / card_per_page * card_counts), h=297)

            os.remove(filepath)

        pdf.output(f'{folder}/{folder}-proxy.pdf', 'F')


if __name__ == '__main__':
    generate()
