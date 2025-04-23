import certifi
print(certifi.where())

import ssl
import socket
from dotenv import load_dotenv
load_dotenv()
hostname = "127.0.0.1"
ctx = ssl.create_default_context()
with socket.create_connection((hostname, 8080)) as sock:
    with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
        cert = ssock.getpeercert()
        print(cert)