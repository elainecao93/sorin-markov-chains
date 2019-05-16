import random
import requests
import string

MAX_TWEET_LENGTH = 280

class Chain():
    lines = []
    words = []
    chain = {}
    isSetup = False

    @staticmethod
    def setup(): #TODO set up the chains
        f = open("data.txt", "r")
        Chain.lines = f.read().split("\n")
        for line in Chain.lines:
            line = line + " EOL"
            Chain.words.append(line.split(" "))

        for line in Chain.words:
            for i, key1 in enumerate(line):
                if key1 == "EOL":
                    break
                key2 = line[i+1]
                if key2 == "EOL":
                    break
                word = line[i+2]
                if (key1, key2) in Chain.chain:
                    Chain.chain[(key1, key2)].append(word)
                else:
                    Chain.chain[(key1, key2)] = [word]
    
    def __init__(self):
        if not Chain.isSetup:
            Chain.setup()
            Chain.isSetup = True
    
    def make(self):
        randstart = random.randint(1, len(Chain.lines))
        key = (Chain.words[randstart][0], Chain.words[randstart][1])
        if "EOL" in key:
            self.make()
            return self.output
        output = key[0] + " " + key[1]
        while True:
            word = random.choice(Chain.chain[key])
            if word == "EOL" or len(output) > 400:
                break
            output = output + " " + word
            key = (key[1], word)
        if output in Chain.lines:
            self.make()
            return self.output
        self.output = output
        return output

def main():
    test = Chain()
    test.make()
    print(test.output)

if __name__ =="__main__":
    main()