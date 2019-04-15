import time
import pymysql
import requests
import random
import re
import datetime
from bs4 import BeautifulSoup
from scrapy.selector import Selector

cnt = 1

# 天猫每页的代码变化多
urls = [
'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.1.4def3336yx2XSF&brand=20578&q=%C4%CD%BF%CB%C4%D0%D0%AC&sort=s&style=g&from=rs_1_key-top-s#J_Filter',
'https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.1c2c3336bqH3Bo&brand=20578&s=60&q=%C4%CD%BF%CB%C4%D0%D0%AC&sort=s&style=g&from=rs_1_key-top-s&type=pc#J_Filter',
'https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.45693336bMqhcS&brand=20578&s=120&q=%C4%CD%BF%CB%C4%D0%D0%AC&sort=s&style=g&from=rs_1_key-top-s&type=pc#J_Filter',
'https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.7b153336o0yMrH&brand=20578&s=180&q=%C4%CD%BF%CB%C4%D0%D0%AC&sort=s&style=g&from=rs_1_key-top-s&type=pc#J_Filter'
]

referers = [
'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.1.7c3b3336cw9Hcj&brand=20578&q=%C4%CD%BF%CB%C4%D0%D0%AC&sort=s&style=g&from=rs_1_key-top-s',
'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.1.4def3336yx2XSF&brand=20578&q=%C4%CD%BF%CB%C4%D0%D0%AC&sort=s&style=g&from=rs_1_key-top-s',
'https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.1c2c3336bqH3Bo&brand=20578&s=60&q=%C4%CD%BF%CB%C4%D0%D0%AC&sort=s&style=g&from=rs_1_key-top-s&type=pc',
'https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.45693336bMqhcS&brand=20578&s=120&q=%C4%CD%BF%CB%C4%D0%D0%AC&sort=s&style=g&from=rs_1_key-top-s&type=pc'
]

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

proxies=[
'http://171.37.155.217',
'http://61.135.217.7',
'http://118.190.95.43',
'http://118.190.95.35',
'http://111.155.116.219',
'http://111.155.116.208',
'http://110.73.11.191',
'http://110.73.9.193',
'http://121.31.153.146',
'http://111.155.116.236',
'http://110.73.1.47',
'http://175.155.24.21',
]

def get_page(url, referer):
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Referer': referer,
        'cookie': 'cna=OP11EqUOUycCAd0E2NyEXPyd; x=__ll%3D-1%26_ato%3D0; enc=EVXBIraVcS%2FpdV%2B1AKzyO0E2Kz%2FxhnZlO8%2BDeJnuN6%2BSYrb7srhItQbascVZVBB2fq67KFuIY3w95yduN2T89A%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E5%BD%92%E9%9B%B6%E8%80%85zz; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; _m_h5_tk=d3af034af51b4c5add72b5c9513f22c4_1533385215730; _m_h5_tk_enc=153ebf64301a8890ee929729883db044; tracknick=%5Cu5F52%5Cu96F6%5Cu8005zz; lgc=%5Cu5F52%5Cu96F6%5Cu8005zz; ck1=""; swfstore=91289; _med=dw:1536&dh:864&pw:1728&ph:972&ist:0; uc1=cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie21=VT5L2FSpccLuJBreKQgf&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false&pas=0&cookie14=UoTfKLAGe4jukA%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dBzrpASsONR8E4bug%3D&id2=UUGlTGanoQjz8A%3D%3D&nk2=2mZvZVWVHDE%3D&lg2=UIHiLt3xD8xYTw%3D%3D; csg=a8fa3b24; skt=94d8ae2ce438f92a; tt=tmall-main; Hm_lvt_3c8ecbfa472e76b0340d7a701a04197e=1533627688,1533633953,1533645079,1533645437; whl=-1%260%260%260; t=822d29d826eab631957edf1ae36f3d2c; _tb_token_=eb535ebe3df31; cookie2=1183d694cbc06de182812a41ed1751ca; cq=ccp%3D1; _uab_collina=153364606833062386832815; _umdata=9FF34244E761CF744541CED6659567185892B4D890B9BDDB47C7A910AF7F944C4DBCC3BDE2723482CD43AD3E795C914C282CEF9E129450850E9D1B6B8B9D5DA5; x5sec=7b22746d616c6c7365617263683b32223a2234323031623665353339363535326662373936356665346666313038366165344349437170747346454d3263374f717a742f7a4c3341453d227d; res=scroll%3A1145*6407-client%3A1145*693-offset%3A1145*6407-screen%3A1536*864; pnm_cku822=098%23E1hvG9vUvbpvUvCkvvvvvjiPPsMO6jlnn2qwzj3mPmPyQjEmPLzpgj1PP2LO1jEvRphvCvvvvvvPvpvhvv2MMTyCvv9vvUmAx2iUxgyCvvOUvvVvay7tvpvIvvvv%2ByCvvjhvvvEVphvUl9vvvQCvpvACvvv2vhCv2R9vvUU%2BphvU1pyCvhQpKRyvClsvaNoURfvK2bmxfwmK5kx%2FQj7%2Bk28zbp%2FQD7zZdignfnV3fX7rVClvI8oQD40Xjomxfa1lDfUfb57QiNoOVjC2sb2XSfpAvphvC9vhvvCvp8wCvvpvvUmm; Hm_lpvt_3c8ecbfa472e76b0340d7a701a04197e=1533646088; isg=BPPzoQcSrPOk5mI_BQUEyg14l_fdgIaPJvLKh6WQB5JJpBJGLfn3O0e2WpTvA9_i'
    } # 需要浏览到所需最后一页的cookie
    proxie = random.choice(proxies)
    try:
        response = requests.get(url, headers=headers, proxies=proxie)
    except:
        response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.text
        # soup = BeautifulSoup(html, "lxml")
        # print(soup)
        # print(html)
        return html
    else:
        print("请求错误：{}".format(response.status_code))

def get_info(url, referer, cnt, db):
    html = get_page(url, referer)
    selector = Selector(text=html)
    for i in range(1, 61):
        price = selector.xpath('//*[@id="J_ItemList"]/div['+ str(i) +']/div/p[1]/em/text()').extract_first()
        obj_names = selector.xpath('//*[@id="J_ItemList"]/div['+ str(i) +']/div/p[2]/a/text()').extract()
        shop_names = selector.xpath('//*[@id="J_ItemList"]/div['+ str(i) +']/div/div['+ str(cnt) +']/a/text()').extract()
        monthly_sales = selector.xpath('//*[@id="J_ItemList"]/div['+ str(i) +']/div/p[3]/span[1]/em/text()').extract()
        comments = selector.xpath('//*[@id="J_ItemList"]/div['+ str(i) +']/div/p[3]/span[2]/a/text()').extract()
        obj_name = ''.join(obj_names)[1:-1].replace('\'', '').strip()
        shop_name = ''.join(shop_names)[1:-1].strip()
        monthly_sale = ''.join(monthly_sales).strip()
        comment_num = ''.join(comments).strip()
        date_time = datetime.datetime.now()
        print(obj_name, price, shop_name, monthly_sale, comment_num, date_time)
        info = {
            '商品名称': obj_name,
            '价格': price,
            '所属店铺': shop_name,
            '月成交': monthly_sale,
            '评价数量': comment_num,
            '爬取日期': date_time
        }
        insert_db(db, info)

def insert_db(db, info):
    values = "'{}'," * 5 + "'{}'"
    sql_values = values.format(info['商品名称'], info['价格'], info['所属店铺'], info['月成交'], info['评价数量'], info['爬取日期'])
    sql = """
        insert into nike_tmall(商品名称, 价格, 所属店铺, 月成交, 评价数量, 爬取日期)
        values({})
    """.format(sql_values)
    # print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

database = {
    'host': 'localhost',
    'database': 'taobao',
    'user': 'root',
    'password': 'likai0223'
}
def get_db(setting):
    return pymysql.connect(**setting)

db = get_db(database)
for url,referer in zip(urls, referers):
    print("第%d次爬取中..." % cnt)
    if cnt == 1:
        info = get_info(url, referer, 3, db)
    else:
        info = get_info(url, referer, 2, db)    # 从第二页开始数据地址换了
    print("完成一次爬取")

    if cnt < 4:
        cnt += 1
        print("等待80秒后再次爬取...")
        time.sleep(20)
    else:
        print("爬取数据完毕")
        db.close()