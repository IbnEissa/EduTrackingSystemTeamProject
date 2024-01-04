import datetime
from peewee import Model, CharField, DateTimeField, ForeignKeyField, DoesNotExist
from models.Members import Members

from models.BaseModel import BaseModel


class BoardFathers(Model):
    member_id = ForeignKeyField(model=Members, backref="member", primary_key=True)
    social_status = CharField(max_length=20)
    address = CharField(max_length=50)
    organic_status = CharField()

    class Meta:
        database = BaseModel().fetch_database_name()
