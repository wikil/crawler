from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import requests
import sys
from urllib.parse import quote,unquote

# html = 'http://www.biqukan.com/0_178/18102757.html'
# ob = urlopen(html)
# bs_ob = bs(ob,'lxml')
# texts = bs_ob.find('div',class_ = 'showtxt',id = 'content')
# print(str(texts).replace('<br/>','\n'))
class downloader(object):
    def __init__(self,name):
        self.server = 'http://www.biqukan.com'
        self.target = 'http://www.biqukan.com/0_178/'
        self.names = []  #章节名
        self.urls = []  #章节链接
        self.nums = 0   #章节数
        self.name = name #书名

    def get_download_url(self):
        req = requests.get(self.target).text
        bs_ob = bs(req, 'lxml')
        bfa = bs_ob.find('div', class_='listmain')
        a = bfa.find_all('a')
        #找到<a>标签
        self.nums = len(a[12:])
        for each_a in a[12:]:
            self.names.append(each_a.string)
            self.urls.append(self.server+each_a.get('href'))

    def get_contents(self,target):
        req = requests.get(url = target).text
        bs_ob = bs(req,'lxml')
        texts = bs_ob.find_all('div',class_ = 'showtxt',id = 'content')
        texts = str(texts[0]).replace('<br/>','\n')
        texts = texts.replace('<div class="showtxt" id="content">','\n')
        return texts

    def writer(self,name,path,text):
        write_flag = True
        with open(path,'a',encoding='utf-8') as f:
            f.write(name+'\n')
            f.writelines(text)
            f.write('\n\n')

    def search_book(self):
        html = 'http://www.biqukan.com/s.php?ie=gbk&q='+quote(self.name)
        req = requests.get(html).text
        bs_oj = bs(req,'lxml')
        a = bs_oj.find('div',class_ = 'bookimg').find('a')
        html = self.server+a.get('href')
        self.target = html


if __name__ =='__main__':
    dl = downloader('青莲剑说')
    dl.search_book()
    dl.get_download_url()
    print('《'+dl.name+'》'+'下载开始：')
    for i in range(dl.nums):
        dl.writer(dl.names[i], dl.name+'.txt', dl.get_contents(dl.urls[i]))
        print('已下载:%.3f' % float(i / dl.nums) + '\n')
    print('《'+dl.name+'》''下载完成')