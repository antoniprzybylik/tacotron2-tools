# Python version based on TypeScript version.
# Original code: https://github.com/Quanosek/Fonetyka/
#
# Ported by Antoni Przybylik

import json
import os

# Read alphabet
alphabet_json_path = os.path.join(
    os.path.dirname(__file__),
    "alphabet.json",
)

with open(alphabet_json_path, "r") as fp:
    letters = json.loads(fp.read())

alphabet = letters['all']

vowelsArray = letters['vowels']
consonantsArray = [
    letter
    for letter in alphabet
    if letter not in vowelsArray
]

voicedArray = letters['voiced']
voicelessArray = letters['voiceless']

softArray = letters['soft']
hardArray = [
    letter
    for letter in alphabet
    if letter not in softArray
]

# Zamiana zapisu gramatycznego
ipa_grammar = {
    "szi": "ʃʲ",
    "sz": "ʃ",
    "wi": "vʲj",
    "w": "v",
    "ł": "w",
    "ą": "ɔ̃w̃",
    "e": "ɛ",
    "ę": "ɛ̃w̃",
    "x": "ks",
    "qu": "q",
    "q": "ku",
    "bi": "bʲ",
    "ch": "h",
    "h": "x",
    "cj": "ʦ̑ʲj",
    "ci": "ć",
    "ć": "ʨ̑",
    "cz": "ʧ̑",
    "c": "ʦ̑",
    "dii": "dʲĩ",
    "di": "dʲ",
    "zi": "ź",
    "dź": "ʥ̑",
    "dz": "ʣ̑",
    "rz": "ż",
    "dż": "ʤ̑",
    "fi": "fʲj",
    "gi": "ɟ",
    "mi": "mʲj",
    "ni": "ń",
    "ń": "ɲ",
    "o": "ɔ",
    "ó": "u",
    "pi": "pʲj",
    "si": "ś",
    "sj": "sʲj",
    "ś": "ɕ",
    "ti": "tʲj",
    "y": "ɨ",
    "ż": "ʒ",
    "ź": "ʑ",
    "zj": "zʲj",
    "ji": "i",
}

softer = {
    "a": "ä",
    "ɛ": "ɛ̇",
    "ɔ": "ɔ̇",
    "u": "ü",
}

# Extend arrays with phonetic alphabet
to_extend = [vowelsArray, consonantsArray,
             voicedArray, voicelessArray,
             softArray, hardArray]
for key, value in ipa_grammar.items():
    for array in to_extend:
        if key in array and value not in array:
            array.append(value)
