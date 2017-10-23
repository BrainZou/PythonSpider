'''
import urllib
page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
try:
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    print(response.read())
except urllib.error.URLError as e:
    if hasattr(e,"code"):
        print(e.code)
    if hasattr(e,"reason"):
        print(e.reason)
        利用 urllib 发起的请求，UA 默认是 Python-urllib/3.6 
        而在 chrome 中访问 UA 则是 User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) 
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36，
        因为服务器根据 UA 来判断拒绝了 python 爬虫。
'''
'''
1）.*? 是一个固定的搭配，.和*代表可以匹配任意无限多个字符，加上？表示使用非贪婪模式进行匹配，也就是我们会尽可能短地做匹配，
以后我们还会大量用到 .*? 的搭配。

2）(.*?)代表一个分组，在这个正则表达式中我们匹配了五个分组，在后面的遍历item中，item[0]就代表第一个(.*?)所指代的内容，
item[1]就代表第二个(.*?)所指代的内容，以此类推。

3）re.S 标志代表在匹配时为点任意匹配模式，点 . 也可以代表换行符。
'''
import urllib
from urllib import request  
import re
page = 1  
url = 'http://www.qiushibaike.com/hot/page/'+str(page)  
def getHTML(url):  
    headers = {'User-Agent':
               'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}  
    req = request.Request(url, headers=headers)  
    return request.urlopen(req)  
  
try:  
    response = getHTML(url)  
    #print(response.read())  
    content = response.read().decode('utf-8')
    pattern = re.compile('''<div class="article block untagged mb15.*?<h2>(.*?)</h2>'''
						 + '''.*?<span>(.*?)</span>'''
						 + '''.*?<!-- 图片或gif -->(.*?)<div class="stats">'''
						 +'''.*?<span class="stats-vote"><i class="number">(.*?)</i>''',re.S)
    items = re.findall(pattern,content)
    for item in items:
        # 0发布人，1发布内容， 2发布图片， 3点赞数
        print(item[0].strip()+'\n'+item[1].strip()+'\n'+item[2].strip()+'\n'+item[3].strip()+'\n')
    
except urllib.request.URLError as e:  
    if hasattr(e,'code'):  
        print(e.code())  
    if hasattr(e,'reason'):  
        print(e,reason())  
