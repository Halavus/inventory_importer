import re
from itertools import zip_longest

from .regex import blck
from .regex import inventory_importer as regex


class Importer:

    def __init__(self, data):
        matchblck = re.findall(blck, data)
        for i in matchblck:
            data = data.replace(str(i), "")

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
