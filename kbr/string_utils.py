
email_match = '[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}'
email_regex = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'

domain_match = '[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}'



def comma_sep(elements:[]) -> str:
    return ", ".join( map(str, elements))


def to_str(value:any) -> str:

    if instance(value, bytearray):
        return value.decode("utf-8")

    return str( value )
