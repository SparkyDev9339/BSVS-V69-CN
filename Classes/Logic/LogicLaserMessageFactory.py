import Configuration
from Classes.Packets.Client.Authentification.LoginMessage import LoginMessage
from Classes.Packets.Client.Home.ChangeAvatarNameMessage import ChangeAvatarNameMessage
from Classes.Packets.Client.Home.AvatarNameCheckRequestMessage import AvatarNameCheckRequestMessage
from Classes.Packets.Server.Authentification.LoginOkMessage import LoginOkMessage
from Classes.Packets.Server.Home.OwnHomeDataMessage import OwnHomeDataMessage
from Classes.Packets.Server.Home.AvailableServerCommandMessage import AvailableServerCommandMessage
from Classes.Packets.Server.Home.AvatarNameCheckResponseMessage import AvatarNameCheckResponseMessage


class LogicLaserMessageFactory:
    messagesList = {
        10101: LoginMessage,
        10212: ChangeAvatarNameMessage,
        14600: AvatarNameCheckRequestMessage,
        20104: LoginOkMessage,
        20300: AvatarNameCheckResponseMessage,
        24101: OwnHomeDataMessage,
        24111: AvailableServerCommandMessage,
    }

    @staticmethod
    def getMessageName(messageType):
        message = LogicLaserMessageFactory.messagesList.get(messageType)
        return message.__name__ if message is not None else str(messageType)

    @staticmethod
    def messageExist(messageType):
        return messageType in LogicLaserMessageFactory.messagesList

    @staticmethod
    def createMessageByType(messageType, messagePayload):
        message = LogicLaserMessageFactory.messagesList.get(messageType)
        if message is None:
            return None
        if Configuration.settings.get('PrintEnabled', False):
            print(messageType, message.__name__)
        return message(messagePayload)
