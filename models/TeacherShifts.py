from peewee import Model, ForeignKeyField
from models.Teachers import Teachers
from models.Shifts import Shifts
from models.BaseModel import BaseModel


class TeacherShifts(BaseModel):
    teacher_id = ForeignKeyField(model=Teachers, backref="Teacher_id")
    shift_time_id = ForeignKeyField(model=Shifts, backref="shift_time_id")

    class Meta:
        database = BaseModel().fetch_database_name()
