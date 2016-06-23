"""cbsa_tract.py

Output one shapefile per MSA containing all the tracts it contains.
"""
import os
import csv
import fiona


#
# Import MSA to tracts crosswalk 
#
cbsa_to_tr = {}
with open('data/crosswalks/cbsa_tract.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        cbsa = rows[0]
        tr = rows[1]
        if cbsa not in cbsa_to_tr:
            cbsa_to_tr[cbsa] = []
        cbsa_to_tr[cbsa].append(tr)


#
# Perform the extraction
#
for cbsa in cbsa_to_tr:
    states = list(set([b[:2] for b in cbsa_to_tr[cbsa]]))

    ## Get all tracts
    all_tr = {}
    for st in states:
        with fiona.open('data/shp/state/%s/tracts.shp'%st, 'r',
                'ESRI Shapefile') as source:
            source_crs = source.crs
            for f in source:
                all_tr[f['properties']['GEOID']] = f['geometry']

    ## tracts within cbsa
    cbsa_tr = {tr: all_tr[tr] for tr in cbsa_to_tr[cbsa]}

    ## Save
    if not os.path.isdir('data/shp/cbsa/%s'%cbsa):
        os.makedirs('data/shp/cbsa/%s'%cbsa)

    schema = {'geometry': 'Polygon',
              'properties': {'GEOID': 'str'}}
    with fiona.open('data/shp/cbsa/%s/tracts.shp'%cbsa, 'w', 
            'ESRI Shapefile',
            crs = source_crs,
            schema = schema) as output:
        for tr in cbsa_tr:
            rec = {'geometry':cbsa_tr[tr], 'properties':{'GEOID':tr}}
            output.write(rec)
