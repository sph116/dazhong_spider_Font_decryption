import requests
import re

city = "changsha"    #城市
type = "ch10"       #类型
chi_type = "g110"    #实物类型 火锅
page_num = 1

cookie = "navCtgScroll=249.99998474121094; _lxsdk_cuid=16add7c85fcc8-00be7b1db7bd3-6b111b7e-1fa400-16add7c85fcc8; _lxsdk=16add7c85fcc8-00be7b1db7bd3-6b111b7e-1fa400-16add7c85fcc8; _hc.v=0bee915e-80f3-3d44-079d-265d58a5cfa4.1558494087; Hm_lvt_e6f449471d3527d58c46e24efb4c343e=1558513049; Hm_lpvt_e6f449471d3527d58c46e24efb4c343e=1558513049; ctu=cdff7056daa2405159990763801b14e0b43def4154e58456822553457c1bb90e; uamo=15292060685; cy=1; cye=shanghai; s_ViewType=10; _dp.ac.v=507d4bb2-ab5b-4aef-be23-72a941f61eec; _thirdu.c=2e49f7a0d2f79712f2ac8b9066678e5a; thirdtoken=00b4ac8f-60c6-45bf-ad32-c6aabb7ba467; dper=8948a6230638aa3bea0c1aeb97f195f2399ccf9787c6ac12d88fe8165e424a578d7c4816f17e4b554e5864c8fd7cc713ab9eb85ca7692c83b0c709a1fadd6570c3bfaf40b4da8f04fe9020ca400bb30fe2614b6a5343ef32f7345371c1339eab; ll=7fd06e815b796be3df069dec7836c3df; ua=sph; ctu=e99c7901999a18e63d1fd4ad148d9b0d4a1ef50af3c9511db823d117d06ba13318b4137c9cfc5c2c50c9e9fd8f43f3a1; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16ae34da4da-f79-f69-14d%7C%7C73"
headers = {
    'Accept': 'application/json, text/javascript',
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    'Connection': 'keep-alive',
    'Host': 'www.dianping.com',
    "Upgrade-Insecure-Requests": "1",
    "Referer": "http://www.dianping.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Cookie": cookie
}
css_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        }
# proxies = {
#     "http": "112.85.128.209:9999"
# }

def action():
    """
    启动函数
    :param shop_id:
    :param cokkies:
    :return:
    """
    url = "http://www.dianping.com/{}/{}/{}".format(city, type, chi_type)

    get_css_link(url)

def get_css_link(url):
    """

    :param url:
    :param cokkies:
    :return:
    """
    try:
        print(url)
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            html = res.text
            svg_text_url = re.findall('<link rel="stylesheet" type="text/css" href="(.*?svg.*?)">', html)[0]    #获得节点名最有坐标 css文件地址
            svg_text_url = "".join(["http:", svg_text_url])  #拼接
    except Exception as e:
        print(e)
    node_data_dict = get_node_dict(svg_text_url)
    node_names = set()
    for i in re.findall('<svgmtsi class="([a-zA-Z0-9]{5,6})"></span>', html):   #提取所有节点名
        node_names.add(i)
    for node_name in node_names:
        html = re.sub('<svgmtsi class="%s"></span>' % node_name, node_data_dict[node_name], html)   #替换html节点为数字
    parse(html)  #解析





def get_node_dict(svg_tesxt_url):
    """
    获取 节点名称 对应 数字字典
    :param svg_tesxt_url:
    :return:
    """
    res = requests.get(svg_tesxt_url, headers=css_headers)
    node_data_ls = re.findall(r'\.([a-zA-Z0-9]{5,6}).*?round:(.*?)px (.*?)px;', res.text)    #提取节点名与对应坐标
    background_image_link = re.findall("background-image: url\((.*?)\)", res.text)[0]   #提取 坐标对应数字 css文件地址
    word_coordinate_dict = get_word_coordinate_dict(background_image_link)
    node_data_dict = {}
    for i in node_data_ls:
        """构造成{节点名: 数字, .........}"""
        x = -int(i[1]) + 5
        if -int(i[2]) < 46:
            y = 46
        if 46 < -int(i[2]) < 88:
            y = 48
        else:
            y = 131
        node_data_dict[i[0]] = word_coordinate_dict[(x, y)]

    return node_data_dict

def get_word_coordinate_dict(background_image_link):
    """
    获取坐标值 对应 文字 字典
    :param background_image_link:
    :return:
    """
    word_coordinate_dict = {}
    for url in background_image_link:
        res = requests.get(url, headers=headers)
        font_list = re.findall(r'<text x="(.*?)" y="(.*?)">(.*?)</text>', res.text)     #提取坐标对应数字
        for i in font_list:
            for j in range(len(i[2])):
                word_coordinate_dict[(i[0][j], i[1])] = i[2][j]
    return word_coordinate_dict


def parse(html):
    """
    解析方法
    :param html:
    :return:
    """
    pass



action()

