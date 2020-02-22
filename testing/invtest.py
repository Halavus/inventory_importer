#!py3

import re
import csv
from itertools import zip_longest
from importer import Importer as importer

with open("inv.txt", "r") as f:
    inputs=f.readlines()

inputs = inputs[0]

parsed_data = importer(inputs)

#print(parsed_data.match)
#print("\n")
print(parsed_data.grouped)

with open('out.csv', 'w') as csvfile:
    outwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in parsed_data.grouped:
        outwriter.writerow(i)
