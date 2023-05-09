#!/usr/bin/python3
import requests
import json
import sys
import difflib
from termcolor import colored

response = requests.get("https://raw.githubusercontent.com/Fyrd/caniuse/main/data.json")
data = response.json()

with open("data.json", "w") as data_file:
    new_data = {}
    for key, value in data["data"].items():
        if key.startswith("css-"):
            new_key = key.replace("css-", "")
        else:
            new_key = key
        new_data[new_key] = value
    data_file.write(json.dumps(new_data, indent=2))

keys = list(new_data.keys())

if len(sys.argv) > 3:
    print("Too many arguments. Please provide at most 2 arguments.")
    exit()
else:
    for input in sys.argv[1:]:
        matches = difflib.get_close_matches(input, keys, 1, 0.7)
        if matches:
            best_match = matches[0]
            chrome = new_data[best_match]["stats"]["chrome"]
            chrome_key = chrome.get(list(chrome.keys())[-1])
            safari = new_data[best_match]["stats"]["safari"]
            safari_key = safari.get(list(safari.keys())[-1])
            firefox = new_data[best_match]["stats"]["firefox"]
            firefox_key = firefox.get(list(firefox.keys())[-1])
            if chrome_key == "y" and firefox_key == "y" and safari_key == "y":
                print(colored("All GOOD", "green"))
            elif not chrome_key == "y":
                print(colored("No Support in chrome", "red"))
            elif not safari_key == "y":
                print(colored("No Support in safari", "red"))
            elif not firefox_key == "y":
                print(colored("No Support in firefox", "red"))
        else:
            print(f"{input}: No such feature was found!")
