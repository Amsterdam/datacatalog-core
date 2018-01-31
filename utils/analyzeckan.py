import json
import pathlib
import pprint
import re

import jsonpointer

PACKAGE_DIR = 'ckandata'

packages = []
for filename in pathlib.Path(PACKAGE_DIR).glob('*.json'):
    with open(filename) as fh:
        packages.append(json.load(fh))


attributes = {}
resource_attributes = {}
licenses = {}
frequencies = set()
gebiedseenheid = set()
organizations = {}
themes = {}
temporal = set()
tijdseenheid = set()
for p in packages:
    for a in p:
        if a not in attributes:
            attributes[a] = 1
        else:
            attributes[a] = attributes[a] + 1
    for r in p['resources']:
        for a in r:
            if a not in resource_attributes:
                resource_attributes[a] = 1
            else:
                resource_attributes[a] = resource_attributes[a] + 1

    v = p.get('license_id')
    if v is not None:
        if v not in licenses:
            licenses[v] = set()
        licenses[v].add(p['license_title'])

    v = p.get('gebiedseenheid')
    if v is not None:
        gebiedseenheid.add(v)

    v = p.get('frequency')
    if v is not None:
        frequencies.add(v)

    for v in p.get('groups'):
        if v['name'] not in themes:
            assert v['title'] == v['display_name']
            o = {
                '@id': f"theme:{v['name']}",
                '@type': 'skos:Concept',
                'skos:prefLabel': v['title']
            }
            themes[v['name']] = o

    v = p.get('organization')
    if v is not None and v['name'] not in organizations:
        o = {
            '@id': f"org:{v['name']}",
            'foaf:name': v['title'],
            'foaf:depiction': v['image_url'],
            'skos:note': v['description']
        }
        match = re.search(r"href='([^']+)'", v['description'])
        if match:
            o['foaf:homepage'] = match[1]
        organizations[v['name']] = o

    v = p.get('temporal')
    if v is not None:
        temporal.add(v)

    v = p.get('tijdseenheid')
    if v is not None:
        tijdseenheid.add(v)

print("Attribute occurrence:")
pprint.pprint(attributes)

print("\nResource attribute occurrence:")
pprint.pprint(resource_attributes)

print("\nLicenses:")
pprint.pprint(licenses)

print("\nFrequencies:")
pprint.pprint(frequencies)

print("\nThemes:")
pprint.pprint(themes)

print("\nOrganizations:")
print(repr(organizations))

print("\nGebiedseenheid:")
pprint.pprint(gebiedseenheid)

print("\nTemporal:")
pprint.pprint(temporal)

print("\nTijdseenheid:")
pprint.pprint(tijdseenheid)

# print("\nmetadata_created:")
# pprint.pprint([
#     p['metadata_created'] for p in packages
# ])

