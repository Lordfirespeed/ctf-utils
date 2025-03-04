import asyncio
from pathlib import Path


# https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams
async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()

    print(f"Received {message!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_unix_server(handle_echo, Path("/", "tmp", "echo-server.sock"))

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
