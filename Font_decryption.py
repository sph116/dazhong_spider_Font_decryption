import redis
import json
import requests
import re
import os


from fontTools.ttLib import TTFont
HASH_TABLE = 'dianping:font'

class Font_Decryption():
    """
    字库替换 模块
    """
    def __init__(self, css_url, redis_host='你的主机', redis_port=端口, redis_pass="你的密码", db=你的数据库):
        """
        redis 默认链接本机
        :param redis_host: redis 链接地址
        :param redis_port: redis 端口号
        :param redis_pass: redis 密码
        """
        self.name_list = None
        if redis_pass:
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, password=redis_pass, db=db, decode_responses=True)
        else:
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)
        self.css_url = css_url
        with open('./font/font.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.FONT_LIST = data.get('FONT_LIST')
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        self.get_font_url()

    def get_font_url(self):
        """
        通过css链接 以及需要替换字体的class属性 从css链接返回数据中 查找到对应字库的下载地址
        :return:
        """
        rep = requests.get(self.css_url, self.headers)
        if rep.status_code == 200:
            text = rep.text
            url_flag = re.findall('"PingFangSC-Regular-(.*?)"', text)
            urls = re.findall(r'url\("//(.*?)"\)', text)
            urls = [url for url in urls if "woff" in url]

            # font_url_item = {}
            # for i, j in zip(url_flag, urls):
            #     if "woff" in j:
            #         font_url_item[i] = j

            font_url_ls = [(i, j) for i, j in zip(url_flag, urls) if "woff" in j]

            self.install_font(font_url_ls)
        else:
            return None

    def get_all_font(self):
        """
        返回所有字体文件
        :return:
        """
        item = {}
        name_list = [i[1] for i in self.name_list]
        result_list = self.r.hmget(HASH_TABLE, name_list)  # 取出对应字库表（已修复bug）
        for i in result_list:
            item.update(eval(i))
        return item

    def check_hash(self, name):
        """
        检查hash是否存在于redis中 若存在返回1
        :param name:
        :return:
        """
        return self.r.hexists(HASH_TABLE, name)

    def add_hash(self, name, json_data):
        """
        新增 hash
        """
        self.r.hset(HASH_TABLE, name, json_data)

    def parse_font(self, class_name, code):
        """
        传入加密字符串 根据字库替换未相应文字
        :param code:
        :return:
        """

        # clean_code = code.replace(';', '')[-4:]  # 只提取匹配区域
        clean_code = code.replace(r'\u', '')
        name_list = [i[1] for i in self.name_list if i[0] == class_name]
        print(self.name_list)
        result_list = self.r.hmget(HASH_TABLE, name_list)  # 取出对应字库表（已修复bug）
        for result in result_list:  # 匹配所有字符集
            json_data = json.loads(result)
            if 'uni' + clean_code in json_data:
                return json_data['uni' + clean_code]
        return clean_code

    def install_font(self, font_urls):
        """
        存储字库进入redis 以css名为字库名 若css未更新 则从旧字库挑选字体 若css更新完毕 则替换旧的字库
        :param font_url:
        :return:
        """
        self.name_list = [(url[0], url[1][url[1].rfind('/')+1: -5]) for url in font_urls]
        for index, name in enumerate(self.name_list):  # enumerate方法可以同时遍历 每个元素内容和下标
            if self.check_hash(name[1]):
                # 已存在无需安装
                pass
            else:
                with open('./font/' + name[1] + '.woff', 'wb+') as f:
                    f.write(requests.get("http://" + font_urls[index][1]).content)  # 下载写入
                    f.close()
                    font = TTFont('./font/' + name[1] + '.woff')
                    uni_list = font['cmap'].tables[1].ttFont.getGlyphOrder()  # 取出字形保存到uniList中
                    json_data = json.dumps(dict(zip(uni_list, self.FONT_LIST)), ensure_ascii=False)
                    self.add_hash(name[1], json_data)
                    os.remove('./font/' + name[1] + '.woff')  # 用完了删掉，节省资源占用



# pf = Font_Decryption(css_url="http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/a29817b9e27f3a5fd06d90a916f64393.css")  # 每次更换页面 切换css重新请求
# print(pf.parse_font('&#xe6e9;'))



