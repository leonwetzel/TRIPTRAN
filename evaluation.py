#!/usr/bin/env python3
import language_check

from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from nltk.translate.meteor_score import meteor_score

language_tool = language_check.LanguageTool("en-US")


def check_sentence(sentence):
    """

    :param sentence: text sentence
    :return: number of grammar mistakes in a sentence
    """
    mistakes = language_tool.check(sentence)
    return len(mistakes)


def average_grammar_score(generated_sentences):
    """
    Loop trough the two lists and calculate the number of grammar
    mistakes for each item and add that to a list
    :param generated_sentences: two lists of lists with sentences
                                in string format
    :return: The avg and total grammar mistakes
    """
    scores = [check_sentence(sentence) for sentence in
              generated_sentences]
    return sum(scores) / len(scores), sum(scores)


def single_bleu_score(references, target_sentences):
    """
    Split the sentences into a list of words
    Calculate the BLEU score
    
    :param references: string
    :param target_sentences: list of strings
    :return: BLEU score for 1 sentence
    """
    reference = [sentence.lower().split() for sentence in references]
    candidate = target_sentences.lower().split()
    score = sentence_bleu(reference, candidate)
    if score < 0.52:
        print("Low score(" + str(score) + "): ")
        print("Reference sentences: ")
        print(references)
        print("Target sentences: " + target_sentences)

    return score


def macro_bleu_score(references, generated_sentences):
    """
    Loop trough the two lists and calculate a bleu score for each item
    and add that to a list
    :param references:
    :param generated_sentences:
    :return: The avarage bleu score
    """
    scores = [single_bleu_score(reference_sentences, generated_sentence)
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
    generated_sentences = [sentence.lower().split() for sentence in
                           generated_sentences]
    reference_sentences = [
        [sentence.lower().split() for sentence in reference] for
        reference
        in reference_sentences]
    return corpus_bleu(reference_sentences, generated_sentences)


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
           macro_bleu_score(reference_sentences, generated_sentences)


def calculate_meteor_scores(references, hypothesis):
    """Calculates the METEOR scores"""
    return meteor_score(references, hypothesis)


if __name__ == '__main__':
    generated = "Hello world, we generated this sentence from a triple"
    target_sentences = [
        "An other sentence generated from a triple",
        "Hello world, this is the second we generated this"
        " sentence from a triple"]
    list_of_references = [[
        "It is a guide to action which ensures that the military"
        " always obeys the command of the party",
        "It is a guide to action which ensures that the military will"
        " forever heed Partyu commands",
        "It is the practical guide for the army always to heed the"
        " directions of the party"],
        ["He was interested in the world history because he read"
         " the book"]]
    hypotheses = [
        "It is a guide, which ensures that the military always obeys"
        " the command of the party",
        "He read the book because he was interested in the"
        " world history"]

    print("The BLEU score of a single sentence: ",
          single_bleu_score(target_sentences, generated))
    print("The corpus BLEU score: ",
          corpus_bleu_score(list_of_references, hypotheses))
    print("The macro average BLEU score:",
          macro_bleu_score(list_of_references, hypotheses))

    print("BLEU scores: ",
          overall_bleu_score(list_of_references, hypotheses))
