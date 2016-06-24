"""cbsa_blockgroup.py

Output one shapefile per MSA containing all the blockgroups it contains.
"""
import os
import csv
import fiona



#
# Read preliminary data
#

# Crosswalk between blockgroups and CBSAs
cbsa_to_bg = {}
with open('data/crosswalks/cbsa_blockgroup.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        cbsa = rows[0]
        bg = rows[1]
        if cbsa not in cbsa_to_bg:
            cbsa_to_bg[cbsa] = []
        cbsa_to_bg[cbsa].append(bg)

# Names of CBSAs
names = {}
with open('data/misc/cbsa_names.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        names[rows[0]] = rows[1]



#
# Perform the extraction
#
for cbsa in cbsa_to_bg:
    print 'Build shapefile with blockgroups for %s'%names[cbsa]
    states = list(set([b[:2] for b in cbsa_to_bg[cbsa]]))

    ## Get all blockgroups
    all_bg = {}
    for st in states:
        with fiona.open('data/shp/state/%s/blockgroups.shp'%st, 'r',
                'ESRI Shapefile') as source:
            source_crs = source.crs
            for f in source:
                all_bg[f['properties']['GEOID']] = f['geometry']

    ## blockgroups within cbsa
    cbsa_bg = {bg: all_bg[bg] for bg in cbsa_to_bg[cbsa]}

    ## Save
    if not os.path.isdir('data/shp/cbsa/%s'%cbsa):
        os.makedirs('data/shp/cbsa/%s'%cbsa)

    schema = {'geometry': 'Polygon',
              'properties': {'GEOID': 'str'}}
    with fiona.open('data/shp/cbsa/%s/blockgroups.shp'%cbsa, 'w', 
            'ESRI Shapefile',
            crs = source_crs,
            schema = schema) as output:
        for bg in cbsa_bg:
            rec = {'geometry':cbsa_bg[bg], 'properties':{'GEOID':bg}}
            output.write(rec)
