class NotificationFactory:
    NotificationsList = {

    }

    def createNotificationByType(notificationID, messagePayload):
        NotificationsList = NotificationFactory.NotificationsList
        if NotificationFactory.messageExist(notificationID):
            if type(NotificationsList[notificationID]) == str:
                pass
            else:
                return NotificationsList[notificationID](messagePayload)
        else:
            print(notificationID, "skipped")
            return None