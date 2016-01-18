__author__ = 'shibin'

f= open("./dictionary/knowledgeBase.txt","r",encoding='utf-8')
d = open("./dictionary/testttt.txt","w",encoding='utf-8')

diction = f.readlines()
words = ()
diction = set(diction)
for word in diction:
    if word == "\n":
        continue
    word = word.replace("\n"," ")
    word = word.strip("\t")
    word = word.replace("  ","")
    d.write(word+"\n")
f.close()
d.close()