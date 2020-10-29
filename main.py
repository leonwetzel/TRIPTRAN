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
    for subdir, dirs, files in os.walk(f'{DATA_DIR}'):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.startswith(r"data\train")\
                    and filepath.endswith("challenge.xml"):
                extract_information(filepath)


def extract_information(file):
    """
    Extract relevant information from
    :param file:
    :return:
    """
    tree = ET.parse(file)
    root = tree.getroot()

    entries = tree.findall('entries')
    # print('Entry count:', len(entries))
    for ent in entries:
        entry = ent.findall('entry')
        for x in entry:
            triple = x.find('modifiedtripleset').find('mtriple').text
            lexical_comments = x.find('lex').text
            print('triple: ', triple)
            print('lexical_comments: ', lexical_comments)


if __name__ == '__main__':
    main()
