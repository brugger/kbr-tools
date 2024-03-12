
email_match = '[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}'
email_regex = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'

domain_match = '[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}'



def comma_sep(elements:list) -> str:
    return ", ".join( map(str, elements))


def to_str(value:any) -> str:

    if isinstance(value, bytearray):
        return value.decode("utf-8")

    return str( value )

def readable_bytes(value:float) -> str:

    value = float( value)
    KB = 1024
    MB = pow(1024, 2)
    GB = pow(1024, 3)
    TB = pow(1024, 4)


    if value > TB:
        return f"{value/TB:.2f} TB"
    elif value > GB:
        return f"{value/GB:.2f} GB"
    elif value > MB:
        return f"{value/MB:.2f} MB"
    elif value > KB:
        return f"{value/KB:.2f} KB"
    else:
        return f"{value}B"

# an explanation: https://realpython.com/python-encodings-guide/
def reencode(s, from_encoding:str='iso-8859-1', to_encoding:str='utf-8') -> str:
    return bytes(s, from_encoding).decode(to_encoding)

def reencodings(s):

    encodings = ['utf-8', 'ascii',
                 'iso-8859-1', 'iso-8859-2', 'iso-8859-3', 'iso-8859-4', 
                 'iso-8859-5', 'iso-8859-6', 'iso-8859-7', 'iso-8859-8', 
                 'iso-8859-9', 'iso-8859-10','iso-8859-11', 'iso-8859-12', 
                 'iso-8859-13', 'iso-8859-14', 'iso-8859-15', 'iso-8859-16']


    for f in encodings:
        for t in encodings:
            if f == t:
                continue

            try:
                print(f" {f} --> {t} ==> {reencode(s, f, t)}")
            except:
                pass


#reencodings("LemminkÃ¤inen")

