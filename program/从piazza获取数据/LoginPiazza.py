__author__ = 'zhangyanni'

#coding='utf-8'
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
    



#�������ݵ��ļ���  
def saveFile(file_name,data):
    output = codecs.open(file_name+".txt",'w',"utf-8")
    output.write(data)
    output.close()   
    print("already write to "+file_name+".txt")


#���ú�����¼��piazza
piazza_login()
    



