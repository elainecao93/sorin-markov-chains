import random
import requests
import string

MAX_TWEET_LENGTH = 280

#initialize outside functions
words = []
chain = {}

f = open("data.txt", "r")
raw = f.read()

lines = raw.split("\n")

for line in lines:
    line = line + " EOL"
    words.append(line.split(" "))
        
for line in words:
    for i, key1 in enumerate(line):
        if key1 == "EOL":
            break
        key2 = line[i+1]
        if key2 == "EOL":
            break
        word = line[i+2]
        if (key1, key2) in chain:
            chain[(key1, key2)].append(word)
        else:
            chain[(key1, key2)] = [word]

def markov():
    randstart = random.randint(1, len(lines))
    key = (words[randstart][0], words[randstart][1])
    if "EOL" in key:
        return markov()
    output = key[0] + " " + key[1]
    while True:
        word = random.choice(chain[key])
        if word == "EOL" or len(output) > 400:
            break
        output = output + " " + word
        key = (key[1], word)
    if output in lines:
        return markov()
    return output

def main():
    print(markov())

if __name__ =="__main__":
    main()