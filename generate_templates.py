import pickle

def clean_names(name):
    # Remove dots if name is not a number:
    # if isinstance(name, str):
    #     name = name.replace('.', '')
    # Replace underscores by spaces:
    name = name.replace('_', ' ')
    # Remove redundant spaces:
    # Er zijn nog spaties voor en na het woord
    " ".join(name.split())
    return name

def generalize_sentence(subj, obj, sentence):
    ''' Replaces the subject and object in a sentence by SUBJ and OBJ to create a template sentence.'''
    newSubject = clean_names(subj)
    newObject = clean_names(obj)
    template = sentence.replace(newSubject, 'SUBJ')
    template = template.replace(newObject, 'OBJ')
    # Remove redundant whitespaces:
    " ".join(template.split())
    return template

def add_values_in_dict(dictionary, key, values):
    """Append multiple values to a key in the given dictionary"""
    if key not in dictionary:
        dictionary[key] = list()
    dictionary[key].extend(values)
    return dictionary

def generate_templates(traincorpus):
    '''Reads a training corpus and generates templates from the examples in it'''
    templates = {}
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
    return templates

def fill_in_templates(templates, testcorpus):
    '''Reads the triples from a testcorpus and generates sentences from them using the templates'''
    for triple in testcorpus[:10]: # Read only first 10 triples (for developmental purposes)
        cleanSubj  = clean_names(triple.subject)
        cleanObj = clean_names(triple.object)
        pred = triple.predicate
        # Test whether there is a template for the current predicate:
        if pred in templates: 
            # For all example sentences of this predicate, fill in the subject and object of the triple in the template:
            for lexical_example in templates[pred]:
                print(triple)
                sentence = lexical_example.replace('SUBJ', cleanSubj)
                sentence = sentence.replace('OBJ', cleanObj)
                print('Generated sentence: ' +sentence)

        else:
            print("No sentence with such predicate in the training corpus")

# Read training corpus:
with open('corpus.pkl', 'rb') as F:
    corpus = pickle.load(F)
# Read test corpus:
with open('devcorpus.pkl', 'rb') as F1:
    devcorpus = pickle.load(F1)
# Generate templates:
templates = generate_templates(corpus)
# Generate sentences from test triples:
fill_in_templates(templates, devcorpus)
