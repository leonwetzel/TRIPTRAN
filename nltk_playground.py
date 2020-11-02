from nltk.corpus import wordnet as wn
from feature_engineering import convert


def main():
    """
    This script tests the use of WordNet's synsets.
    We extract both synonyms and antonyms.

    Please check https://www.nltk.org/howto/wordnet.html
    for more information.
    :return:
    """
    sample = "location"
    synonyms = []
    antonyms = []

    for syn in wn.synsets(sample):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())

    print(set(synonyms))
    print(set(antonyms))


if __name__ == '__main__':
    main()
