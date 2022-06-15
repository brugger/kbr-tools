import socket
import sys


def prefix_path() -> str:
  return sys.prefix


def share_path(project:str='') -> str:
  return f"{prefix_path}/{project}"



def get_host_ip() -> str:
    """ gets the host ip address
    Args:
      None
    returns:
      Host Ip 4 address
    Raises:
      None
    """
    try:
        address = socket.gethostbyname(socket.gethostname())
        # On some system, this always gives me 127.0.0.1. Hence...
    except:
        address = ''

    if not address or address.startswith('127.'):
        # ...the hard way.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        address = s.getsockname()[0]

    return address



def get_host_name() -> str:
    """ gets the host name
    Args:
      None
    Returns:
      full host name
    Raises:
      None
    """
    return socket.getfqdn()
