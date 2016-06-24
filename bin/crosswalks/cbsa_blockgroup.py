"""cbsa_blockgroup.py

Extract the crosswalk between cbsa and blockgroups
"""
import os
import csv
import fiona
import collections




#
# Read preliminary data
#

## MSA to counties crosswalk
county_to_msa = {}
with open('data/crosswalks/cbsa_county.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        county = rows[1]
        msa = rows[0]
        county_to_msa[county] = msa

## List of states
states = []
with open('data/states_list.txt') as source:
    line = source.readline()
    while line:
        states.append(line.replace('\n', ''))
        line = source.readline()



#
# Extract cities per MSA by iterating through shapefiles
#
msa_blockgroup = {}
for st in states:
    blockgroups = []
    with fiona.open('data/shp/state/%s/blockgroups.shp'%st, 'r',
            'ESRI Shapefile') as source:
        source_crs = source.crs
        for f in source:
            county = (f['properties']['STATEFP'] +
                    f['properties']['COUNTYFP']).encode('utf8')

            ## Skip rural counties
            try:
                msa = county_to_msa[county.encode('utf8')]

                if msa not in msa_blockgroup:
                    msa_blockgroup[msa] = []
                msa_blockgroup[msa].append(f['properties']['GEOID'])

            except:
                pass 

    



#
# Save the crosswalk 
#
with open('data/crosswalks/cbsa_blockgroup.txt', 'w') as output:
    output.write('MSA FIP\tBLOCKGROUP FIP\n')
    for msa in msa_blockgroup:
        ## Remove duplicates
        bgs = list(set(msa_blockgroup[msa]))
        for bg in bgs:
            output.write('%s\t%s\n'%(msa, bg))
