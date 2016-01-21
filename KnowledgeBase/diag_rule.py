__author__ = 'shibin'
import re
from pymongo import MongoClient
import pinyin

conn = MongoClient('192.168.10.108',27017)
db = conn.knowledgeBase
knowledgeBase = db.knowledgeBase

level1 = re.compile('^第(.*?)章+(.*)\n')
level2 = re.compile('^第(.*?)节+(.*)\n')


f = open("texts/diag_rule.txt","r",encoding='utf-8')
# w = open("knowledgeBase/dictionary/diag_rule.txt","w",encoding='utf-8')

content = []

line = f.readline()
keyword = []
value = []
global words
global item

def wordslist():
    wordlist = ()
    knowdict = open("dictionary/knowledgeBase.txt","r",encoding='utf-8')
    words = knowdict.readlines()
    for word in words:
        if word == "\n":
            continue
        word = word.replace("\n","")
        res = word.split("$$")
        wordlist += ((res[0],res[1]),)
    knowdict.close()
    return(wordlist)

def insertMongo(cont):
    print(type1+'#########')
    print(type2+'#########')
    print(type3+'#########')
    global keyword
    global key
    global value
    keyword = []
    tech = []
    if cont == None:
        pass
    tech = [{"名称":[type3]},]
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

    key_word = {"keyword":result}

    tech = {"content":tech}
    tech.update(key_word)
    rank = (("rankone",type1.strip('\n')),("ranktwo",type2.strip('\n')),("rankthree",type3.strip('\n')),("source","diag_rule"),)
    tech.update(dict(rank))
    sort = (("sortrankone",pinyin.get(str(type1).strip('\n'))),("sortranktwo",pinyin.get(str(type2).strip('\n'))),("sortrankthree",pinyin.get(str(type3).strip('\n'))),)
    index = {"index":type3.strip('\n')}
    tech.update(index)
    tech.update(sort)
    #w.write(str(type3).strip('\n')+"$$"+"diag_rule"+"\n")

    knowledgeBase.insert(tech)
    print(tech)
    # #print(keyword)

tag = 0
while line:
    if line == '\n':
        line = f.readline()
        continue
    if re.match(level1,line):
        if(tag==1):
            insertMongo(content)
            type2=''
            type3=''
            content=[]
            tag=0
        type1 = re.match(level1,line).group(2)
        type1 = type1.replace(" ","")
        # print(type1)
        line = f.readline()
        continue
    if re.match(level2,line):
        if(tag==1):
            insertMongo(content)
            type3=''
            content=[]
            tag=0
        type2 = re.match(level2,line).group(2)
        type2 = type2.replace(" ","")
        # print(type2)
        line = f.readline()
        continue

    if '#' in line:
        if tag ==1:
            insertMongo(content)
        else:tag =1

        if len(content) != 0:
            content=[]
        type3 = line.replace('#','')
        type3 = type3.replace(' ','')
        print(type3)
        tag = 1
        line = f.readline()
        continue

    if tag != 0:
        content.append(line)
    line = f.readline()
insertMongo(content)

f.close()
# w.close()
