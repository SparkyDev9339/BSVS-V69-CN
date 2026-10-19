import asyncio
import socket
import time
import traceback

import Configuration
from Classes.AsyncSocketAdapter import AsyncSocketAdapter
from Classes.ClientsManager import ClientsManager
from Classes.Instances.Classes.Player import Player
from Classes.MessageManager import MessageManager
from Classes.Messaging import Messaging
from Classes.Utility import Utility


class AsyncConnectionContext:
    def __init__(self, writer: asyncio.StreamWriter, address):
        self.client = AsyncSocketAdapter(writer)
        self.address = address
        self.player = Player()
        self.timeout = time.time()


class AsyncServerConnection:
    def __init__(self, address):
        self.address = address

    async def serve_forever(self):
        server = await asyncio.start_server(
            self._handle_client, *self.address, reuse_address=True
        )
        socknames = ", ".join(str(s.getsockname()) for s in (server.sockets or []))
        print(f"Listening for new connection (asyncio): {socknames}")
        async with server:
            await server.serve_forever()

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        address = writer.get_extra_info("peername")
        if address is None:
            address = ("unknown", 0)
        print("New connection with address", address[0], "on port", address[1])

        sock = writer.get_extra_info("socket")
        if sock is not None and Configuration.settings.get("DisableNagle", False):
            try:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            except Exception:
                pass

        ctx = AsyncConnectionContext(writer, address)

        try:
            while True:
                try:
                    header = await asyncio.wait_for(reader.readexactly(7), timeout=Configuration.settings.get("IdleTimeout", 120))
                except asyncio.TimeoutError:
                    print(f"Client with ip: {address} disconnected (timeout)!")
                    break
                except asyncio.IncompleteReadError:
                    print(f"Client with ip: {address} disconnected!")
                    break

                headerData = Messaging.readHeader(header)
                ctx.timeout = time.time()

                payload_len = headerData[1]
                if not 0 <= payload_len <= Configuration.settings.get("MaxPacketSize", 1024 * 1024):
                    break
                if payload_len:
                    try:
                        payload = await asyncio.wait_for(
                            reader.readexactly(payload_len),
                            timeout=Configuration.settings.get("ReadTimeout", 7),
                        )
                    except (asyncio.IncompleteReadError, asyncio.TimeoutError):
                        print(f"Client with ip: {address} disconnected!")
                        break
                else:
                    payload = b""

                if Configuration.settings.get("DumpPacket", False):
                    Utility.dumpPacket(payload, headerData[0])

                MessageManager.receiveMessage(ctx, headerData[0], payload)

        except Exception:
            print(traceback.format_exc())

        finally:
            try:
                allSockets = ClientsManager.GetAll()
                if (
                    ctx.player.ID[1] in allSockets.keys()
                    and allSockets[ctx.player.ID[1]]["Socket"] == ctx.client
                ):
                    ClientsManager.RemovePlayer(ctx.player.ID)
            except Exception:
                pass

            try:
                await ctx.client.aclose()
            except Exception:
                pass
