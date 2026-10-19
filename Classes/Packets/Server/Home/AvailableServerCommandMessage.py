from Classes.Commands.Server.LogicChangeAvatarNameCommand import LogicChangeAvatarNameCommand
from Classes.Packets.PiranhaMessage import PiranhaMessage


class AvailableServerCommandMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        command_id = fields["Command"]["ID"]
        if command_id != 201:
            raise ValueError(f"Unsupported server command: {command_id}")
        self.writeVInt(command_id)
        command = LogicChangeAvatarNameCommand(self.messagePayload)
        self.messagePayload = command.encode(fields)

    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24111

    def getMessageVersion(self):
        return self.messageVersion