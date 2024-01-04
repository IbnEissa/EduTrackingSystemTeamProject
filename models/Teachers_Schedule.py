from peewee import Model, CharField
from models.BaseModel import BaseModel


class Teachers_Schedule(BaseModel):
    Teacher_Name = CharField()
    Day = CharField()
    Subject = CharField()
    session = CharField()
    Class_Name = CharField()

    class Meta:
        database = BaseModel().fetch_database_name()
