import os
import asyncio
import Configuration
from Classes.AsyncServerConnection import AsyncServerConnection
from Classes.ServerConnection import ServerConnection

print(r"""
    ____                      __   _____ __                 
   / __ )_________ __      __/ /  / ___// /_____ ___________
  / __  / ___/ __ `/ | /| / / /   \__ \/ __/ __ `/ ___/ ___/
 / /_/ / /  / /_/ /| |/ |/ / /   ___/ / /_/ /_/ / /  (__  ) 
/_____/_/   \__,_/ |__/|__/_/   /____/\__/\__,_/_/  /____/  
                                                            
    """)

if Configuration.settings.get("UseAsyncServer", True):
    asyncio.run(AsyncServerConnection(("0.0.0.0", 9339)).serve_forever())
else:
    ServerConnection(("0.0.0.0", 9339))
