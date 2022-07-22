import re

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



def snake2CamelCase(name): #col_nav --> ColNav
    return re.sub(r'(?:^|_)([a-z])', lambda x: x.group(1).upper(), name)
 
def snake2camelBack(name): #col_nav --> colNav
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), name)
 
def CamelCase2snake(name): #ColNav -> col_nav
    return name[0].lower() + re.sub(r'(?!^)[A-Z]', lambda x: '_' + x.group(0).lower(), name[1:])
 
def camelBack2snake(name): # colNav -> col_nav
    return re.sub(r'[A-Z]', lambda x: '_' + x.group(0).lower(), name)

def minus2CamelCase(name): #colum-navigator --> ColumNavigator
    return re.sub(r'(?:^|-)([a-z])', lambda x: x.group(1).upper(), name)

def minus2camelBack(name): #colum-navigator --> columNavigator
    return re.sub(r'-([a-z])', lambda x: x.group(1).upper(), name)


# These surely could be done more intelligent, like this one:

def to_CamelCase(name): #col_nav --> ColNav, col-NAV --> ColNav
    return re.sub(r'(?:^|_|-)([a-z])', lambda x: x.group(1).upper(), name.lower())

def to_camelBack(name): #col_nav --> colNav, Col-Nav -> colNav
    name = name.lower().replace('-', '_')
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), name)

#def to_snake(name:str) -> str:
#    name = name.replace('-', '_')
#    return name[0].lower() + re.sub(r'(?!^)[A-Z]', lambda x: '_' + x.group(0).lower(), name[1:])

