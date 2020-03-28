import re


def timeparser(data):

    def f(back, data=data):
        match="\d+(?="+back+")"

        # outputs a list with 1 object or an empty list if no match
        out = re.findall(match, data)

        if out==[]:
            out=0
        else:
            out=int(re.findall(match, data)[0])

        return out


    days = f(" day")
    hours = f("h")+days*24
    minutes = f("m")
    sec = f("s")

    def summ(*args):
        return sum(args)


    def formater(digit):
        if digit<10:
            formated = str(0)+str(digit)
        else:
            formated = str(digit)

        return formated

    time = {"timestamp": summ(hours/24, minutes/24/60, sec/24/60**2),
            "timer": ":".join((formater(hours), formater(minutes), formater(sec)))}

    return time
