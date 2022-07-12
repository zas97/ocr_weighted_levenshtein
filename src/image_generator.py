import random
import string
from typing import Iterable
from pathlib import Path
from trdg.generators import GeneratorFromStrings

def rand_string(min_len, max_len, posible_chars):
    l = random.randint(min_len, max_len)
    return ''.join(random.choice(posible_chars) for i in range(l))


def get_chars():
    # return all printable chars except spaces, \n \t, etc...
    return string.printable[:-6]
    
    
def get_fonts():
    import trdg.utils as tu
    fonts = tu.load_fonts('latin')
    return fonts


def filter_fonts(fonts: Iterable[Path]):
    # exclude fonts with same chars for upper than for lower
    exclude = ['seasrn', 'amatic', 'bebas', 'capture']

    def exclude_font(font: Path):
        stem = font.stem
        for e in exclude:
            if stem.lower().startswith(e.lower()):
                return True
        return False

    return [f for f in fonts if not exclude_font(Path(f))]


def random_chars_generator(count=1000):
    list_strings = [rand_string(2, 10, get_chars()) for it in range(count)]
    generator = GeneratorFromStrings(list_strings, 
                                    random_blur=True, 
                                    random_skew=True, 
                                    skewing_angle=5,
                                    blur=1,
                                    background_type=0,
                                    count=count,
                                    fonts=filter_fonts(get_fonts()))
    return generator