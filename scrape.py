print("Warning: This program scrapes the entirety of the ScryFall database via its api, one page at a time.")
print("There are approximately 1420 pages total. This process will take approximately 40 minutes.")
print("Would you like to continue?")
verify = input("y/n:")
if verify != "y":
    quit()
print("Initializing...")

import requests
import time

p = 1

f = open("data.txt", "w")
f.truncate(0)
f.close()

e = open("errors.txt", "w")
e.truncate(0)
e.close()

f = open("data.txt", "a")

e = open("errors.txt", "a")

print("Initialized.")
while(True):
    URL = "https://api.scryfall.com/cards/?page=" + str(p)

    r = requests.get(url = URL)

    data = r.json()

    cards = data["data"]

    for card in cards:
        if card["lang"] == "en" and"flavor_text" in card:
            ftext = card["flavor_text"].replace("\n", " ")
            try:
                f.write(ftext)
                f.write("\n")
            except:
                uri = card["uri"]
                print(uri)
                e.write(uri)
                e.write("\n")
    
    if not data["has_more"]:
        break;
    
    time.sleep(1)
    
    if p%10 == 0:
        print(p + " pages read")
    p += 1