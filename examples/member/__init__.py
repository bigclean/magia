# -*- coding: utf-8 -*-

from magia import Database

db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'eleme',
    'password': 'eleme',
    'database': 'dev_member'
}

Database.connect(**db_config)
