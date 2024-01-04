import datetime
from peewee import CharField, DateTimeField
from models.BaseModel import BaseModel


class Users(BaseModel):
    account_type = CharField()
    Name = CharField()
    userName = CharField()
    userPassword = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    state = CharField()
    initialization = CharField()
    database = BaseModel().fetch_database_name()

    class Meta:
        database = BaseModel().fetch_database_name()

    @staticmethod
    def get_name_with_true_state():
        # try:
        user = Users.select(Users.Name).where(Users.state == 'True').get()
        return user.Name
        # except Users.DoesNotExist:
        #     return None

    @staticmethod
    def update_all_states_to_false():
        Users.update(state=False).execute()
