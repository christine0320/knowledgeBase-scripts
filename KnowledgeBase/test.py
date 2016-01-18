wordlist = ()
knowdict = open("./dictionary/knowledgeBase.txt","r",encoding='utf-8')
words = knowdict.readlines()
for word in words:
    if word == "\n":
        continue
    word = word.strip("\n")
    res = word.split("$$")
    wordlist += ((res[0],res[1]),)
print(wordlist)
knowdict.close()