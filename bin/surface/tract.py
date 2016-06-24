""" tracts.py

Script to compute the surface area of tracts per CBSA.
"""
import os
import csv
from functools import partial
import fiona
import pyproj
from shapely.geometry import shape
from shapely.ops import transform




#
# Preparation
#

# Projection used to project polygons
project = partial(
    pyproj.transform,
    pyproj.Proj(init='epsg:4326'), # source coordinate system
    pyproj.Proj(init='epsg:3575')) # destination coordinate system


# Import list of CBSA
cbsa = {}
with open('data/misc/cbsa_names.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        cbsa[rows[0]] = rows[1]


for i,city in enumerate(cbsa):
    print "Surface area of tracts for %s (%s/%s)"%(cbsa[city], i+1, len(cbsa))

    ## Import tracts' surface area
    tracts = {}
    with fiona.open('data/shp/cbsa/%s/tracts.shp'%city, 'r', 'ESRI Shapefile') as source:
        for f in source:
            tracts[f['properties']['GEOID']] = transform(project,
                                                        shape(f['geometry'])).area

    ## Create destination folder
    path = 'data/surface_area/cbsa/%s'%city
    if not os.path.exists(path):
        os.makedirs(path)

    ## Save data
    with open(path+'/tracts.txt', 'w') as output:
        output.write('TRACT FIPS\tSurface area (m^2)\n')
        for tr in tracts:
            output.write('%s\t%s\n'%(tr, tracts[tr]))
