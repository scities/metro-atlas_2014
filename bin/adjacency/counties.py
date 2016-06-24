"""counties.py

Script to compute the adjacency list for the counties in all CBSA.
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
    counties = {}
    with fiona.open('data/shp/cbsa/%s/counties.shp'%city, 'r', 'ESRI Shapefile') as source:
        for f in source:
            counties[f['properties']['GEOIDEC']] = shape(f['geometry'])


    ## Compute adjacency list
    adjacency = {b:[] for b in counties}
    for b0,b1 in itertools.permutations(counties, 2):
        if counties[b1].touches(counties[b0]):
            adjacency[b0].append(b1)

    ## Create necessary directories
    path = "data/adjacency/cbsa/%s/"%city
    if not os.path.exists(path):
        os.makedirs(path)


    ## Save data
    with open('data/adjacency/cbsa/%s/counties.txt'%(city), 'w') as output:
       output.write("COUNTIES FIPS\tNEIGHBOURS FIPS\n")
       for b0 in adjacency:
           output.write("%s"%b0)
           for b1 in adjacency[b0]:
               output.write("\t%s"%b1)
           output.write("\n")
