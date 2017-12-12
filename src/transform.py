# coding: utf-8

import re
import fileinput

def revoice_cluster(match):
    cluster = match.group(0)
    last_letter = cluster[-1]
    if cluster.endswith("@") or cluster.endswith("v"):
        last_letter = cluster[-2]
    last_voiced = last_letter in VOICED
    last_devoiced = last_letter in DEVOICED
    if last_voiced:
        return ''.join(DEVOICED_TO_VOICED.get(x) or x for _, x in enumerate(cluster))
    elif last_devoiced:
        return ''.join(VOICED_TO_DEVOICED.get(x) or x for _, x in enumerate(cluster))
    return cluster

VOWEL = u"a|e|i|o|u|ą|ę|y"

TO_IPA = [
    # polish ortography, ipa
    ("i", "i"),
    ("a", "a"),
    ("e", "ɛ"),
    ("y", "ɨ"),
    ("u", "u"),
    ("ó", "u"),
    ("o", "ɔ"),
    ("ę", "ɛ̃"),
    ("ą", "ɔ̃"),
    
    ("b", "b"),
    ("c(?!(i|z|h))", "t͡s"),
    ("ci(?!" + VOWEL + ")", "t͡ɕi"),
    ("ci(?=" + VOWEL +")", "t͡ɕ"),
    ("ć", "t͡ɕ"),
    ("cz", "t͡ʂ"),
    ("ch", "x"),
    ("d(?!z|ż|ź)", "d"),
    ("dz(?!i)", "d͡z"),
    ("dzi(?!" + VOWEL + ")", "d͡ʑi"),
    ("dzi(?=" + VOWEL + ")", "d͡ʑ"),
    ("dź", "d͡ʑ"),
    ("dż", "d͡ʐ"),
    ("f", "f"),
    ("g", "g"),
    ("h", "x"),
    ("j", "j"),
    ("k", "k"),
    ("l", "l"),
    ("ł", "w"),
    ("m", "m"),
    ("n(?!i)", "n"),
    ("ni(?!" + VOWEL + ")", "ɲi"),
    ("ni(?=" + VOWEL +")", "ɲ"),
    ("ń", "ɲ"),
    ("p", "p"),
    ("r(?!z)", "r"),
    # This works because "z" is not changed.
    ("rz", "@"),
    ("s(?!(i|z))", "s"),
    ("si(?!" + VOWEL + ")", "ɕi"),
    ("si(?=" + VOWEL +")", "ɕ"),
    ("ś", "ɕ"),
    ("sz", "ʂ"),
    ("t", "t"),
    # To make it execute before ł.
    ("w(?=.)", "v"),
    ("z(?!(i|z))", "z"),
    ("zi(?!" + VOWEL + ")", "ʑi"),
    ("zi(?=" + VOWEL +")", "ʑ"),
    ("ź", "ʑ"),
    ("ż", "ʐ")
]
NASAL_TO_M = "p|b"
NASAL_TO_N = "t|d|n|s|k|g"
NASAL_TO_NI = "t͡ɕ|d͡ʑ"
VOICED_TO_DEVOICED = {
    "b": "p",
    "d": "t",
    "v": "f",
    "z": "s",
    "g": "k",
    "d͡z": "t͡s",
    "d͡ʐ": "t͡ʂ",
    "d͡ʑ": "t͡ɕ",
    "ʐ": "ʂ",
    "ʑ": "ɕ",
    "z": "s",
}
DEVOICED_TO_VOICED = dict([(y, x) for (x, y) in VOICED_TO_DEVOICED.items()])
VOICED_TO_DEVOICED["@"] = "ʂ"
VOICED = set(VOICED_TO_DEVOICED.keys())
ALWAYS_DEVOICED = set(["x"])
DEVOICED = set(VOICED_TO_DEVOICED.values()) | ALWAYS_DEVOICED
VOICED_AND_DEVOICED = VOICED | DEVOICED
VOICE_AGNOSTIC = set(["r", "l", "j", "w", "n", "m", "ɲ"])
CONSONANTS = VOICED | DEVOICED | VOICE_AGNOSTIC

TRANSFORMATIONS = [
    # They happen sequentially.
    ("((" + '|'.join(VOICED_AND_DEVOICED) + "){2,})", revoice_cluster),
    ("ɛ̃(?=\W)", "ɛ"),
    ("ɛ̃(?=" + NASAL_TO_M + ")", "ɛm"),
    ("ɛ̃(?=" + NASAL_TO_N + ")", "ɛn"),
    ("ɛ̃(?=" + NASAL_TO_NI + ")", "ɛɲ"),
    ("ɛ̃", "ɛu"),
    ("ɔ̃(?=" + NASAL_TO_M + ")", "ɔm"),
    ("ɔ̃(?=" + NASAL_TO_N + ")", "ɔn"),
    ("ɔ̃(?=" + NASAL_TO_NI + ")", "ɔɲ"),
    ("ɔ̃", "ɔu"),
    ("(" + '|'.join(VOICED) + ")(?=\s)", lambda x: VOICED_TO_DEVOICED[x.group(0)]),
]

DIFFERENCE = u"\u0302"
   
IPA_TO_TURKISH = [
    ("i", "i"),
    ("a", "a"),
    ("ɛ", "e"),
    ("ɨ", "ı"),
    ("u", "u"),
    ("ɔ", "o"),
    
    ("b", "b"),
    ("t͡s", "ts"),
    ("t͡ɕ", "ç" + DIFFERENCE),
    ("t͡ʂ", "ç"),
    ("d", "d"),
    ("d͡z", "dz"),
    ("d͡ʑ", "c" + DIFFERENCE),
    ("d͡ʐ", "c"),
    ("f", "f"),
    ("g", "g"),
    ("x", "h"),
    ("k", "k"),
    ("l", "l"),
    ("w", "w"),
    ("m", "m"),
    ("n", "n"),
    ("ɲ", "ñ"),
    ("p", "p"),
    ("r", "r"),
    ("s", "s"),
    ("ɕ", "ş" + DIFFERENCE),
    ("ʂ", "ş"),
    ("t", "t"),
    ("v", "v"),
    ("z", "z"),

    # Those operate on j on both sides, they need to have good order.
    ("j", "y"),
    ("@", "j"),
    ("ʑ", "j" + DIFFERENCE),
    ("ʐ", "j"),
]

def polish_to_turkish_ortography(input):
  result = input.lower()
  for polish, ipa in sorted(TO_IPA, key=lambda x: -len(x[0])):
      result = re.sub(polish, ipa, result)
  for from_string, to in TRANSFORMATIONS:
      result = re.sub(from_string, to, result)
  for from_string, to in IPA_TO_TURKISH:
      result = re.sub(from_string, to, result)
  return result

if __name__ == '__main__':
  for line in fileinput.input():
    print(polish_to_turkish_ortography(line))

