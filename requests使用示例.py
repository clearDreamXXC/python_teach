#!/uesr/bin/python3.7.4
#coding=utf-8
#Auther:清梦XXC
#@Time:2019/11/25 10:23
import requests,time,json,re,hashlib
from urllib.parse import urlencode,quote
from useragentxxc import PersonComputer as PC
"""
以下示例都是尽量选取的我之前有发过视频的源码，方便大家学习！
"""

"""
1.最基本的请求（堆糖网）
"""
url='https://www.duitang.com/napi/blog/list/by_filter_id/?' \
    'include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2C' \
    'status%2Clike_count%2Csender%2Calbum%2Creply_count' \
    '&filter_id=%E6%91%84%E5%BD%B1_%E4%BA%BA%E5%83%8F&start=0&_=1574648820'
headers={
    'Referer':'https://www.duitang.com/category/?cat=photography&sub=%E6%91%84%E5%BD%B1_%E4%BA%BA%E5%83%8F',
    'User-Agent':PC.random()
}
requests.get(url,headers=headers).content.decode('utf-8')

"""
2.post请求需要添加表单的示例（哔哩哔哩）
"""
url='https://api.bilibili.com/x/v2/reply/add'
SESSDATA='这个值大家需要自己获取'
headers={
        'Referer':f'https://www.bilibili.com/video/av70187406',
        'User-Agent':PC.random(),
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':f"SESSDATA={SESSDATA}"      #唯一一个需要的cookie参数是“SESSDATA”，找一个网络请求复制就可以了，有效期挺长的，应该是7天！
    }
data={
    'oid':'70187406',
    'type':'1',
    'message':'我喜欢你',
    'plat':'1',
    'jsonp':'jsonp',
    'csrf':'7dad9d85424ee10db7633a541a729a41'
}
response=requests.post(url,data=urlencode(data),headers=headers)

"""
3.需要设置请求超时的请求。（获取steam模拟登陆所需的加密参数）
"""
def get(username):
    url='https://store.steampowered.com/login/getrsakey/'
    headers={
        'Referer':'https://store.steampowered.com/login/?redir=&redir_ssl=1',
        'User-Agent':PC.random()
    }
    data={
        'donotcache':int(time.time()*1000),
        'username':username
    }
    try:
        requests.post(url,headers=headers,data=data,timeout=3)
    except Exception as e :
        print(f'请求错误:{e}')


"""
4.需要代理的请求（萝卜研投网）
"""
url='https://gw.datayes.com/rrp_adventure/web/supervisorCenter/slot/9080/indics?isDefaultTimeSlot=true'
headers={
    'referer':'https://robo.datayes.com/v2/landing/industrygrp',
    'user-agent':PC.random(),
    'cookie':'UM_distinctid=16e40fa44b46b4-0c48a0a18779d4-7711b3e-144000-16e40fa44b5648; gr_user_id=d30cde92-e3be-4995-a50d-45c380749e89; _ga=GA1.2.969237489.1573048174; _gid=GA1.2.1847386258.1573048174; grwng_uid=68cd7e6d-91b9-4bdb-855c-f3b5d4561301; cloud-anonymous-token=79b8045c4ec94c8084223fd963e5301b; ba895d61f7404b76_gr_last_sent_cs1=5631731%40wmcloud.com; ba895d61f7404b76_gr_session_id=6302d029-3319-43bf-8717-7ca8a66a12cf; ba895d61f7404b76_gr_last_sent_sid_with_cs1=6302d029-3319-43bf-8717-7ca8a66a12cf; ba895d61f7404b76_gr_session_id_6302d029-3319-43bf-8717-7ca8a66a12cf=true; cloud-sso-token=1CB54F7049BC3098F58EB9D87943EFBD; _gat=1; ba895d61f7404b76_gr_cs1=5631731%40wmcloud.com'
}
proxies={'https':'47.100.171.38:8080','http':'219.131.243.114:9797'}
res=requests.get(url,headers=headers,proxies=proxies).json()['data']

"""
5.需要cookie的请求。（12306官网）
"""
url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2019-12-08&leftTicketDTO.from_station=VAP&leftTicketDTO.to_station=CQW&purpose_codes=ADULT'
headers={
        'Referer':'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC,BJP&ts=%E9%87%8D%E5%BA%86,CQW&date=2019-11-30&flag=N,N,Y',
        'User-Agent':PC.random(),
        'Cookie':'RAIL_DEVICEID='  #在试验过后发现，只有这段参数有用
    }
requests.get(url,headers=headers).json()

"""
6.控制台输出请求到的数据
"""
#这里的response必须是.content.decode('utf-8')或.json()之后的
print(response)

"""
7.保存音频、视频、图片和文字的简单示例。（抖音短视频）
"""
url='https://api.amemv.com/aweme/v1/play/?video_id=v0200f8b0000bmmt34edm153h8no3rq0&line=1&ratio=540p&watermark=1&media_type=4&vr_type=0&improve_bitrate=0&logo_name=aweme_self'
headers={
    'User-Agent':'com.ss.android.ugc.aweme/820 (Linux; U; Android 5.1.1; zh_CN; SM-G955F; Build/JLS36C; Cronet/58.0.2991.0)',
    'Range':'bytes=0-'
}
with open('名称.mp4','wb')as f:
    f.write(requests.get(url, headers=headers).content)
"""
8.比较难的，各类参数都需要的请求。(携程国际-港澳台机票)
"""
#有很多可以优化的地方，但是看起来挺清晰的，就不做修改了
def link_data(date,dcity,acity):
    citydata = {'Code': [], 'CityId': [], 'CountryId': [], 'ProvinceId': [], 'CityName': [], 'CountryName': [],'TimeZone': []}
    date = '-'.join((date[0:4], date[4:6], date[6:8]))
    for i in [dcity,acity]:
        response=json.loads(requests.get('https://flights.ctrip.com/international/search/api/poi/search?key=%s'%quote(i)).content.decode('utf-8'))['Data'][0]
        citydata['Code'].append(response['Code'])
    url='https://flights.ctrip.com/international/search/oneway-%s-%s?depdate=%s&cabin=y_s&adult=1&child=0&infant=0'%(citydata['Code'][0],citydata['Code'][1],date)
    headers={
        'Referer':'https://flights.ctrip.com/international/search/',
        'User-Agent':PC.random()
    }
    datas=json.loads(re.findall('[GlobalSearchCriteria =](.*)[;]',requests.get(url,headers=headers).content.decode('utf-8'))[2].split('=')[-1])
    citydata['CityId']=[datas['flightSegments'][0]['departureCityId'],datas['flightSegments'][0]['arrivalCityId']]
    citydata['CountryId']=[datas['flightSegments'][0]['departureCountryId'],datas['flightSegments'][0]['arrivalCountryId']]
    citydata['ProvinceId']=[datas['flightSegments'][0]['departureProvinceId'],datas['flightSegments'][0]['arrivalProvinceId']]
    citydata['CityName']=[datas['flightSegments'][0]['departureCityName'],datas['flightSegments'][0]['arrivalCityName']]
    citydata['CountryName']=[datas['flightSegments'][0]['departureCountryName'],datas['flightSegments'][0]['arrivalCountryName']]
    citydata['TimeZone']=[datas['flightSegments'][0]['departureCityTimeZone'],datas['flightSegments'][0]['arrivalCityTimeZone']]
    citydata['timeZone']=datas['flightSegments'][0]['timeZone']
    citydata['transactionID']=datas['transactionID']
#以下是请求包含航班信息的部分
    url0='https://flights.ctrip.com/international/search/api/search/batchSearch?v='
    headers={
        'Referer':'https://flights.ctrip.com/international/search/oneway-%s-%s?depdate=%s&cabin=y_s&adult=1&child=0&infant=0&directflight='%(citydata['Code'][0],citydata['Code'][1],date),
        'User-Agent':PC.random(),
        'Content-Type':'application/json;charset=utf-8',
        'sign':hashlib.md5(bytes(citydata['transactionID']+citydata['Code'][0]+citydata['Code'][1]+date,encoding='utf-8')).hexdigest(),
        'transactionid':citydata['transactionID']
    }
    data={"flightWayEnum":"OW","arrivalProvinceId":citydata['ProvinceId'][1],
          "extGlobalSwitches":{"useAllRecommendSwitch":'false'},"arrivalCountryName":citydata['CountryName'][1],
          "infantCount":0,"cabin":"Y_S","cabinEnum":"Y_S","departCountryName":citydata['CountryName'][0],
          "flightSegments":[{"departureDate":date,"arrivalProvinceId":citydata['ProvinceId'][1],
                             "arrivalCountryName":citydata['CountryName'][1],"departureCityName":citydata['CityName'][0],
                             "departureCityCode":citydata['Code'][0],"departureCountryName":citydata['CountryName'][0],
                             "arrivalCityName":citydata['CityName'][1],"arrivalCityCode":citydata['Code'][1],
                             "departureCityTimeZone":citydata['TimeZone'][0],"arrivalCountryId":citydata['CountryId'][1],
                             "timeZone":citydata['timeZone'],"departureCityId":citydata['CityId'][0],"departureCountryId":citydata['CountryId'][0],
                             "arrivalCityTimeZone":citydata['TimeZone'][1],"departureProvinceId":citydata['ProvinceId'][0],"arrivalCityId":citydata['CityId'][1]}],
          "childCount":0,"segmentNo":1,"adultCount":1,"extensionAttributes":{"isFlightIntlNewUser":'false'},"transactionID":citydata['transactionID'],
          "directFlight":'false',"departureCityId":citydata['CityId'][0],"isMultiplePassengerType":0,"flightWay":"S","arrivalCityId":citydata['CityId'][1],"departProvinceId":citydata['ProvinceId'][0]}
    return json.loads(requests.post(url0,data=json.dumps(data),headers=headers).content.decode('utf-8'))['data']['flightItineraryList']