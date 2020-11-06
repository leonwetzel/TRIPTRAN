import re
import dateparser

from feature_engineering import get_pos_tag


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
