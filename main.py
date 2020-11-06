#!/usr/bin/env python3
import nltk

from datamanager import load_corpus
from generate_templates import generate_templates,\
    fill_in_most_frequent_template
from evaluation import overall_bleu_score, average_grammar_score,\
    calculate_meteor_scores
from generate_templates import generate_templates,\
    fill_in_most_frequent_template
from evaluation import overall_bleu_score


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

    devcorpus = load_corpus(DATA_DIR, DEVCORPUS_PICKLE, type='dev',
                            suffix='challenge', triple_size=1)

    train_corpus = load_corpus(DATA_DIR, TESTCORPUS_PICKLE, type='test',
                               suffix='challenge', triple_size=1)

    # Generate templates
    print("Generating templates...")
    templates = generate_templates(corpus)
    # Generate output
    print("Generating output...")
    list_of_references, hypotheses = fill_in_most_frequent_template(
        templates, devcorpus
    )
    # Calculate BLEU score
    print("Calculating BLEU score...")
    print(overall_bleu_score(list_of_references, hypotheses))
    print("Calculating Grammar scores...")
    print("Grammar mistakes (avg, total): ",
          average_grammar_score(hypotheses))

    print()


if __name__ == '__main__':
    main()
