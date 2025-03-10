'''
Helper functions that can be called from a jinja2 template
'''
from datetime import datetime
import ipaddress
import random
import string
from uuid import uuid4

def now() -> str:
    '''Returns current date and time'''
    return datetime.now().isoformat('T')

def uuid() -> str :
    '''Returns a UUID 4'''
    return str(uuid4())

def random_ipv4(exclude_reserved: bool = False) -> str:
    '''
    Returns a random IPV4 address

    Args:
        exclude_reserved (bool, optional): exclude IETF reserved address. Defaults to False.

    Returns:
        str: a random IPV4 address
    '''
    while True:
        ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
        if not (exclude_reserved and ipaddress.IPv4Address(ip).is_reserved):
            return ip

def random_ipv6(exclude_reserved: bool = False) -> str:
    '''
    Returns a random IPV6 address

    Args:
        exclude_reserved (bool, optional): exclude IETF reserved address. Defaults to False.

    Returns:
        str: a random IPV6 address
    '''
    while True:
        ip = ':'.join(f"{random.randint(0, 0xFFFF):04x}" for _ in range(8))
        if not (exclude_reserved and ipaddress.IPv6Address(ip).is_reserved):
            return ip

def random_string(length: int = 5) -> str:
    '''
    Returns a random string of lowercase letters

    Args:
        length (int, optional): the length of the string. Defaults to 5.

    Returns:
        str: a random string
    '''
    return ''.join(random.choices(string.ascii_lowercase,k=length))

HELPER_FUNS = {
    'now':now,
    'uuid':uuid,
    'random_ipv4':random_ipv4,
    'random_ipv6':random_ipv6,
    'random_string':random_string,
}
