# -*- coding: utf-8 -*-

#import lxml.etree as ET
import lxml.etree as lxml_ET
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pandas as pd
import sys


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons", "Alley",
            "Bridge", "Highway", "Circle", "Terrace", "Way"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_street(osm_file):
    street_types = defaultdict(set)

    context = iter(ET.iterparse(osm_file, events=("start", "end")))
    _, root = next(context) # root.tag == "osm"
    for event, elem in context:
        if event == "start":
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    # if the tag is a street
                    if tag.attrib['k'] == "addr:street":
                        audit_street_type(street_types, tag.attrib['v'])
        if event == "end":
            root.clear()
    return street_types


mapping = { "Av": "Avenue",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Avenue)": "Avenue",
            "Baselin": "Baseline",
            "Blf": "Boulevard",
            "Blvd.": "Boulevard",
            "Cir.": "Circle",
            "Ct": "Court",
            "Dr": "Drive",
            "Hwy": "Highway",
            "Ln": "Lane",
            "Pkwy": "Parkway",
            "Pky": "Parkway",
            "Rd": "Road",
            "Rd.": "Road",
            "St": "Street",
            "St.": "Street",
            "Strret.": "Street",
            "Thornton,": "Thornton"
            }

# update street name according to the mapping dictionary
#def fix_street(osm_file):
def fix_street(st_types):
    # st_types = audit_street(osm_file)
    for st_type, ways in st_types.iteritems():
        for name in ways:
            if st_type in mapping:
                better_name = name.replace(st_type, mapping[st_type])
                print name, "=>", better_name


def audit_city(osm_file):
    city_list = set()

    context = iter(ET.iterparse(osm_file, events=("start", "end")))
    _, root = next(context) # root.tag == "osm"
    for event, elem in context:
        if event == "start":
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == "addr:city" and tag.attrib['v'] != "Denver":
                        city_list.add(tag.attrib['v'])
        if event == "end":
            root.clear()
    return city_list


# zipcode data from http://www.unitedstateszipcodes.org/zip-code-database/
zipcode = pd.read_csv("zipcode.csv")
denver_zipcode = zipcode[(zipcode.primary_city == "Denver") & (zipcode.state == "CO")].zip

denver_zipcode_str = [str(x) for x in list(denver_zipcode)]

def audit_postcode(osm_file):
    code_list = set()
    long_code = 0

    context = iter(ET.iterparse(osm_file, events=("start", "end")))
    _, root = next(context) # root.tag == "osm"
    for event, elem in context:
        if event == "start":
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == "addr:postcode":
                        if len(tag.attrib['v']) > 5:
                            long_code += 1
                            tag.attrib['v'] = tag.attrib['v'].split('-')[0]
                        code_list.add(tag.attrib['v'])
        if event == "end":
            root.clear()
    print 'There are', long_code, 'long post codes.'
    return [code for code in code_list if code not in denver_zipcode_str]


def audit_phone(osm_file):
    phone_list = []

    context = iter(ET.iterparse(osm_file, events=("start", "end")))
    _, root = next(context) # root.tag == "osm"
    for event, elem in context:
        if event == "start":
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if (tag.attrib['k'] == "phone") or (tag.attrib['k'] == "contact:phone"):
                        phone_list.append(tag.attrib['v'])
        if event == "end":
            root.clear()
    return phone_list

# standard format: XXX-XXX-XXXX or 1-XXX-XXX-XXXX
def fix_phone(phone):
    # first deal with strings with no separators
    if re.compile(r'^(\d{3})(\d{3})(\d{4})$').search(phone):
        # XXXXXXXXXX
        return phone[:3] + '-' + phone[3:6] + '-' + phone[6:]
    elif re.compile(r'^1(\d{10})$').search(phone):
       # 1XXXXXXXXXX
        return phone[1:4] + '-' + phone[4:7] + '-' + phone[7:]
    elif re.compile(r'^\+1(\d{10})$').search(phone):
       # +1XXXXXXXXXX
        return phone[2:5] + '-' + phone[5:8] + '-' + phone[8:]
    elif re.compile(r'^\+1\s(\d{10})$').search(phone):
       # +1 XXXXXXXXXX
        return phone[3:6] + '-' + phone[6:9] + '-' + phone[9:]
    elif re.compile(r'^\+1\s(\d{3})\s(\d{3})(\d{4})$').search(phone):
        # +1 XXX XXXXXXX
        return phone[3:6] + '-' + phone[7:10]+ '-' + phone[10:]
    elif re.compile(r'^01\s(\d{3})\s(\d{3})\s(\d{4})$').search(phone):
        # 01 XXX XXX XXXX
        # return phone[3:].replace(' ', '-')
        return phone[3:6] + '-' + phone[7:10]+ '-' + phone[11:]

    # if more than one number in the string, split to a list
    elif phone.find(';') > 0:
        for ph in phone.split(';'):
            fix_phone(ph)

    # if there are 3 or 4 digital parts, concatenate with dash
    # ????
    elif len(re.findall('\d+', phone)) > 2:
        return '-'.join(re.findall('\d+', phone))

    else:
        print phone


def fix_phones(phone_list):
    for phone in phone_list:
        fix_phone(phone)


# validate the XML OSM file via schema
def validator(osm_file, schema):
    xmlschema_doc = lxml_ET.parse(schema)
    xmlschema = lxml_ET.XMLSchema(xmlschema_doc)

    for event, element in lxml_ET.iterparse(osm_file, events=("end", )):
        if not xmlschema.validate(element):
            print xmlschema.error_log, element.attrib
        element.clear()
        if element.tag in ["node", "way", "relation"]:
            for ancestor in element.xpath("ancestor-or-self::*"):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]

###
def run():
    OSM_FILE = "./denver-boulder_colorado.osm"
    with open("audit.txt", 'wb') as output:
        print("=== audit_street() ===")
        output.write("=== audit_street() ===\n")
        street_types = audit_street(OSM_FILE)
        output.write(str(street_types))

        print("=== fix_street() ===")
        output.write("\n=== fix_street() ===\n")
        sys.stdout = output
        fix_street(street_types)
        sys.stdout = sys.__stdout__

        print("=== audit_city() ===")
        output.write("=== audit_city() ===\n")
         Note: which city the values should be compared with?
        output.write(str(audit_city(OSM_FILE)))

        print("=== audit_postcode() ===")
        output.write("\n=== audit_postcode() ===\n")
        sys.stdout = output
        output.write(str(audit_postcode(OSM_FILE)))
        sys.stdout = sys.__stdout__

        print("=== audit_phone() ===")
        output.write("\n=== audit_phone() ===\n")
        phone_list = audit_phone(OSM_FILE)
        output.write(str(phone_list))

        print("=== fix_phones() ===")
        output.write("\n=== fix_phones() ===\n")
         Note: fix_phone() is partially broken
        sys.stdout = output
        fix_phones(phone_list)
        sys.stdout = sys.__stdout__

    with open("audit_xsd.txt", 'wb') as output:
        print("=== validator() ===")
        output.write("=== validator() ===\n")
        sys.stdout = output
        #SAMPLE_FILE = OSM_FILE[0:-4] + '_sample.osm'
        # validator(SAMPLE_FILE, 'schema.xsd')
        validator(OSM_FILE, 'schema.xsd')
        sys.stdout = sys.__stdout__
#run()
###
