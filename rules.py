#!/usr/bin/env python3
import dateparser

from feature_engineering import get_pos_tag, clean_predicate,\
    clean_names


def noun_rule(triple):
    """

    Parameters
    ----------
    triple

    Returns
    -------

    """
    sentence = "The " + clean_predicate(triple.predicate)[
        0] + " of " + clean_names(
        triple.subject) + " is " + clean_names(triple.object) + "."
    sentence = " ".join(sentence.split())
    return sentence


def verb_rule(triple):
    """

    Parameters
    ----------
    triple

    Returns
    -------

    """
    if dateparser.parse(triple.object) is None:
        sentence = clean_names(triple.subject) + " is " + \
                   clean_predicate(triple.predicate)[
                       0] + " " + clean_names(triple.object) + "."
    else:
        # If the object is a date, use a different template:
        sentence = clean_names(triple.subject) + " was " + \
                   clean_predicate(triple.predicate)[
                       0] + " on " + clean_names(triple.object) + "."
    sentence = " ".join(sentence.split())
    return sentence


def generate_rule_based_sentence(triple):
    """

    Parameters
    ----------
    triple : rdf.Triple containing

    Returns
    -------

    """
    predicate, predicate_list = clean_predicate(triple.predicate)
    # print(get_pos_tag(predicate_list))
    if get_pos_tag(predicate_list)[-1] == 'NN' or \
            get_pos_tag(predicate_list)[-1] == 'NNS':
        sentence = noun_rule(triple)
    elif 'VBN' in get_pos_tag(predicate_list) or 'VBD' in get_pos_tag(
            predicate_list):
        sentence = verb_rule(triple)
    else:
        sentence = '...'
    return sentence