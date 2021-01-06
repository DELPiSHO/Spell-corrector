import re
import time
from timeit import default_timer as timer
from datetime import timedelta
from collections import Counter
from spellchecker import SpellChecker
from autocorrect import Speller

spell = SpellChecker()
check = Speller(lang='en')

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big2.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

print(len(edits1('somthing')))
print(known(edits1('somthing')))

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

print(len(set(edits2('something'))))
print(known(edits2('something')))
print(spell.word_frequency.unique_words)


def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = spell.correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))


def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

#spelltest(Testset(open('spell-testset1.txt')))  # Development set
#spelltest(Testset(open('spell-testset2.txt')))  # Final test set

def unit_test_spellCHECKER():
    print("Pyspellchecker little test")
    start = timer()
    assert spell.correction('speling') == 'spelling'
    assert spell.correction('korrectud') == 'corrected'
    assert spell.correction('bycycle') == 'bicycle'
    assert spell.correction('inconvient') == 'inconvenient'
    assert spell.correction('arrainged') == 'arranged'
    assert spell.correction('peotry') == 'poetry'
    assert spell.correction('peotryy') == 'poetry'
    assert spell.correction('word') == 'word'
    assert spell.correction('quintessential') == 'quintessential'
    assert spell.correction('acess') == 'access'
    assert spell.correction('basicaly') == 'basically'
    assert spell.correction('benifit') == 'benefit'
#    assert spell.correction('benining') == 'beginning'
#    assert spell.correction('beetween') == 'between'
    assert spell.correction('biult') == 'built'
#    assert spell.correction('carrer') == 'career'
    assert spell.correction('cirtain') == 'certain'
    assert spell.correction('descided') == 'decided'
    end = timer()
    print(timedelta(seconds=end-start))
    return 'unit_test_2 passed'
def unit_test_AUTOCORRECT():
    print("Autocorrect little test")
    start = timer()
    assert check.autocorrect_word('speling') == 'spelling'
    assert check.autocorrect_word('korrectud') == 'corrected'
    assert check.autocorrect_word('bycycle') == 'bicycle'
    assert check.autocorrect_word('inconvient') == 'inconvenient'
    assert check.autocorrect_word('arrainged') == 'arranged'
    assert check.autocorrect_word('peotry') == 'poetry'
    assert check.autocorrect_word('peotryy') == 'poetry'
    assert check.autocorrect_word('word') == 'word'
    assert check.autocorrect_word('quintessential') == 'quintessential'
    assert check.autocorrect_word('acess') == 'access'
    assert check.autocorrect_word('benining') == 'beginning'
    assert check.autocorrect_word('basicaly') == 'basically'
    assert check.autocorrect_word('benifit') == 'benefit'
    assert check.autocorrect_word('beetween') == 'between'
    assert check.autocorrect_word('biult') == 'built'
    assert check.autocorrect_word('carrer') == 'career'
    assert check.autocorrect_word('cirtain') == 'certain'
    assert check.autocorrect_word('descided') == 'decided'
    end = timer()
    print(timedelta(seconds=end-start))
    return 'unit test AUTOCORRECT passed'

test = "does this sentece have misspelled wordz?"
print(check(test))
print(unit_test_spellCHECKER())
print(unit_test_AUTOCORRECT())