from urllib.request import Request, urlopen
import json
import string

# Function that gets the entire text from the json

def get_text(ver="akjv", bk=None, ch=None):
    
    if bk == None:
        bibleURL = "https://getbible.net/v2/%s.json" %(ver)
    elif ch == None:
        bibleURL = "https://getbible.net/v2/%s/%s.json" %(ver, bk)
    else:
        bibleURL = "https://getbible.net/v2/%s/%s/%s.json" %(ver, bk, ch)
    

    req = Request(
        url=bibleURL,
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    resp = urlopen(req)
    data = json.loads(resp.read())
    allWords = ""

    if bk == None:
        for book in data["books"]:
            for chapter in book["chapters"]:
                for verse in chapter["verses"]:
                    allWords += verse["text"]
                    allWords += " "

    elif ch == None:
        for chapter in data["chapters"]:
            for verse in chapter["verses"]:
                allWords += verse["text"]
                allWords += " "

    else:
        for verse in data["verses"]:
            allWords += verse["text"]
            allWords += " "

    
    return allWords


def top_words(text, n=10):
    # split words
    splitWords = text.split()

    # strip leading and trailing punc
    for i in range(len(splitWords)):
        splitWords[i] = stripPunc(splitWords[i])

    # filter stopwords
    f = open("./stopwords.txt", 'r')
    stopwords = []
    while True:
        line = f.readline()
        if not line:
            break
        parsedLine = line.split()
        for word in parsedLine:
            stopwords.append(word)
    
    # preprocess words
    preprocessedWords = []
    for word in splitWords:
        if len(word) > 1 and word.lower() not in stopwords:
            preprocessedWords.append(word)

    # dictionary
    dict = {}
    for word in preprocessedWords:
        if word in dict.keys():
            dict[word] += 1
        else:
            dict[word] = 1

    # get keys and values
    keys = []
    values = []
    for key in dict.keys():
        keys.append(key)
        values.append(dict[key])
    
    # descending sort the values
    values.sort(reverse=True)

    # sliced dictionary
    slicedDict = {}
    for i in range(n):
        value = values[i]
        for key in keys:
            if dict[key] == value:
                slicedDict[key] = value
                keys.remove(key)
                break

    return slicedDict

def stripPunc(word):
    while len(word) > 0 and word[0] in string.punctuation:
        word = word[1:]

    while len(word) > 0 and word[len(word) - 1] in string.punctuation:
        word = word[:len(word) - 1]

    return word
    
# The sample run in the given question.

if __name__ == "__main__":
    versions = ["akjv", "kjv", "web"]
    torah = {"Gen": 1, "Ex": 2, "Lev": 3, "Num": 4, "Deut": 5} 
    gospel = {"Matt": 40, "Mark": 41, "Luke": 42, "John": 43}

    scripture = get_text("web", torah["Gen"], 1) # chapter 
    words = top_words(scripture)
    print("Gen1:\n", words)

    for g in gospel: # book
        scripture = get_text(bk=gospel[g]) 
        words = top_words(scripture) 
        print(g + ":\n", words)

    for v in versions:  # bible
        scripture = get_text(v)
        words = top_words(scripture)
        print(v + ":\n", words)