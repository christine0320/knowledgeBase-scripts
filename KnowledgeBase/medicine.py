#coding: utf-8
import os.path
import re
from pymongo import MongoClient
import os
dir = os.path.abspath(__file__)
print(dir)
base = os.path.dirname(dir)
#os.mkdir(base+"/"+"la")
print(os.curdir)
print(base)

conn = MongoClient('192.168.10.108',27017)
db = conn.knowledgeBase
mediciness = db.medicine

level1 = re.compile('^\d+\.(\w+)\n')
level2 = re.compile('^\d+\.\d+\.(\w+)\n')
level3 = re.compile('^\d+\.\d+\.\d+[\.|\s]((\w| )+)\n')

f = open("./texts/medicine.txt","r",encoding='utf-8')
w = open("./dictionary/medicine.txt","w",encoding='utf-8')

content = []

line = f.readline()
line = f.readline()
line = f.readline()
count = 0

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

while line :
    medinfo = ()
    medic = ()
    keyword = []
    if re.match(level1,line):
        type1 = re.match(level1,line).group(1)
        # print(line)
        print(type1)
        line = f.readline()
        type2 = None
        type3 = None
        continue
    if re.match(level2,line):
        type2 = re.match(level2,line).group(1)

        # print(line)
        print(type2)
        type3 = None
        line = f.readline()
        continue
    if re.match(level3,line):
        type3 = re.match(level3,line).group(1)
        # print(line)
        print(type3)
#     print(line)
        line = f.readline()
        continue
    content.append(line)
    if '￥' in line:
        #count +=1
        #if count >10:
        #    break
        #content.append(line)
        medicine = content[0]
    #    print("medicine: "+ content[0].strip('\n'))
        words = wordslist()

        result = "".join(content[1:])
        for word in words:
            name = word[0].strip('\n')
            name = name.strip(" ")
            datasource = word[1]
           # print('--------------%r-------------' % word)
            if name in result:
                keyword +=((name,datasource),)
        result = result.replace('￥','')
        result = result.replace('\n','')
        result = result.replace(' ','')
        levela = re.compile('【(\w+)】([\w。；（(.)）、：~/，%]+)')
        # levela = re.compile('【(\w+)】')
        last = re.finditer(levela,result)
        if type1:
            medinfo += (("rankone",type1),)
        if type2:
            medinfo += (("ranktwo",type2),)
        if type3:
            medinfo += (("rankthree",type3),)
        medic += (('药品名称',content[0].strip('\n')),)
        #medinfo = (("rankone",type1),("ranktwo",type2),("rankthree",type3),)
        for i in last:
        #    print("key: "+i.group(1)+"\n"+"value:"+i.group(2))
            medic += ((i.group(1).strip('￥'),i.group(2).strip('￥')),)
        keyword = set(keyword)
        res = []
        for it in keyword:
            keysss = {}
            keysss["name"] = it[0]
            keysss["datasource"] = it[1]
            res += [keysss,]
        print(res)
        key_word = {"keyword":res}

        medic = {"medicines":dict(medic)}
        medinfo = dict(medinfo)
        meds = medinfo.copy()
        meds.update(medic)
        meds.update(key_word)
        rank = (("rankone",""),("ranktwo",""),("ranktwoConcept",""),("rankthree",""),("source","medicine"),)
        meds.update(dict(rank))

        if type3:
            index = ''
            w.write(str(type3)+"\n")
            index = {"index":str(type3).strip('\n')}
            meds.update(index)

        elif type2:
            index = ''
            w.write(str(type2)+"\n")
            index = {"index":str(type2).strip('\n')}
            meds.update(index)
        else:
            index = ''
            w.write(str(type1)+"\n")
            index = {"index":str(type1).strip('\n')}
            meds.update(index)
        mediciness.insert(meds)
        print(meds)

        content=[]
    line = f.readline()
f.close()
w.close()
