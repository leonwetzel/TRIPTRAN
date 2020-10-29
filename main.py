#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET

from rdf import Triple


DATA_DIR = "data"


def main():
    """
    Read XML files and store relevant information.
    :return:
    """
    corpus = []
    for subdir, dirs, files in os.walk(f'{DATA_DIR}'):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.startswith(r"data\train")\
                    and filepath.endswith("challenge.xml"):
                corpus.extend(extract_information(filepath))


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
                output.add_lexical_example(comment)
            subcorpus.append(output)

    return subcorpus


if __name__ == '__main__':
    main()
