import asyncio
from string import ascii_lowercase

from gmpy2 import mpq

from extras.collections_extras import bidict, sortabledict

from toy_cryptography.substitution_cipher.markov_chain_monte_carlo import (
    PlaintextPlausibilityMaximiser,
    BigramProportions,
)
from toy_cryptography.substitution_cipher.frequency_analysis import analyse_character_proportions, infer_cipher_key
from toy_cryptography.substitution_cipher.scheme import decode, update_key

from utils.data.monograms import english_text_letter_frequencies
from utils.data.bigrams import load_lowercase_bigrams_dataset



ciphertext_paragraph = """
xmeagiyiyzaglyagiknnyxciazeykrykrkfyktpxaoiacikorgpmazxiiacyahkragjixolhaznriykik
fyxnrfkoiyxoqkorpaccxjneraxipzkfixfknneeaghagnroifaocikoinezgokfzaccmanqciarkehya
fnkxtiykikfyxnrraoiqoahkoeiyxolkfyxnrcjzkxocikzicmgofixaoxolkijxziykorykcktaolcix
ictkoexomkoifaowangixaociyagckorcamraztkoikiatcxoiahyxfylarykcpgiktecixfpaccxjxnx
iemazoaixfxolkokrgnickfikormxlgzxolagixicpgzpazigpiakjagixicpzxtkzecfyaanrkeckfyx
nriyxoqcokigzknneaoneampnkejgitkoekmaztampnkefaoikxocrxcfxpnxokzemkfiazceagfkoira
iyxcaziykipgiceagagicyahckfyxnriykixitgciiyxoqpzkfixfknneazmkxnoahxmiyzaglyagifyx
nryaarkjzkxoykcoaappacxixaoxixcpnkxoiykixihxnnkiikxokpacxixaoamcikigcugakchxiyagz
azrxokzekoxtknctkoqoahcoaihyekfahralaznxaohkcoaijazohxiykjzkxoaokpkzhxiyagzchyecg
fykoxtkncfkooaikrrcgjizkfiazajikxomzatjaaqckorcfyaanxoliykipkzktagoipacxixaohyxfy
tkoyanrciarke
"""

ciphertext_paragraph_lines = ciphertext_paragraph.strip().splitlines()
ciphertext = "".join(ciphertext_paragraph_lines)

english_text_letter_frequencies_without_e = english_text_letter_frequencies.copy()
del english_text_letter_frequencies_without_e["e"]


async def load_english_bigram_proportions_without_e() -> BigramProportions:
    lowercase_bigram_frequencies = await load_lowercase_bigrams_dataset()
    lowercase_bigram_frequencies = dict(lowercase_bigram_frequencies)

    keys_to_remove = [key for key in lowercase_bigram_frequencies.keys() if "e" in key]
    for key in keys_to_remove:
        lowercase_bigram_frequencies.pop(key)

    total_frequency = sum(lowercase_bigram_frequencies.values())
    lowercase_bigram_proportions = BigramProportions(sortabledict[str, mpq]())
    for bigram, frequency in lowercase_bigram_frequencies.items():
        lowercase_bigram_proportions[bigram] = mpq(frequency, total_frequency)
    return lowercase_bigram_proportions


english_bigram_proportions_without_e = asyncio.run(load_english_bigram_proportions_without_e())


def main():
    ciphertext_character_frequency = analyse_character_proportions(ciphertext)
    cipher_key = infer_cipher_key(
        ciphertext_character_frequency,
        reference=english_text_letter_frequencies_without_e,
    )
    confident_key = bidict()
    cipher_key = update_key(cipher_key, confident_key)
    chain = PlaintextPlausibilityMaximiser(
        ciphertext,
        cipher_key,
        confident_key,
        reference=english_bigram_proportions_without_e,
    )
    chain.main_loop(threshold=30)
    better_key = chain.current_key
    print(ascii_lowercase)
    print("".join(better_key.get(c, "_") for c in ascii_lowercase))
    plaintext = decode(ciphertext, better_key)
    print(plaintext)


if __name__ == "__main__":
    main()
