__author__ = 'shibin'
import re
from pymongo import MongoClient
import pinyin

conn = MongoClient('192.168.10.108',27017)
db = conn.knowledgeBase
knowledgeBase = db.knowledgeBase

level1 = re.compile('^第(.*?)节+(.*)\n')
level2 = re.compile('^[a-z]+\.+(.*)\n')
content = []

keyword = []
tag = 0
type1 = 0
key = ''
value = ''
f = open("./texts/common_symptons.txt","r",encoding='utf-8')
w = open("./dictionary/common_symptons.txt","w",encoding='utf-8')
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
    keyword = []
    global key
    global value
    symps = []
    if cont == None:
        pass
    symps=[{"症状名称":[type1]},]
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
        if re.match(level2,item):
            if flaga == 1:
                symps += [{key:value},]
                #print("key=="+key+"value::"+str(value)+'\n\n\n')
            else: flaga=1
            key = re.match(level2,item).group(1)
            key = key.strip('\n')
            value = []
            continue
        else:
            value.append(item)
    #print("key=="+key+"value::"+str(value)+'\n\n\n')
   # sympton += ((key,value),)
    keyword = set(keyword)

    result = []
    for i in list(keyword):
        keysss = {}
        keysss["name"] = i[0]
        keysss["datasource"] = i[1]
        result += [keysss,]
    print(result)
    key_word = {"keyword":result}


    print(symps)
    sympton = {"content":symps }
    sympton.update(key_word)
    rank = (("rankone",str(type1).strip('\n')),("ranktwo",""),("rankthree",""),("source","common_symptom"),)
    sympton.update(dict(rank))
    sort = (("sortrankone",pinyin.get(str(type1).strip('\n'))),("sortranktwo",""),("sortrankthree",""),)

    index = {"index":str(type1).strip('\n')}
    sympton.update(index)
    sympton.update(dict(sort))

    w.write(str(type1)+"$$"+"common_symptom"+"\n")
    knowledgeBase.insert(sympton)
    print(sympton)
    #common_symptons.insert(sympton)


while line:
    if line == '\n':
        line = f.readline()
        continue
    if re.match(level1,line):
        insertMongo(content)
        if len(content) != 0:
            content=[]
        type1 = re.match(level1,line).group(2)
        type1 = type1.replace(' ','')
        tag = 1
        line = f.readline()
        continue
    if tag ==1:
        content.append(line)
    line = f.readline()
insertMongo(content)
