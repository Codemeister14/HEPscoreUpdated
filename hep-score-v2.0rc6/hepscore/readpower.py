import subprocess
import requests
import base64
import sys
from datetime import datetime
import socket
import urllib3.util.connection
token = sys.argv[1]
def ipv4_only_create_connection(address, *args, **kwargs):
    kwargs.pop('socket_options', None)
    return socket.create_connection((socket.gethostbyname(address[0]), address[1]), *args, **kwargs)

urllib3.util.connection.create_connection = ipv4_only_create_connection
def get_dell_serial_linux():
    try:
        result = subprocess.run(
            ["sudo", "dmidecode", "-s", "system-serial-number"],
            capture_output=True,
            text=True,
            check=True
        )
        serial_number = result.stdout.strip()
        return serial_number
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

with open("/tmp/perf_output.txt", "r") as f:
    powerData = f.read()
fileName = f"{get_dell_serial_linux()}+{datetime.now()}"

url = f"https://api.github.com/repos/Codemeister14/HEPscoreData/contents/{fileName}Power.txt"
headers = {"Authorization": f"token {token}"}
data = {
    "message": "commited",
    "content": base64.b64encode(powerData.encode()).decode(),
    "branch": "main",
}

res = requests.put(url, headers=headers, json=data)
res.raise_for_status()
print(" File committed")
with open("power.json", "r") as f:
    powerData = f.read()

fileName2 = f"{get_dell_serial_linux()}+{datetime.now()}"

url = f"https://api.github.com/repos/Codemeister14/HEPscoreData/contents/{fileName2}.json"
headers = {"Authorization": f"token {token}"}
data = {
    "message": "commited",
    "content": base64.b64encode(powerData.encode()).decode(),
    "branch": "main",
}

res = requests.put(url, headers=headers, json=data)
res.raise_for_status()
print("second file commited")