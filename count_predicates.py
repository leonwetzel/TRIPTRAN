import xml.etree.ElementTree as ET
import re
from collections import Counter

tree = ET.parse('sportsTeam.xml')
root = tree.getroot()

entries = tree.findall('entries')
tripels = []
predicates = []

print('Entry count:', len(entries))
for ent in entries:
    entry = ent.findall('entry')
    for x in entry:
        triple = x.find('modifiedtripleset').find('mtriple').text
        tripels.append(triple.split(' | '))

#Voeg middelste deel tripel toe aan een lijst
for tripel in tripels:
    print(tripel)
    predicates.append(tripel[1])
print(predicates)
#Print een counter van alle tripels in de lijst
print("Counter voor alle predicates:", Counter(predicates))
