#!/usr/bin/env python3
import nltk

from datamanager import load_corpus
from evaluation import macro_score, average_grammar_score, \
    corpus_bleu_score
from generate_templates import generate_templates, \
    fill_in_most_frequent_template

DATA_DIR = "data"
TRAIN_CORPUS_PICKLE = "corpus.pkl"
DEVCORPUS_PICKLE = "devcorpus.pkl"
TESTCORPUS_PICKLE = "testcorpus.pkl"


def main():
    """
    This script converts the downloaded WebNLG data
    and generates sentences from the indicated triples.
    """
    try:
        nltk.data.find('corpora/wordnet')
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')

    corpus = load_corpus(DATA_DIR, TRAIN_CORPUS_PICKLE, type='train',
                         suffix='challenge', triple_size=1)

    test_corpus = load_corpus(DATA_DIR, TESTCORPUS_PICKLE, type='test',
                              suffix='release', triple_size=1)

    # Generate templates
    print("Generating templates...")
    templates = generate_templates(corpus)
    # Generate output
    print("Generating output...")
    list_of_references, hypotheses = fill_in_most_frequent_template(
        templates, test_corpus
    )
    print()

    for references, hypothesis in zip(list_of_references, hypotheses):
        print(references)
        print(hypothesis)
        print()

    print()

    # Calculate BLEU score
    print("Corpus BLEU score", corpus_bleu_score(list_of_references,
                                                 hypotheses))
    print("Macro BLEU score", macro_score(list_of_references,
                                          hypotheses, metric='bleu'))
    print("Macro METEOR score", macro_score(list_of_references,
                                            hypotheses,
                                            metric='meteor'))

    avg_mistakes, sum_mistakes, zero_mistakes = average_grammar_score(hypotheses)
    print("Average amount of grammar mistakes", avg_mistakes)
    print("Total amount of grammar mistakes:", sum_mistakes)
    print("Total amount of correct sentences: ", zero_mistakes)
    print("Total amount of sentences", len(hypotheses))


if __name__ == '__main__':
    main()
