def is_string( value ) -> bool:
    return isinstance(value, str)


def is_int( value ) -> bool:
    return isinstance(s, int)


def is_float( value ) -> bool:
    return isinstance(s, float)

def is_number( value ) -> bool:
    return is_int( value ) or is_float( value )

def is_positive_number( value ) -> bool:
    return is_number( value ) and float( value ) > 0


#def is_type( value, types[] ) -> bool: