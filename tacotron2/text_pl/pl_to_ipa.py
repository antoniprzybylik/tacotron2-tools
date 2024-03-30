# Python version based on TypeScript version.
# Original code: https://github.com/Quanosek/Fonetyka/
#
# Ported by Antoni Przybylik

import sys
import re

from . import (
    ipa_grammar,
    softer,
    consonantsArray,
    vowelsArray,
    softArray,
    hardArray,
    voicedArray,
    voicelessArray,
)
from .rewrite import (
    sonority,
    reduceRepeat,
    makeSofter,
    vowelsAccent,
    specialSofter,
)


# Główna funkcja
def format_ipa(word):
    changed = changeGrammar(word)
    changed = reduceRepeat(changed)
    return changed


# Zmiana gramatyki
def changeGrammar(word):
    # Jeśli "i" jest ostatnią głoską, to "i" musi zostać
    if word.endswith("i") and not word.endswith("ii"):
        word += "i"

    for consonant in consonantsArray:
        # Jeśli po "i" występuje spółgłoska, to "i" musi zostać
        if word.endswith("i"):
            word = word.replace("i" + consonant, "ii" + consonant)

        # Wyjątki z "i"
        if ("i" + consonant) in word and \
           not (word.startswith("i") or
                ("li" + consonant) in word or
                "ri" in word):
            word = word.replace("i" + consonant, "ii" + consonant)

    # Bezdźwięczność "n"
    if "n" in word:
        for vowel in vowelsArray:
            for consonant in consonantsArray:
                word = word.replace(vowel + "n" + consonant,
                                    vowel + "ŋ" + consonant)

    # Zmiana "ą" i "ę"
    for soft in softArray:
        word = word.replace("ą" + soft, "ɔ̇̃ŋ" + soft)
        word = word.replace("ę" + soft, "ɛ̃ŋ" + soft)

    # Wyjątki z "ŋ"
    if "ŋ" in word:
        if "ŋgi" in word or "ŋki" in word:
            word = word.replace("ŋ", "ŋʲ")

        for hard in hardArray:
            word = word.replace("ŋ" + hard, "n" + hard)

        word = word.replace("yn", "yŋ")

    # Wyjątki z dźwięcznością głosek przy spółgłoskach
    word = sonority(word, "l", "l̥")
    word = sonority(word, "m", "m̥")
    word = sonority(word, "n", "n̥")
    word = sonority(word, "ń", "ɲ̊")
    word = sonority(word, "r", "r̥")

    # Zmiana wymowy przed głoskami dźwięcznymi na twardszą
    for voiced in voicedArray:
        if "yŋ" in word and "yŋi" not in word:
            word = word.replace(voiced + "yŋ", voiced + "ɨ̃n")

        word = word.replace(voiced + "li", voiced + "lʲi")

    # Zmiękczenie przed głoską bezdźwięczną
    for voiceless in voicelessArray:
        if word.startswith("li"):
            word = word.replace("li" + voiceless, "lʲi" + voiceless)

        if not ("cz" in word or
                "sz" in word or
                "rz" in word or
                "dz" in word):
            word = word.replace("z" + voiceless, "s" + voiceless)

        word = word.replace("in" + voiceless, "ĩ" + voiceless)
        word = word.replace("un" + voiceless, "ũ" + voiceless)

        if not word.endswith(voiceless):
            word = word.replace("ą" + voiceless, "on͇" + voiceless)

    # Specjalne
    word = word.replace("aur", "ałr")
    word = word.replace("rin", "rʲin")
    word = word.replace("rzi", "rź")

    # Zanik dźwięczności "ń"
    if "ń" in word and "oń" not in word:
        for hard in hardArray:
            word = word.replace("ń" + hard, "j̃" + hard)

    # Bezdźwięczność "dz"
    word = specialSofter(word, "dz", "c")
    word = specialSofter(word, "dź", "ć")
    word = specialSofter(word, "dż", "cz")

    # Wyjątki
    word = word.replace("ĩtr", "intr")
    word = word.replace("podż", "poḍż")

    # Zamiana zapisu gramatycznego
    for key, value in ipa_grammar.items():
        word = word.replace(key, value)

    # Dodatkowe akcenty
    word = vowelsAccent(word, "a", "ã")
    word = vowelsAccent(word, "ɛ", "ɛ̃")
    word = vowelsAccent(word, "i", "ĩ")
    word = vowelsAccent(word, "ɔ", "ɔ̃")
    word = vowelsAccent(word, "u", "ũ")
    word = vowelsAccent(word, "ɨ", "ɨ̃")
    word = vowelsAccent(word, "v", "vʲ")

    # Zmiękczanie głoski pomiędzy dwiema miękkimi
    word = makeSofter(word, softArray, softer)

    # Zanik wymowy pierwszej głoski przed głoską bezdźwięczną
    for voiceless in voicelessArray:
        if word.startswith("l"):
            word = word.replace("l" + voiceless, "l̥" + voiceless)
        if word.startswith("w"):
            word = word.replace("w" + voiceless, "w̥" + voiceless)
        if word.startswith("m"):
            word = word.replace("m" + voiceless, "m̥" + voiceless)
        if word.startswith("r"):
            word = word.replace("r" + voiceless, "r̥" + voiceless)

    # Dźwięczność "ł"
    if "w" in word:
        word = sonority(word, "w", "w̥")
        word = word.replace("bw̥k", "pw̥k")

    # Kiedy zostaje "ki" na końcu wyrazu
    if not word.endswith("ki"):
        word = word.replace("ki", "c")
    else:
        word = word.replace("ki", "ci")

    # Wyjątki z dźwięcznością "hi"
    if "x" in word:
        for voiceless in voicelessArray:
            word = word.replace("xi" + voiceless, "xʲi" + voiceless)

        if word.startswith("xi"):
            word = word.replace("xi", "x́j")
        word = word.replace("x́jĩ", "xʲĩ")
        word = word.replace("xi", "x́")

        for vowel in vowelsArray:
            if word.endswith(vowel + "x"):
                word = word.replace(vowel + "x", vowel + "h")

            if word.endswith("x́" + vowel):
                word = word.replace("x́" + vowel, "x́j" + vowel)

        if "ɛx" in word:
            for voiced in voicedArray:
                word = word.replace("ɛx" + voiced, "ɛγ" + voiced)

        if word.startswith("x́jɛ") and not word.startswith("x́jɛ̃"):
            word = word.replace("x́jɛ", "x́ɛ")

        word = word.replace("x́ji", "xʲi")

    # Zmiany dźwięczności
    word = word.replace("fan", "van")
    word = word.replace("ɕb", "ʑb")
    word = word.replace("ʒi", "ʒʲi")

    # Przypadki z "ć"
    if "ʨ̑" in word:
        word = word.replace("ɔ̃n͇ʨ̑", "ɔɲʨ̑")
        word = word.replace("ŋʨ̑", "ɲʨ̑")

    # Wyjątki ze zmiękczaniem
    for soft in softArray:
        if word.startswith("k"):
            word = word.replace("k" + soft, "c" + soft)
        word = word.replace(soft + "ʨ̑ʥ̑", soft + "ʥ̑")
        word = word.replace("ɛ̃w̃" + soft, "ɛɲ" + soft)

    for voiced in voicedArray:
        # Utwardzanie "c"
        word = word.replace("ʦ̑" + voiced, "ʣ̑" + voiced)
        word = word.replace("ʨ̑" + voiced, "ʥ̑" + voiced)
        if voiced != "ɲ":
            word = word.replace("ʧ̑" + voiced, "ʤ̑" + voiced)

        # Ujednolicenie zapisu
        word = word.replace(voiced + "ɔn͇", voiced + "ɔ̃")
        word = word.replace(voiced + "ia", voiced + "ja")
        word = word.replace(voiced + "r̥z", voiced + "ʒ")
        word = word.replace(voiced + "r̥s", voiced + "ʒ")

        word = word.replace("aʒ" + voiced, "arz" + voiced)
        word = word.replace("ɛ̃w̃" + voiced, "ɛn" + voiced)

    word = word.replace("dʒ", "ḍʒ")

    for voiceless in voicelessArray:
        # Ubezdźwięcznienie "dz"
        word = word.replace("ʣ̑" + voiceless, "ʦ̑" + voiceless)

        if voiceless != "s":
            word = word.replace("ɛ̃w̃" + voiceless, "ɛn" + voiceless)
        word = word.replace("b" + voiceless, "p" + voiceless)
        word = word.replace("d" + voiceless, "t" + voiceless)

        # "sz"/"rz"
        word = word.replace("ʒ" + voiceless, "ʃ" + voiceless)
        word = word.replace(voiceless + "r̥z", voiceless + "ʃ")
        word = word.replace(voiceless + "r̥s", voiceless + "ʃ")

        # "w"/"f"
        word = word.replace(voiceless + "v", voiceless + "f")
        word = word.replace("v" + voiceless, "f" + voiceless)

        # Końcówki
        word = word.replace(voiceless + "ɔ̃n͇", voiceless + "ɔ̃n")

    for voiced in voicedArray:
        word = word.replace("ą" + voiced, "om" + voiced)
        word = word.replace("ɛn" + voiced, "ɛm" + voiced)
        word = word.replace("f" + voiced, "v" + voiced)

    word = word.replace("ãns", "ãw̃s")
    word = word.replace("ɕɔ̃w̃ʦ̑", "ɕɔ̃nʦ̑")
    word = word.replace("l̥v", "l̥f")
    word = word.replace("tʃ", "ṭʃ")

    if word[-1] == "b":
        word = word[:-1] + "p"

    if word[-1] == "g":
        word = word[:-1] + "k"

    # Zmiękczenie końcówek wyrazów
    for vowel in vowelsArray:
        if word.endswith(vowel + "ʒ"):
            word = word[:-1] + "ʃ"

        if word.endswith(vowel + "d"):
            word = word[:-1] + "t"

        if word.endswith(vowel + "i"):
            word = word[:-1] + "ji"

        if word.endswith("iji"):
            word = word[:-3] + "ji"

        word = word.replace("dʲ" + vowel, "dj" + vowel)
        word = word.replace("bʲ" + vowel, "bj" + vowel)
        word = word.replace("ɟ" + vowel, "ɟj" + vowel)

    # Anglicyzmy
    if word.startswith("vɛɛ"):
        word = word.replace("v", "w")
    word = word.replace("ɔɔ", "u")
    word = word.replace("ɛɛ", "i")
    word = word.replace("autɔ", "awtɔ")

    # Specjalne końcówki
    if word.endswith("zn̥"):
        word = word[:-2] + "sn̥"
    if word.endswith("mʲa"):
        word = word[:-3] + "mja"
    if word.endswith("nd"):
        word = word[:-2] + "nt"

    # Wyjątki
    word = word.replace("ibʲ", "ibʲi")
    word = word.replace("ɔȵt", "ɔȵit")
    word = word.replace("çjɛr", "çɛr")

    # Korekty
    word = word.replace("w̃w", "w")
    word = word.replace("rj", "rʲj")

    word = word.replace("iĩ", "i")
    word = word.replace("ii", "i")

    return word


def text_to_ipa(text):
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

    return text_ipa
