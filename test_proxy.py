import requests
from pyquery import PyQuery as pyq

from configs import *


class Proxy(object):

    def __init__(self):
        pass

    def get_proxy_list(self):
        r = requests.get(gPROXY, timeout=5)
        doc = pyq(r.content)
        tr_list = [i.text() for i in doc('#proxylisttable').find('tr').items()]
        tr_list = [i for i in tr_list[1:] if i]
        proxy_list = [i.split('/n')[:2] for i in tr_list]
        proxy_list = [':'.join(i) for i in proxy_list]
        proxy_list = [{'http': i, 'https': i} for i in proxy_list]
        return proxy_list

    def proxy_validater(self):
        result_list = []
        proxy_list = self.get_proxy_list()
        for proxy in proxy_list:
            if len(result_list) == 5:
                break
            try:
                r = requests.get('https://tw.yahoo.com/', timeout=3, proxies=proxy)
                # proxy.pop('no')
                if r.status_code == 200:
                    print(proxy)
                    result_list.append(proxy)
            except Exception as e:
                print(e)
        return result_list

    def main(self):
        proxy_list = self.proxy_validater()
        return proxy_list

