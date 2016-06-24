"""cbsa_county.py

Output one shapefile per MSA containing all the counties it contains.
"""
import os
import csv
import fiona





#
# Read preliminary data
#

# Import CBSA to counties crosswalk 
cbsa_to_ct = {}
with open('data/crosswalks/cbsa_county.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        cbsa = rows[0]
        ct = rows[1]
        if cbsa not in cbsa_to_ct:
            cbsa_to_ct[cbsa] = []
        cbsa_to_ct[cbsa].append(ct)


# Import counties shapefiles
all_ct = {}
with fiona.open('data/shp/us/counties.shp', 'r',
        'ESRI Shapefile') as source:
    source_crs = source.crs
    for f in source:
        all_ct[f['properties']['GEOIDEC']] = f['geometry']


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
for cbsa in cbsa_to_ct:
    print 'Build shapefiles with counties for %s'%names[cbsa]

    ## counties within cbsa
    cbsa_ct = {ct: all_ct[ct] for ct in cbsa_to_ct[cbsa]}

    ## Save
    if not os.path.isdir('data/shp/cbsa/%s'%cbsa):
        os.makedirs('data/shp/cbsa/%s'%cbsa)

    schema = {'geometry': 'Polygon',
              'properties': {'GEOIDEC': 'str'}}
    with fiona.open('data/shp/cbsa/%s/counties.shp'%cbsa, 'w', 
            'ESRI Shapefile',
            crs = source_crs,
            schema = schema) as output:
        for ct in cbsa_ct:
            rec = {'geometry':cbsa_ct[ct], 'properties':{'GEOIDEC':ct}}
            output.write(rec)
