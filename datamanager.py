import os
import pickle
import shutil
import requests
import zipfile

import xml.etree.ElementTree as ET

from rdf import Triple

URLS = [
    {"year": 2017,
     "url": "https://gitlab.com/shimorina/webnlg-dataset/-/archive/master/webnlg-dataset-master.zip?path=webnlg_challenge_2017"},
    {"year": 2020,
     "url": "https://gitlab.com/shimorina/webnlg-dataset/-/archive/master/webnlg-dataset-master.zip?path=release_v2.1/xml"}
]


def download():
    """ Script for downloading all the relevant WebNLG files,
        used for testing, development and training.
    """
    if os.path.isdir('data'):
        check = input("The data directory already exists."
                      " Do you want to empty this directory and"
                      " download all assets (again)? [Y/N]\n")
        try:
            _ = str(check)
            if check == "Y":
                shutil.rmtree("data")
            elif check == "N":
                print("Your opinion does not matter, I do what I want!")
                shutil.rmtree("data")
            else:
                exit("f you")
        except ValueError:
            exit("Invalid input! Please restart the script and make"
                 "sure you enter either Y or N.\n")
    os.mkdir('data')

    for urls in URLS:
        file_name = f'data/{urls["year"]}.zip'
        response = requests.get(urls["url"])

        file = open(file_name, 'wb')
        file.write(response.content)

        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(path='data',
                               members=get_members(zip_ref))

        file.close()
        os.remove(file_name)


def get_members(zip):
    """ Extracts the files from a given zip file. Stolen from\
     https://stackoverflow.com/questions/8689938/extract-files-from-zip-without-keep-the-top-level-folder-with-python-zipfile

    Parameters
    ----------
    zip : ZipFile
        ZIP file containing the XML files with the data.
    """
    parts = []
    # get all the path prefixes
    for name in zip.namelist():
        print("Element name: ", name)
        # only check files (not directories)
        if not name.endswith('/'):
            # keep list of path elements (minus filename)
            parts.append(name.split('/')[:-1])
            # print(name.split('/')[:-1])
    # now find the common path prefix (if any)
    prefix = os.path.commonprefix(parts)
    if prefix:
        # re-join the path elements
        prefix = '/'.join(prefix) + '/'
    # get the length of the common prefix
    offset = len(prefix)
    # now re-set the filenames
    for zipinfo in zip.infolist():
        name = zipinfo.filename
        # only check files (not directories)
        if len(name) > offset:
            print(name[offset:], '\n')
            # remove the common prefix
            zipinfo.filename = name[offset:]
            yield zipinfo


def extract_information(file):
    """Extract relevant information from the XML files.

    Parameters
    ----------
    file : str
        XML file of which information can be extracted.
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
                output.add_lexical_example(comment.text)
            subcorpus.append(output)

    return subcorpus


def load_corpus(data_directory, pickle_name, type='train',
                suffix='challenge',
                triple_size=1):
    """ Loads the WebNLG corpus into or from a pickle.

        Parameters
        ----------
        data_directory : str
            Directory containing all the WebNLG data
        pickle_name : str
            Name of the pickle file.
        type : str
            Indicates which part of the data should be used.
            Can be either train, dev or test.
        suffix : str
            Part of file name indicating which data of WebNLG should
            be used. Can be either 'challenge' (2017 edition) or
            'release' (2020 edition).
        triple_size : int
            Amount of triples per item
    """
    if not os.path.isfile(pickle_name):
        print("Constructing pickle...")
        corpus = []
        for subdir, dirs, files in os.walk(f'{data_directory}'):
            for filename in files:
                filepath = subdir + os.sep + filename

                if filepath.startswith(rf"data\{type}") \
                        and filepath.endswith(f"{suffix}.xml") and\
                        f"{triple_size}triples" in filepath:
                    corpus.extend(extract_information(filepath))

        with open(pickle_name, 'wb') as F:
            pickle.dump(corpus, F)
    else:
        print("Loading pickle...")
        with open(pickle_name, 'rb') as F:
            corpus = pickle.load(F)

    return corpus
