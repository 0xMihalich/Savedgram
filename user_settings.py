import json
from os.path import exists

from cryptography.fernet import Fernet

from data_coding import get_filename, get_fernetkey

def get_settings():
    file = get_filename()
    if exists(file):
        cipher = Fernet(get_fernetkey())
        with open(file, "rb") as file_dec:
            data = cipher.decrypt(file_dec.read())
        base = json.loads(data)
        return base['token'], base['folder']
    return '', ''


def save_settings(token: str, folder: str):
    chk_token, chk_folder = get_settings()
    if token == chk_token and folder == chk_folder:
        return
    data = json.dumps({'token': token, 'folder': folder}).encode('utf-8')
    cipher = Fernet(get_fernetkey())
    data_enc = cipher.encrypt(data)
    with open(get_filename(), "wb") as file_enc:
        file_enc.write(data_enc)