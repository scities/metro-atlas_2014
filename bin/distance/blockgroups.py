#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Compute, within each metropolitan area, the distance between block groups
projection used: Lambert Equal Area

:date: 29/01/2015
"""
from __future__ import division
import sys
import os
import itertools as it
import numpy as np
import csv
import fiona
from shapely.geometry import shape
import pyproj
from scipy.spatial import distance


csv.field_size_limit(sys.maxsize)

def LatLonToMeters(lat, lon ):
	""""Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913
	We Use Lambert Azimuthal Equal Area projection.
	"""

	proj = pyproj.Proj(proj='laea')
	mx,my = proj(lon,lat)

	return mx, my


def Distance(a,b):
	"Computes the euclidean distance between point a and points b"
	d = math.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )
	return d




#
# Import data
#

## List of cities
cbsa = {}
with open("data/misc/cbsa_names.txt","r") as inputfile:
    reader = csv.reader(inputfile,delimiter="\t")
    reader.next()
    for rows in reader:
        cbsa[rows[0]] = rows[1]




#
# Compute the distances for all cities
#
for i, city in enumerate(cbsa):
    print "Compute distance for %s (%s/%s)"%(cbsa[city], i+1, len(cbsa))

    ## Import the blockgroups' centroids
    blockgroups = {}
    with fiona.open('data/shp/cbsa/%s/blockgroups.shp'%city, 'r', 'ESRI Shapefile') as source:
        for f in source:
            bg = shape(f['geometry'])
            blockgroups[f['properties']['GEOID']] = LatLonToMeters(bg.centroid.y, bg.centroid.x) 


    ## Compute distances
    crosswalk = {b:i for i,b in enumerate(blockgroups)}
    positions = np.array([[blockgroups[b][0], blockgroups[b][1]] for b in blockgroups])

    distances = distance.cdist(positions, positions, 'euclidean')

    ## Write the distances
    # Create directory
    if not os.path.exists('data/distance/cbsa/%s'%city):
        os.makedirs('data/distance/cbsa/%s'%city)

    with open('data/distance/cbsa/%s/blockgroups.txt'%city, 'w') as output:
        output.write("blockgroup 1\tblockgroup 2\tdistance (m)\n")
        for b0, b1 in it.product(crosswalk, repeat=2):
            output.write("%s\t%s\t%s\n"%(b0, 
                                         b1,
                                         distances[crosswalk[b0]][crosswalk[b1]]))

