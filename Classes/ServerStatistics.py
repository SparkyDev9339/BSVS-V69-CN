import asyncio
import psutil
import time
from Classes.ClientsManager import ClientsManager

class ServerStatistics:
    def __init__(self):
        self.process = psutil.Process()
        self.start_time = time.time()
        self.total_packets_received = 0
        self.total_packets_sent = 0

    async def run_statistics_loop(self, interval=60):
        print("Server statistics started...")
        while True:
            await asyncio.sleep(interval)
            
            uptime = int(time.time() - self.start_time)
            clients_count = ClientsManager.GetCount()
            cpu_usage = self.process.cpu_percent()
            ram_usage = self.process.memory_info().rss / (1024 * 1024)
            
            print(f"--- Server Statistics ---")
            print(f"Uptime: {uptime}s | Connected Clients: {clients_count}")
            print(f"CPU Usage: {cpu_usage:.1f}% | RAM Usage: {ram_usage:.1f} MB")
            print(f"Packets Received: {self.total_packets_received} | Packets Sent: {self.total_packets_sent}")
            print(f"-------------------------")

# Global instance to be used everywhere
stats = ServerStatistics()
