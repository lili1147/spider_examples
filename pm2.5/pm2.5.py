# -*- coding: utf-8 -*-
# @Author: leedagou
# @Date:   2020-08-05 22:16:36
# @Last Modified by:   leedagou
# @Last Modified time: 2020-08-09 17:10:51

# https://www.aqistudy.cn/historydata/


import re
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd
import urllib.parse
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 改变标准输出的默认编码


# 获取网页的源码
def get_url_text(url):
    try:
        headers = {
            'User-Agent': 'User-Agent  Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('获取错误')
        return None


# 获取所有城市的列表
def get_city_list(html):
    city_list = []
    soup = BeautifulSoup(html, 'lxml')
    all = soup.find_all('div', {'class': 'all'})
    all_city = all[0].find_all('ul', {'class': 'unstyled'})
    # print(len(all_city))
    for word_city in all_city:
        # print(word_city)
        a = word_city.find_all('li')
        for i in a:
            city_list.append(i.get_text())
    return city_list


# 获取城市的数据
def get_city_pm(city_list):
    index = 0
    for city in city_list:
        index += 1
        url = 'https://www.aqistudy.cn/historydata/monthdata.php?city=' + urllib.parse.quote(city[1:-1])

        driver = webdriver.PhantomJS(executable_path=r'D:\bin\phantomjs.exe')
        sleep(3)
        # soup = driver.find_element_by_name('html')
        # lxml_html=parse_from_unicode（soup）
        # print(lxml_html)

        driver.get(url)
        sleep(3)
        print(city[1:-1])
        city_name = city[1:-1]
        prase_table_data(driver.page_source, city_name, index)
        # break

# 解析动态网页的数据，保存到列表中


def prase_table_data(page_source, city_name, index):
    soup = BeautifulSoup(page_source, 'lxml')
    tbody = soup.find_all('tbody')
    # print(tbody[0])
    trs = tbody[0].find_all('tr')
    city, month, AQI, range, rating, pm2, pm10, so2, co, no2, o3 = [], [], [], [], [], [], [], [], [], [], []

    for tr in trs[1:]:  # 获取城市的所有table数据
        city_data = tr.get_text()  # 获取到的每一列数据
        '''
        city:city
        月份：month
        AQI: AQI
        范围：range
        质量等级:rating
        pm2.5:pm2
        pm10: pm10
        s02:s02
        co:co
        no2:no2
        o3:o3

        '''
        city_data = city_data.split(' ')
        city.append(str(city_name))
        month.append(city_data[1])
        AQI.append(city_data[2])
        range.append(city_data[3])
        rating.append(city_data[4])
        pm2.append(city_data[5])
        pm10.append(city_data[6])
        so2.append(city_data[7])
        co.append(city_data[8])
        no2.append(city_data[9])
        o3.append(city_data[10])

    # 写入csv文件
    save_csv(city, month, AQI, range, rating, pm2, pm10, so2, co, no2, o3, index)


# 保存到csv文件中
def save_csv(city, month, AQI, range, rating, pm2, pm10, so2, co, no2, o3, index):
    # print(city)
    # print(month)

    print(index)
    data = pd.DataFrame()
    data['城市'] = city
    data['月份'] = month
    data['AQI'] = AQI
    data['范围'] = range
    data['质量等级'] = rating
    data['PM2.5'] = pm2
    data['PM10'] = pm10
    data['SO2'] = so2
    data['CO'] = co
    data['NO2'] = no2
    data['O3'] = o3
    # print(index)
    if index == 1:
        data.to_csv('pm.csv', mode='a', encoding='utf-8_sig', index=None)
    else:
        data.to_csv('pm.csv', mode='a', encoding='utf-8_sig', index=None, header=None)


def run():
    # city_list = ['\n阿坝州\n', '\n安康\n']
    city_list = ['\n阿坝州\n', '\n安康\n', '\n阿克苏地区\n', '\n阿里地区\n', '\n阿拉善盟\n', '\n阿勒泰地区\n', '\n安庆\n', '\n安顺\n', '\n鞍山\n', '\n克孜勒苏州\n', '\n安阳\n', '\n蚌埠\n', '\n白城\n', '\n保定\n', '\n北海\n', '\n宝鸡\n', '\n北京\n', '\n毕节\n', '\n博州\n', '\n百色\n', '\n白沙\n', '\n白山\n', '\n保山\n', '\n保亭\n', '\n包头\n', '\n本溪\n', '\n白银\n', '\n巴彦淖尔\n', '\n滨州\n', '\n巴中\n', '\n亳州\n', '\n长春\n', '\n承德\n', '\n成都\n', '\n常德\n', '\n昌都\n', '\n赤峰\n', '\n昌江\n', '\n昌吉州\n', '\n五家渠\n', '\n澄迈\n', '\n重庆\n', '\n常熟\n', '\n长沙\n', '\n楚雄州\n', '\n朝阳\n', '\n滁州\n', '\n郴州\n', '\n潮州\n', '\n常州\n', '\n长治\n', '\n崇左\n', '\n沧州\n', '\n池州\n', '\n定安\n', '\n丹东\n', '\n东方\n', '\n东莞\n', '\n德宏州\n', '\n大连\n', '\n大理州\n', '\n大庆\n', '\n大同\n', '\n定西\n', '\n大兴安岭地区\n', '\n黔南州\n', '\n德阳\n', '\n东营\n', '\n达州\n', '\n德州\n', '\n儋州\n', '\n鄂尔多斯\n', '\n恩施州\n', '\n鄂州\n', '\n防城港\n', '\n抚顺\n', '\n佛山\n', '\n阜新\n', '\n阜阳\n', '\n富阳\n', '\n福州\n', '\n抚州\n', '\n广安\n', '\n贵港\n', '\n果洛州\n', '\n桂林\n', '\n甘南州\n', '\n贵阳\n', '\n广元\n', '\n固原\n', '\n广州\n', '\n甘孜州\n', '\n赣州\n', '\n淮安\n', '\n淮北\n', '\n鹤壁\n', '\n海北州\n', '\n河池\n', '\n邯郸\n', '\n海东地区\n', '\n哈尔滨\n', '\n合肥\n', '\n黄冈\n', '\n鹤岗\n', '\n红河州\n', '\n怀化\n', '\n黑河\n', '\n呼和浩特\n', '\n海口\n', '\n呼伦贝尔\n', '\n葫芦岛\n', '\n海门\n', '\n哈密地区\n', '\n淮南\n', '\n黄南州\n', '\n海南州\n', '\n黄山\n', '\n衡水\n', '\n黄石\n', '\n和田地区\n', '\n海西州\n', '\n衡阳\n', '\n河源\n', '\n湖州\n', '\n汉中\n', '\n杭州\n', '\n贺州\n', '\n菏泽\n', '\n惠州\n', '\n吉安\n', '\n金昌\n', '\n晋城\n', '\n景德镇\n', '\n西双版纳州\n', '\n金华\n', '\n九江\n', '\n吉林\n', '\n荆门\n', '\n江门\n', '\n即墨\n', '\n佳木斯\n', '\n济南\n', '\n济宁\n', '\n胶南\n', '\n酒泉\n', '\n句容\n', '\n湘西州\n', '\n金坛\n', '\n嘉兴\n', '\n鸡西\n', '\n济源\n', '\n揭阳\n', '\n江阴\n', '\n嘉峪关\n', '\n锦州\n', '\n荆州\n', '\n晋中\n', '\n焦作\n', '\n胶州\n', '\n库尔勒\n', '\n开封\n', '\n黔东南州\n', '\n克拉玛依\n', '\n昆明\n', '\n昆山\n', '\n喀什地区\n', '\n临安\n', '\n六安\n', '\n来宾\n', '\n聊城\n', '\n临沧\n', '\n乐东\n', '\n娄底\n', '\n廊坊\n', '\n临汾\n', '\n临高\n', '\n漯河\n', '\n丽江\n', '\n吕梁\n', '\n陇南\n', '\n六盘水\n', '\n丽水\n', '\n凉山州\n', '\n拉萨\n', '\n乐山\n', '\n陵水\n', '\n莱芜\n', '\n临夏州\n', '\n莱西\n', '\n辽源\n', '\n辽阳\n',
                 '\n溧阳\n', '\n龙岩\n', '\n洛阳\n', '\n临沂\n', '\n连云港\n', '\n莱州\n', '\n林芝\n', '\n泸州\n', '\n柳州\n', '\n兰州\n', '\n马鞍山\n', '\n牡丹江\n', '\n茂名\n', '\n眉山\n', '\n绵阳\n', '\n梅州\n', '\n宁波\n', '\n南充\n', '\n南昌\n', '\n宁德\n', '\n南京\n', '\n内江\n', '\n怒江州\n', '\n南宁\n', '\n南平\n', '\n那曲地区\n', '\n南通\n', '\n南阳\n', '\n平度\n', '\n平顶山\n', '\n普洱\n', '\n盘锦\n', '\n蓬莱\n', '\n平凉\n', '\n莆田\n', '\n萍乡\n', '\n濮阳\n', '\n攀枝花\n', '\n青岛\n', '\n琼海\n', '\n秦皇岛\n', '\n曲靖\n', '\n齐齐哈尔\n', '\n七台河\n', '\n黔西南州\n', '\n清远\n', '\n庆阳\n', '\n钦州\n', '\n衢州\n', '\n琼中\n', '\n泉州\n', '\n荣成\n', '\n日喀则\n', '\n乳山\n', '\n日照\n', '\n寿光\n', '\n韶关\n', '\n上海\n', '\n绥化\n', '\n石河子\n', '\n石家庄\n', '\n商洛\n', '\n三明\n', '\n三门峡\n', '\n遂宁\n', '\n山南\n', '\n四平\n', '\n宿迁\n', '\n商丘\n', '\n上饶\n', '\n汕头\n', '\n汕尾\n', '\n绍兴\n', '\n松原\n', '\n沈阳\n', '\n十堰\n', '\n三亚\n', '\n邵阳\n', '\n双鸭山\n', '\n朔州\n', '\n苏州\n', '\n宿州\n', '\n随州\n', '\n深圳\n', '\n石嘴山\n', '\n泰安\n', '\n铜川\n', '\n屯昌\n', '\n太仓\n', '\n塔城地区\n', '\n通化\n', '\n天津\n', '\n铁岭\n', '\n铜陵\n', '\n通辽\n', '\n吐鲁番地区\n', '\n铜仁地区\n', '\n唐山\n', '\n天水\n', '\n太原\n', '\n台州\n', '\n泰州\n', '\n文昌\n', '\n文登\n', '\n潍坊\n', '\n瓦房店\n', '\n武汉\n', '\n乌海\n', '\n芜湖\n', '\n威海\n', '\n吴江\n', '\n乌兰察布\n', '\n乌鲁木齐\n', '\n渭南\n', '\n万宁\n', '\n文山州\n', '\n武威\n', '\n无锡\n', '\n温州\n', '\n梧州\n', '\n吴忠\n', '\n五指山\n', '\n兴安盟\n', '\n西安\n', '\n宣城\n', '\n许昌\n', '\n襄阳\n', '\n孝感\n', '\n迪庆州\n', '\n锡林郭勒盟\n', '\n厦门\n', '\n西宁\n', '\n咸宁\n', '\n湘潭\n', '\n邢台\n', '\n新乡\n', '\n咸阳\n', '\n新余\n', '\n信阳\n', '\n忻州\n', '\n徐州\n', '\n雅安\n', '\n延安\n', '\n延边州\n', '\n宜宾\n', '\n伊春\n', '\n银川\n', '\n宜春\n', '\n宜昌\n', '\n盐城\n', '\n运城\n', '\n云浮\n', '\n阳江\n', '\n营口\n', '\n玉林\n', '\n榆林\n', '\n伊犁哈萨克州\n', '\n阳泉\n', '\n玉树州\n', '\n烟台\n', '\n鹰潭\n', '\n义乌\n', '\n宜兴\n', '\n玉溪\n', '\n益阳\n', '\n岳阳\n', '\n永州\n', '\n扬州\n', '\n淄博\n', '\n自贡\n', '\n珠海\n', '\n镇江\n', '\n湛江\n', '\n诸暨\n', '\n张家港\n', '\n张家界\n', '\n张家口\n', '\n周口\n', '\n驻马店\n', '\n章丘\n', '\n肇庆\n', '\n舟山\n', '\n中山\n', '\n昭通\n', '\n中卫\n', '\n招远\n', '\n资阳\n', '\n张掖\n', '\n遵义\n', '\n郑州\n', '\n漳州\n', '\n株洲\n', '\n枣庄\n']

    get_city_pm(city_list)


if __name__ == '__main__':
    run()
