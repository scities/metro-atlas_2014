"""tracts.py

Script to compute the adjacency list for the tracts in all CBSA.
"""
import os
import csv
import sys
import itertools
import fiona
from shapely.geometry import shape


csv.field_size_limit(sys.maxsize)


#
# Import list of cities 
#
cbsa = {}
with open('data/names/cbsa_names.txt', 'r') as source:
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
    with fiona.open('data/shp/cbsa/%s/tracts.shp'%city, 'r', 'ESRI Shapefile') as source:
        for f in source:
            blocks[f['properties']['GEOID']] = shape(f['geometry'])


    ## Compute adjacency list
    adjacency = {b:[] for b in blocks}
    for b0,b1 in itertools.permutations(blocks, 2):
        if blocks[b1].touches(blocks[b0]):
            adjacency[b0].append(b1)

    ## Create necessary directories
    path = "data/adjacency/cbsa/%s/"%city
    if not os.path.exists(path):
        os.makedirs(path)


    ## Save data
    with open('data/adjacency/cbsa/%s/%s_adjacency_tracts.txt'%(city, city), 'w') as output:
       output.write("TRACTS FIPS\tNEIGHBOURS FIPS\n")
       for b0 in adjacency:
           output.write("%s"%b0)
           for b1 in adjacency[b0]:
               output.write("\t%s"%b1)
           output.write("\n")
