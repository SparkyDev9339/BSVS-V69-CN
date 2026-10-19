
# DisableNagle: reduce delay and improve performance between client and server BUT require more power #

settings = {
    "DisableNagle": True,
    "PrintEnabled": False,
    "ReadTimeout": 7,
    "IdleTimeout": 120,
    "WriteTimeout": 7,
    "MaxPacketSize": 1024 * 1024,
    "MaxSendQueueBytes": 4 * 1024 * 1024,
    "UseAsyncServer": True,
    "UseContentUpdater": False,
    "Proxy": False,
    "DumpPacket": False,
    "Blacklist": [24109],
    "DumpMajor": 69
}
