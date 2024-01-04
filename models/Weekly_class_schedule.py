from peewee import Model, ForeignKeyField
from playhouse.mysql_ext import MySQLConnectorDatabase
from models.Session import Session
from models.Members import Members
from models.Subjects import Subjects
from models.ClassRoom import ClassRoom

db = MySQLConnectorDatabase(None)


class WeeklyClassSchedule(Model):
    teacher_id = ForeignKeyField(model=Members, backref="Teacher")
    subject_id = ForeignKeyField(model=Subjects, backref="Subjects")
    class_room_id = ForeignKeyField(model=ClassRoom, backref="Class_room")
    # day_id = ForeignKeyField(model=Days, backref='Teacher_Subjects')
    session_id = ForeignKeyField(model=Session, backref='Teacher_Subjects')

    class Meta:
        database = db
