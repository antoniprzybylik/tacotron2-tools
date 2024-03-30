# Python version based on TypeScript version.
# Original code: https://github.com/Quanosek/Fonetyka/
#
# Ported by Antoni Przybylik

from . import (
    consonantsArray,
    voicelessArray,
)


def sonority(word, a, b):
    for con1 in consonantsArray:
        for con2 in consonantsArray:
            if con1 + a + con2 in word:
                word = word.replace(con1 + a + con2, con1 + b + con2)

        if word.endswith(con1 + a):
            word = word.replace(con1 + a, con1 + b)

    return word


# Replace repeating letters with •
def reduceRepeat(word):
    splitted = list(word)

    prev = ""
    reduced = []
    for letter in splitted:
        reduced.append(letter if letter != prev else "•")
        prev = letter

    return ''.join(reduced)


# Replace phonemes with softer ones
def makeSofter(word, array, softer):
    forDeletion = ["g", "h", "k"]
    newSofts = [c for c in array if c not in forDeletion]

    splitted = list(word)
    for soft1 in newSofts:
        for soft2 in newSofts:
            for key, value in softer.items():
                for i in range(1, len(word)+1):
                    if word[:i].endswith(soft1 + key + soft2):
                        splitted[i - len(soft2) - 1] = value

    return "".join(splitted)


# Dodawanie zapisu akcentów w szczególnych przypadkach
def vowelsAccent(word, a, b):
    word = word.replace(a + "m", b + "m")
    word = word.replace(a + "n", b + "n")
    word = word.replace(a + "ŋ", b + "ŋ")
    word = word.replace(a + "ń", b + "ń")
    word = word.replace(a + "ɲ", b + "ɲ")
    word = word.replace(a + "j̃", b + "j̃")
    word = word.replace(a + "ĩ ̯", b + "ĩ ̯")

    return word


# Zmiękczanie wyjątków
def specialSofter(word, a, b):
    for voiceless in voicelessArray:
        word = word.replace(a + voiceless, b + voiceless)

    if word.endswith(a):
        word = word.replace(a, b)

    return word
