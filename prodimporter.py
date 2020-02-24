#!py3

import re
from itertools import zip_longest
from modules.regex import prod_importer as regex
from modules.timeparser import timeparser

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

        self.formated_prodtimes = []
        self.formated_queuetimes = []

        for tup in self.grouped_times:
            
            dic = {}

            times = timeparser(tup[0])

            if tup[1] == "queue":
                status = "queue"

            else:
                status = "prod"

            if status == "prod":
                dic["timer"] = times["timer"]
                dic["timestamp"] = times["timestamp"]

                self.formated_prodtimes.append(dic)

            else:
                dic["timer"] = times["timer"]
                dic["timestamp"] = times["timestamp"]

                self.formated_queuetimes.append(dic)
        
        def sorting(dic=self.formated_prodtimes, arg="timestamp"):
            return dic[arg]

        self.formated_prodtimes.sort(key=sorting)
