print("Warning: This program scrapes the entirety of the ScryFall database via its api, one page at a time.")
print("There are approximately 1420 pages total. This process will take several minutes.")
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
            line = card["flavor_text"]
            line = line + " EOL " + card["name"] + " " +  card["set_name"]
            line = line.replace("\n", " ")
            line = line + "\n"
            try:
                f.write(line)
            except:
                uri = card["uri"]
                print(uri)
                e.write(uri)
                e.write("\n")
    
    if not data["has_more"]:
        break;
    
    time.sleep(.1)
    
    if p%10 == 0:
        print(str(p) + " pages read")
    p += 1