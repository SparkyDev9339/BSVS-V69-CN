import random
from Classes.ClientsManager import ClientsManager

class Gameroom:
    def create(self, roomID, roomType, map_id, playerID):
        count = len(ClientsManager.rooms)
        new_room = {'index': count, 'roomID': roomID, 'roomType': roomType, 'map_id': map_id, 'players': [{'id': playerID, 'isOwner': 1, 'state': 2}],'invites':[]}
        ClientsManager.rooms.append(new_room)