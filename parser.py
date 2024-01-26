import os

import requests
import shutil

from constants import (
    PROBERSERK_IMAGES_URL,
    SETS,
    CARD_COUNT, LONGS, SHORTS,
)


def parse():
    for release in SETS:

        if not os.path.exists(release):
            os.makedirs(release)

        for card_number in range(1, CARD_COUNT[release] + 1):
            filename = f'{LONGS[release]}-{str(card_number).rjust(3, "0")}.jpg'
            filepath = os.path.join('.', SHORTS[release], filename)

            if not os.path.exists(filepath):
                r = requests.get(f'{PROBERSERK_IMAGES_URL}/{filepath}', stream=True)

                if r.status_code == 200:
                    with open(filepath, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)

                    print(f'Downloaded {filepath}')


if __name__ == '__main__':
    parse()