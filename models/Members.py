import datetime
from peewee import Model, CharField, DateTimeField, ForeignKeyField, IntegerField, DoesNotExist
from models.School import School
from models.BaseModel import BaseModel


class Members(BaseModel):
    school_id = ForeignKeyField(School, backref='school')
    fName = CharField()
    lName = CharField()
    dateBerth = CharField()
    phone = IntegerField()
    type = CharField()
    gender = CharField()

    def get_members_by_id(self, member_id):
        try:
            class_obj = Members.get(Members.id == member_id)
            return class_obj
        except DoesNotExist:
            return None

    def get_member_id_from_name(self, member_name):
        try:
            member_object = Members.get(Members.name == member_name)
            return member_object.id
        except DoesNotExist:
            return None

    def get_obj_by_name(self, member_name):
        try:
            member_object = Members.get(Members.fName.contains(member_name) )
            return member_object
        except DoesNotExist:
            return None

    class Meta:
        database = BaseModel().fetch_database_name()
