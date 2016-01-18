__author__ = 'shibin'
import re
from pymongo import MongoClient
import pinyin

conn = MongoClient('192.168.10.108',27017)
db = conn.knowledgeBase
knowledgeBase = db.diag_rule

level1 = re.compile('^第(.*?)章+(.*)\n')
level2 = re.compile('^第(.*?)节+(.*)\n')


f = open("texts/diag_rule.txt","r",encoding='utf-8')
# w = open("knowledgeBase/dictionary/diag_rule.txt","w",encoding='utf-8')

content = []
tag = 0

line = f.readline()
keyword = []
value = []
global words
global item


def insertMongo(cont):
    print(type3+'#########')
    print(cont)
    # global keyword
    # global key
    # global value
    # keyword = []
    # tech = []
    # if cont == None:
    #     pass
    # tech = [{"名称":[type3]},]
    # flaga = 0
    # for item in content:
    #     if '【' in item:
    #         print(content)
    #         if flaga == 1:
    #             tech += [{key:value},]
    #             #print("key=="+key+"value: :"+str(value)+'\n\n\n')
    #         else: flaga=1
    #         item = item.replace('【','')
    #         item = item.replace('】','')
    #         key = item.replace(' ','')
    #         key = key.strip('\n')
    #         value = []
    #         continue
    #     else:
    #         value.append(item)
    # #print("key=="+key+"value::"+str(value)+'\n\n\n')
    # tech += [{key:value},]
    # print(tech)
    # keyword = set(keyword)
    # result = []
    # for i in list(keyword):
    #     keysss = {}
    #     keysss["name"] = i[0]
    #     keysss["datasource"] = i[1]
    #     result += [keysss,]
    #
    # key_word = {"keyword":result}
    #
    # tech = {"content":tech}
    # tech.update(key_word)
    # rank = (("rankone",type1.strip('\n')),("ranktwo",type2.strip('\n')),("rankthree",type3.strip('\n')),("source","diag_rule"),)
    # tech.update(dict(rank))
    # sort = (("sortrankone",pinyin.get(str(type1).strip('\n'))),("sortranktwo",pinyin.get(str(type2).strip('\n'))),("sortrankthree",pinyin.get(str(type3).strip('\n'))),)
    # index = {"index":type3.strip('\n')}
    # tech.update(index)
    # tech.update(sort)
    # w.write(str(type3).strip('\n')+"$$"+"diag_rule"+"\n")
    #
    # #knowledgeBase.insert(tech)
    # print(tech)
    # #print(keyword)

while line:
    if line == '\n':
        line = f.readline()
        continue
    if re.match(level1,line):
        type1 = re.match(level1,line).group(2)
        type1 = type1.replace(" ","")
        # print(type1)
        line = f.readline()
        continue
    if re.match(level2,line):
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