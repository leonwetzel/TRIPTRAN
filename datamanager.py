import os
import shutil
import requests
import zipfile

URLS = [
    {"year": 2017,
     "url": "https://gitlab.com/shimorina/webnlg-dataset/-/archive/master/webnlg-dataset-master.zip?path=webnlg_challenge_2017"},
    {"year": 2020,
     "url": "https://gitlab.com/shimorina/webnlg-dataset/-/archive/master/webnlg-dataset-master.zip?path=release_v2.1/xml"}
]


def main():
    """
    Script for downloading all the relevant WebNLG files,
    used for testing, development and training.
    :return:
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
            zip_ref.extractall(path='data', members=get_members(zip_ref))

        file.close()
        os.remove(file_name)


def get_members(zip):
    """
    Extracts the files from a given zip file.
    Stolen from https://stackoverflow.com/questions/8689938/extract-files-from-zip-without-keep-the-top-level-folder-with-python-zipfile
    :param zip:
    :return:
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


if __name__ == '__main__':
    main()
