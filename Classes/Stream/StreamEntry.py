from Classes.ByteStream import ByteStream

class StreamEntry:
    def encode(self: ByteStream, info):
        self.writeLong(info['StreamID'][0], info['StreamID'][1]) # StreamEntryID
        self.writeLong(info['PlayerID'][0], info['PlayerID'][1]) # TargetID
        self.writeString(info['PlayerName'])
        self.writeVInt(info['PlayerRole'])
        self.writeVInt(0)
        self.writeBoolean(False)

