


def isnumber(value):
    ''' check if value is either an int or float '''
    
    if (isinstance(value, int) or
        isinstance( value, float )):

        return True

    return False



def none_or_contains_value( data, value ):
    """ return true if data is not set, or value is in data """
    if ( data is None or
         not data or
         value in data ):
        return True

    return False

