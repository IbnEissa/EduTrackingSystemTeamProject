import datetime
from peewee import CharField, DateTimeField, DoesNotExist
from models.BaseModel import BaseModel


class School(BaseModel):
    school_name = CharField(max_length=100)
    city = CharField(max_length=30)
    directorate = CharField(max_length=30)
    village = CharField(max_length=30)
    academic_level = CharField(max_length=20)
    student_gender_type = CharField(max_length=10)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def add(cls, name, city, directorate, village, academic_level, student_gender_type):
        school = cls(
            school_name=name,
            city=city,
            directorate=directorate,
            village=village,
            academic_level=academic_level,
            student_gender_type=student_gender_type
        )
        school.save()
        return school

    # def get_school_by_id(self, id):
    #     try:
    #         school_obj = School.get(School.id == id)
    #         return school_obj
    #     except DoesNotExist:
    #         return None

    def get_all_schools(self):
        try:
            schools = School.select()
            return schools
        except DoesNotExist:
            return None
    class Meta:
        database = BaseModel().fetch_database_name()
