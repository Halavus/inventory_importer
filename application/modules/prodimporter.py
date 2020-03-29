import re
from itertools import zip_longest

from .regex import prod_importer as regex
from .timeparser import timeparser

class Importer:

    def __init__(self, data):

        # self.data for testing purposes
        self.data = data

        # colors, mat, unit(s)
        mats_import = re.findall(regex["mat"], data)
        # Testing
        self.mats = mats_import

        # completion times prod & queue
        prodtimes_import = re.findall(regex["prodtime"], data)
        prodtimes_formated = [i.replace("<span>in ", "") for i in prodtimes_import]

        # progress prod
        progress = re.findall(regex["progress"], data)

        def grouper(n, iterable, fillvalue=None):
            "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
            args = [iter(iterable)] * n
            return list(zip_longest(fillvalue=fillvalue, *args))

        mats_units = grouper(3, mats_import)
        grouped_times = list(zip_longest(
            prodtimes_formated, progress, fillvalue="queue"))

        prod_times = []
        queue_times = []

        for tup in grouped_times:

            dic = {}

            times = timeparser(tup[0])

            if tup[1] == "queue":
                status = "queue"

            else:
                status = "prod"

            if status == "prod":
                dic["timer"] = times["timer"]
                dic["timestamp"] = times["timestamp"]

                prod_times.append(dic)

            else:
                dic["timer"] = times["timer"]
                dic["timestamp"] = times["timestamp"]

                queue_times.append(dic)
        
        def sorting(dic=prod_times, arg="timestamp"):
            return dic[arg]

        prod_times.sort(key=sorting)

        production = {
                "mats_units": mats_units[:len(prod_times)],
                "times": prod_times}

        queue = {
                "mats_units": mats_units[len(prod_times):],
                "times": queue_times}

        #   OUTPUTS

        def outputmaker(key, index, dic):
            lst = []
            counter = 0
            for i in dic[key]:
                lst.append(dic[key][counter][index])
                counter += 1
            return lst

        self.nodata=False

        o=outputmaker

        self.prod = {
                "styles" : o("mats_units", 0, production),
                "mats" : o("mats_units", 1, production),
                "units" : o("mats_units", 2, production),
                "timestamps" : o("times", "timestamp", production),
                "timers" : o("times", "timer", production)}
        self.queue = {
                "styles" : o("mats_units", 0, queue),
                "mats" : o("mats_units", 1, queue),
                "units" : o("mats_units", 2, queue),
                "timestamps" : o("times", "timestamp", queue),
                "timers" : o("times", "timer", queue)}

        if prodtimes_import==[]:
             self.nodata=True
