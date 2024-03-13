
def transpose(lines:list) -> list:
    return list(map(list, zip(*lines)))

def rotate(lines:list) -> list:
    return  list(map(list, zip(*reversed(lines ))))

def to_tuple(lines:list) -> tuple:
    tmp = []
    for l in lines:
        tmp.append( tuple(l))
    return tuple( tmp )

def to_list(lines:tuple) -> list:
    tmp = []
    for l in lines:
        tmp.append( list(l))
    return  tmp



