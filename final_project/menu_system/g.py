



def printarray(lst, howmany):
    if howmany == 0:
        return None
    else:
        printarray(lst, howmany - 1)
        print(lst[howmany - 1])
