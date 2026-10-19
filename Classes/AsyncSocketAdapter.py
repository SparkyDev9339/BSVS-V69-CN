import asyncio
import threading

import Configuration


class AsyncSocketAdapter:
    """
    Provides a minimal socket-like API (`send`, `close`) on top of an asyncio
    StreamWriter so existing code can keep using `fields["Socket"].send(...)`.
    """

    def __init__(self, writer: asyncio.StreamWriter):
        self._writer = writer
        self._loop = asyncio.get_running_loop()
        self._loop_thread = threading.current_thread()
        self._queue: "asyncio.Queue[bytes | None]" = asyncio.Queue(maxsize=1024)
        self._queued_bytes = 0
        self._max_queued_bytes = Configuration.settings.get("MaxSendQueueBytes", 4 * 1024 * 1024)
        self._closed = False
        self._sender_task = asyncio.create_task(self._sender(), name="socket-sender")

    def send(self, data) -> int:
        if self._closed:
            return 0

        if isinstance(data, bytearray):
            data = bytes(data)
        elif not isinstance(data, (bytes,)):
            data = bytes(data)

        def _enqueue():
            if self._closed:
                return
            try:
                if self._queued_bytes + len(data) > self._max_queued_bytes:
                    self.close()
                    return
                self._queue.put_nowait(data)
                self._queued_bytes += len(data)
            except asyncio.QueueFull:
                # Backpressure: if the client doesn't read, close it to avoid OOM.
                self.close()

        if threading.current_thread() is self._loop_thread:
            _enqueue()
        else:
            self._loop.call_soon_threadsafe(_enqueue)

        return len(data)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True

        def _shutdown():
            try:
                self._queue.put_nowait(None)
            except Exception:
                # If the queue is full (backpressure), force-stop the sender.
                try:
                    self._sender_task.cancel()
                except Exception:
                    pass
            try:
                self._writer.close()
            except Exception:
                pass

        if threading.current_thread() is self._loop_thread:
            _shutdown()
        else:
            self._loop.call_soon_threadsafe(_shutdown)

    async def aclose(self) -> None:
        self.close()
        try:
            await self._sender_task
        except (Exception, asyncio.CancelledError):
            pass

    async def _sender(self) -> None:
        try:
            while True:
                data = await self._queue.get()
                if data is None:
                    break
                self._writer.write(data)
                await asyncio.wait_for(
                    self._writer.drain(),
                    timeout=Configuration.settings.get("WriteTimeout", 7),
                )
                self._queued_bytes -= len(data)
        except (ConnectionError, OSError, asyncio.TimeoutError):
            pass
        finally:
            self._closed = True
            while not self._queue.empty():
                self._queue.get_nowait()
            self._queued_bytes = 0
            try:
                self._writer.close()
            except Exception:
                pass
            try:
                await asyncio.wait_for(self._writer.wait_closed(), timeout=1)
            except Exception:
                pass
