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
