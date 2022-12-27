from zlib import crc32
from hashlib import md5, sha1
from base64 import b64encode

from get_values import *

def get_data():
    return f'login="{get_login()}", username="{get_name()}"'


def get_filename():
    data = get_data().encode()
    data = (crc32(data).to_bytes(4, "big").hex() + md5(data).hexdigest())[::2]
    data = b64encode(data.encode()).decode().replace('=', '')
    return f'{data}.settings'


def get_fernetkey():
    data = get_data().encode()
    return b64encode((sha1(data).hexdigest()[:-1] + crc32(data).to_bytes(4, 'little').hex()[-5:])[31::-1].encode())
