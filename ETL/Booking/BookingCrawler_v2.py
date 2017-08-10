# import lib
from datetime import datetime, timedelta, date
import requests
from bs4 import BeautifulSoup
import re
import time
import os
import json

start_time = time.time()

# Settings
surveyRange = 180
travelPeriod = 4

# Date List 
# args: start date, survey range, travel period(days)
# ex. [datetime.date(2017, 8, 7), datetime.date(2017, 8, 11)] ~ [datetime.date(2017, 9, 5), datetime.date(2017, 9, 9)]]
def getDateList(dt = date.today(), ran = surveyRange, period = travelPeriod):
    timeList = []
    start = dt
    end = start + timedelta(days = period)
    for i in range(1, ran+1):  # i = 1 ~ ran
        timeList.append([start, end])
        start = start + timedelta(days = 1)
        end = end + timedelta(days = 1) 
    return timeList
timeList = getDateList() # from dt = date(2017, 12 ,31)

# Date List components
checkinM = []
checkinD = []
checkinY = []
checkoutM = []
checkoutD = []
checkoutY = []
for i in timeList:
    checkinM.append(i[0].month)
    checkinD.append(i[0].day)
    checkinY.append(i[0].year)
    checkoutM.append(i[1].month)
    checkoutD.append(i[1].day)
    checkoutY.append(i[1].year)
    
# headers
# cookies
# location
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
cookie = {"Cookie":"zz_cook_tms_seg1=2; zz_cook_tms_seg3=8; vpmss=1; has_preloaded=1; _gat=1; header_signin_prompt=1; _ga=GA1.2.771830251.1501676071; _gid=GA1.2.1896765923.1502154343; BJS=-; utag_main=v_id:015da2de69b200b09a95a293b1480407200b206a00bd0$_sn:9$_ss:0$_st:1502342742673$4split:0$4split2:2$ses_id:1502340934781%3Bexp-session$_pn:2%3Bexp-session; zz_cook_tms_ed=1; bkng=11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLbiKbS0JOgDBL0fnqjd4vBkPcI8rkGKzraI1suV7nd3XzAVU3u4Xj1lbHkdMgnvM8eZTMMJRnu%2B%2BZcZjRbYIMEBjqo0avzmRl9k1LkfZZbKA%2BwUGHQmNGg6nxYFeKrIZPn0sVzmTaMLLz0M5NoM2kCXMpBOw3S4AHu7OrBOAPFK%2Fw%3D; lastSeen=0"}
location = '京都'

# Pages amount for each travel period.  
# ex. numHotelList = [ ['145'], ['160'], ['167'], ['203'], ['239'], ['294'], ['353'], ['371'], ... increasing by date to date

pagesList = []
numHotelList = []
turnPageList = []
for i in range(1, surveyRange+1): # i = 1 ~ surveyRange
    # url位址為XHR文件中的searchresults，去除AJAX部分
    print("loading period info: " + str(i))
    url = "https://www.booking.com/searchresults.zh-tw.html?aid=304142&label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaOcBiAEBmAEwuAEGyAEM2AED6AEBkgIBeagCAw&sid=25f3195cbf76726e8ffac861269a0d24&checkin_month="+str(checkinM[i-1])+"&checkin_monthday="+str(checkinD[i-1])+"&checkin_year="+str(checkinY[i-1])+"&checkout_month="+str(checkoutM[i-1])+"&checkout_monthday="+str(checkoutD[i-1])+"&checkout_year="+str(checkoutY[i-1])+"&class_interval=1&dest_id=-235402&dest_type=city&group_adults=2&group_children=0&label_click=undef&no_rooms=1&raw_dest_type=city&room1=A%2CA&sb_price_type=total&src=index&src_elem=sb&ss="+str(location)+"&ssb=empty&ssne="+str(location)+"&ssne_untouched="+str(location)+"&rows=50"###+"&sr_ajax=1&b_gtt=dLYAeZFVJfNTBdAHUdPHUBSSUVJfcbWYaNLDRCAET&_=1501050897864"
    res = requests.get(url, headers = headers, cookies = cookie)
    soup = BeautifulSoup(res.text, 'lxml')
    
    # 找總頁數
    clue1 = soup.select('#right')[0].find(lambda x: x.get('data-et-view') == 'TULQWNVLBLWIJDAOfUYdXaO:1')
    pattern = "找到\s(\d+)\s間" #找頁數用
    numHotelText = re.findall(pattern, clue1.find('h1').text)
    # 這區間共幾間hotel
    numHotel = int(numHotelText[0])
    # numHotel / 一頁有50筆  =  翻頁數
    turnPage = round(numHotel/50)
    # append to lists
    pagesList.append(numHotel)
    turnPageList.append(turnPage)


# for each period (ex. 10/7 ~ 10/11), grab the hotelList information


for i in range(1, surveyRange+1): # i = 1 ~ surveyRange
    HotelList = [] # This list store and reflash by each travelPeriod
    url = "https://www.booking.com/searchresults.zh-tw.html?aid=304142&label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaOcBiAEBmAEwuAEGyAEM2AED6AEBkgIBeagCAw&sid=25f3195cbf76726e8ffac861269a0d24&checkin_month="+str(checkinM[i-1])+"&checkin_monthday="+str(checkinD[i-1])+"&checkin_year="+str(checkinY[i-1])+"&checkout_month="+str(checkoutM[i-1])+"&checkout_monthday="+str(checkoutD[i-1])+"&checkout_year="+str(checkoutY[i-1])+"&class_interval=1&dest_id=-235402&dest_type=city&group_adults=2&group_children=0&label_click=undef&no_rooms=1&raw_dest_type=city&room1=A%2CA&sb_price_type=total&src=index&src_elem=sb&ss="+str(location)+"&ssb=empty&ssne="+str(location)+"&ssne_untouched="+str(location)+"&rows=50"###+"&sr_ajax=1&b_gtt=dLYAeZFVJfNTBdAHUdPHUBSSUVJfcbWYaNLDRCAET&_=1501050897864"
    res = requests.get(url, headers = headers, cookies = cookie)
    soup = BeautifulSoup(res.text, 'lxml')
    print("="*50)
    print("period: " + str(i))
    for page in range(1, turnPageList[i-1]+1): # page = 1 ~ turnPage
        time.sleep(1)
        print("this is page: " + str(page) + " from total " + str(turnPageList[i-1]))
        offset = (page-1)*50  # offset: from index of hotel(in below url)
        url2 = "https://www.booking.com/searchresults.zh-tw.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaOcBiAEBmAEwuAEGyAEM2AED6AEBkgIBeagCAw&sid=4996667e149bfae490c17f2eb37eafa9&checkin_month="+str(checkinM[i-1])+"&checkin_monthday="+str(checkinD[i-1])+"&checkin_year="+str(checkinY[i-1])+"&checkout_month="+str(checkoutM[i-1])+"&checkout_monthday="+str(checkoutD[i-1])+"&checkout_year="+str(checkoutY[i-1])+"&class_interval=1&dest_id=-235402&dest_type=city&dtdisc=0&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&src=index&src_elem=sb&ss="+str(location)+"&ss_all=0&ssb=empty&sshis=0&ssne="+str(location)+"&ssne_untouched="+str(location)+"&rows=50&offset="+ str(offset)### + "&sr_ajax=1&b_gtt=dLYAeZFVJfNTBdAHUdHPGZDfIfVNASUcbTYWPJLO&_=1501678454525"        
        res2 = requests.get(url2, headers = headers, cookies = cookie)
        soup2 = BeautifulSoup(res2.text, 'lxml')
        items = soup2.select(".sr_item")
#        with open('BookingCrawl_now-{}-{}-{}-from-{}-to-{}-Page{}.txt'.format(time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, timeList[i-1][0], timeList[i-1][1], page), 'w', encoding = 'UTF-8') as f:
#            f.write(str(items))
#            print("save done.")
#            time.sleep(5)
#            print("Cost time: " + str(time.time()-start_time-5*i))
        for item in items:
            dictBook = {}
# Name
            HotelName = item.select(".sr-hotel__name")[0].text
#             print(HotelName.strip())
            if re.findall("\\n[\w|\s|\&|\(|\)|\-|,|']+（([\w|（|）|・]+)）", HotelName) != []: # ex. Toji Houses沒有中文
                #print(re.findall("\\n[\w|\s|\&|\(|\)|\-|,|']+（([\w|（|）|・]+)）", HotelName)[0])
                dictBook["ChiName"] = re.findall("\\n[\w|\s|\&|\(|\)|\-|,|']+（([\w|（|）|・]+)）", HotelName)[0]
                #print(re.findall("\\n([\w|\s|\&|\(|\)|\-|,|'|・]+)（", HotelName)[0])
                dictBook["EngName"] = re.findall("\\n([\w|\s|\&|\(|\)|\-|,|'|・]+)（", HotelName)[0].upper()
            else:
                #print("NA")
                dictBook["ChiName"] = "NA"
                #print(HotelName.strip())
                dictBook["EngName"] = HotelName.strip().upper()
# Price
            if "TWD" not in item.select('.sr_rooms_table_block')[0].text: 
                #print("--------> " + " Sell Out!!!")
                dictBook["Price"] = "NA"
            else:
                target = item.select('.sr_rooms_table_block')[0].select('strong > b')[0].text
                #print("--------> " + target)
                price = "".join(re.findall("TWD\s(\w+,\w+$)", target)[0].split(","))
                dictBook["Price"] = int(price)/4
# Check in/out time
            dictBook["CheckIn"] = "{}-{}-{}-15-00".format(timeList[i-1][0].year, timeList[i-1][0].month, timeList[i-1][0].day)
            dictBook["CheckOut"] = "{}-{}-{}-11-00".format(timeList[i-1][1].year, timeList[i-1][1].month, timeList[i-1][1].day)
# Latitude, Longitude
            coor1 = item.findAll(lambda y: y.get('data-coords'))[1] 
            coor2 = re.findall('data-coords="(135[\w|,|\.]+)"', str(coor1))
            Latitude = coor2[0].split(",")[0]
            Longitude = coor2[0].split(",")[1]
            #print(Latitude)
            dictBook["Latitude"] = Latitude
            #print(Longitude)
            dictBook["Longitude"] = Longitude
# Star Rate
            sr = item.select("div.sr_property_block_main_row")
            sr2 = re.findall('-sprite-ratings_stars_(\w+)"', str(sr))
            if sr2 == []:
                dictBook["StarRate"] = "NA"
            else:
                dictBook["StarRate"] = sr2[0]
# Score
            score1 = item.select("div.sr-review-score")
            score2 = re.findall('review-score-badge">\\n([\w|\.]+)', str(score1))
            if score2 == []:
                dictBook["Score"] = "NA"
            else:
                dictBook["Score"] = score2[0]
# Comments
                comment1 = item.select("div.sr-review-score")
                comment2 = re.findall('review-score-widget__subtext">\\n([\w|,]+)\s則評語\\n<', str(comment1))
                if comment2 == []:
                    dictBook["Comment"] = "NA"
                else: 
                    dictBook["Comment"] = "".join(comment2[0].split(","))
            #print("==========================")
            #print(dictBook)
            HotelList.append(dictBook)
        HotelList2 = json.dumps(HotelList, ensure_ascii = False)
            #time.sleep(1)
#     print("saving dictBook...")
    if os.path.exists('D:\\DATA\\data-grabTime-{}'.format(time.localtime()[1:4])) == False:
        os.makedirs('D:\\DATA\\data-grabTime-{}'.format(time.localtime()[1:4]))
    with open('D:\\DATA\\data-grabTime-{}\\BookingList-from-{}-to-{}.txt'.format(                           time.localtime()[1:4], timeList[i-1][0], timeList[i-1][1]), 'w', encoding = 'UTF-8') as f:
         f.write(HotelList2.strip('[').strip(']'))   
print("Cost time: " + str(time.time()-start_time))