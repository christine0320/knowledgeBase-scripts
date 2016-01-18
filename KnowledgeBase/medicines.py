import re
from pymongo import MongoClient
import pinyin

conn = MongoClient('192.168.10.108',27017)
db = conn.knowledgeBase
mediciness = db.knowledgeBase

level1 = re.compile('^\d+\.(\w+)\n')
level2 = re.compile('^\d+\.\d+\.(\w+)\n')
level3 = re.compile('^\d+\.\d+\.\d+[\.|\s]((\w| )+)\n')

f = open("./texts/medicine.txt","r",encoding='utf-8')
w = open("./dictionary/medicine.txt","w",encoding='utf-8')
index = {}
medicine_name = []

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
    words = wordslist()
    rank = ()
    sort = ()
    medic = []
    keyword = ()
    for word in words:
        name = word[0].strip('\n')
        name = name.strip(" ")
        datasource = word[1]
        if name in result:
            keyword +=((name,datasource),)
    names = med_name.split(' ')
    name_med = names[0].strip('\n')
    # print(names[0].strip('\n'))
    rank = (("rankone",type1),("ranktwo",type2),("rankthree",name_med,))
    rank += (("source","medicine"),)
    index = {"index":name_med};

    levela = re.compile('【(\w+)】([\w。；（(.)）、：~/，%]+)')
    medic += [{'药品名称':med_name.strip('\n')},]
    if type3:
        medic += [{'药品类别':type3},]
    item = re.finditer(levela,result)
    for i in item:
        medic += [{i.group(1).strip('￥'):i.group(2).strip('￥')},]
    keyword = set(keyword)
    res = []
    for it in keyword:
        keysss = {}
        keysss["name"] = it[0]
        keysss["datasource"] = it[1]
        res += [keysss,]
    key_word = {"keyword":res}
    medic = {"content":medic}
    meds = medic.copy()
    meds.update(key_word)
    meds.update(dict(rank))
    sort = {"sortrankone":pinyin.get(str(type1).strip('\n')),"sortranktwo":pinyin.get(str(type2).strip('\n')),"sortrankthree":pinyin.get(str(med_name).strip('\n')),}
    meds.update(sort)
    meds.update(index)
    print(meds)
    mediciness.insert(meds)


content = []
line = f.readline()
while line:
    if re.match(level1,line):
        type1 = re.match(level1,line).group(1)
        type2 = ''
        type3 = ''
        line = f.readline()
        continue
    if re.match(level2,line):
        type2 = re.match(level2,line).group(1)
        type3 = ''
        line = f.readline()
        continue
    if re.match(level3,line):
        type3 = re.match(level3,line).group(1)
        line = f.readline()
        continue
    content.append(line)
    if '￥' in line:
        med_name = content[0]
        result = "".join(content[1:])
        result = result.replace('￥','')
        result = result.replace('\n','')
        result = result.replace(' ','')
        insertMongo(result)

        content=[]
        medicine_name = med_name.split(' ')
        print(med_name)
        # print(medicine_name[0].strip('\n'))
        w.write(medicine_name[0].strip('\n')+"$$"+"medicine"+"\n")
    line = f.readline()

f.close()
w.close()







