from peewee import Model, CharField, TextField, DateTimeField, datetime, DoesNotExist

from models.BaseModel import BaseModel


class Shifts(BaseModel):
    name = CharField(max_length=50)
    start_date_shift = CharField()
    end_date_shift = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Shifts, self).save(*args, **kwargs)

    def get_shift_id_from_name(self, shift_name):
        try:
            shift_obj = Shifts.get(Shifts.name == shift_name)
            return shift_obj.id
        except DoesNotExist:
            return None

    class Meta:
        database = BaseModel().fetch_database_name()
#################################################
# from peewee import *
# from models.BaseModel import BaseModel, db
#
#
# class Shifts(BaseModel):
#     name = CharField(max_length=50)
#     start_date_shift = CharField()
#     end_date_shift = CharField()
#
#
# db.create_tables([Shifts])
