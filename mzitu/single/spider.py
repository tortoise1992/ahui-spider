# -*- coding=UTF-8 -*-
# __author__ ='ahui'
from pyquery import PyQuery as pq
import requests
import time
import json
import os
import re
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}
base_url='http://www.mzitu.com'
page_url='http://www.mzitu.com/page/'
save_path=os.path.abspath(os.path.dirname(__file__))+r'\images'
# print(save_path)
def get_html(url,header):
    response=requests.get(url,header).text
    return pq(response)

def make_dir(absPath,name):
    name=name.strip().replace('?','')
    name=name.strip().replace(':','')
    if not os.path.exists(absPath+'\\'+name):
        os.makedirs(absPath+'\\'+name)
def change_dir(absPath,name):
    name = name.strip().replace('?', '')
    name = name.strip().replace(':', '')
    os.chdir(absPath + '\\' + name)

base_html=get_html(base_url,headers)
max_page=re.search(r'.*?(\d+)',str(base_html('.page-numbers span').eq(8))).group(1)
max_page=int(max_page)

for n in range(1,3):
    links=page_url+str(n)
    page_html=get_html(links,headers)
    page_list=page_html('#pins li a img')
    for item in page_list.items():
        title=item.attr('alt')
        href=item.parent().attr('href')
        print('准备爬取套图----%s' % title)
        make_dir(save_path,title)
        change_dir(save_path,title)
        # print(href)
        detail_html=get_html(href,headers)
        print('>>> %s页面爬取完毕' % title)
        print('正在进行下一级解析...')
        span = detail_html('.pagenavi span')
        length = int(span.eq(6).text())
        for i in range(1,length+1):
            gos=href+'/'+str(i)
            header_img={
                'Referer': href
            }
            img_data=get_html(gos,headers)
            img_path = img_data('.main-image a img').attr('src')
            filename=img_path.split(r'/')[-1]
            if not os.path.exists(filename):
                time.sleep(0.5)
                print('正在下载>>>%s下第%d张图片' % (title,i))
                data=requests.get(img_path,headers=header_img).content
                with open(filename,'wb') as f:
                    f.write(data)
                print('>>>%s下第%d张图片保存完毕' % (title,i))
print('全部图片下载完毕')