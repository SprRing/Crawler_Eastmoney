import requests
from pyquery import PyQuery as pyq
import json

from configs import *
import test_proxy


class ReportCrawler(object):
    def __init__(self):
        pass

    def cleanse(self, final_dict, data_info, url, pdf, channel):  # 丟入頁面資料、pdf的url，跑出json
        count = 0
        temp_dict = {}
        for i in pdf:
            if channel == '0':  # 因為解析時，個股的寫法是dict，所以用setdefault
                if i is None:  # 要在每筆資料後標註，是否有pdf，若有，名稱為何
                    data_info['data'][count].setdefault('status', 'None')
                else:
                    i = i.split('/')
                    data_info['data'][count].setdefault('status', i[4])
            if channel == '1':  # 然而行業的是用string，所以直接用相加的
                if i is None:
                    data_info['data'][count] += ', None'
                else:
                    i = i.split('/')
                    data_info['data'][count] += i[4]
            temp_dict = {url[count]: data_info['data'][count]}  # 將每筆資料與其網址對應
            final_dict.update(temp_dict)
            count += 1

    # def get_report_date(self, channel, time):  # 給channel和日期，會使用這個func，最後給出頁面資料、url_list
    #     page = 1
    #     url_list_date =[]
    #     temp_dict = {}
    #     while True:
    #         url = gAPI[channel]['URL'] + str(page) + gAPI[channel]['URL2']  # 前三句會不斷翻頁，爬出程式碼
    #         r = requests.get(url)
    #         r_string = r.content.decode('utf8').replace(gAPI[channel]['replace_pattern'], '')
    #         r_dict = eval(r_string)  # 將程式碼轉成dict
    #         if page == 1:  # 用這個if-else，將每頁的dict記在一起，才不會洗掉
    #             temp_dict.update(r_dict)
    #         else:
    #             temp_dict['data'].append(r_dict['data'][0])
    #         if channel == '0':  # 個股頁面的解析方法
    #             for i in r_dict['data']:
    #                 date = i['datetime'][:10].replace('-', '')
    #                 if int(date) < time:  # 如果發現已經爬到比設定時間還早的資料，跳出
    #                     return url_list_date, temp_dict
    #                 url_list_date.append(gURL + "%s/%s.html" % (date, i['infoCode']))
    #         if channel == '1':  # 行業頁面的解析方法
    #             for i in r_dict['data']:
    #                 ii = i.split(',')
    #                 Y, m, d = ii[1].split(' ')[0].split('/')
    #                 dtime_string = "%s%02d%02d" % (Y, int(m), int(d))
    #                 if int(dtime_string) < time:
    #                     return url_list_date, temp_dict
    #                 url_list_date.append(gURL + "%s/%s.html" % (dtime_string, 'hy,' + ii[2]))
    #         page += 1  # 翻頁

    def get_report(self, channel, page):  # 給頁數，爬到指定頁數的網頁資料
        # if not proxy_list:
        #     proxy_list = [{}]
        url = gAPI[channel]['URL'] + str(page) + gAPI[channel]['URL2']  # 前三句會不斷翻頁，爬出程式碼
        r = requests.get(url)  # , proxies=random.choice(proxy_list))
        result_string = r.content.decode('utf8').replace(gAPI[channel]['replace_pattern'], '')
        print(result_string)
        result_dict = eval(result_string)  # 將程式碼轉成dict
        print(result_dict)
        url_list = []
        # if channel == '0':  # 個股頁面的解析方法
        #     for i in result_dict['data']:
        #         url_list.append(gURL + "%s/%s.html" % (i['datetime'][:10].replace('-', ''), i['infoCode']))
        # if channel == '1':  # 行業頁面的解析方法
        #     for i in result_dict['data']:
        #         ii = i.split(',')
        #         dtime = ii[1].split(' ')[0].split('/')
        #         Y, m, d = dtime
        #         dtime_string = "%s%02d%02d" %(Y, int(m), int(d))
        #         url_list.append(gURL + "%s/%s.html" % (dtime_string, 'hy,' + ii[2]))
        if channel == '2':
            for i in result_dict['data']:
                ii = i.split(',')
                dtime = ii[0].split(' ')[0].split('/')
                Y, m, d = dtime
                dtime_string = "%s%02d%02d" %(Y, int(m), int(d))
                url_list.append(gURL + "%s/%s.html" % (dtime_string, 'hg,' + ii[1]))
        return url_list, result_dict

    def get_pdf_url(self, url_list):
        pdf_list =[]
        print(url_list)
        for i in url_list:  # 進去每個報告的網頁，找到pdf的連結網址
            r = requests.get(i)
            doc = pyq(r.content.decode('gbk'))
            #print(doc)
            pdf = doc('a').filter(lambda j, this: 'PDF' in pyq(this).text()).eq(0)
            pdf_list.append(pdf.attr['href'])
        return pdf_list

    def get_pdf(self, pdf_list, g_data_path):
        msg_pdf = {'status': "yes", "msg": "download successfully"}
        count = 0
        try:  # 讀取pdf，並下載
            for i in pdf_list:
                if i is None:
                    continue
                get_response = requests.get(i, stream=True)
                file_name = i.split("/")[-1]
                with open(os.path.join(g_data_path, file_name), 'wb') as f:
                    for chunk in get_response.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunk
                            f.write(chunk)
                count += 1
        except Exception as e:
            msg_pdf = {'status': "no", "order": count, "msg": e}
        return msg_pdf

    def main(self, channel, pages=0, date=0):
        g_data_path = os.path.join(gPROJECT_PATH, 'data', 'channel' + str(channel))  # 設定pdf要下載的位置
        final_dict = {}
        if pages == 0:  # 若是丟入的是日期，就會進到這個判斷式
            url_list, data_json = self.get_report_date(channel, date)
            pdf_list = self.get_pdf_url(url_list)
            msg_pdf = self.get_pdf(pdf_list, g_data_path)
            self.cleanse(final_dict, data_json, url_list, pdf_list, channel)
        else:  # 若丟入的是頁數，進到這個迴圈
            for i in range(0, pages):
                url_list, data_json = self.get_report(channel, i + 1)
                pdf_list = self.get_pdf_url(url_list)
                msg_pdf = self.get_pdf(pdf_list, g_data_path)
                self.cleanse(final_dict, data_json, url_list, pdf_list, channel)
        with open(os.path.join(g_data_path, 'json', 'data.json'), 'w') as d:  # 設定json檔要儲存的位置
            json.dump(final_dict, d)
        return msg_pdf


if __name__ == '__main__':
    RC = ReportCrawler()
    TP = test_proxy.Proxy()
    # proxy_list = TP.main()
    # 要以頁數下載，輸入pages=數字; 要以日期下載，輸入date=yyyymmdd
    # 要下載個股 channel='0'，要下載行業 channel='1'
    msg = RC.main(channel='2', pages=6)
    print(msg)

