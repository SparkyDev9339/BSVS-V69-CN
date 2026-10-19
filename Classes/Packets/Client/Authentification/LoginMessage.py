from Classes.ClientsManager import ClientsManager
from Classes.Messaging import Messaging

from Classes.Packets.PiranhaMessage import PiranhaMessage
from Database.DatabaseHandler import DatabaseHandler


class LoginMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        pass

    def decode(self):
        fields = {}
        fields["AccountID"] = self.readLong()
        fields["PassToken"] = self.readString()
        fields["ClientMajor"] = self.readInt()
        fields["ClientMinor"] = self.readInt()
        fields["ClientBuild"] = self.readInt()
        fields["ResourceSha"] = self.readString()
        fields["Device"] = self.readString()
        fields["PreferredLanguage"] = self.readDataReference()
        fields["PreferredDeviceLanguage"] = self.readString()
        fields["OSVersion"] = self.readString()
        fields["isAndroid"] = self.readBoolean()
        fields["IMEI"] = self.readString()

        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields):
        if fields["ClientMajor"] != 69:
            return
        with DatabaseHandler() as db:
            player = db.login(fields["AccountID"], fields["PassToken"])
        if player is None:
            return
        calling_instance.player = player
        ClientsManager.AddPlayer(player.ID, calling_instance.client)
        response = {"Socket": calling_instance.client}
        Messaging.sendMessage(20104, response, player)
        Messaging.sendMessage(24101, response, player)

    def getMessageType(self):
        return 10101

    def getMessageVersion(self):
        return self.messageVersion