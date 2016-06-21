"""cbsa_population.py

Script to compute the total number of households there is per CBSA.
"""
import csv


## Import the list of MSA
msa = {}
with open('data/names/cbsa_names.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        msa[rows[0]] = rows[1]


## Get the total number of households per MSA
households = {}
for city in msa:
    households[city]=0
    with open('data/income/cbsa/%s/%s_income_bg.txt'%(city,city), 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            households[city] += sum(map(int, rows[1:]))


## Save the data
with open('data/counts/cbsa_households.txt', 'w') as output:
    output.write('CBSA FIP\tNumber of households\n')
    for city in households:
        output.write('%s\t%s\n'%(city, households[city]))
