#!/usr/bin/env python3
import numpy as np

from nltk.translate.bleu_score import sentence_bleu, corpus_bleu,\
    SmoothingFunction
from nltk.translate.meteor_score import meteor_score

from feature_engineering import count_linguistic_mistakes

smoothing_function = SmoothingFunction()


def single_bleu_score(references, target_sentence, verbose=False):
    """
    Split the sentences into a list of words
    Calculate the BLEU score
    
    :param references: string
    :param target_sentence: the target sentence (ground truth)
    :return: BLEU score for 1 sentence
    """
    reference = [sentence.lower().split() for sentence in references]
    candidate = target_sentence.lower().split()
    score = sentence_bleu(reference, candidate)

    return score


def macro_score(references, generated_sentences, metric="bleu"):
    """Calculates the macro score, using a given metric.

    Loop trough the two lists and calculate a score for each item
    and add that to a list.

    Parameters
    ----------
    references : iterable
        List of reference sentences related to the hypothesis.
    generated_sentences : iterable
        List of translations by TRIPTRAN.
    metric : str
        Indicates which metric should be used as scorer. Can either be
        bleu (default) or meteor.

    Returns
    -------
    score : float
        The metric score.
    """
    scores = []
    if metric.lower() == "bleu":
        scores = [single_bleu_score(reference_sentences, generated_sentence)
                  for reference_sentences, generated_sentence in
                  zip(references, generated_sentences)]
    elif metric.lower() == "meteor":
        scores = [single_meteor_score(reference_sentences, generated_sentence)
                  for reference_sentences, generated_sentence in
                  zip(references, generated_sentences)]
    return sum(scores) / len(scores)


def corpus_bleu_score(reference_sentences, generated_sentences):
    """
    Lower and split() the sentences
    Calculate the corpus Bleu score
    Note: This is different from the (macro) average bleu score!!
    http://www.nltk.org/api/nltk.translate.html#nltk.translate.bleu_score.corpus_bleu
    :param reference_sentences: [[ref1a, ref1b, ref1c], [ref2a]]
    :param generated_sentences: [hyp1, hyp2]
    :return: BLEU score for corpus
    """
    generated_sentences = [
        sentence.lower().split() for sentence in generated_sentences
    ]
    reference_sentences = [
        [sentence.lower().split() for sentence in reference]
        for reference in reference_sentences
    ]
    return corpus_bleu(reference_sentences, generated_sentences,
                       smoothing_function=None)


def overall_bleu_score(reference_sentences, generated_sentences):
    """
    Lower and split() the sentences in different functions
    Calculate the corpus Bleu score
    :param reference_sentences: [[ref1a, ref1b, ref1c], [ref2a]]
    :param generated_sentences: [hyp1, hyp2]
    :return: The corpus and macro bleu score
    """
    return "Corpus BLEU score: ", \
           corpus_bleu_score(reference_sentences, generated_sentences), \
           "Macro average BLEU score:", \
           macro_score(reference_sentences, generated_sentences,
                       metric='bleu')


def single_meteor_score(references, hypothesis):
    """Calculates the METEOR scores

    Parameters
    ----------
    references : list
        List of reference sentences related to the hypothesis
    hypothesis : str
        Estimated translation

    Returns
    -------
    meteor_score : float
        METEOR score
    """
    return meteor_score(references, hypothesis)


def wer_score(hypotheses, references, print_matrix=False):
    """Calculate the Word Error Rate (WER) score.

    Stolen from https://github.com/gcunhase/NLPMetrics/blob/master/notebooks/wer.ipynb.

    Parameters
    ----------
    hypotheses : iterable
        List containing the hypotheses.
    references : iterable
        List containing the reference sentences.
    print_matrix : bool
        Indicates if a result matrix should be printed or not

    Returns
    -------
    word_error_score : int
        The Word Error Rate (WER) score of a given list of sentences
    """
    N = len(hypotheses)
    M = len(references)
    L = np.zeros((N, M))
    for i in range(0, N):
        for j in range(0, M):
            if min(i, j) == 0:
                L[i, j] = max(i, j)
            else:
                deletion = L[i - 1, j] + 1
                insertion = L[i, j - 1] + 1
                sub = 1 if hypotheses[i] != references[j] else 0
                substitution = L[i - 1, j - 1] + sub
                L[i, j] = min(deletion, min(insertion, substitution))
                # print("{} - {}: del {} ins {} sub {} s {}".format(
                #     hypotheses[i], references[j], deletion, insertion, substitution,
                #     sub)
                # )
    if print_matrix:
        print("WER matrix ({}x{}): ".format(N, M))
        print(L)
    return int(L[N - 1, M - 1])


def average_grammar_score(generated_sentences):
    """
    Loop trough the two lists and calculate the number of grammar
    mistakes for each item and add that to a list
    :param generated_sentences: two lists of lists with sentences
                                in string format
    :return: The avg and total grammar mistakes
    """
    scores = [count_linguistic_mistakes(sentence) for sentence in
              generated_sentences]
    return sum(scores) / len(scores), sum(scores)


# if __name__ == '__main__':
#     # single sample example
#     generated = "Hello world, we generated this sentence from a triple"
#     target_sentences = [
#         "An other sentence generated from a triple",
#         "Hello world, this is the second we generated this"
#         " sentence from a triple"]
#
#     # multi sample example
#     list_of_references = [[
#         "It is a guide to action which ensures that the military"
#         " always obeys the command of the party",
#         "It is a guide to action which ensures that the military will"
#         " forever heed Partyu commands",
#         "It is the practical guide for the army always to heed the"
#         " directions of the party"],
#         ["He was interested in the world history because he read"
#          " the book"]]
#     hypotheses = [
#         "It is a guide, which ensures that the military always obeys"
#         " the command of the party",
#         "He read the book because he was interested in the"
#         " world history"]
#
#     print("The BLEU score of a single sentence: ",
#           single_bleu_score(target_sentences, generated))
#     print("The METEOR score of a single sentence: ",
#           single_meteor_score(target_sentences, generated))
#     print("The corpus BLEU score: ",
#           corpus_bleu_score(list_of_references, hypotheses))
#     print("The macro average BLEU score:",
#           macro_score(list_of_references, hypotheses, metric='bleu'))
#     print("The macro average METEOR score: ",
#           macro_score(list_of_references, hypotheses, metric='meteor'))
#
#     print("BLEU scores: ",
#           overall_bleu_score(list_of_references, hypotheses))
