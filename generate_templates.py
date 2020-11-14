import re

from feature_engineering import clean_names, clean_sentence
from rules import generate_rule_based_sentence


def generalize_sentence(subj, obj, sentence):
    """Replaces the subject and object in a sentence by SUBJ and OBJ
     to create a template sentence.

    Parameters
    ----------
    subj
        The subject in the sentence.
    obj
        The object in the sentence.
    sentence
        A sentence containing (at least) a subject and
        an object.

    Returns
    -------
    template
        Lexicalised sentence
    """
    new_subject = clean_names(subj)
    new_object = clean_names(obj)
    template = sentence.replace(new_subject, ' SUBJ ')
    template = template.replace(new_object, ' OBJ ')
    # Remove redundant whitespaces:
    template = " ".join(template.split())
    return template


def add_values_in_dict(dictionary, key, values):
    """
    Append multiple values to a key in the given dictionary

    Parameters
    ----------
    dictionary
    key
    values

    Returns
    -------

    """
    if key not in dictionary:
        dictionary[key] = list()
    dictionary[key].extend(values)
    return dictionary


def most_frequent(data):
    """
    Returns the most frequent item of a list. If multiple occur
    the same number of times, it returns the last of those.

    Parameters
    ----------
    data

    Returns
    -------

    """
    return max(set(data), key=data.count)


def generate_templates(training_corpus):
    """
    Reads a training corpus and generates templates from the examples
    in it

    Parameters
    ----------
    training_corpus

    Returns
    -------

    """
    templates = {}
    single_templates = {}
    for triple in training_corpus:
        subj = triple.subject
        obj = triple.object
        predicate = triple.predicate
        lexical_examples = triple.lexical_examples
        # Read all sentences in the lexical examples and replace
        # the subjects and objects by placeholders
        for i in range(len(lexical_examples)):
            sentence = lexical_examples[i]
            template = generalize_sentence(subj, obj, sentence)
            # Only add the template to the dictionary if subject
            # and object are properly replaced.
            if 'SUBJ' in template and 'OBJ' in template:
                templates = add_values_in_dict(templates, predicate,
                                               [template])
    # Find most frequent template:
    for predicate in templates:
        single_templates[predicate] = most_frequent(templates[predicate])
    # Remove duplicates from templates:
    for predicate in templates:
        templates[predicate] = list(set(templates[predicate]))
    return single_templates


def fill_in_all_templates(templates, test_corpus):
    """
    Reads the triples from a testcorpus and generates
    multiple sentences from them using all templates.

    Parameters
    ----------
    templates
    test_corpus

    Returns
    -------

    """
    for triple in test_corpus:  # Read only first 10 triples (for developmental purposes)
        cleaned_subject = clean_names(triple.subject)
        cleaned_object = clean_names(triple.object)
        predicate = triple.predicate
        # print(triple)
        # Test whether there is a template for the current predicate:
        if predicate in templates:
            # For all example sentences of this predicate, fill in the subject and object of the triple in the template:
            for lexical_example in templates[predicate]:
                sentence = lexical_example.replace('SUBJ', cleaned_subject)
                sentence = sentence.replace('OBJ', cleaned_object)
                sentence = clean_sentence(sentence)
                # print('Generated sentence: ' +sentence)
        # else:
        #    print("No sentence with such predicate in the training corpus")


def fill_in_most_frequent_template(singleTemplates, testcorpus):
    """Reads the triples from a test_corpus and generates one sentence for each triple, from the most frequent template in the training sentences"""
    not_found = []
    list_of_references = []
    hypotheses = []
    for triple in testcorpus:  # Read only first 10 triples (for developmental purposes)
        cleanSubj = clean_names(triple.subject)
        cleanObj = clean_names(triple.object)
        pred = triple.predicate
        # print(triple)
        list_of_references.append(triple.lexical_examples)
        # Test whether there is a template for the current predicate:
        if pred in singleTemplates:
            # Fill in the subject and object of the triple in the template sentence:
            sentence = singleTemplates[pred].replace('SUBJ', cleanSubj)
            sentence = sentence.replace('OBJ', cleanObj)
            sentence = clean_sentence(sentence)
            # print('Generated sentence: ' +sentence)
            # print('Original sentences: ')
            # print(triple.lexical_examples)
        else:
            not_found.append(pred)
            sentence = generate_rule_based_sentence(triple)
            # print('Generated sentence: ' + sentence)
            # print('Original sentences: ')
            # print(triple.lexical_examples)
            # print("No sentence with such predicate in the training corpus")
        hypotheses.append(sentence)
    return list_of_references, hypotheses
