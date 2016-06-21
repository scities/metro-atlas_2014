"""cbsa_tract.py

Extract the crosswalk between cbsa and tracts.
"""
import os
import csv
import collections


#
# Import data
#

## MSA to counties crosswalk
# county_to_cbsa = {county: {cbsa: [cousub ids]}
county_to_cbsa = {}
with open('data/crosswalks/cbsa_county.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        county = rows[1]
        cbsa = rows[0]
        county_to_cbsa[county] = cbsa


## Income data at block-group level
incomes = {}
with open('data/income/us/ACS_14_5YR_B19001.csv', 'r') as source:
    reader = csv.reader(source, delimiter=',')
    reader.next()
    reader.next()
    for rows in reader:
        incomes[rows[1]] = [int(i) for i in rows[7:]]




#
# Group by CBSA
#
cbsa_tract = {}
for bg in incomes:
    county = bg[:5]
    tract = bg[:11]
    if county in county_to_cbsa:
        cbsa = county_to_cbsa[county]
        if cbsa not in cbsa_tract:
            cbsa_tract[cbsa] = []
        cbsa_tract[cbsa].append(tract)




#
# Save the crosswalk 
#
with open('data/crosswalks/cbsa_tract.txt', 'w') as output:
    output.write('MSA FIP\tTRACT FIP\n')
    for cbsa in cbsa_tract:
        ## Remove duplicates
        tracts = list(set(cbsa_tract[cbsa]))
        for tr in tracts:
            output.write('%s\t%s\n'%(cbsa, tr))
