from peewee import Model, CharField
from models.BaseModel import BaseModel


class SystemScreens(BaseModel):
    name = CharField(max_length=40)
    system_fr = CharField(max_length=40)
    additional = CharField(max_length=40)

    class Meta:
        database = BaseModel().fetch_database_name()
