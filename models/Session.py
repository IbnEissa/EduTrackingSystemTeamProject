from peewee import CharField, TimeField
from models.BaseModel import BaseModel


class Session(BaseModel):
    name = CharField(max_length=20)
    start_time = TimeField()
    end_time = TimeField()

    class Meta:
        db = BaseModel().fetch_database_name()
