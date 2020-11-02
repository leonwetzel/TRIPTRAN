#!/usr/bin/env python3
import os
import pickle
import xml.etree.ElementTree as ET

import spacy

from rdf import Triple


DATA_DIR = "data"
CORPUS_PICKLE = "corpus.pkl"
DEVCORPUS_PICKLE = "devcorpus.pkl"

nlp = spacy.load("en_core_web_sm")


def main():
    """
    Read XML files and store relevant information.
    :return:
    """
    if not os.path.isfile(CORPUS_PICKLE):
        print("Constructing pickle...")
        corpus = []
        for subdir, dirs, files in os.walk(f'{DATA_DIR}'):
            for filename in files:
                filepath = subdir + os.sep + filename

                if filepath.startswith(r"data\train")\
                        and filepath.endswith("challenge.xml") and "1triple" in filepath:
                    corpus.extend(extract_information(filepath))

        with open(CORPUS_PICKLE, 'wb') as F:
            pickle.dump(corpus, F)
    else:
        print("Loading pickle...")
        with open(CORPUS_PICKLE, 'rb') as F:
            corpus = pickle.load(F)

    # Same for devcorpus:
    if not os.path.isfile(DEVCORPUS_PICKLE):
        print("Constructing pickle...")
        devcorpus = []
        for subdir, dirs, files in os.walk(f'{DATA_DIR}'):
            for filename in files:
                filepath = subdir + os.sep + filename

                if filepath.startswith(r"data\dev")\
                        and filepath.endswith("challenge.xml") and "1triple" in filepath:
                    devcorpus.extend(extract_information(filepath))

        with open('devcorpus.pkl', 'wb') as F1:
            pickle.dump(devcorpus, F1)
    else:
        print("Loading pickle...")
        with open(DEVCORPUS_PICKLE, 'rb') as F:
            corpus = pickle.load(F)


    # for triple in corpus[:100]:
    #     print(triple)
    #     for sentence in triple.lexical_examples:
    #         doc = nlp(sentence)

    #         for token in doc:
    #             print(token.text, token.pos_, token.dep_)
    #         print()


def extract_information(file):
    """
    Extract relevant information from
    the XML files.
    :param file:
    :return:
    """
    subcorpus = []
    tree = ET.parse(file)
    entries = tree.findall('entries')

    for ent in entries:
        entry = ent.findall('entry')
        for x in entry:
            triple = x.find('modifiedtripleset').find('mtriple').text
            lexical_comments = x.findall('lex')
            output = Triple(triple)
            for comment in lexical_comments:
                output.add_lexical_example(comment.text)
            subcorpus.append(output)

    return subcorpus


if __name__ == '__main__':
    main()
