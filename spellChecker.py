from spellchecker import SpellChecker
spell = SpellChecker()
print(spell.correction('hellou'))
sentence = spell.split_words("Howw are theyi?")
print([spell.correction(word) for word in sentence])