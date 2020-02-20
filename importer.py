import re
import csv
from itertools import zip_longest

'''
with open("/home/walo/code_the_web/python/PrUn/inv.txt", "r") as f:
    data=f.readlines()
'''

class Importer:

    def __init__(self, data):

        self.d = data

        matches = ["[A-Z]+","H2O","HE3","NV1","NV2","\d+"]
        start = "(?<=\">)"
        end = "(?=</)"

        def regexmaker(matches, start, end, separator="|"):
            s=""
            for i in matches:
                s=s+start+i+end+separator
            s = s[:-1]
            return s

        self.regex=regexmaker(matches, start, end)

        self.match = re.findall(self.regex, self.d)

        #print match

        def grouper(n, iterable, fillvalue=None):
            "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
            args = [iter(iterable)] * n
            return list(zip_longest(fillvalue=fillvalue, *args))

        self.grouped = grouper(2, self.match)

    '''
        with open('out.csv', 'wb') as csvfile:
            outwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in grouped:
                outwriter.writerow(i)

    '''
