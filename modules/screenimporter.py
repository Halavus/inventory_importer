#!py3

import re
from itertools import zip_longest
from modules.regex import commodity_data as regex 


class Importer:

    def __init__(self, data):
        
        self.data=data
        data=data

        dic={}
        '''
        for i in regex:               
            m=re.findall(regex[i], data)
            dic[i]=m
        '''

        for i in regex:
            matches = re.finditer(regex[i], data)
            m=[match.group(1) for match in matches]
            dic[i]=m
    

        self.dic=dic
        def compiler(dic=dic):
            
            element = {}

            for n in range(len(dic["ticker"])):
                infos = {}
                identifier = dic["ticker"][n-1]+"."+dic["cx"][n-1]
                
                for i in dic:
                    infos[i]=dic[i][n-1]
                    #element[i]=dic[i][n]
                    element[identifier]=infos

            return element

        self.element=compiler()

        self.nodata=False
        
        if self.element==[]:
            self.nodata=True
