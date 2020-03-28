#!py3

import re
import json

from .regex import commodity_data as regex


class Importer:

    def __init__(self, data, debug=False):

        data=data.replace('\r\n', '\n')

        dic={}

        for i in regex:
            "Structure: {[{infos}]}"

            m = []
            matches = re.finditer(regex[i], data)
            for match in matches:

                if match.group(1)!=None:
                    m.append(match.group(1))
                else:
                    m.append(match.group(4))

                dic[i]=m

        def compiler(dic=dic):
            "New structure: {ticker: {cx.label: info}}"
            "            == {identifier: {cx.label: info}}"

            element = {}
            headers = ["Ticker"]

            try:
                "try in order to return an empty dic for data checking"

                for n in range(len(dic["ticker"])):
                    infos = {}
                    cx = dic["cx"][n-1]
                    identifier = dic["ticker"][n-1]
                    for i in dic:
                        id2=str(cx)+"."+str(i)
                        infos[id2]=dic[i][n-1]
                        if id2 in headers:
                            pass
                        else:
                            headers.append(id2)
                        try:
                            if element[identifier]:
                                element[identifier][id2]=infos[id2].replace(",", "")
                        except Exception:
                            element[identifier]=infos

                    ''' Do currencies have to be present in this dataset?
                    if yes correct the code...

                    if cx=="IC1":
                        element[identifier]["currency"]="ICA"
                    elif cx=="NC1":
                        element[identifier]["currency"]="NCC"
                    else:
                        element[identifier]["currency"]="CIS"
                    '''

            except Exception:
                pass

            return element, headers

        def cleaner(element=compiler()[0], headers=compiler()[1]):
            rm = ["cx", "ticker"]
            for dic in element:
                for k in list(element[dic]):
                    for s in rm:
                        if s in k:
                            del element[dic][k]

            headers[:] = [h for h in headers if h[4:] not in rm]

            element["headers"]=headers

            return element

        element = cleaner()
        self.element = element

        # This nice fill func should be copied in a private package
        def fill(lst, index, add, fillvalue=None):
            '''Fills a list with a add value based on list index'''
            '''Let the value in place if present'''
            for n in range(index):
                try:
                    if lst[n]:
                        pass
                except Exception:
                    lst.append(fillvalue)
            try:
                if lst[index]:
                    pass
                else:
                    lst[index]=add
            except Exception:
                if index==len(lst):
                    #if check not mandatory
                    lst.append(add)
            return lst

        matrix = [element["headers"]]

        linenumber=1
        for row in element:
            if row=="headers":
                pass
            else:
                matrix.append([])
                matrix[linenumber].append(row)
                for label in element[row]:
                    if debug:
                        print(element[row])
                        print("label: "+label)
                    for header in matrix[0][1:]:
                        if debug:
                            print("header: "+header)
                        if label==header:
                            if debug:
                                print("linenumber: "+str(linenumber))
                                print("matrix line: "+str(matrix[linenumber]))
                                print("index header: "+str(matrix[0].index(header)))
                                print(element[row][label])

                                #use tuples in matrix for datacheck
                                add=(header, element[row][label])
                            else:
                                add=element[row][label]

                            fill(lst=matrix[linenumber],
                                 index=matrix[0].index(header),
                                 add=add,
                                 fillvalue=None)
                        else:
                            pass
                if debug:
                    print(matrix)
                linenumber+=1

        self.matrix=matrix

        self.json = json.dumps(self.element)

        self.nodata=False
        if self.element=={"headers": ["Ticker"]}:
            self.nodata=True
