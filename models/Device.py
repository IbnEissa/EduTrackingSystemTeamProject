import datetime
from peewee import Model, CharField, DateTimeField, ForeignKeyField, IntegerField
from zk import ZK

from models.School import School
from models.BaseModel import BaseModel


class Device(BaseModel):
    school_id = ForeignKeyField(model=School, backref='Devices')
    name = CharField(max_length=30)
    ip = CharField(max_length=20)
    port = IntegerField()
    status = CharField(max_length=20)

    @classmethod
    def add(cls, school_id, name, ip, port, status):
        device = cls(
            school_id=school_id,
            name=name,
            ip=ip,
            port=port,
            status=status,
        )
        device.save()
        return device

    def connect_device(self, device_ip, device_port):
        zk = ZK(ip=device_ip, port=device_port, timeout=5)
        message = ''
        try:
            conn = zk.connect()
            if conn:
                message = 'تم الاتصال بنجاح'
                return True, message
            else:
                message = 'فشل الاتصال'
                return False, message
        except Exception as e:
            message = 'فشل الاتصال' + str(e)
            return False, message

    def retrieve_attendance(self, device_ip, device_port):
        zk = ZK(ip=device_ip, port=device_port, timeout=5)
        message = ''
        try:
            conn = zk.connect()
            if conn:
                message = 'تم الاتصال بنجاح'
                return True, message
            else:
                message = 'فشل الاتصال'
                return False, message
        except Exception as e:
            message = 'فشل الاتصال' + str(e)
            return False, message

    class Meta:
        database = BaseModel().fetch_database_name()
