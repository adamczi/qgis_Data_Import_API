# coding: utf-8
from peewee import *
from config import db_name, user, pword, host

db = PostgresqlDatabase(db_name,
                        user=user,
                        password=pword,
                        host=host)
