# TRIPTRAN

This repository contains our work for the final project of the course 
Semantic Web Technology of the MA Information Science program, taught at the
 University of Groningen.
 
The goal of our application is to translate RDF (Resource Description Framework)
 triples to natural language. The **Triple Translator** (also known as **TRIPTRAN**)
 takes a single RDF triple as input and translates it to English.
 
## How to run
 
TRIPTRAN relies on several Python packages - including NLTK -  for its
 functionality. You can easily install these package by running the 
 following command:
 
 ```pip install -r requirements.txt```
 
 After you have succesfully installed all the packes, you first need to
 download the data from the WebNLG repository. You can use the
  `download()` function in `datamanager.py` to achieve this. Simply run
  the following lines of code in your Python console:
  
  ```
>>> from datamanager import download
>>> download()
```

The data is stored in XML files in a newly created directory named _data_.

Once you have succesfully downloaded all the data, you can start using
TRIPTRAN! You can start by running ``main.py``, which trains the TRIPTRAN
model on the training data of WebNLG 2020. The script then uses WebNLG
test data from 2017 to evaluate the translation performances. Simply run
the following line of code in your console:

```python
py -m main
```