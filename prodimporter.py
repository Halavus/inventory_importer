#!py3

import re
import csv
from itertools import zip_longest
from modules.regex import prod_importer as regex


class Importer:

    def __init__(self, data):

        # self.data for testing purposes
        self.data = data
        
        # colors, mat, unit(s)
        self.mats = re.findall(regex["mat"], data)

        # completion times prod & queue
        prodtimes = re.findall(regex["prodtime"], data)
        self.prodtimes = [i.replace("<span>in ", "") for i in prodtimes]
        
        # progress prod
        self.progress = re.findall(regex["progress"], data)

        def grouper(n, iterable, fillvalue=None):
            "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
            args = [iter(iterable)] * n
            return list(zip_longest(fillvalue=fillvalue, *args))

        self.grouped_mats = grouper(3, self.mats)
        self.grouped_times = list(zip_longest(
            self.prodtimes, self.progress, fillvalue="queue"))
