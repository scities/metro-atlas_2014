"""county.py

Script to compute the surface area of counties per CBSA.
"""
import os
import csv
from functools import partial
import fiona
import pyproj
from shapely.geometry import shape
from shapely.ops import transform



#
# Read preliminary data
#

# Projection used to project polygons
project = partial(
    pyproj.transform,
    pyproj.Proj(init='epsg:4326'), # source coordinate system
    pyproj.Proj(init='epsg:3575')) # destination coordinate system


# Import list of MSA
cbsa = {}
with open('data/misc/cbsa_names.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        cbsa[rows[0]] = rows[1]



#
# Compute the surface area of counties and save
#
for i,city in enumerate(cbsa):
    print "Surface area of counties for %s (%s/%s)"%(cbsa[city], i+1, len(cbsa))

    ## Import blockgroups' surface area
    counties = {}
    with fiona.open('data/shp/cbsa/%s/counties.shp'%city, 'r', 'ESRI Shapefile') as source:
        for f in source:
            counties[f['properties']['GEOIDEC']] = transform(project,
                                                        shape(f['geometry'])).area

    ## Create destination folder
    path = 'data/surface_area/cbsa/%s'%city
    if not os.path.exists(path):
        os.makedirs(path)

    ## Save data
    with open(path+'/counties.txt', 'w') as output:
        output.write('COUNTY FIPS\tSurface area (m^2)\n')
        for bg in counties:
            output.write('%s\t%s\n'%(bg, counties[bg]))
