# -*- coding: utf-8 -*-

 import xml.etree.cElementTree as ET
 import re
 import pprint

 OSM_FILE = "/Users/awadbin-jawed/Desktop/Udacity/Files/denver.osm"
 postcode_re = re.compile(r'^\d{5}( [\-]?\d{4})?$')

 def audit_postcode(postcodes,value):
  m = postcode_re.search(value)
  if not m:
    postcodes.add(value)

 def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode" or elem.attrib['k'] == "postal_code")

 def audit(osmfile):
    osm_file = open(osmfile, "r")
    postcodes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
      if elem.tag == "node" or elem.tag == "way":
        for tag in elem.iter("tag"):
          if is_postcode(tag):
              audit_postcode(postcodes,tag.attrib['v'])
 osm_file.close()
 return postcodes

 postcodes = audit(OSM_FILE)
 print "unexpected postcode values:"
 pprint.pprint(postcodes)
