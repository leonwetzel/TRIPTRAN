import xml.etree.ElementTree as ET
import re

tree = ET.parse('sportsTeam.xml')
root = tree.getroot()

entries = tree.findall('entries')
print('Entry count:', len(entries))
for ent in entries:
    entry = ent.findall('entry')
    for x in entry:
        triple = x.find('modifiedtripleset').find('mtriple').text
        print('triple: ', triple)
        newTriple = triple.split(' | ')
        print(newTriple)

