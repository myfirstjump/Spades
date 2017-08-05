# Booking Crawler.py
import requests
import time
from bs4 import BeautifulSoup
from collections import Counter
import re
import time
import numpy

# headers, cookies

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
cookie = {"Cookie":"zz_cook_tms_seg1=2; zz_cook_tms_seg3=8; _gat=1; header_signin_prompt=1; zz_cook_tms_ed=1; _ga=GA1.2.771830251.1501676071; _gid=GA1.2.1419963344.1501676071; vpmss=1; BJS=-; lastSeen=0; utag_main=v_id:015da2de69b200b09a95a293b1480407200b206a00bd0$_sn:2$_ss:0$_st:1501769227015$4split:0$4split2:2$ses_id:1501767389598%3Bexp-session$_pn:3%3Bexp-session; bkng=11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLbiKbS0JOgDBKd%2F%2B1hfoh7ruge6jtQj94MRrpMF%2FpqHNgFKbqjK6qKparQ6HF%2F7cbmaUhvrmXJdWrAyM%2BdeeHStXDwtIVqpQgscTT9xQwPJ8Zsa7GGheChMpsfi%2Bhx8zBNCE1PaRkYUwFaLWnIkGv25tUKrXlnc1itnQWmh4crrbI%3D"}

# 輸出每頁html
# 跑多頁
location = '京都'
### %E4%BA%AC%E9%83%BD ---> 京都
url = "https://www.booking.com/searchresults.zh-tw.html?aid=304142&label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaOcBiAEBmAEwuAEGyAEM2AED6AEBkgIBeagCAw&sid=25f3195cbf76726e8ffac861269a0d24&checkin_month=10&checkin_monthday=7&checkin_year=2017&checkout_month=10&checkout_monthday=11&checkout_year=2017&class_interval=1&dest_id=-235402&dest_type=city&group_adults=2&group_children=0&label_click=undef&no_rooms=1&raw_dest_type=city&room1=A%2CA&sb_price_type=total&src=index&src_elem=sb&ss="+str(location)+"&ssb=empty&ssne="+str(location)+"&ssne_untouched="+str(location)+"&rows=50"###+"&sr_ajax=1&b_gtt=dLYAeZFVJfNTBdAHUdPHUBSSUVJfcbWYaNLDRCAET&_=1501050897864"
res = requests.get(url, headers = headers, cookies = cookie)
soup = BeautifulSoup(res.text, 'lxml')

# 找總頁數
totPage = soup.select('#right')[0].find(lambda x: x.get('data-et-view') == 'TULQWNVLBLWIJDAOfUYdXaO:1')
pattern = "找到\s(\d+)\s間" #找頁數用
totPage2 = re.findall(pattern, totPage.find('h1').text)
pageAmount = int(totPage2[0])
# pageAmount / 50筆  =  翻頁數
turnPage = round(pageAmount/50)
tot = 1
print("pageAmount= " + str(pageAmount))
print("turnPage= " + str(turnPage))
for page in range(0, turnPage+1):
    print("==="*20+"page:" + str(page+1))
    #offset表示從第幾筆開始，第一頁offset = 0；row表示一頁顯示幾筆。
    offset = page*50
    # 首頁和
    #url2 = "https://www.booking.com/searchresults.zh-tw.html?aid=304142&label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaOcBiAEBmAEwuAEGyAEM2AED6AEBkgIBeagCAw&sid=25f3195cbf76726e8ffac861269a0d24&checkin_month=8&checkin_monthday=24&checkin_year=2017&checkout_month=8&checkout_monthday=27&checkout_year=2017&class_interval=1&dest_id=-235402&dest_type=city&group_adults=2&group_children=0&label_click=undef&no_rooms=1&raw_dest_type=city&room1=A%2CA&sb_price_type=total&src=index&src_elem=sb&ss="+str(location)+"&ssb=empty&ssne="+str(location)+"&ssne_untouched=%E4%BA%AC%E9%83%BD&rows=50" + "&offset=" + str(offset)###+"&sr_ajax=1&b_gtt=dLYAeZFVJfNTBdAHUdPHUBSSUVJfcbWYaNLDRCAET&_=1501050897864"    
    url2 = "https://www.booking.com/searchresults.zh-tw.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaOcBiAEBmAEwuAEGyAEM2AED6AEBkgIBeagCAw&sid=4996667e149bfae490c17f2eb37eafa9&checkin_month=10&checkin_monthday=7&checkin_year=2017&checkout_month=10&checkout_monthday=11&checkout_year=2017&class_interval=1&dest_id=-235402&dest_type=city&dtdisc=0&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&src=index&src_elem=sb&ss="+str(location)+"&ss_all=0&ssb=empty&sshis=0&ssne="+str(location)+"&ssne_untouched="+str(location)+"&rows=50&offset="+ str(offset)### + "&sr_ajax=1&b_gtt=dLYAeZFVJfNTBdAHUdHPGZDfIfVNASUcbTYWPJLO&_=1501678454525"        
    
    
    res2 = requests.get(url2, headers = headers, cookies = cookie)
    soup2 = BeautifulSoup(res2.text, 'lxml')
    items = soup2.select(".sr_item")
    with open('BookingCrawl-{}-{}-{}-Page{}.txt'.format(time.localtime().tm_mon,time.localtime().tm_mday, time.localtime().tm_hour, page+1 ), 'w', encoding = 'UTF-8') as f:
        f.write(str(items).strip('[]'))