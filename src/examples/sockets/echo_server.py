import asyncio
from asyncio import StreamReader, StreamWriter
from pathlib import Path


# https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams
async def handle_echo(reader: StreamReader, writer: StreamWriter) -> None:
    data = await reader.read(100)
    message = data.decode()
    print(f"Received {message!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()


async def handle_echo_uppercase(reader: StreamReader, writer: StreamWriter) -> None:
    data = await reader.read(100)
    message = data.decode()
    print(f"Received {message!r}")

    response = message.upper()
    print(f"Send: {response!r}")
    writer.write(response.encode())
    await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()


async def main():
    echo_server = await asyncio.start_unix_server(handle_echo, Path("/", "tmp", "echo-server.sock"))
    echo_uppercase_server = await asyncio.start_unix_server(handle_echo_uppercase, Path("/", "tmp", "echo-uppercase-server.sock"))

    addrs = ', '.join(str(sock.getsockname()) for server in (echo_server, echo_uppercase_server) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with echo_server, echo_uppercase_server:
        await echo_server.serve_forever()
        await echo_uppercase_server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
