#!/usr/bin/env python3
from rdf import Triple


def main():
    """The TRIPTRAN application can be used to translate RDF
    triples to the English natural language.
    """

    while True:
        # TODO add additional input possibilities (such as entire strings)
        # TODO implement extra input validation
        subject = input("Enter the subject: ")
        predicate = input("Enter the predicate: ")
        object = input("Enter the object: ")

        triple = Triple(subject, predicate, object)

        # TODO implement actual translation of triple
        print(triple, '\n')


if __name__ == '__main__':
    main()
