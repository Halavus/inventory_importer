#!py3

import re
import csv
from itertools import zip_longest
from prodimporter import Importer as importer

with open("testing/prod.txt", "r") as f:
    inputs=f.readlines()

inputs = inputs[0]

parsed_data = importer(inputs)
p = parsed_data

#print(parsed_data.match)
#print("\n")
print(p.grouped_mats)
#print(p.grouped_times)

'''
with open('out.csv', 'w') as csvfile:
    outwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in parsed_data.grouped:
        outwriter.writerow(i)
'''
