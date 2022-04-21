def is_string( value ) -> bool:
    return isinstance(value, str)

def is_int( value ) -> bool:
    # because some classes can become an int, and we dont want those!
    if 'class' in str(type(value)):
        return False

    try:
        int(value)
        return True
    except:
        return isinstance(value, int)


def is_float( value ) -> bool:
    try:
        float(value)
        return True
    except:
        return isinstance(value, float)

def is_number( value ) -> bool:
    return is_int( value ) or is_float( value )

def is_positive_number( value ) -> bool:
    return is_number( value ) and float( value ) > 0


def is_negative_number( value ) -> bool:
    return is_number( value ) and float( value ) < 0

def none_or_contains_value( data, value ):
    """ return true if data is not set, or value is in data """
    if ( data is None or
            not data or
            value in data ):
        return True

    return False

