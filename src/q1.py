from string import ascii_lowercase

from toy_cryptography.substitution_cipher.markov_chain_monte_carlo import PlaintextPlausibilityMaximiser
from toy_cryptography.substitution_cipher.frequency_analysis import analyse_character_proportions, infer_cipher_key
from toy_cryptography.substitution_cipher.scheme import decode


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

ciphertext_paragraph_lines = ciphertext_paragraph.strip().splitlines()
ciphertext = "".join(ciphertext_paragraph_lines)


def main():
    ciphertext_character_frequency = analyse_character_proportions(ciphertext)
    cipher_key = infer_cipher_key(ciphertext_character_frequency)
    chain = PlaintextPlausibilityMaximiser(ciphertext, cipher_key)
    chain.main_loop()
    better_key = chain.current_key
    print("".join(better_key[c] for c in ascii_lowercase))
    plaintext = decode(ciphertext, better_key)
    print(plaintext)


if __name__ == "__main__":
    main()
