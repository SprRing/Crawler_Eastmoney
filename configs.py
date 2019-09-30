import os

gPROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

gURL = 'http://data.eastmoney.com/report/'

gAPI = {'0': {'name': '個股研報',
              'replace_pattern': 'var acrslrCT=',
              'URL': 'http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20acrslrCT={%22'
                     'data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p=',
              'URL2': '&mkt=0&stat=0&cmd=2&code=&rt=51569528'},

        '1': {'name': '行業研報',
              'URL': 'http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HYSR&mkt=0&stat=0&cmd=4&'
                     'code=&sc=&ps=50&p=',
              'URL2': '&js=var%20IQApjPfP={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22'
                      '(ud)%22,%22count%22:%22(count)%22}&rt=51569531',
              'replace_pattern': 'var IQApjPfP='},
        '2': {'name': '宏觀研究',
              'replace_pattern': 'var QvFmCOwC=',
              'URL': 'http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HGYJ&cmd=4&code=&ps=50&p=',
              'URL2': '&js=var%20QvFmCOwC={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22'
                      ':%22(count)%22}&rt=51627717'}}

gPROXY = 'https://free-proxy-list.net/'
