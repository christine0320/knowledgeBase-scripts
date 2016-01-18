__author__ = 'shibin'
import re
from pymongo import MongoClient
import pinyin

conn = MongoClient('192.168.10.108',27017)
db = conn.knowledgeBase
knowledgeBase = db.knowledgeBase


content = []
tag = 0
type1 = 0
key = ''
value = ''
level1 = re.compile('^[a-z]+\.+(.*)\n')

f = open("./texts/emergency.txt","r",encoding='utf-8')
w = open("./dictionary/emergency.txt","w",encoding='utf-8')
line = f.readline()

def wordslist():
    wordlist = ()
    knowdict = open("./dictionary/knowledgeBase.txt","r",encoding='utf-8')
    words = knowdict.readlines()
    for word in words:
        if word == "\n":
            continue
        word = word.strip("\n")
        res = word.split("$$")
        wordlist += ((res[0],res[1]),)
    knowdict.close()
    return(wordlist)

def insertMongo(cont):
    global key
    global value
    keyword = []
    emergency = []
    if cont == None:
        pass
    emergency = [{"症状名称":type1},]
    flaga = 0
    for item in content:
        words = wordslist()
        for word in words:
            name = word[0].strip('\n')
            name = name.strip(" ")
            datasource = word[1]
           # print('--------------%r-------------' % word)
            if name in item:
                keyword +=((name,datasource),)
        if re.match(level1,item):
            if flaga == 1:
                emergency += [{key:value},]
                #print("key=="+key+"value::"+str(value)+'\n\n\n')
            else: flaga=1
            key = re.match(level1,item).group(1)
            key = key.strip('\n')
            value = []
            continue
        else:
            value.append(item)
    #print("key=="+key+"value::"+str(value)+'\n\n\n')
    emergency += [{key:value},]
    #emergency = dict(emergency)
    keyword = set(keyword)
    result = []
    for i in list(keyword):
        keysss = {}
        keysss["name"] = i[0]
        keysss["datasource"] = i[1]
        result += [keysss,]
    print(result)
    key_word = {"keyword":result}
    emergency = {"content":emergency}
    emergency.update(key_word)
    rank = (("rankone",type1.strip('\n')),("ranktwo",""),("rankthree",""),("source","emergency"),)
    emergency.update(dict(rank))
    index = {"index":type1.strip('\n')}
    sort = (("sortrankone",pinyin.get(str(type1).strip('\n'))),("sortranktwo",""),("sortrankthree",""),)
    emergency.update(index)
    emergency.update(dict(sort))
    w.write(str(type1).strip('\n')+"$$"+"emergency"+"\n")
    knowledgeBase.insert(emergency)
   # print(knowledgeBase)

while line:
     if line == '\n':
        line = f.readline()
        continue
     if '＃' in line:
         if tag ==1:
             insertMongo(content)
         else:tag =1
         if len(content) != 0:
             content=[]
         type1 = line.replace('＃','')
         type1 = type1.replace(' ','')
         print(type1)
         tag = 1
         line = f.readline()
         continue
     if tag != 0:
         content.append(line)
     line = f.readline()
insertMongo(content)