#!py3

import re
import csv
from itertools import zip_longest


class Importer:

    def __init__(self, data):

        # self.data for testing purposes
        self.data = data

        matches_mat = ["H2O", "HE3", "NV1", "NV2", "[A-Z]+"]

        start_mat = '(?<=<span class="MaterialIcon__ticker___1qLDE5z">)'

        match_prodtime = '(?<=span><span>).*?(?=<\/span>)'

        match_progress = '(?<="><span>)\d+(?=% done)'

        units_prod = '(?<=p"><span>)\d+(?= unit)'

        # to export to importer.py
        regexcolor = (
                'background: linear-gradient\(135deg,'
                ' rgb\(\d+, \d+, \d+\),'
                ' rgb\(\d+, \d+, \d+\)\); color: rgb\(\d+, \d+, \d+\);'
                ' font-size: \d+.\d+px')

        def regexmaker_mat(
                matches_mat=matches_mat,
                start_mat=start_mat,
                units_prod=units_prod,
                separator="|"):
            s = ""
            # creates the regex string with correct syntax for every match
            for i in matches_mat:
                s = ""
                s = s+start_mat+i+separator

            s = regexcolor+"|"+s+units_prod
            return s

        self.regex_mat = regexmaker_mat()
        self.regex_prodtime = match_prodtime
        self.regex_progress = match_progress

        # colors, mat, unit(s)
        self.mats = re.findall(self.regex_mat, data)

        # completion times prod & queue
        prodtimes = re.findall(self.regex_prodtime, data)
        self.prodtimes = []
        for i in prodtimes:
            i = i.replace("<span>in ", "")
            self.prodtimes.append(i)

        # progress prod
        self.progress = re.findall(self.regex_progress, data)

        def grouper(n, iterable, fillvalue=None):
            "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
            args = [iter(iterable)] * n
            return list(zip_longest(fillvalue=fillvalue, *args))

        self.grouped_mats = grouper(3, self.mats)
        self.grouped_times = list(zip_longest(
            self.prodtimes, self.progress, fillvalue="queue"))
