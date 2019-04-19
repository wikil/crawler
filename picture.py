# -*- coding:UTF-8 -*-
import requests,json,time,sys
from contextlib import closing

class get_photos(object):
    def __init__(self):         #基本参数
        self.photosID = []
        self.headers = {'authorization':'Client-ID c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626'}
        self.target = 'http://unsplash.com/napi/feeds/home'
        self.download_server1 = 'https://unsplash.com/photos/'
        self.download_server2 = '/download?force=trues'


    def get_ids(self):     #获得图片ID
        req = requests.get(url=self.target, headers=self.headers, verify=False)
        html = json.loads(req.text)
        next_page = html['next_page']
        for photo in html['photos']:
            self.photosID.append(photo['id'])
        time.sleep(1)
        for i in range(5):
            req = requests.get(url = next_page , headers = self.headers , verify = False)
            html = json.loads(req.text)
            next_page = html['next_page']
            for photo in html['photos']:
                self.photosID.append(photo['id'])
            time.sleep(1)

    def download_picture(self,photo_id,filename):          #访问下载并保存在本地
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
        target = self.download_server1+photo_id+self.download_server2
        with closing(requests.get(url=target, stream=True, verify=False, headers=self.headers)) as r:
            with open('photos\%d.jpg'%filename,'ab+') as f:
                for chunk in r.iter_content(chunk_size= 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()


if __name__ =='__main__':
    gp = get_photos()
    print('获取图片链接ing')
    gp.get_ids()
    print('图片下载中:')
    for i in range(len(gp.photosID)):
        print('正在下载第%d张图片' % (i+1))
        gp.download_picture(gp.photosID[i],(i+1))





# if __name__ == '__main__':
#     target = 'http://unsplash.com/napi/feeds/home'
#     headers = {'authorization':'Client-ID c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626','Referer':'https: // unsplash.com /'}
#
#
#     req = requests.get(url=target,headers = headers, verify=False)
#     html = json.loads(req.text)
#     next_page = html['next_page']
#     print(next_page)
#     for photo in html['photos']:
#
#         print('图片ID',photo['id'])