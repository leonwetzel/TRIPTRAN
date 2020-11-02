import pickle
import re

def clean_predicate(pred):
    '''Split the predicate by upper cases, make everything lower case and convert to list '''
    predicate = " ".join(pred.split())
    predicate = re.sub(r'([A-Z])', r' \1', predicate)
    predicate = predicate.lower()
    # convert to a list:
    predicate = predicate.split(" ")
    return predicate

def noun_rule(triple):
    sentence = "The " + triple.predicate + " of " + triple.subject + " is " + triple.object
    sentence = " ".join(sentence.split())
    return sentence

def verb_rule(triple):
    sentence = triple.subject +  " is " +  triple.predicate + triple.object
    sentence = " ".join(sentence.split())
    return sentence

def generate_rule_based_sentence(triple):
    pred = clean_predicate(triple.predicate)
    if get_pos_tag(pred) == 'noun':
       sentence = noun_rule(triple)
    elif get_pos_tag(pred) == 'verb':
        sentence = verb_rule(triple)
    return sentence

def clean_names(name):
    # Replace underscores by spaces:
    name = name.replace('_', ' ')
    # Remove redundant spaces:
    name = " ".join(name.split())
    return name

def clean_sentence(sentence):
    # If there is a space in front of a dot, remove it:
    sentence = sentence.replace(" .", ".")
    # TODO: In de output kijken of er nog meer nodig is.
    return sentence

def generalize_sentence(subj, obj, sentence):
    ''' Replaces the subject and object in a sentence by SUBJ and OBJ to create a template sentence.'''
    newSubject = clean_names(subj)
    newObject = clean_names(obj)
    template = sentence.replace(newSubject, ' SUBJ ')
    template = template.replace(newObject, ' OBJ ')
    # Remove redundant whitespaces:
    template = " ".join(template.split())
    return template

def add_values_in_dict(dictionary, key, values):
    """Append multiple values to a key in the given dictionary"""
    if key not in dictionary:
        dictionary[key] = list()
    dictionary[key].extend(values)
    return dictionary

def most_frequent(List): 
    '''Returns the most frequent item of a list. If multiple occur the same number of times, it returns the last of those.'''
    return max(set(List), key = List.count) 
  

def generate_templates(traincorpus):
    '''Reads a training corpus and generates templates from the examples in it'''
    templates = {}
    singleTemplates = {}
    for triple in traincorpus:
        subj = triple.subject
        obj = triple.object
        pred = triple.predicate
        lexical_examples = triple.lexical_examples
        # Read all sentences in the lexical examples and replace the subjects and objects by placeholders
        for i in range(len(lexical_examples)):
            sentence = lexical_examples[i]
            template = generalize_sentence(subj, obj, sentence)
            # Only add the template to the dictionary if subject and object are properly replaced.
            if 'SUBJ' in template and 'OBJ' in template: 
                templates = add_values_in_dict(templates, pred, [template])
    # Find most frequent template:
    for pred in templates:
        singleTemplates[pred] = most_frequent(templates[pred])
    # Remove duplicates from templates:
    for pred in templates:
        templates[pred] = list(set(templates[pred]))
    return templates, singleTemplates

def fill_in_all_templates(templates, testcorpus):
    '''Reads the triples from a testcorpus and generates multiple sentences from them using all templates'''
    for triple in testcorpus[:10]: # Read only first 10 triples (for developmental purposes)
        cleanSubj  = clean_names(triple.subject)
        cleanObj = clean_names(triple.object)
        pred = triple.predicate
        print(triple)
        # Test whether there is a template for the current predicate:
        if pred in templates: 
            # For all example sentences of this predicate, fill in the subject and object of the triple in the template:
            for lexical_example in templates[pred]:
                sentence = lexical_example.replace('SUBJ', cleanSubj)
                sentence = sentence.replace('OBJ', cleanObj)
                sentence = clean_sentence(sentence)
                print('Generated sentence: ' +sentence)
        else:
            print("No sentence with such predicate in the training corpus")

def fill_in_most_frequent_template(singleTemplates, testcorpus):
    '''Reads the triples from a testcorpus and generates one sentence for each triple, from the most frequent template in the training sentences'''
    notFound = []
    for triple in testcorpus: # Read only first 10 triples (for developmental purposes)
        cleanSubj  = clean_names(triple.subject)
        cleanObj = clean_names(triple.object)
        pred = triple.predicate
        print(triple)
        # Test whether there is a template for the current predicate:
        if pred in singleTemplates: 
            # Fill in the subject and object of the triple in the template sentence:
            sentence = singleTemplates[pred].replace('SUBJ', cleanSubj)
            sentence = sentence.replace('OBJ', cleanObj)
            sentence = clean_sentence(sentence)
            #print('Generated sentence: ' +sentence)
        else:
            notFound.append(pred)
            sentence = generate_rule_based_sentence(triple)
            print(sentence)
            print("No sentence with such predicate in the training corpus")
    return notFound

# Read training corpus:
with open('corpus.pkl', 'rb') as F:
    corpus = pickle.load(F)
# Read test corpus:
with open('devcorpus.pkl', 'rb') as F1:
    devcorpus = pickle.load(F1)
    
# Generate templates:
templates, singleTemplates = generate_templates(corpus)

# Generate sentences from test triples (choose whether you want all sentences or only the most frequent one):
#fill_in_all_templates(templates, devcorpus)
notFound = fill_in_most_frequent_template(singleTemplates, devcorpus)
print("Not found: ")
print(notFound)
