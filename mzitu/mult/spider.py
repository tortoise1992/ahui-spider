# -*- coding=UTF-8 -*-
# __author__ ='ahui'
# 这是一个多进程的爬虫
from pyquery import PyQuery as pq
import requests
import time
import json
import os
import re
import multiprocessing
class MzSpider():
    def __init__(self):
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }
        self.baseUrl='http://www.mzitu.com'
        self.pageUrl='http://www.mzitu.com/page/'
        self.savePath=os.path.abspath(os.path.dirname(__file__))+r'\images'

    def get_html(self,url):
        response = requests.get(url,headers=self.headers).text
        return pq(response)
    def get_byte(self,url,header):
        return requests.get(url,headers=header).content

    def get_refer_header(self,url):
        # copy_header=self.headers.copy()
        # referer_header=copy_header.update({'Referer':url})
        return {'Referer':url}

    def make_dir(self,absPath, name):
        name = name.strip().replace('?', '')
        name = name.strip().replace(':', '')
        if not os.path.exists(absPath + '\\' + name):
            os.makedirs(absPath + '\\' + name)
        return absPath + '\\' + name

    def change_work_dir(self,realPath):
        os.chdir(realPath)

    def get_max_pages(self,html):
        max_page = re.search(r'.*?(\d+)', str(html('.page-numbers span').eq(8))).group(1)
        max_page = int(max_page)
        return max_page

    def save_img(self,refer,imgPath,title,index):
        filename = imgPath.split(r'/')[-1]
        if not os.path.exists(filename):
            time.sleep(0.5)
            print('正在下载>>>%s下第%d张图片' % (title, index))
            data = self.get_byte(imgPath,self.get_refer_header(refer))
            with open(filename, 'wb') as f:
                f.write(data)
            print('>>>%s下第%d张图片保存完毕' % (title, index))

    def start(self):
        pool=multiprocessing.Pool(multiprocessing.cpu_count())

        base_html=self.get_html(self.baseUrl)
        max_page=self.get_max_pages(base_html)
        for i in range(1,max_page+1):
            page_url=self.pageUrl+str(i)
            page_html=self.get_html(page_url)
            page_list = page_html('#pins li a img')
            for item in page_list.items():
                title = item.attr('alt')
                href = item.parent().attr('href')
                print('准备爬取套图----%s' % title)
                save_path=self.make_dir(self.savePath,title)
                self.change_work_dir(save_path)
                detail_html=self.get_html(href)
                print('>>> %s页面爬取完毕' % title)
                print('正在进行下一级解析...')
                span = detail_html('.pagenavi span')
                length = int(span.eq(6).text())
                for j in range(1,length+1):
                    links=href+'/'+str(j)
                    img_data = self.get_html(links)
                    img_path = img_data('.main-image a img').attr('src')
                    # print(href)
                    pool.apply_async(self.save_img,(href,img_path,title,j))
                    # self.save_img(href,img_path,title,j)
        pool.close()
        pool.join()
        print('全部图片下载完毕')

if __name__ == '__main__':

    spider=MzSpider()
    spider.start()