#!/usr/bin/env python3
import os
import pickle
import xml.etree.ElementTree as ET
import nltk

from datamanager import load_corpus
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from nltk.translate.meteor_score import meteor_score
from generate_templates import fill_in_all_templates, generate_templates

""""Input: targetsentence: string
    Input: referencesentences: list of strings
    Process: Split the sentences into a list of words
    Calculate the BLEU score
    Output: BLEU score for 1 sentence"""
def singleBleu(referenceSents, targetSent):
    reference = [sent.lower().split() for sent in referenceSents]
    candidate = targetSent.lower().split()
    score = sentence_bleu(reference, candidate)

    return score


""""Input: two lists of lists with sentences in string format 
    Process: loop trough the two lists and calculate a bleu score for each item and add that to a list
    Return: The avarage bleu score"""
def macroBleu(referenceSentences, generatedSentences):
    scores = [singleBleu(refSents, generatedSent) for refSents, generatedSent in zip(referenceSentences, generatedSentences)]
    return sum(scores) / len(scores)




"""Input: two lists of lists with sentences in string format 
        listOfReferencesSentences = [[ref1a, ref1b, ref1c], [ref2a]]
        listOfGenratedSenteces = [hyp1, hyp2]
        Process: lower and split() the sentences 
        Calculate the corpus Bleu score
        Note: This is different from the (macro) average bleu score!! 
        http://www.nltk.org/api/nltk.translate.html#nltk.translate.bleu_score.corpus_bleu 
        Output: Blue score corpus
"""
def corpusBleu(referenceSentences, generatedSentences):

    generatedSentences = [sent.lower().split() for sent in generatedSentences]
    referenceSentences = [[sent.lower().split() for sent in ref] for ref in referenceSentences]
    score = corpus_bleu(referenceSentences, generatedSentences)

    return score

"""Input: two lists of lists with sentences in string format 
        listOfReferencesSentences = [[ref1a, ref1b, ref1c], [ref2a]]
        listOfGenratedSenteces = [hyp1, hyp2]
        Process: lower and split() the sentences in different functions
        Calculate the corpus Bleu score
        Return: the corpus and macro bleu score"""

def overallBleuScore(referenceSentences, generatedSentences):

    return "The corpus Bleu score: ", corpusBleu(referenceSentences, generatedSentences), \
           "The macro average blue score:", macroBleu(referenceSentences, generatedSentences)


def calculate_meteor_scores(references, hypothesis):
    """Calculates the METEOR scores"""
    return meteor_score(references, hypothesis)


def main():
    """
    Test the bleu functions
    """
    generated = "Hello world, we generated this sentence from a triple"
    targetsSentences = ["An other sentence generated from a triple",
                       "Hello world, this is the second we generated this sentence from a triple"]
    list_of_references = [["It is a guide to action which ensures that the military always obeys the command of the party",
                           "It is a guide to action which ensures that the military will forever heed Partyu commands",
                           "It is the practical guide for the army always to heed the directions of the party"],
                          ["He was interested in the world history because he read the book"]]
    hypotheses = ["It is a guide, which ensures that the military always obeys the command of the party",
                  "He read the book because he was interested in the world history"]

    print("The Bleu score of a single sentence: ",singleBleu(targetsSentences, generated))
    print("The corpus Bleu score: ", corpusBleu(list_of_references, hypotheses))
    print("The macro average blue score:", macroBleu(list_of_references, hypotheses))

    print("Bleu scores: ", overallBleuScore(list_of_references, hypotheses))

if __name__ == '__main__':
    main()
