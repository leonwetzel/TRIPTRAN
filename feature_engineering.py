import nltk
from nltk.corpus import wordnet as wn

import dateparser


# Just to make it a bit more readable
WN_NOUN = 'n'
WN_VERB = 'v'
WN_ADJECTIVE = 'a'
WN_ADJECTIVE_SATELLITE = 's'
WN_ADVERB = 'r'


def convert(word, from_pos, to_pos):
    """ Transform words given from/to POS tags
        Stolen from https://stackoverflow.com/a/48218093.

    Parameters
    ----------
    word : str
        A single word that should be translated.
    from_pos : str
        The POS tag related to the provided word.
    to_pos : str
        Indicates to which word form the provided
        word should be translated to.
    """
    synsets = wn.synsets(word, pos=from_pos)

    # Word not found
    if not synsets:
        return []

    # Get all lemmas of the word (consider 'a'and 's' equivalent)
    lemmas = []
    for s in synsets:
        for lemma in s.lemmas():
            if s.name().split('.')[1] == from_pos or from_pos in (
                    WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and \
                    s.name().split('.')[1] in \
                    (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                lemmas += [lemma]

    # Get related forms
    derivationally_related_forms = [
        (lemma, lemma.derivationally_related_forms()) for lemma in lemmas
    ]

    # filter only the desired pos (consider 'a' and 's' equivalent)
    related_noun_lemmas = []

    for drf in derivationally_related_forms:
        for lemma in drf[1]:
            if lemma.synset().name().split('.')[1] == to_pos or to_pos in (
                    WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and \
                    lemma.synset().name().split('.')[1] in (
                    WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                related_noun_lemmas += [lemma]

    # Extract the words from the lemmas
    words = [lemma.name() for lemma in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing
    # tuples (word, probability)
    result = [(word, float(words.count(word)) / len_words) for
              word in set(words)]
    result.sort(key=lambda word: -word[1])

    # return all the possibilities sorted by probability
    return result


def get_pos_tag(tokens):
    """ Retrieves the POS tags of a given list of tokens.

    Parameters
    ----------
    tokens : list
        A list of tokens, originating from a predicate.
    """
    pos_tags = []
    if len(tokens) > 1:
        pos_tags = [token[1] for token in nltk.pos_tag(tokens)]
    elif len([tokens]) == 1:
        pos_tags = [token[1] for token in nltk.pos_tag(tokens)]
    return pos_tags


if __name__ == '__main__':
    print(convert('hurry', 'v', 'n'))
    print(convert('destroy', 'v', 'n'))
    print(convert('affiliation', 'n', 'v'))
    print(convert('studying', 'v', 'n'))
    print(convert('dinner', 'n', 'v'))
    print(convert('eat', 'v', 'r'))
    print()

    print(get_pos_tag(["cheese"]))
    print(get_pos_tag(["hot", "dog"]))
    print(get_pos_tag(["clock", "house"]))
    print(get_pos_tag(["is", "part", "of"]))
    print(get_pos_tag(["affiliated"]))
    print(get_pos_tag(["current", "tennants"]))
    print()

    print(dateparser.parse("2020-02-21"))
    print(dateparser.parse("Cheese is nice"))
