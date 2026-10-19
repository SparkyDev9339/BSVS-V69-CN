from Classes.Packets.PiranhaMessage import PiranhaMessage

class SkinRewardNotification(PiranhaMessage):
    def __init__(self, NotificationData):
        super().__init__(NotificationData)
        self.messageVersion = 0

    def encode(self, fields):
        self.writeVInt(0) 
        self.writeVInt(0) # Skin Donated
        self.writeBoolean(False)

    def decode(self):
        return {}