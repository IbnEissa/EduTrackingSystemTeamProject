from peewee import Model, CharField, ForeignKeyField, IntegerField, DoesNotExist, TextField
from models.Members import Members
from models.BaseModel import BaseModel
from models.Teachers import Teachers


class AbsentExcuse(BaseModel):
    teacher_id = ForeignKeyField(model=Teachers, backref='members_id')
    absent_date = TextField()
    note = TextField()

    def get_teacher_id_from_name(self, teacher_name):
        try:
            teacherObj = Members.get(Members.fName == teacher_name)
            return teacherObj.id
        except DoesNotExist:
            return None

    class Meta:
        database = BaseModel().fetch_database_name()
