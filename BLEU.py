#!/usr/bin/env python3
import os
import pickle
import xml.etree.ElementTree as ET
import nltk

from datamanager import load_corpus
from nltk.translate.bleu_score import sentence_bleu


""""Input: targetsentence: string
    Input: referencesentences: list of strings
    Process: Split the sentences into a list of words
    Calculate the BLEU score
    Output: BLEU score for 1 sentence"""
def singleBleu(targetSent, referenceSents):
    reference = []
    for sent in referenceSents:
        reference.append(sent.lower().split())
    candidate = targetSent.lower().split()

    score = sentence_bleu(reference, candidate)
    print(score)


def main():
    """
    Test the bleu functions
    """
    generated = "Hello world, we generated this sentence from a triple"
    targetsSentence = ["An other sentence generated from a triple"
                       "Hello world, this is the second we generated this sentence from a triple"]
    print(singleBleu(generated, targetsSentence))



if __name__ == '__main__':
    main()
