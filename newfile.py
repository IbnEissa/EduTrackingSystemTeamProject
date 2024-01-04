import logging
from zk import ZK
class YourClassName:
    def __init__(self):
        # Initialize the self.zk object (replace with your initialization code)
        self.zk = ZK()  # Replace with the appropriate initialization code

    def FetchAll(self, info_deel):
        uid = {}  # A dictionary to store user information (user ID and username)
        self.zk.get_users()  # Read all user IDs from the device

        while True:
            uid = self.zk.user
        logging.warning(uid)  # Log the fetched user information
        return uid