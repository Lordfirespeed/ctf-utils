from string import ascii_lowercase
from typing import Sequence, NewType

from extras.collections_extras import bidict, sortabledict
from utils.data.monograms import english_text_letter_frequencies

from .scheme import CipherKey, decode


CharacterFrequencies = NewType("CharacterFrequencies", sortabledict[str, float])


def analyse_character_frequencies(text: str) -> CharacterFrequencies:
    character_counts: dict[str, int] = {c: 0 for c in ascii_lowercase}
    text_length = 0

    for character in text:
        if character.isspace():
            continue
        text_length += 1
        character_count = character_counts.get(character, 0)
        character_count += 1
        character_counts[character] = character_count

    character_frequencies = sortabledict({character: (count / text_length) for character, count in character_counts.items()})
    character_frequencies.sort_by_value(reverse=True)
    return CharacterFrequencies(character_frequencies)


def letters_ordered_by_frequency(frequency: CharacterFrequencies) -> Sequence[str]:
    frequency.sort_by_value(reverse=True)
    return [letter for letter in frequency.keys()]


def infer_cipher_key(
    ciphertext_frequency: CharacterFrequencies,
    reference_frequency: CharacterFrequencies = None,
) -> CipherKey:
    if reference_frequency is None:
        reference_frequency = english_text_letter_frequencies

    reference_letter_order = letters_ordered_by_frequency(reference_frequency)
    text_letter_order = letters_ordered_by_frequency(ciphertext_frequency)

    return bidict(zip(reference_letter_order, text_letter_order))


ciphertext_paragraph = """
glnonppfnasjdfzfoixaupzudoigrlnjaoslrjufglrdgatpdggnjrtglnzafpzaobuazagjnzgglntprr
blabvabnglnufobuazonajpxsapvaobenfoierdobbruoglnjfynjglnropxglfoitrjfguazgrsrvngra
obuafgtrjglngdjortglngfbnglnznajnaslrtglnglavnzzgjngslnbentrjndzpfqnglnenifoofoirt
aofognjvfoaepnuagnjuaxfoglnrttfoiglnznaaobglnzqxunjnunpbnbgringlnjufglrdgahrfogaob
foglnpdvfordzzkasnglngaoonbzafpzrtglneajinzbjftgfoidkufglglngfbnznnvnbgrzgaobzgfpp
fojnbspdzgnjzrtsaoyazzlajkpxknaqnbufglipnavzrtyajofzlnbzkjfgzalamnjnzgnbroglnpruzl
rjnzglagjaordggrznafoyaofzlfoitpagonzzglnafjuazbajqaerynijaynznobaobtajglnjeasqzgf
ppznnvnbsrobnoznbfogravrdjotdpiprrvejrrbfoivrgfropnzzrynjglnefiinzgaobglnijnagnzgg
ruoronajgl
"""

plaintext_paragraph = """
thenellieacruisingyawlswungtoheranchorwithoutaflutterofthesailsandwasatrestthefloo
dhadmadethewindwasnearlycalmandbeingbounddowntherivertheonlythingforitwastocometoa
ndwaitfortheturnofthetidetheseareachofthethamesstretchedbeforeuslikethebeginningof
aninterminablewaterwayintheoffingtheseaandtheskywereweldedtogetherwithoutajointand
intheluminousspacethetannedsailsofthebargesdriftingupwiththetideseemedtostandstill
inredclustersofcanvassharplypeakedwithgleamsofvarnishedspritsahazerestedonthelowsh
oresthatranouttoseainvanishingflatnesstheairwasdarkabovegravesendandfartherbacksti
llseemedcondensedintoamournfulgloombroodingmotionlessoverthebiggestandthegreatestt
ownonearth
"""

ciphertext_paragraph_lines = ciphertext_paragraph.strip().splitlines()
ciphertext = "".join(ciphertext_paragraph_lines)

plaintext_paragraph_lines = plaintext_paragraph.strip().splitlines()
plaintext = "".join(plaintext_paragraph_lines)

real_key = bidict({a: b for a, b in zip(ascii_lowercase, "aesbntilfhqpvorkcjzgdyuwxm")})


# this is abysmal. Improve it: https://www.dcode.fr/monoalphabetic-substitution#q7
def main():
    ciphertext_character_frequency = analyse_character_frequencies(ciphertext)
    cipher_key = infer_cipher_key(ciphertext_character_frequency)
    round_trip_plaintext = decode(ciphertext, cipher_key)
    print(round_trip_plaintext)


def debug_main():
    foo = letters_ordered_by_frequency(english_text_letter_frequencies)
    ciphertext_letter_frequencies = analyse_character_frequencies(ciphertext)
    bar = letters_ordered_by_frequency(ciphertext_letter_frequencies)
    print(english_text_letter_frequencies)
    print(ciphertext_letter_frequencies)
    print(foo)
    print(bar)


if __name__ == "__main__":
    main()
