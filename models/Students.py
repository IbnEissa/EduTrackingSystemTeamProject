from peewee import Model, CharField, ForeignKeyField

from models.Members import Members
from models.ClassRoom import ClassRoom

from models.BaseModel import BaseModel


class Students(BaseModel):
    member_id = ForeignKeyField(model=Members, backref="id", primary_key=True)
    class_id = ForeignKeyField(model=ClassRoom, backref="class_id")

    class Meta:
        database = BaseModel().fetch_database_name()
