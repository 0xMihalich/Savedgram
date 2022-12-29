import ctypes
from os import getlogin
from platform import system


def get_name():
    if system() != 'Windows':
        return get_login()
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3
 
    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)
 
    nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(NameDisplay, nameBuffer, size)
    return nameBuffer.value


def get_login():
    return getlogin().lower()
