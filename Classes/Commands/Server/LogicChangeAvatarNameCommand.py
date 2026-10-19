from Classes.ByteStream import ByteStream


class LogicChangeAvatarNameCommand(ByteStream):
    def encode(self, fields):
        self.writeString(fields["Name"])
        self.writeVInt(0)  # name change cost
        self.writeString('')  # secondary name string (v69 native +48)
        self.writeVInt(0)  # TickWhenGiven
        self.writeVInt(0)  # ExecuteTick
        self.writeVLong(0, 0)  # ExecutorAccountID
        self.writeVInt(0)  # server command ID (native +28)
        return self.messagePayload

    def getCommandType(self):
        return 201
