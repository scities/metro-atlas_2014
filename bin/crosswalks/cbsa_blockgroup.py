"""cbsa_blockgroup.py

Extract the crosswalk between cbsa and blockgroups
"""
import os
import csv
import collections


#
# Import data
#

## MSA to counties crosswalk
# county_to_msa = {county: {msa: [cousub ids]}
county_to_msa = {}
with open('data/crosswalks/cbsa_county.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        county = rows[1]
        msa = rows[0]
        county_to_msa[county] = msa


## Income data at block-group level
incomes = {}
with open('data/income/us/ACS_14_5YR_B19001.csv', 'r') as source:
    reader = csv.reader(source, delimiter=',')
    reader.next()
    reader.next()
    for rows in reader:
        incomes[rows[1]] = [int(i) for i in rows[7:]]




#
# Group by MSA
#
msa_blockgroup = {}
for bg in incomes:
    county = bg[:5]
    if county in county_to_msa:
        msa = county_to_msa[county]
        if msa not in msa_blockgroup:
            msa_blockgroup[msa] = []
        msa_blockgroup[msa].append(bg)




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
