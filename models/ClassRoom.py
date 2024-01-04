import datetime
from peewee import Model, CharField, DateTimeField, ForeignKeyField, DoesNotExist
from models.School import School
from models.BaseModel import BaseModel


def get_class_id_from_name(class_name):
    try:
        class_obj = ClassRoom.get(ClassRoom.name == class_name)
        return class_obj.id
    except DoesNotExist:
        return None


class ClassRoom(BaseModel):
    school_id = ForeignKeyField(model=School, backref="Users")
    name = CharField(max_length=20, unique=True)
    Name_major = CharField()
    @classmethod
    def add(cls, school_id, names):
        created_classes = []
        for name in names:
            class_obj = cls(
                school_id=school_id,
                name=name,
            )
            class_obj.save()
            created_classes.append(class_obj)
        return created_classes

    def get_class_name_from_id(self, class_id):
        try:
            class_obj = ClassRoom.get(ClassRoom.id == class_id)
            return class_obj.name
        except DoesNotExist:
            return None

    def get_class_id_from_name(self, class_name):
        try:
            class_obj = ClassRoom.get(ClassRoom.name == class_name)
            return class_obj.id
        except DoesNotExist:
            return None

    class Meta:
        database = BaseModel().fetch_database_name()
