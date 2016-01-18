__author__ = 'shibin'
import re
from pymongo import MongoClient
import pinyin

conn = MongoClient('192.168.10.108',27017)
db = conn.knowledgeBase
knowledgeBase = db.diag_rule

level1 = re.compile('^第(.*?)章+(.*)\n')
level2 = re.compile('^第(.*?)节+(.*)\n')


f = open("./texts/diag_rule.txt","r",encoding='utf-8')
w = open("./dictionary/diag_rule.txt","w",encoding='utf-8')

line = f.readline()
print(line)
content = []
tag = 0
type1 = '心血管疾病'
type2 = '高血压'
diseaseName = "原发性高血压"
diseaseinfo = []
key = []
value = []
def wordslist():
    wordlist = ()
    knowdict = open("./dictionary/knowledgeBase.txt","r",encoding='utf-8')
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
    global value
    global key
    keyword = []

    diseaseinfo = [{"名称":[diseaseName.strip("#")]},]
    print(diseaseName)
    if cont == None:
        pass
    # flaga 防止第一次存到上一个药的key value
    flaga = 0
    for item in cont:
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
                diseaseinfo += [{key:value},]
                #print("key=="+key+"value::"+str(value)+'\n\n\n')
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
    disease = (("rankone",type1),("ranktwo",type2),("rankthree",diseaseName),)
    diseaseinfo = {"content":diseaseinfo}
    dis = dict(disease).copy()
    dis.update(diseaseinfo)
    keywords = set(keyword)
    result = []

    for i in list(keywords):
        keysss = {}
        keysss["name"] = i[0]
        keysss["datasource"] = i[1]
        result += [keysss,]
    #print(result)
    key_word = {"keyword":result}
    dis.update(key_word)
    w.write(str(diseaseName).strip('\n')+"$$"+"diag_rule"+"\n")
    sort = (("sortrankone",pinyin.get(str(type1).strip('\n'))),("sortranktwo",pinyin.get(str(type2).strip('\n'))),("sortrankthree",pinyin.get(str(diseaseName).strip('\n'))),)
    index = {"index":diseaseName}
    dis.update(dict(sort))
    dis.update(index)
    source = {"source":"diag_rule"}
    dis.update(source)

    #print('-----------------######\n'+ str(dis)+'\n-----------------$$$$$$$\n')
    knowledgeBase.insert(dis)


while line:
    if line == "\n":
        line = f.readline()
        continue

    if re.match(level1,line):
        type1 = re.match(level1,line).group(2)
        type1 = type1.replace(" ","")
        line = f.readline()
        continue

    if re.match(level2,line):
        type2 = re.match(level2,line).group(2)
        type2 = type2.replace(" ","")
        type2 = type2.strip("\t")
        line = f.readline()

    if "＃" in line:
        line = line.replace('＃','')
        line = line.replace(' ','')
        line = line.strip("\n")
        diseaseName = line

        if tag ==1:
            diseaseName
            insertMongo(content)
        else:
            tag = 1
        if len(content) != 0:
             content = []
        line = f.readline()
        continue

    if "#" in line:
        line = line.replace('#','')
        line = line.replace(' ','')
        line = line.strip("\n")
        diseaseName = line
        if tag ==1:
            print(diseaseName+"!!!!!")
            insertMongo(content)
        else:
            tag = 1
        if len(content) != 0:
            content = []
        line = f.readline()
        continue

    if tag ==1:
        content.append(line)
    line = f.readline()
    #print(type1+"~~~"+type2+"~~~")
    #print(content)
print(diseaseName+"~~~~~")
insertMongo(content)
