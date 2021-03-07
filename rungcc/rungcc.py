import os
import pyuv
import signal
import subprocess

from rungcc.utils import replace_special_chars

HOSTNAME = '127.0.0.1'
PORT = 8080

loop = pyuv.Loop.default_loop()
signal_h = pyuv.Signal(loop)
server = pyuv.TCP(loop)
clients: list[pyuv.TCP] = []

server.bind((HOSTNAME, PORT))

root_path = os.path.dirname(os.path.realpath('__file__'))
cpp_source_file = os.path.join(root_path, "sandbox/src/main.cpp")


def on_tcp_read(client: pyuv.TCP, data, error):
    if not data:
        print("Client disconnected, closing connection")
        client.close()
        clients.remove(client)
        return
    print(f"Got data [{data}]")
    req = data.split(b'\r\n')[0].split(b'\x20')
    setup = ""
    output = ""
    with open("index.html", "r") as fh:
        index = fh.read()
    if req[0] == b'POST':
        params = data.split(b'\r\n')[-1]
        print(params)
        source = params.split(b'&')[0].split(b'=')[1].decode("utf-8")
        print(source)
        source = replace_special_chars(source)
        with open(cpp_source_file, "w") as fh:
            fh.write(source)
        cmd_setup = ["docker", "build", "-t", "myapp", "sandbox"]
        cmd_run = ["docker", "run", "myapp"]
        try:
            setup = subprocess.check_output(cmd_setup).decode("utf-8")
        except Exception as e:
            setup = "Build failed: " + str(e)
        try:
            output = subprocess.check_output(cmd_run).decode("utf-8")
        except Exception as e:
            output = "Build failed: " + str(e)
    else:
        with open(os.path.join(root_path, "examples/helloworld.cpp")) as fh:
            source = fh.read()
    index = index.replace("<%source>", source)
    index = index.replace("<%setup>", setup)
    index = index.replace("<%output>", output)
    client.write("HTTP/1.1 200 OK\r\n\r\n".encode("utf-8"))
    client.write(index.encode("utf-8"))
    client.write(b'\r\n')
    client.close()
    clients.remove(client)


def on_tcp_connection(server: pyuv.TCP, error):
    client = pyuv.TCP(server.loop)
    server.accept(client)
    clients.append(client)
    client.start_read(on_tcp_read)


def signal_callback(handle, signum):
    [c.close() for c in clients]
    signal_h.close()
    server.close()


def main():
    server.listen(on_tcp_connection)
    signal_h.start(signal_callback, signal.SIGINT)
    loop.run()
