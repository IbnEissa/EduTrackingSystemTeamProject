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


# Example usage of the Finger class

def main():
    # Send data to the Finger class
    finger = Finger(uid=123, fid=1, valid=1, template=b'\x01\x23\x45\x67\x89\xAB\xCD\xEF')

    # Perform operations on the Finger object
    packed_data = finger.repack()
    unpacked_finger = Finger.json_unpack(finger.json_pack())

    # Print the original and unpacked Finger objects
    print("Original Finger: ", finger)
    print("Unpacked Finger: ", unpacked_finger)

    # Convert the Finger object to JSON
    finger_json = json.dumps(finger.json_pack())

    # Print the JSON representation
    print("Finger JSON: ", finger_json)

    # Create a Finger object from JSON
    parsed_json = json.loads(finger_json)
    created_finger = Finger.json_unpack(parsed_json)

    # Print the created Finger object
    print("Created Finger: ", created_finger)


if __name__ == '__main__':
    main()