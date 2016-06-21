"""income_tract.py

Extract the household income per tract for each cbsa, using the
crosswalk between CBSA and Tracts.
"""
import csv
import os


# Income file comprises estimates and margin of error
income_rows = [5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35]





#
# Import data
#

## CBSA to tract 
tr_to_cbsa = {}
with open('data/crosswalks/cbsa_tract.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        tr_to_cbsa[rows[1]] = rows[0]

## Income data at blockgroup level
incomes = {}
with open('data/income/us/ACS_14_5YR_B19001.csv', 'r') as source:
    reader = csv.reader(source, delimiter=',')
    reader.next()
    reader.next()
    for rows in reader:
        incomes[rows[1]] = [int(rows[i]) for i in income_rows]



#
# Group by CBSA
#
incomes_cbsa = {}
in_cbsa = 0
out_cbsa = 0
for bg in incomes:
    tr = bg[:11]
    if tr in tr_to_cbsa:
        in_cbsa += 1
        cbsa = tr_to_cbsa[tr]
        if cbsa not in incomes_cbsa:
            incomes_cbsa[cbsa] = {}
        if tr not in incomes_cbsa[cbsa]:
            incomes_cbsa[cbsa][tr] = [0 for i in income_rows]

        ## Add value from blockgroup
        for i,val in enumerate(incomes[bg]):
            incomes_cbsa[cbsa][tr][i] += val

    else:
        out_cbsa += 1

print '%s tracts are inside CBSAs'%in_cbsa
print '%s tracts are outside CBSAs'%out_cbsa



#
# Save the data
#
for cbsa in incomes_cbsa:
    ## Create dir if needed
    if not os.path.isdir('data/income/cbsa/%s'%cbsa):
        os.mkdir('data/income/cbsa/%s'%cbsa)
    
    ## Save
    with open('data/income/cbsa/%s/%s_income_tract.txt'%(cbsa, cbsa), 'w') as output:
        output.write("TRACT FIP\tLess than $10000\t$10000-$14999\t$15000-$19999\t$20000-$24999\t$25000-$29999\t$30000-$34999\t$35000-$39999\t$40000-$44999\t$45000-$49999\t$50000-$59999\t$60000-$74999\t$75000-$99999\t$100000-$124999\t$125000-$149999\t$150000-$199999\t$200000 or more\n")
        for tr in incomes_cbsa[cbsa]:
            output.write(str(tr)+'\t')
            output.write('\t'.join(map(str, incomes_cbsa[cbsa][tr])))
            output.write('\n')
