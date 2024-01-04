from peewee import Model, CharField, ForeignKeyField, IntegerField
from models.ClassRoom import ClassRoom

from models.BaseModel import BaseModel


class TeacherSubjectClassRoomTermTable(BaseModel):
    subject_id = CharField()
    class_room_id = ForeignKeyField(model=ClassRoom, backref='Teacher_Subjects')
    number_of_lessons = IntegerField()

    term_id = None

    def get_elements(self, term_id, class_name, subject, number_of_sessions):
        return term_id, class_name, subject, number_of_sessions

    class Meta:
        database = BaseModel().fetch_database_name()
