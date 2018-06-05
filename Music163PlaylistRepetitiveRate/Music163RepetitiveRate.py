# encoding=utf8
from __future__ import division
import requests
from bs4 import BeautifulSoup
from urllib import quote
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import re
# 使用PhantomJS
# executable_path指明PhantomJS的路径
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.loadImages"] = False
headers = {
    'Referer':'http://music.163.com',
    'Host':'music.163.com',
    'User-Agent':'Mozilla/5.e(X11;Linux ×86_64;rv:38.e) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
#根据名字获取到喜欢的歌单链接
def get_playlist_by_name(username):
    locatorttc = (By.CLASS_NAME, 'ttc')
    locatordec = (By.CLASS_NAME, 'dec')
    #指定contentFrame 获取"ttc"class,再获取"a"tag,最后获取到用户主页链接
    #quote转码中文
    try:
        driver = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        driver.get('http://music.163.com/#/search/m/?s={}&type=1002'.format(quote(username.encode('utf8'))))
        #WebDriverWait(driver, 5, 0.3).until(EC.presence_of_element_located(locatorttc))
        driver.switch_to.frame("contentFrame")
        sleep(1)
        tr = driver.find_element_by_class_name('ttc')
        user = tr.find_element_by_tag_name('a')
        #加载用户主页 获取到私人最喜欢的歌单的链接并返回
        driver.get(user.get_attribute('href'))
        #WebDriverWait(driver, 5, 0.3).until(EC.presence_of_element_located(locatordec))
        driver.switch_to.frame("contentFrame")
        sleep(1)
        dec = driver.find_element_by_class_name('dec')
        #print(dec.page_source)
        playlist = dec.find_element_by_tag_name('a')
        return playlist.get_attribute('href')
    except Exception as e:
	print e
        return ""
    finally:
        driver.close()
def repetitive_rate_by_playlistlink(link1,link2):
    #找到歌单中所有歌组成字符串数组
    lists1=[]
    lists2=[]
    #linklist=[link1,link2]
    #for url in linklist:
    #    s = requests.session()
    #    s = BeautifulSoup(s.get(url, headers=headers).content, 'lxml')
    #    main = s.find('ul', {'class': 'f-hide'})
    #    for music in main.find_all('a'):
    #        lists.append(music.text)
    s1 = requests.session()
    s1 = BeautifulSoup(s1.get(link1,headers=headers).content,'lxml')
    main = s1.find('ul', {'class': 'f-hide'})
    for music in main.find_all('a'):
        lists1.append(music.text)
    s2 = requests.session()
    s2 = BeautifulSoup(s2.get(link2,headers=headers).content,'lxml')
    main = s2.find('ul', {'class': 'f-hide'})
    for music in main.find_all('a'):
        lists2.append(music.text)
    myset1 = set(lists1)
    myset2 = set(lists2)
    pattern = re.compile('\Wu\'')
    intersectionset = re.sub(pattern,'<br>\'',str(myset1 & myset2))
    length = len(myset1 | myset2)+len(myset1 & myset2)
    print intersectionset
    return(u"你们的歌单重合率为:%f%%<br><br>重复歌曲共%d首如下:%s"%(len(myset1 & myset2)*200/length,len(myset1&myset2),intersectionset.decode('unicode-escape')))
#if __name__ == '__main__':
#    sys.exit(repetitive_rate_by_playlistlink(get_playlist_by_name(sys.argv[1]),get_playlist_by_name(sys.argv[2])))
