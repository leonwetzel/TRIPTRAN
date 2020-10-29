import pickle
# 1._FC_Köln | capacity | 50000
# 1. FC Köln has 50000 members.
# F.C. Koln have 50000 members.

# 1._FC_Köln | season | 2014
# 1 FC Köln played in the 2014 season.

with open('corpus.pkl', 'rb') as F:
    corpus = pickle.load(F)

def generalize(subj, pred, obj, sentence):
    newSubject = subj.replace('.', '')
    newSubject = newSubject.replace('_', ' ')
    newObject = obj.replace('_', ' ')
    template = sentence.replace(newSubject, ' SUBJ ')
    template = template.replace(newObject, ' OBJ ')
    output = (pred, template)
    return output

def add_values_in_dict(dictionary, key, values):
    """Append multiple values to a key in the given dictionary"""
    if key not in dictionary:
        dictionary[key] = list()
    dictionary[key].extend(values)
    return dictionary

def generate_templates():
    templates = {}
    # read corpus
    with open('corpus.pkl', 'rb') as F:
        corpus = pickle.load(F)

    # generate templates from tripels and sentences in corpus
    for triple in corpus[:100]:
        subj = triple.subject
        #print("subject: " + subj)
        obj = triple.object
        #print("object: " + obj)
        pred = triple.predicate
        lexical_examples = triple.lexical_examples
        for i in range(len(lexical_examples)):
            #print(lexical_examples[i])
            sentence = lexical_examples[i]
            pred, template = generalize(subj, pred, obj, sentence)
            #print(template)
            templates = add_values_in_dict(templates, pred, [template])
        print(templates)

generate_templates()