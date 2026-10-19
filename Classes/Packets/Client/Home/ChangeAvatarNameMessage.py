from Classes.Messaging import Messaging

from Classes.Packets.PiranhaMessage import PiranhaMessage
from Database.DatabaseHandler import DatabaseHandler


class ChangeAvatarNameMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        self.writeString(fields["Name"])
        self.writeBoolean(fields["NameSetByUser"])

    def decode(self):
        fields = {}
        fields["Name"] = self.readString()
        fields["NameSetByUser"] = self.readBoolean()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields):
        with DatabaseHandler() as db:
            if not db.set_name(calling_instance.player, fields["Name"]):
                return
        response = {
            "Socket": calling_instance.client,
            "Command": {"ID": 201},
            "Name": calling_instance.player.Name,
        }
        Messaging.sendMessage(24111, response)

    def getMessageType(self):
        return 10212

    def getMessageVersion(self):
        return self.messageVersion