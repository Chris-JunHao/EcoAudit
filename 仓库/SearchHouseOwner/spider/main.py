import sys
import re
import requests
import bs4
import codecs
import sqlite3
try:
    import leancloud
    from leancloud import Object
    from leancloud import Query


    leancloud.init('aIvRjO9nNktIWXYTORzbIoQS-gzGzoHsz', 'XedakwWQtCVo5ADjvdHm3gw6')

    class HouseInfo(leancloud.Object):
        def __init__(self, **kwargs):
            super(HouseInfo, self).__init__()
            for k, v in kwargs.items():
                self.set(k, v)
    query = Query(HouseInfo)
except ImportError:
    pass

def ganji_get_house_list(district, pages=1):
    result = []
    for i in range(1, pages+1):
        r = requests.get("http://bj.ganji.com/fang1/"+district+"/a1o%d"%i)
        result = re.findall("/fang./[^.]*\.htm", r.text)
        for s in result:
            yield "http://bj.ganji.com"+s

def ganji_get_house_page(url):
    try:
        result = dict()
        result["source"] = url
        result["site"] = "ganji"
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        result["title"] = soup.find("h1", "title-name").text
        result["create_at"] = re.sub("[^-0-9: ]*", "", soup.find("ul", "title-info-l").text)
        basic = soup.find("div", class_="basic-box")
        result["img"] = basic.find("div", "basic-imgs-big").find("img")['src']
        ul = basic.find("ul", "basic-info-ul")
        lis = ul.find_all("li")
        result["price"] = lis[0].find("b", "basic-info-price").text
        result["huxing"] = lis[1].text.strip()
        result["gaikuang"] = lis[2].text.strip()
        result["louceng"] = lis[3].text.strip()
        result["xiaoqu"] = lis[4].find('a')["title"]
        result["weizhi"] = "-".join(map(lambda x: x.text, lis[5].find_all('a')))
        result["peizhi"] = lis[7].text.strip()

        result["owner"] = basic.find("div", "contact-person").text.strip()
        result["phone"] = basic.find("em", "contact-mobile").text.strip()

        for k, v in result.items():
            if k == "create_at": continue
            result[k] = re.sub(r"(\n|\t|\r| |\xa0)", "", v)
        return result

    except Exception as e:
        print(e)
        return None

def wuba_get_house_list(district):
    result = []
    for i in range(1, 71):
        r = requests.get("http://bj.58.com/"+district+"/chuzu/pn%d"%i)
        result = re.findall("http://jump.zhineng.58.com/clk[^\"]*", r.text)
        for s in result:
            yield s

def wuba_get_house_page(url):
    try:
        result = dict()
        result["source"] = url
        result["site"] = "wuba"
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        result["title"] = soup.find("h1", "main-title").text
        result["create_at"] = re.sub("[^-0-9: ]*", "", soup.find("div", "title-right-info").find("span").text)
        basic = soup.find("ul", "house-primary-content")
        result["img"] = soup.find("img", id="smainPic")["src"]
        lis = basic.find_all("li", "house-primary-content-li")
        result["price"] = lis[0].find("em", "house-price").text
        des = lis[1].text
        m = re.search(u"(.*)-\xa0([0-9/]*)\u5c42", des, re.DOTALL)
        result["huxing"] = m.group(1)
        result["gaikuang"] = des[des.index(u"\u5c42")+1:]
        result["louceng"] = m.group(2)
        result["xiaoqu"] = " ".join(map(lambda x: x.text, lis[2].find("div", "fl").find_all("a")[:-2]))
        if len(lis) > 4:
            result["weizhi"] = lis[3].text
            result["peizhi"] = lis[4].text
        else:
            result["weizhi"] = ""
            result["peizhi"] = lis[3].text

        result["owner"] = soup.find("span", "f18").text
        result["phone"] = soup.find("span", "tel-num").text

        for k, v in result.items():
            if k == "create_at": continue
            result[k] = re.sub(r"(\n|\t|\r| |\xa0)", "", v)
        return result
    except Exception as e:
        print(e)
        return None

def save_to_leancloud(d):
    h = HouseInfo(**d)
    h.save()

def run():
    #pages = ganji_get_house_list("chaoyang")
    pages = wuba_get_house_list("chaoyang")
    for p in pages:
        print(p)
        query.equal_to('source', p)
        if not query.find():
            r = wuba_get_house_page(p)
            if r: save_to_leancloud(r)

def test():
    with codecs.open("output.txt", "w", "utf-8") as f:
        pages = ganji_get_house_list("chaoyang")
        for p in pages:
            print(p)
            f.write("-"*50+"\n")
            r = ganji_get_house_page(p)
            if not r: print(p)
            if r:
                for k, v in r.items():
                    f.write(k+"|"+v+"\n")

if __name__ == "__main__":
    #run()
    #r = wuba_get_house_list("chaoyang")
    test()
