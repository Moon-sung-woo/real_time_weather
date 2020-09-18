# -*- coding: utf-8 -*-
while True:
    from urllib.request import urlopen, Request
    import urllib
    import bs4
    import serial
    import time

    afternoon_flag = True
    morning_flag = True
    weather = [0, 0, 1, 1, 1, 1, 0]

    #----------------------------------------------------------------------------------------------------------------------
    location = '월계3동'

    enc_location = urllib.parse.quote(location + '+날씨')

    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+ enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html5lib')
    print('현재 ' + location + ' 온도는 ' + soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text + '도 입니다.')
    now_temp =int(soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text)

    if now_temp < 0:
        weather[6] = 1
    else:
        weather[6] = 0
    #print('현재 ' + location + ' 미세먼지 농도는 ' + soup.find('dd', class_='lv2').find('span', class_='num').text + ' 입니다.')
    print('현재 ' + location + ' 날씨는 ' + soup.find('ul', class_='info_list').find('p', class_='cast_txt').text + ' 입니다.')
    #print('현재 ' + location + ' 자외선 지수' + soup.find('span', class_='lv2').find('span', class_='num').text + ' 입니다.')

    temp_location = '서울'

    temp_enc_location = urllib.parse.quote(location + '+온도')

    temp_url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+ enc_location

    temp_req = Request(temp_url)
    temp_page = urlopen(temp_req)
    temp_html = temp_page.read()
    temp_soup = bs4.BeautifulSoup(html, 'html5lib')
    morning_temp = temp_soup.find('ul', class_='list_area _pageList').text
    list_morning_temp = morning_temp.split()
    m_temp = temp_soup.find('li', class_='date_info today').text
    m_temp.split()
    #print(m_temp.split())
    print(m_temp.split()[8])
    #print('현재 ' + location + ' 온도는 ' + temp_soup.find('ul', class_='list_area _pageList').text + '도 입니다.')
    #print(list_morning_temp)


    #---------------------------------------------초미세먼지----------------------------------------------------------------
    dust_location = '오전'
    dust_enc_location = urllib.parse.quote(dust_location + '+초미세먼지')

    dust_url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query='+ dust_enc_location

    dust_req = Request(dust_url)
    dust_page = urlopen(dust_req)
    dust_html = dust_page.read()
    dust_soup = bs4.BeautifulSoup(dust_html, 'html5lib')
    dust = dust_soup.find('div', class_='tb_scroll').text
    list_dust = dust.split()
    #print('현재 ' + location + ' 초미세먼지 ' + dust)#.find('span', class_='lv2').text + ' 입니다.')
    #print(list_dust)
    print(' 서울 오전 초미세먼지: ' + list_dust[9])
    print(' 서울 오후 초미세먼지: ' + list_dust[10])

    if list_dust[9].find('나쁨') == -1:
        weather[4] = 0

    if list_dust[10].find('나쁨') == -1:
        weather[5] = 0

    #-------------------------------------------------자외선----------------------------------------------------------------
    uv_location = '월계3동'
    uv_enc_location = urllib.parse.quote('전국자외선')

    uv_url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+ uv_enc_location

    uv_req = Request(uv_url)
    uv_page = urlopen(uv_req)
    uv_html = uv_page.read()
    uv_soup = bs4.BeautifulSoup(uv_html, 'html5lib')
    uv = uv_soup.find('div', class_='detail_box').text
    list_uv = uv.split()
    #print('현재 ' + location + ' 자외선 ' + uv)
    #print(list_uv)
    print(' 서울 오전 자외선: ' + list_uv[16])
    print(' 서울 오후 자외선: ' + list_uv[17])

    if list_uv[16].find('나쁨') == -1:
        weather[2] = 0

    if list_uv[17].find('나쁨') == -1:
        weather[3] = 0

    #-------------------------------------------------전국날씨---------------------------------------------------------------
    morning_location = '전국오늘오전'
    morning_enc_location = urllib.parse.quote(morning_location + '날씨')
    morning_url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+ morning_enc_location

    morning_req = Request(morning_url)
    morning_page = urlopen(morning_req)
    morning_html = morning_page.read()
    morning_soup = bs4.BeautifulSoup(morning_html, 'html5lib')
    morning = morning_soup.find('div', class_='map _map_normal').text
    list_morning = morning.split()
    print('현재전국오전날씨는 ' + morning)

    for i in range(5):
        if list_morning[i] == '비':
            print(' 현재 서울 오전 날씨: ' + list_morning[i])
            weather[0] = 1
            morning_flag = False

    if morning_flag:
        print(' 현재 서울 오전 날씨: ' + list_morning[1])

    morning_flag = True

    #-----------------------------------------------------------------------------------------------------------------------

    afternoon_location = '전국오늘오후'
    afternoon_enc_location = urllib.parse.quote(afternoon_location + '날씨')
    afternoon_url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+ afternoon_enc_location

    afternoon_req = Request(afternoon_url)
    afternoon_page = urlopen(afternoon_req)
    afternoon_html = afternoon_page.read()
    afternoon_soup = bs4.BeautifulSoup(afternoon_html, 'html5lib')
    afternoon = afternoon_soup.find('div', class_='map _map_normal').text
    list_afternoon = afternoon.split()
    print(list_afternoon)

    for i in range(5):
        if list_afternoon[i] == '비':
            print(' 현재 서울 오후 날씨: ' + list_afternoon[i])
            weather[1] = 1
            afternoon_flag = False

    if afternoon_flag:
        print(' 현재 서울 오후 날씨: ' + list_afternoon[1])

    afternoon_flag = True

    print(weather)
    re_w = str(weather[0]) + str(weather[1]) + str(weather[2]) + str(weather[3]) + str(weather[4]) + str(weather[5]) + str(weather[6])
    print(re_w)
    k = "w" + re_w
    print(k)
    time.sleep(10)
#-------------------------------------------------통신------------------------------------------------------------------
'''
PORT = '/dev/ttyACM1'
BaudRate = 9600

ARD = serial.Serial(PORT, BaudRate)

str_weather = str(weather)
Trans = "w" + str_weather
Trans = Trans.encode('utf-8')

while (True):
    ARD.write(Trans)  # Q12345678 전송
    time.sleep(10)
'''