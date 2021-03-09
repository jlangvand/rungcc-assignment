# Copyright (C) 2021  Joakim Skogø Langvand

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import pyuv
import signal
import subprocess

from rungcc.utils import replace_special_chars, html_safe

HOSTNAME = '127.0.0.1'
PORT = 8080

loop = pyuv.Loop.default_loop()
signal_h = pyuv.Signal(loop)
server = pyuv.TCP(loop)
clients: list[pyuv.TCP] = []

server.bind((HOSTNAME, PORT))

root_path = os.path.dirname(os.path.realpath('__file__'))
cpp_source_file = os.path.join(root_path, "sandbox/src/main.cpp")

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.DEBUG)


def on_tcp_read(client: pyuv.TCP, data, error):
    if not data:
        logging.info("No data received, closing connection")
        client.close()
        clients.remove(client)
        return
    req = data.split(b'\r\n')[0].split(b'\x20')
    setup = ""
    output = ""
    logging.debug("Got a %s request", req[0])
    with open("index.html", "r") as fh:
        index = fh.read()
    if req[0] == b'POST':
        params = data.split(b'\r\n')[-1]
        source = params.split(b'&')[0].split(b'=')[1].decode("utf-8")
        source = replace_special_chars(source)
        with open(cpp_source_file, "w") as fh:
            logging.debug("Loading template file")
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
    index = index.replace("<%source_html>", html_safe(source))
    client.write("HTTP/1.1 200 OK\r\n\r\n".encode("utf-8"))
    client.write(index.encode("utf-8"))
    client.write(b'\r\n')
    client.close()
    clients.remove(client)


def on_tcp_connection(server: pyuv.TCP, error):
    client = pyuv.TCP(server.loop)
    logging.info("Client connected")
    server.accept(client)
    clients.append(client)
    client.start_read(on_tcp_read)


def signal_callback(handle, signum):
    logging.debug("signal_callback called")
    [c.close() for c in clients]
    signal_h.close()
    server.close()


def main():
    server.listen(on_tcp_connection)
    logging.info("Listening for connections on %s:%d", HOSTNAME, PORT)
    signal_h.start(signal_callback, signal.SIGINT)
    loop.run()
