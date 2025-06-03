import subprocess
import requests
import base64
import sys
from datetime import datetime

token = sys.argv[1]

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