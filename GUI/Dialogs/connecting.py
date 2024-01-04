import json
from struct import pack
import codecs

class Finger(object):
    def __init__(self, uid, fid, valid, template):
        self.size = len(template)
        self.uid = int(uid)
        self.fid = int(fid)
        self.valid = int(valid)
        self.template = template
        self.mark = codecs.encode(template[:8], 'hex') + b'...' + codecs.encode(template[-8:], 'hex')

    def repack(self):
        return pack("<HHbb%is" % (self.size), self.size+6, self.uid, self.fid, self.valid, self.template)

    def repack_only(self):
        return pack("<H%is" % (self.size), self.size, self.template)

    @staticmethod
    def json_unpack(json):
        return Finger(
            uid=json['uid'],
            fid=json['fid'],
            valid=json['valid'],
            template=codecs.decode(json['template'],'hex')
        )

    def json_pack(self):
        return {
            "size": self.size,
            "uid": self.uid,
            "fid": self.fid,
            "valid": self.valid,
            "template": codecs.encode(self.template, 'hex').decode('ascii')
        }

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "<Finger> [uid:{:>3}, fid:{}, size:{:>4} v:{} t:{}]".format(self.uid, self.fid, self.size, self.valid, self.mark)

    def __repr__(self):
        return "<Finger> [uid:{:>3}, fid:{}, size:{:>4} v:{} t:{}]".format(self.uid, self.fid, self.size, self.valid, self.mark)

    def dump(self):
        return "<Finger> [uid:{:>3}, fid:{}, size:{:>4} v:{} t:{}]".format(self.uid, self.fid, self.size, self.valid, codecs.encode(self.template, 'hex'))


def create_finger():
    uid = input("Enter UID: ")
    fid = input("Enter FID: ")
    valid = input("Enter Validity: ")
    template = input("Enter Template (hex): ")
    finger = Finger(uid=uid, fid=fid, valid = valid, template=codecs.decode(template, 'hex'))
    return finger


def display_finger(finger):
    print("UID: ", finger.uid)
    print("FID: ", finger.fid)
    print("Validity: ", finger.valid)
    print("Template: ", codecs.encode(finger.template, 'hex').decode('ascii'))


def main():
    print("Finger Application\n")

    while True:
        print("1. Create Finger")
        print("2. Display Finger")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            finger = create_finger()
        elif choice == '2':
            display_finger(finger)
        elif choice == '3':
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == '__main__':
    main()