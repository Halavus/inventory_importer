import re
from itertools import zip_longest

from .regex import num, cleaner
from .regex import inventory_importer as regex


class Importer():

    def __init__(self, data, debug=False):
        # Cleanup job for BLCK and SHPT items
        # 
        # TODO: find more elegant way to achieve this cleaning
        # - concatenate tuples?
        # - do not output tuples? 

        matchnum = re.findall(num, data)
        if debug:
            print(matchnum)
        self.matchnum = matchnum

        for i in matchnum:
            for w in i:
                # matchnum outputs a list of tuple. ('', 'match'). Do nothing with the empty string.
                if w:
                    if debug:
                        print(w)
                    blsh = cleaner(w)
                    if debug:
                        print(blsh)
                    matchblsh = re.findall(blsh, data)
                    if debug:
                        print(matchblsh)
                    data = data.replace(matchblsh[0], "")
        
        # Match the cleaned data

        self.match = re.findall(regex, data)

        def grouper(n, iterable, fillvalue=None):
            '''Returns a tuple
            example: grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx'''
            args = [iter(iterable)] * n
            return list(zip_longest(fillvalue=fillvalue, *args))

        self.grouped = grouper(3, self.match)

        self.nodata = False

        if self.grouped == []:
            self.nodata = True
