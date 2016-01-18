__author__ = 'shibin'
import re
from pymongo import MongoClient
import pinyin

conn = MongoClient('192.168.10.108',27017)
db = conn.knowledgeBase
knowledgeBase = db.knowledgeBase

level1 = re.compile('^＃+(.*)\n')
level2 = re.compile('【(.*)】+(.*)\n')
content = []
tag = 0
f = open("./texts/diag_tech.txt","r",encoding='utf-8')
w = open("./dictionary/diag_tech.txt","w",encoding='utf-8')
line = f.readline()
keyword = []
global words
global item
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
    global keyword
    keyword = []
    tech = []
    if cont == None:
        pass
    tech = [{"技术名称":[type1]},]
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
        if '【' in item:
            if flaga == 1:
                tech += [{key:value},]
                #print("key=="+key+"value: :"+str(value)+'\n\n\n')
            else: flaga=1
            item = item.replace('【','')
            item = item.replace('】','')
            key = item.replace(' ','')
            key = key.strip('\n')
            value = []
            continue
        else:
            value.append(item)
    #print("key=="+key+"value::"+str(value)+'\n\n\n')
    tech += [{key:value},]
    keyword = set(keyword)
    result = []
    for i in list(keyword):
        keysss = {}
        keysss["name"] = i[0]
        keysss["datasource"] = i[1]
        result += [keysss,]
    print(result)
    key_word = {"keyword":result}
    print(tech)
    tech = {"content":tech}
    tech.update(key_word)
    rank = (("rankone",str(type1).strip('\n')),("ranktwo",""),("rankthree",""),("source","diag_tech"),)
    tech.update(dict(rank))
    sort = (("sortrankone",pinyin.get(str(type1).strip('\n'))),("sortranktwo",""),("sortrankthree",""),)
    index = {"index":type1.strip('\n')}
    tech.update(index)
    tech.update(dict(sort))
    w.write(type1.strip('\n')+"$$"+"diag_tech"+"\n")


    knowledgeBase.insert(tech)
    print(tech)
    #print(keyword)

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
        #print(type1)
        tag = 1
        line = f.readline()
        continue
    if tag != 0:
        content.append(line)
    line = f.readline()
insertMongo(content)
