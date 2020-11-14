import re

import nltk
from nltk.corpus import wordnet as wn

import dateparser
import language_check

language_tool = language_check.LanguageTool("en-US")

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
    tokens : iterable
        A list of tokens, originating from a predicate.
    """
    pos_tags = []
    if len(tokens) > 1 or len([tokens]) == 1:
        pos_tags = [token[1] for token in nltk.pos_tag(tokens)]
    return pos_tags


def count_linguistic_mistakes(sentence):
    """
    Counts the amount of linguistic mistakes
    found by the language_check package.
    :param sentence:
    :return:
    """
    mistakes = language_tool.check(sentence)
    return len(mistakes)


def clean_predicate(pred):
    """Split the predicate by upper cases, make everything lower case
    and convert to list

    Parameters
    ----------
    pred
        A predicate in its original form, originating
        from the corpus.

    Returns
    -------
    predicate
        Cleaned version of the predicate

    predicate_parts
        Separate parts of the original predicate
    """
    predicate = " ".join(pred.split())
    predicate = re.sub(r'([A-Z])', r' \1', predicate)
    predicate = predicate.lower()
    # convert to a list:
    predicate_parts = predicate.split(" ")
    return predicate, predicate_parts


def clean_names(name):
    """

    Parameters
    ----------
    name

    Returns
    -------

    """
    # Replace underscores by spaces:
    name = name.replace('_', ' ')
    # Remove redundant spaces:
    name = " ".join(name.split())
    return name


def clean_sentence(sentence):
    """

    Parameters
    ----------
    sentence

    Returns
    -------

    """
    # If there is a space in front of a dot, remove it:
    sentence = sentence.replace(" .", ".")
    # If there is a space in front of a 's, remove it:
    sentence = sentence.replace(" 's", "'s")
    # TODO: In de output kijken of er nog meer nodig is.
    return sentence
