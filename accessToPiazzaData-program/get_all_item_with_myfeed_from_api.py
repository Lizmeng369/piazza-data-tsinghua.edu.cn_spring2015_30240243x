__author__ = 'zhangyanni'

#coding=utf-8
import gzip
import http.cookiejar
import urllib.request
import urllib.parse
import json
import codecs



#ungzip��ѹ����
def ungzip(data):
    try:        # ���Խ�ѹ
        print('���ڽ�ѹ.....')
        data = gzip.decompress(data)
        print('��ѹ���!')
    except:
        print('δ��ѹ��, �����ѹ')
    return data


#getOpener ��������һ�� head ����, ���������һ���ֵ�. �������ֵ�ת����Ԫ�鼯��, �Ž� opener.
#�Զ�����ʹ�� opener ������������ Cookies
#�Զ��ڷ����� GET ���� POST �����м����Զ���� Header
cj = http.cookiejar.CookieJar()
pro = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(pro)
urllib .request .install_opener(opener)

def piazza_login():
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection':'keep-alive',
        'Host':'piazza.com',
        'Referer:':'https://piazza.com/class/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
        'X-Requested-With':'XMLHttpRequest'
        }
    #postDict�ǵ�¼ʱ��post�ı�
    email = 'jennyzhang8800@163.com'
    password = 'jeny20110607'
    postDict = {'from': '/signup','email':email ,'password': password , 'remember': 'on'}
    postData = urllib.parse.urlencode(postDict).encode()


    #��¼��piazza����get��¼�����ҳ������piazza_data.txt
    url = 'https://piazza.com/class/'

    req = urllib.request.Request (url,postData,header)
    response=urllib .request .urlopen(req)
    data=response.read()
    data = ungzip(data)
    output = open('piazza_login-6-5.txt','w')
    output.write(data.decode())
    output.close()
    print("login suceesful!")
    print('''already write to "piazza_login.txt".''')

#��piazza��api�л��json���ݣ����ݷ��͵�postJson��ͬ��ò�ͬ�����ݣ��ɻ��ĳһ����ǩ���������⣬��ָ��cid��ĳһ������    
def piazza_getdata_from_api(postJson):
    
    header_new={
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Host':'piazza.com',
        'Referer:':'https://piazza.com/class',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
        'X-Requested-With':'XMLHttpRequest'
        }
    
    postData=json.dumps(postJson).encode()
    url="https://piazza.com/logic/api/"
    req = urllib.request.Request(url,postData,header_new)
    response=urllib .request .urlopen(req)
    data=response.read()
    data = ungzip(data)
    data=data.decode() 
    #����data������
    myjson=json.loads(data)
    newjson=json.dumps(myjson,ensure_ascii=False)
    return newjson

#�������ݵ��ļ���  
def saveFile(file_name,data):
    output = codecs.open("result/"+file_name+".json",'w',"utf-8")
    output.write(data)
    output.close()   
    print("already write to "+file_name+".json")
#���ļ�
def readFile(file_name):
    fileIn = codecs.open(file_name,'r',"utf-8")
    data=fileIn.read()
    fileIn.close()
    return data

#���ú�����¼��piazza
piazza_login()
#������������б�,get_my_feed_form_api
postJson={"method":"network.get_my_feed","params":{"nid":"i5j09fnsl7k5x0","offest":170,"sort":"updated"}}
data=piazza_getdata_from_api(postJson)
saveFile("piazza_my_feed",data)

data=readFile("piazza_my_feed.txt")
#�� json�ַ���ת���ֵ䣬���ڽ�������
data_dict=json.loads(data)

dict = {}
#���"result"�µ�"feed"�б�
items=data_dict['result']['feed']
#����items������������id��nr
for item in items:
    id = item['id']
    nr = item['nr']
    dict[nr]=id
#����nr��api����POST���������������json����
for nr in dict.keys():
    postJson={"method":"content.get","params":{"cid":nr,"nid":"i5j09fnsl7k5x0"}}
    data=piazza_getdata_from_api(postJson)
    file_name=str(nr)
    saveFile(file_name,data)



