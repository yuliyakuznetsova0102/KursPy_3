import os
from configparser import ConfigParser

ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, "data")
COMPANY_NAMES = [
    "Сбер",
    "БТБ",
    "VK",
    "Яндекс",
    "Авито",
    "Ozon",
    "Ростелеком",
    "Газпром",
    "Литрес",
]

filename = os.path.join(ROOT_DIR, "database.ini")


def config(filename=filename, section="postgresql"):
    parser = ConfigParser()  # create a parser
    parser.read(filename)  # read config file
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} is not found in the {1} file.".format(section, filename)
        )
    return db
