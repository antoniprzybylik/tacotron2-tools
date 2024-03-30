import sys
import re

from .pl_to_ipa import format_ipa

_symbols = {'ʃ': 0, 'ʲ': 1, 'v': 2, 'j': 3, 'w': 4, 'ɔ': 5, '̃': 6, 'ɛ': 7, 'k': 8, 's': 9, 'q': 10, 'u': 11, 'b': 12, 'h': 13, 'x': 14, 'ʦ': 15, '̑': 16, 'ć': 17, 'ʨ': 18, 'ʧ': 19, 'd': 20, 'ĩ': 21, 'ź': 22, 'ʥ': 23, 'ʣ': 24, 'ż': 25, 'ʤ': 26, 'f': 27, 'ɟ': 28, 'm': 29, 'ń': 30, 'ɲ': 31, 'p': 32, 'ś': 33, 'ɕ': 34, 't': 35, 'ɨ': 36, 'ʒ': 37, 'ʑ': 38, 'z': 39, 'i': 40, 'ä': 41, '̇': 42, 'ü': 43, 'c': 44, 'g': 45, 'l': 46, 'ł': 47, 'n': 48, 'r': 49, 'a': 50, 'ą': 51, 'e': 52, 'ę': 53, 'o': 54, 'ó': 55, 'y': 56, '̥': 57, '̊': 58, '͇': 59, 'ḍ': 60, 'ã': 61, 'ũ': 62, '́': 63, 'ṭ': 64, 'ç': 65, 'ŋ': 66, '3': 67, 'ȵ': 68, 'γ': 69, '!': 70, ',': 71, '.': 72, '?': 73, ' ': 74, '-': 75}


def text_to_sequence(text):
    special = '!,.? -'
    letters = 'aąbcćdeęfghijklłmnńoóprsśtuwyzźż'

    # Normalize text
    text = text.lower().lstrip().rstrip()
    text = re.sub("\s\s+", " ", text)

    # Check for forbidden symbols
    for c in text:
        if c not in special + letters:
            print(f"Symbol \"{c}\" not allowed!")
            sys.exit()

    # Separate symbols from words and convert words
    pattern = "|".join(re.escape(c) for c in special)
    words = re.split(f"({pattern})", text)
    text_ipa = "".join([format_ipa(word) if word not in special else word
                        for word in words])
    sequence = [_symbols[c] for c in text_ipa]

    return sequence
