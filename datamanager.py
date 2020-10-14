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
            zip_ref.extractall("data")

        file.close()
        os.remove(file_name)


if __name__ == '__main__':
    main()
