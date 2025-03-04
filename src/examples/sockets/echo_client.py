import asyncio
from pathlib import Path


# https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-client-using-streams
async def tcp_echo_client(message):
    reader, writer = await asyncio.open_unix_connection(Path("/", "tmp", "echo-server.sock"))

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(tcp_echo_client('Hello World!'))
