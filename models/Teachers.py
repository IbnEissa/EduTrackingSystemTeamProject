from peewee import Model, CharField, ForeignKeyField, IntegerField, DoesNotExist
from models.Members import Members
from models.BaseModel import BaseModel
from models.Shifts import Shifts


class Teachers(BaseModel):
    member_id = ForeignKeyField(model=Members, backref='id', primary_key=True)
    shift_id = ForeignKeyField(model=Shifts, backref="shift_id")
    cities = CharField()
    major = CharField()
    task = CharField()
    exceperiance_years = IntegerField()
    qualification = CharField()
    date_qualification = CharField()
    state = CharField()

    class Meta:
        database = BaseModel().fetch_database_name()
