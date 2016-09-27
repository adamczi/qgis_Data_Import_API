# coding: utf-8
from peewee import *
from config import user, password, host, port, db_name

db = PostgresqlDatabase(db_name , user=user, password=password, host=host)