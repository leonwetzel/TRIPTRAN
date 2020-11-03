#!/usr/bin/env python3
import os
import pickle
import xml.etree.ElementTree as ET

import spacy
import nltk

from datamanager import load_corpus
from generate_templates import generate_templates, fill_in_most_frequent_template
from BLEU import overallBleuScore


DATA_DIR = "data"
TRAIN_CORPUS_PICKLE = "corpus.pkl"
DEVCORPUS_PICKLE = "devcorpus.pkl"

nlp = spacy.load("en_core_web_sm")


def main():
    """
    Read XML files and store relevant information.
    :return:
    """
    corpus = load_corpus(DATA_DIR, TRAIN_CORPUS_PICKLE, type='train',
                         suffix='challenge', triple_size=1)

    devcorpus = load_corpus(DATA_DIR, DEVCORPUS_PICKLE, type='dev',
                            suffix='challenge', triple_size=1)

    # print(corpus[:100])
    # print()
    # print(devcorpus[:100])

    # Generate templates
    print("Generating templates...")
    templates = generate_templates(corpus)
    # Generate output
    print("Generating output...")
    list_of_references, hypotheses = fill_in_most_frequent_template(templates, devcorpus)
    # Calculate BLEU score
    print("Calculating BLEU score...")
    print(overallBleuScore(list_of_references, hypotheses))


if __name__ == '__main__':
    main()
