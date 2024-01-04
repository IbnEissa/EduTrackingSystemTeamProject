from peewee import CharField, TimeField, TextField, ForeignKeyField, IntegerField
from models.BaseModel import BaseModel
from models.Shifts import Shifts


class Periods(BaseModel):
    shift_id = ForeignKeyField(model=Shifts, backref="id")
    name = CharField(max_length=20)
    attendance_time = TimeField()
    departure_time = TimeField()
    period_price = IntegerField()
    time_allowed_for_late = IntegerField()
    time_allowed_for_leaving = IntegerField()

    class Meta:
        database = BaseModel().fetch_database_name()



# ################################################
# from peewee import *
# from BaseModel import BaseModel, db
# from models.Shifts import Shifts
#
#
# class Periods(BaseModel):
#     shift_id = ForeignKeyField(model=Shifts, backref="id")
#     name = CharField(max_length=20)
#     attendance_time = TimeField()
#     departure_time = TimeField()
#     period_price = TextField()
#     time_allowed_for_late = TextField()
#     time_allowed_for_leaving = TextField()
#
#
# db.create_tables([Periods])
