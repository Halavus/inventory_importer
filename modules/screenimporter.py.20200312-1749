#!py3

import re
from itertools import zip_longest
import json
from modules.regex import commodity_data as regex


class Importer:

    def __init__(self, data):

        data=data.replace('\r\n', '\n')

        self.data=repr(data)
        dic={}

        for i in regex:
            m = []
            matches = re.finditer(regex[i], data)
            for match in matches:

                if match.group(1)!=None:
                    m.append(match.group(1))
                else:
                    m.append(match.group(4))

                dic[i]=m

        self.dic=dic
        def compiler(dic=dic):
            "Structure: {ticker.cx: {label: info}}"
            "== {identifier: {label: info}}"

            element = {}

            try:
                for n in range(len(dic["ticker"])):
                    infos = {}
                    cx = dic["cx"][n-1]
                    identifier = dic["ticker"][n-1]+"."+cx
                    for i in dic:
                        infos[i]=dic[i][n-1]
                        element[identifier]=infos
                    if cx=="IC1":
                        infos["currency"]="ICA"
                        element[identifier]=infos
                    elif cx=="NC1":
                        infos["currency"]="NCC"
                        element[identifier]=infos
                    else:
                        infos["currency"]="CIS"
                        element[identifier]=infos

            except Exception:
                pass

            return element

        def iferror(func, *args, **kw):
            try:
                func(*args, **kw)
                return True
            except Exception:
                return False

        self.element = compiler()

        self.json = json.dumps(self.element)

        self.nodata=False
        if self.element=={}:
            self.nodata=True
