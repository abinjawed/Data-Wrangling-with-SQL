# -*- coding: utf-8 -*-

"""
Your task is to use the iterative parsing to process the map file and find out
not only what tags are there, but also how many, to get the feeling on how much
of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the
tagname as the key and number of times this tag can be encountered in the map
as value.
"""
import xml.etree.cElementTree as ET
from collections import defaultdict

# return a dictionary of top level tags and their counts
def count_tags(filename):
    tags_dict = defaultdict(int)

    # iteratively parse the file
    context = iter(ET.iterparse(filename, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end':
            tags_dict[elem.tag] += 1
            root.clear()
    
    return tags_dict

###
def run():
    OSM_FILE = "./denver-boulder_colorado.osm"
    with open("mapparser.txt", 'wb') as output:
        print("=== count_tags() ===")
        output.write("=== count_tags() ===\n")
        output.write(str(count_tags(OSM_FILE)))
#run()
###