"""blockgroups.py

Script to compute the adjacency list for the blockgroups in all CBSA.
"""
import os
import csv
import sys
import itertools
import fiona
from shapely.geometry import shape


csv.field_size_limit(sys.maxsize)



#
# Read preliminary data
#

# Names of CBSAs
cbsa = {}
with open('data/misc/cbsa_names.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        cbsa[rows[0]] = rows[1]




#
# Compute the adjacency list
#
for i,city in enumerate(cbsa):
    print "Adjacency %s (%s/%s)"%(cbsa[city], i+1, len(cbsa))

    ## Import blockgroups
    blocks = {}
    with fiona.open('data/shp/cbsa/%s/blockgroups.shp'%city, 'r', 'ESRI Shapefile') as source:
        for f in source:
            blocks[f['properties']['GEOID']] = shape(f['geometry'])


    ## Compute adjacency list
    adjacency = {b:[] for b in blocks}
    for b0,b1 in itertools.permutations(blocks, 2):
        if blocks[b1].touches(blocks[b0]):
            adjacency[b0].append(b1)


    # Data export

    ## Create directory
    export_path = 'data/adjacency/cbsa/%s/'%(city)
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    ## Write data
    with open(export_path + '%s_adjacency_blockgroups.txt'%city, 'w') as output:
       output.write("BLOCKGROUP FIPS\tNEIGHBOURS FIPS\n")
       for b0 in adjacency:
           output.write("%s"%b0)
           for b1 in adjacency[b0]:
               output.write("\t%s"%b1)
           output.write("\n")
