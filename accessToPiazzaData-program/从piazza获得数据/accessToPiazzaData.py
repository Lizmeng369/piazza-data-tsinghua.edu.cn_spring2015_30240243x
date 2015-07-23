__author__ = 'zhangyanni'

#coding='utf-8'
import gzip
import http.cookiejar
import urllib.request
import urllib.parse
import json
import codecs
import socket


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
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
        'X-Requested-With':'XMLHttpRequest'
        }
    #postDict�ǵ�¼ʱ��post�ı�
   
    email = input('������piazza�û�����')
   
    password = input('���������룺')
    print('��¼��...')
    postDict = {'from': '/signup','email':email ,'password': password , 'remember': 'on'}
    postData = urllib.parse.urlencode(postDict).encode()


   
    url = 'https://piazza.com/class/'

    req = urllib.request.Request (url,postData,header)
    response=urllib .request .urlopen(req)
    data=response.read()
    data = ungzip(data)
    #��¼��piazza����get��¼�����ҳ������piazza_logindata.txt
    data=data.decode(encoding='UTF-8',errors='ignore')
    saveFile("piazza-login-data",data)
    print("��¼�ɹ���")
    


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
    socket.setdefaulttimeout(20)
    try:
        req = urllib.request.Request(url,postData,header_new)
        response=urllib .request .urlopen(req)
        data=response.read()
        data = ungzip(data)
        data=data.decode() 
        #����data������
        myjson=json.loads(data)
        newjson=json.dumps(myjson,ensure_ascii=False)
        return newjson
    except:
        print("timeout")
        return "timeout"

#�������ݵ��ļ���  
def saveFile(file_name,data):
    output = codecs.open("piazza-data/"+file_name+".json",'w',"utf-8")
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
print("------------------------------------------------------------------------")
select = input('��ȡȫ�����ۼ�¼������1����ȡĳһ�����ۼ�¼������2��')
nid=input("����������nid ���磺https://piazza.com/class/i5j09fnsl7k5x0?cid=493��nidΪi5j09fnsl7k5x0��") 
if select=='1':   
    
    postJson={"method":"network.get_my_feed","params":{"nid":nid,"sort":"updated"}}
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
        print(nr)
        postJson={"method":"content.get","params":{"cid":nr,"nid":"i5j09fnsl7k5x0"}}
        data=piazza_getdata_from_api(postJson)
        file_name=str(nr)
        saveFile(file_name,data)
elif select=='2':
    #���cid��json����
    while(1):
                     
        cid=input('���������ۼ�¼��id(���磺https://piazza.com/class/i5j09fnsl7k5x0?cid=493��idΪ493)��')
        postJson={"method":"content.get","params":{"cid":cid,"nid":nid}}
        data=piazza_getdata_from_api(postJson)
        file_name=str(cid)
        saveFile(file_name,data)
        exit_2=input('�˳�?(y/n)��')
        if exit_2=='y':
            break
        
    
        
                   

   



