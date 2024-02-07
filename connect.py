import configparser
import pathlib

from mongoengine import connect

import certifi
ca = certifi.where()

file_config = pathlib.Path(__file__).parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

user = config.get('DB', 'user')
passwd = config.get('DB', 'passwd')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

connect(host=f"mongodb+srv://{user}:{passwd}@{domain}{db_name}", ssl=True, tlsCAFile=ca)

