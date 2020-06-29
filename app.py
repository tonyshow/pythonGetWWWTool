# coding:utf-8
import re
import requests
import base64
import datetime
import time
import datetime
import os
import sys
import urllib.request
import urllib
import shutil
import threading
import json
import urllib.request as ur

#解析html里面的所有连接 https://www.cnblogs.com/chengxuyuanaa/p/12986320.html
from bs4 import BeautifulSoup

# https://www.cnblogs.com/ppwang06/p/12469157.html
from urllib.parse import urlparse

currPath = os.path.dirname(__file__)
currPathFull= os.path.abspath(os.path.dirname(__file__))
# 是否为忽略类型文件
def isIgnoreType(fPath):
    isBool=False
    for _fileType in cfg["noNeedCheckFileTypes"]["value"]:
        if(fPath.find(_fileType)>=0): 
            isBool=True
    return isBool       

def downloadFinsh(fName,localFName,fInfo):
    print("下载完成{}".format( localFName))
    if( False==isIgnoreType(localFName) ): 
        doFullFile(localFName,fInfo)
 
   
# class Doal(threading.Thread): 
#     def __init__(self,a,b,fName,_downloadFinsh):
#         # 继承类多线程
#         threading.Thread.__init__(self)
#         self.__path=a
#         self.__name=b
#         self.fName=fName
#         self._downloadFinsh= _downloadFinsh;
#     def run(self):
#         #开启实时显示
#         ur.urlretrieve(self.__path,self.__name,self.jindu)
#     def jindu(self,a,b,size): 
#         time.sleep(0.1)
#         per=100*a*b/size
#         per=round(per, 2)
#         if per>100:   
#             self._downloadFinsh(self.fName,self.__name)
#             per=100 
#         sys.stdout.flush()
        
def btoa(info):
    tmp = base64.b64encode(info.encode("utf-8"))
    tmp = str(tmp, "utf-8")
    return tmp


def getMd5():
    f_time = time.time()
    f_time = int(f_time)
    return str(f_time)


def download_file(url, store_path):
    if os.path.isfile(store_path):
        return
    print(url+"->"+store_path)
    file_data = requests.get(url, allow_redirects=True).content
    store_path = store_path.replace("?m=", "")
    with open(store_path, 'wb') as handler:
        handler.write(file_data)


def createFolder(newUrl, _path): 
    filename = os.path.basename(_path) 
    needCreate = _path.replace(filename, "")
    clientPath = os.path.join(os.getcwd(), "client")+needCreate
    if not os.path.exists(clientPath):
        os.makedirs(clientPath) 
    download_file(newUrl, os.path.join(os.getcwd(), "client")+_path) 

# 读取文件内容 
def readFile(fPath):
    try:
        with open(fPath,"r") as file_object:
            content=file_object.read() 
            if(content==""):
                print("\nerror读取到的数据为空:={}".format(fPath))
            return content         
    except:
        return None    
   

# 正则解析网页文件
def pairData(_data):
    if _data==None:
        return
    link_list = re.findall(
    r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')\
    |(?<=src=\").+?(?=\")|(?<=src=\').+?(?=\')\
    |(?<=href=\").+?(?=\")\
    |(?<=exports=\").+?(?=\")"
    , _data,re.M)
    for s in link_list:  
        doDownLoad(s)  
def pairHtml(_data):
    soup=BeautifulSoup(_data)
    # link
    link=[] 
    links=soup.find_all("link",href=True)
    for links in links:
        url=links.get("href")
        print(url)

    # script 
    script=[]
    scripts=soup.select('script',src=True)
    for links in scripts:
        url=links.get("src")
        if(url!=None):
            print(url)


def startUp(url,fullFileLocalPath,fName):
    print("启动下载:{}".format(url))
    r = requests.get(url)
    if( fullFileLocalPath=="" ): 
        urlJData=urlparse(url)
        if( urlJData.path.find('.')>=0 ):
            pairData(r.text) 
        else:
            pairHtml(r.text) 
    else:
        with open(fullFileLocalPath, "wb") as code:
            code.write(r.content) 
            downloadFinsh(fName,fullFileLocalPath,r.text) 
def doDownLoad(fullUrl):
    if fullUrl.find("http")<=-1 :
        print("非法url={}".format(fullUrl))
        return
    # 去掉域名
    # ParseResult(scheme='https', netloc='ww.baidu.com', path='/index.html/index.html', params='', query='', fragment='') 
    urlJData=urlparse(fullUrl)
    needCreateFolr = urlJData.path
 
    if(len(needCreateFolr)==0):
        print("非法url={}".format(fullUrl))
        return; 
    fName=needCreateFolr.split("/")[-1]
 
    needCreateFolr=needCreateFolr[0:-len(fName)]
    if needCreateFolr=="":
        print("非法2url={}".format(fullUrl))
        return 
    if(needCreateFolr[-1]=='/'):
        needCreateFolr=needCreateFolr[0:len(needCreateFolr)-1] 
    clientPath =os.path.abspath(os.path.join(currPathFull,'./client'))  
    fullPath = clientPath+"/"+urlJData.netloc+needCreateFolr
    if not os.path.exists(fullPath):
        print("创建的目录needCreateFolr={},fullPath={}".format(needCreateFolr,fullPath))
        if needCreateFolr.find("https://")>=0:
            return
        if needCreateFolr.find("http://")>=0:
            return
        os.makedirs(fullPath)

    fullFileLocalPath = os.path.join(fullPath,fName)
    isFile = os.path.exists(fullFileLocalPath) 
    if( False == isFile ):
        startUp(fullUrl,fullFileLocalPath,fName) 
        # print("启动下载:{}".format(fullUrl))
        # r = requests.get(fullUrl)
        # with open(fullFileLocalPath, "wb") as code:
        #     code.write(r.content) 
        #     downloadFinsh(fName,fullFileLocalPath,r.text)

def doOneFile(_path):
    fPath= os.path.join( currPathFull, _path)
    fPath=os.path.abspath(fPath); 
    doFullFile(fPath,None)
def doFullFile(fPath,fInfo):
    idxInfo=""
    if( None != fInfo ):
        idxInfo=fInfo
    else: 
        idxInfo = readFile(fPath) 

    if( fPath.find('.html')>=0 ):
        pairHtml(idxInfo) 
    else:
        pairData(idxInfo)
def main(): 
    ctermPath = os.path.abspath(os.path.join(currPathFull,'./client'))  
    if  os.path.exists(ctermPath):  
        shutil.rmtree(ctermPath)
    os.makedirs(ctermPath)
     
    with open("./config.json","r",encoding='utf8') as fp:
        global cfg 
        cfg = json.load(fp) 
        for s in cfg["needDownLoadFiles"]["value"]:
            startUp(s,"","")    
main()
