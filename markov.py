import random
import requests
import string

MAX_TWEET_LENGTH = 280

#TODO refactor this to use postgres database

class Chain():
    lines = []
    words = []
    links = {}
    isSetup = False

    @staticmethod
    def setup():
        f = open("data.txt", "r")
        Chain.lines = f.read().split("\n")
        for line in Chain.lines:
            Chain.words.append(line.split(" "))

        for ind, line in enumerate(Chain.words):
            eol = line.index("EOL")
            source = ""
            first = True
            for i in range(eol+1, len(line)):
                if not first:
                    source += " "
                first = False
                source += line[i]
            
            for i in range(0, eol-1):
                key1 = line[i]
                key2 = line[i+1]
                word = line[i+2]
                link = Link(word, source, ind)
                if (key1, key2) in Chain.links:
                    Chain.links[(key1, key2)].append(link)
                else:
                    Chain.links[(key1, key2)] = [link]
    
    def __init__(self):
        #Sets up the chain, but does not make it. Use make()
        if not Chain.isSetup:
            Chain.setup()
            Chain.isSetup = True
        self.solution = []

    def __repr__(self):
        if len(self.solution) == 0:
            self.make() #This shouldn't happen but just in case
        output = ""
        first = True
        for elem in self.solution:
            if not first:
                output += " "
            first = False
            output += elem.word
        return output

    def make(self):
        #reset chain to blank
        self.solution = []

        #init
        startindex = random.randint(1, len(Chain.lines))
        startline = Chain.words[startindex]
        indEOL = startline.index("EOL")
        startsource = ""
        first = True
        for i in range(indEOL+1, len(startline)):
            if not first:
                startsource += " "
            first = False
            startsource += startline[i]
        
        key1 = Link(startline[0], startsource, startindex)
        key2 = Link(startline[1], startsource, startindex)

        #if the line picked is too short, just grab another line
        key = (key1, key2)
        if key[0].word == "EOL" or key[1].word == "EOL":
            self.make()
            return None
        self.solution.append(key[0])
        self.solution.append(key[1])

        #recursively grab
        while True:
            word = random.choice(Chain.links[(key[0].word, key[1].word)])
            if word.word == "EOL" or len(self.solution) > 100:
                break
            self.solution.append(word)
            key = (key[1], word)
        
        #check to see if it matches a particular line exactly: if so, make a new chain
        isDuplicate = True
        for elem in self.solution:
            if not elem.source == startsource:
                isDuplicate = False
        if isDuplicate:
            self.make()

        return None
    
    def trace(self):
        #Trace for log. Don't post this.
        if len(self.solution) == 0:
            self.make()
        output = ""
        for elem in self.solution:
            pad = " "*(20 - len(elem.word))
            output += elem.word + pad + elem.source + "\n"
        return output
    
    def fulltrace(self):
        #Mostly unused.
        if len(self.solution) == 0:
            self.make()
        output = ""
        first = True
        for i, elem in enumerate(self.solution):
            pad = " "*(20 - len(elem.word))
            output += elem.word + pad + elem.source + "\n"
            if not first and not elem.word == "EOL":
                key = (self.solution[i-1].word, self.solution[i].word)
                for j in Chain.links[key]:
                    output += j.word + " "
                output += "\n"
            first = False
        print(output)
        return(output)

class Link():

    def __init__(self, word, source, lineindex):
        self.word = word
        self.source = source
        self.lineindex = lineindex

def markov():
    chain = Chain()
    chain.make()
    return chain

def main():
    print(markov())

if __name__ =="__main__":
    main()