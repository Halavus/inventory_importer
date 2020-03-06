#!py3
#

import re
import csv
from itertools import zip_longest
from modules.prodimporter import Importer as importer
from modules.timeparser import timeparser

with open("inv.txt", "r") as f:
    inputs=f.readlines()

inputs = inputs[0]

parsed_data = importer(inputs)
p = parsed_data

#print(parsed_data.match)
#print("\n")
#print(p.grouped_mats)
#print("p.grouped_times:")
#print(p.grouped_times)
#print("\n")
#print(p.formated_prodtimes)
#print("\n")
#print(p.formated_queuetimes)
#print(p.production)
#print(p.queue)

'''
with open('out.csv', 'w') as csvfile:
    outwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in parsed_data.grouped:
        outwriter.writerow(i)
'''
