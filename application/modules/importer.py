import re
import csv
from itertools import zip_longest

from .regex import inventory_importer as regex


class Importer:

    def __init__(self, data):
        
        self.match = re.findall(regex, data)

        def grouper(n, iterable, fillvalue=None):
            "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
            args = [iter(iterable)] * n
            return list(zip_longest(fillvalue=fillvalue, *args))

        self.grouped = grouper(3, self.match)
        
        self.nodata=False

        if self.grouped==[]:
            self.nodata=True
