import datetime
from peewee import Model, BooleanField, DateTimeField, ForeignKeyField, DoesNotExist
from models.Users import Users
from models.BaseModel import BaseModel


class Permissions(BaseModel):
    users_id = ForeignKeyField(Users, backref='users')
    led_main = BooleanField(default=False)
    led_manage = BooleanField(default=False)
    led_setting = BooleanField(default=False)
    # grant permissions to student tab
    bt_save_student = BooleanField(default=False)
    bt_search_student = BooleanField(default=False)
    bt_update_student = BooleanField(default=False)
    bt_delete_student = BooleanField(default=False)
    bt_reports_student = BooleanField(default=False)
    bt_show_student = BooleanField(default=False)
    bt_export_student = BooleanField(default=False)
    # grant permissions to teacher tab
    bt_save_teacher = BooleanField(default=False)
    bt_search_teacher = BooleanField(default=False)
    bt_update_teacher = BooleanField(default=False)
    bt_delete_teacher = BooleanField(default=False)
    bt_reports_teacher = BooleanField(default=False)
    bt_show_teacher = BooleanField(default=False)
    bt_export_teacher = BooleanField(default=False)
    # grant permissions to fathers tab
    bt_save_fathers = BooleanField(default=False)
    bt_search_fathers = BooleanField(default=False)
    bt_update_fathers = BooleanField(default=False)
    bt_delete_fathers = BooleanField(default=False)
    # grant permissions to user tab
    bt_save_user = BooleanField(default=False)
    bt_search_user = BooleanField(default=False)
    bt_update_user = BooleanField(default=False)
    bt_delete_user = BooleanField(default=False)
    # grant permissions to device tab
    bt_save_device = BooleanField(default=False)
    bt_search_device = BooleanField(default=False)
    bt_update_device = BooleanField(default=False)
    bt_delete_device = BooleanField(default=False)
    bt_export_device = BooleanField(default=False)
    bt_show_device = BooleanField(default=False)
    # grant permissions to Attendance tab
    bt_save_attendance = BooleanField(default=False)
    bt_search_attendance = BooleanField(default=False)
    bt_update_attendance = BooleanField(default=False)
    bt_delete_attendance = BooleanField(default=False)
    bt_export_attendance = BooleanField(default=False)
    bt_show_attendance = BooleanField(default=False)

    # grant permissions to timetable student tab
    bt_save_timetable_student = BooleanField(default=False)
    bt_show_timetable_student = BooleanField(default=False)
    bt_export_timetable_student = BooleanField(default=False)

    # grant permissions to timetable teacher tab
    # bt_save_timetable_teacher = BooleanField(default=False)
    bt_show_timetable_teacher = BooleanField(default=False)

    class Meta:
        database = BaseModel().fetch_database_name()
