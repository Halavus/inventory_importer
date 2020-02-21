#!py3

import re
import csv
from itertools import zip_longest

class Importer:

    def __init__(self, data):
        
        #self.data for testing purposes
        self.data = data

        matches = ["H2O","HE3","NV1","NV2","[A-Z]+"]
        startmat = '(?<=<span class="MaterialIcon__ticker___1qLDE5z">)'
        startamount = ('(?<=<div class="MaterialIcon__indicator___2QhPuFO'
                       ' MaterialIcon__type-very-small___kE8NFjh">)')
        end = "(?=</)"

        regexcolor = ('background: linear-gradient\(135deg,'
                ' rgb\(\d+, \d+, \d+\),'
                ' rgb\(\d+, \d+, \d+\)\); color: rgb\(\d+, \d+, \d+\);'
                ' font-size: 15.84px')
        
        def regexmaker(
                matches=matches, 
                startmat=startmat, 
                startamount=startamount, 
                end="", 
                separator="|",
                regexcolor=regexcolor):

            s=""
            for i in matches:
                #creates the regex string with correct syntax for every match
                s=s+startmat+i+end+separator

            #removes the last separator
            s=regexcolor+separator+s+startamount+"\d+"
            return s

        self.regex=regexmaker()
       
        self.match = re.findall(self.regex, data)

        def grouper(n, iterable, fillvalue=None):
            "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
            args = [iter(iterable)] * n
            return list(zip_longest(fillvalue=fillvalue, *args))

        self.grouped = grouper(3, self.match)
