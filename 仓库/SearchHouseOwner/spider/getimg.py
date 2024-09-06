import requests
import re
import json

from main import ganji_get_house_list

ganji_cookies = {
    "citydomain":"bj",
    "GANJISESSID":"9494bf5be0f46c68ef6a59b863bbb7a1",
    "ganji_uuid":"9403229930635847422817",
    "statistics_clientid":"me",
    "ganji_xuuid":"c720999a-a2f2-4e7a-a131-f7396a107e56.1453881537397",
    "webimFangTips":"2373545737",
    "bdshare_firstime":"1453881578145",
    "_gl_tracker":"%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%2220%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A57522360749%7D",
}

req_img_url = "http://bj.ganji.com/ajax.php"
test_url = "http://bj.ganji.com/fang1/1816620948x.htm"

"""
<input id="fphone" value="MTUyMTA2MDgwNDIyMA==" type="hidden">
<input id="ca_id" value="20" type="hidden">
<input id="puid" value="1816620948" type="hidden">
<input id="street" value="chaoyangqita" type="hidden">
<input id="house_type" value="1" type="hidden">
"""

def getimg(u):
    try:
        if isinstance(u, requests.Response): r = u
        else: r = requests.get(u)
        partial_phone = re.search("contact-mobile\">[^<]*", r.text).group(0)
        params = {
            "fphone" : re.search('"fphone" value="([^"]*)"', r.text).group(1),
            "ca_id"  : re.search('"ca_id" value="([^"]*)"', r.text).group(1),
            "puid"   : re.search('"puid" value="([^"]*)"', r.text).group(1),
            "dir"    : "house",
            "module" : "get_detail_viewer_login_status",
        }
        r = requests.get(req_img_url, params=params, cookies=ganji_cookies)
        r = json.loads(r.text)["phoneshow"]
        r = r[r.index('"')+1:r.rindex('"')]
        r = "http://bj.ganji.com" + r
        return r
    except Exception as e:
        print(e)
        return None

def get_and_save_img(url, filename):
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)

if __name__ == "__main__":
    for p in ganji_get_house_list("chaoyang", pages=2):
        print(p)
        img_url = getimg(p)
        if img_url:
            filename = p[p.rindex("/")+1:p.rindex(".")]
            get_and_save_img(img_url, filename)
