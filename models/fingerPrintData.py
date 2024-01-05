import datetime
from peewee import Model, CharField, IntegerField, ForeignKeyField, DoesNotExist
from models.Teachers import Teachers

from models.BaseModel import BaseModel


class FingerPrintData(BaseModel):
    teacher_id = ForeignKeyField(model=Teachers, backref='Finger_Print_Datas')
    card_id = IntegerField()
    password = CharField(max_length=30)
    f0 = CharField()
    f1 = CharField()
    f2 = CharField()
    f3 = CharField()
    f4 = CharField()
    f5 = CharField()
    f6 = CharField()
    f7 = CharField()
    f8 = CharField()
    f9 = CharField()

    def get_teacher_fingers(self, teacer_id):
        try:
            finger_obj = FingerPrintData.select().where(FingerPrintData.teacher_id == teacer_id)
            if finger_obj:
                return True
            else:
                return False
        except DoesNotExist:
            return 'First'

    class Meta:
        database = BaseModel().fetch_database_name()
