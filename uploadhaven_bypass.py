import sys
import requests
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm

if len(sys.argv) != 4:
	print(sys.argv[0] + ": <uploadhaven link> <save to> <site where you got the link from>")
	print("\nexample:")
	print(sys.argv[0] + " https://uploadhaven.com/download/3a27143bbc81d2b25e174e30dbed3876 game.zip https://steamunlocked.org")
	exit()

print(r"""
   _____     _           _ _                   
  |  |  |___| |___ ___ _| | |_ ___ _ _ ___ ___ 
  |  |  | . | | . | .'| . |   | .'| | | -_|   |
  |_____|  _|_|___|__,|___|_|_|__,|\_/|___|_|_|
        |_|  by https://github.com/m3xploit                               
""")

uploadhaven_url = sys.argv[1]

session = requests.Session()
base_req = session.get(uploadhaven_url, headers={
	"Referer": sys.argv[3] # Bypasses hotlink protection
})

soup = BeautifulSoup(base_req.text, features="lxml")

for input_tag in soup.find_all("input"):
	if input_tag.get("name") == "_token":
		_token = input_tag.get("value")  # hidden in post form

	if input_tag.get("name") == "key":
		key = input_tag.get("value")     # hidden in post form

	if input_tag.get("name") == "hash":
		hash = input_tag.get("value")    # hidden in post form

	if input_tag.get("name") == "time":
		time = input_tag.get("value")    # hidden in post form


print("[+] Dumped _token : " + _token)
print("[+] Dumped key    : " + key)
print("[+] Dumped hash   : " + hash)
print("[+] Dumped time   : " + time)

print("[*] Waiting 15 seconds for uploadhaven to grant our download ...")
sleep(16)

post_req = session.post(uploadhaven_url, data={
	"_token": _token,
	"key": key,
	"time": time,
	"hash": hash,
	"type": "premium" # Hehehehhe
})

new_soup = BeautifulSoup(post_req.text, features="lxml")

# Parse download link out of HTML received from HTTP post response
for a in new_soup.find_all("a"):
	if a.get("target") == "_new" and "uploadhaven.com" in a.get("href"):
		link = a.get("href")
		break

# loadingbar
file_req = session.get(link, stream=True)
total_size = int(file_req.headers.get("content-length", 0))

with open(sys.argv[2], "wb") as file, tqdm(
    desc=sys.argv[2],
    total=total_size,
    unit="B",
    unit_scale=True,
    unit_divisor=1024,
) as bar:
    for chunk in file_req.iter_content(chunk_size=1024):
        size = file.write(chunk)
        bar.update(size)