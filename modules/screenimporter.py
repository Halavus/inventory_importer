#!py3

import re
from itertools import zip_longest
from modules.regex import commodity_data as regex 


class Importer:

    def __init__(self, data):
        
        self.data=data
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
            element = {}
            
            try:
                for n in range(len(dic["ticker"])):
                    infos = {}
                    identifier = dic["ticker"][n-1]+"."+dic["cx"][n-1]
                    for i in dic:
                        infos[i]=dic[i][n-1]
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
        
        self.element=compiler()
        
        self.nodata=False
        if self.element=={}:
            self.nodata=True
