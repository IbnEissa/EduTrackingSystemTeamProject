import datetime
from peewee import Model, CharField, DateTimeField, ForeignKeyField, DoesNotExist

from models.Members import Members
from models.Teachers import Teachers
from models.BaseModel import BaseModel


class AttendanceModel(BaseModel):
    member_id = ForeignKeyField(model=Members, backref='attendances')
    device_number = CharField(max_length=50)
    out_time = DateTimeField()
    input_time = DateTimeField()
    status = CharField(max_length=15)
    punch = CharField(max_length=50)

    def get_all_attendance(self):
        try:
            attendanceData = AttendanceModel.select()
            return attendanceData
        except DoesNotExist:
            return None

    class Meta:
        database = BaseModel().fetch_database_name()
