import os
import time
import requests
from bs4 import BeautifulSoup

class Belle(object):

    def __init__(self, url):
        self.url = url
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
            "Referer": "https://www.mzitu.com/209835"
        }
        self.title = ""
        self.soup = ""
        self.path = ""

    def get_soup(self, url):
        result = requests.get(url, headers=self.header, timeout=50)
        html = result.content.decode("utf-8")
        self.soup = BeautifulSoup(html, "lxml")
        return self.soup

    def get_title(self):
        self.title = self.soup.find("h2").get_text()
        print(f"此篇写真标题是: {self.title}")
        self.path = os.path.join(os.path.split(__file__)[0], "清纯妹子", self.title)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        print(f"图片保存路径是：{self.path}")

    def get_all_num(self):
        # 通过第一页链接获取总的页数
        soup = self.get_soup(self.url)
        next_link = soup.select(".pagenavi a span")
        all_num = [i.get_text() for i in next_link][4]
        self.all_num = all_num
        # print(all_num)

    def find_jpg(self):
        temp_img = self.soup.select("p a img")
        img_src = [i.get("src") for i in temp_img]
        if img_src:
            return img_src[0]
        else:
            return None

    def find_jpgs(self):
        all_imgs = []
        temp_img = self.soup.select("p a img")
        img_src = [i.get("src") for i in temp_img][0]
        # 由第一张图片链接和总的页数拼成所有图片链接
        for i in range(1, int(self.all_num)+1):
            num = "%02d" % i
            img_link = img_src.replace("01.jpg", f"{num}.jpg")
            all_imgs.append(img_link)
        print(f"共有{len(all_imgs)}张图片")
        return all_imgs

    def down_jpg(self, nameint, img_url):
        # 开始下载图片
        name = str(nameint + 1) + ".jpg"
        print(f"开始下载图片{name}-------->")
        res = requests.get(img_url, headers=self.header)
        if res.status_code == 404:
            print(f"图片{img_url}下载出错------->")
        img_name = os.path.join(self.path, name)
        with open(img_name, "wb") as f:
            f.write(res.content)
        print(f"图片{name}下载完成--------->")

    def run(self):
        # 获取所有页面链接
        self.get_all_num()
        self.get_title()
        all_imgs = self.find_jpgs();
        for num, jpglink in enumerate(all_imgs):
            self.down_jpg(num, jpglink)
            time.sleep(2)


class DownloadImg(object):

    def __init__(self):
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
            "Referer": "https://www.mzitu.com/209835"
        }
        self.title = ""
        self.soup = ""
        self.path = ""

    def get_soup(self, url):
        result = requests.get(url, headers=self.header, timeout=50)
        html = result.content.decode("utf-8")
        self.soup = BeautifulSoup(html, "lxml")
        return self.soup

    def run(self):
        input("妹子写真套图爬虫：windows用户下载后图片在当前目录下，mac用户下载的图片在用户根目录下，按回车即可开始下载？")
        # 生产每一页url地址
        for i in range(10, 12):
            #templete = f"https://www.mzitu.com/mm/page/{i}/"
            templete = f"https://www.mzitu.com/xinggan/page/{i}/"
            # 提取地址中的图文链接
            soup = self.get_soup(templete)
            img_links = soup.select("li span a")
            #print([i.get("href") for i in zipai_links])
            for j in img_links:
                href = j.get("href");
                print(f"开始爬取链接:{href}")
                try:
                    Belle(href).run()
                    time.sleep(2)
                except Exception as e:
                    continue
        print("所有图片已经下载完成！")


if __name__ == '__main__':
   DownloadImg().run()
