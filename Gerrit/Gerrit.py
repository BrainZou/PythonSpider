import requests
import json
import re
import csv
import matplotlib.pyplot as plt
import pandas
import numpy as np

#gerrit的默认url是下面这个url，然后下一页按钮的url是这个url加上这一页最后一项的_sortkey(形如0049b98c0000f3b8)
DOWNLOAD_URL = 'http://192.168.8.40:8080/changes/?q=status:merged&n=25&O=1'
# DOWNLOAD_URL = 'http://192.168.8.40:8080/changes/?q=status:merged&n=25&O=1&N=0049b98c0000f3b8'


# 请求访问接口，获取到json格式数据，稍加处理，写入表格。
# 返回继续标志continue_flag，下一页URl。
def requesst(url,limit_time):
    continue_flag = 1
    # while(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Cookie': 'GerritAccount=aRqdfpU4Oa1tMBZglP3GWlz.y1oY.8am'
    }
    data = requests.get(url, headers=headers).text
    # content = data.text #你要的数据,JSON格式的
    remove = re.compile('\)\]\}\'')
    # data = data.replace(')]}\'',"")
    data = re.sub(remove, "", data)
    data_json = json.loads(data)

    with open("gerrit.csv", "a",newline='') as csvfile:
        writer = csv.writer(csvfile)
        for one in data_json:
            one["updated"] = time_format(one["updated"])
            if (time_cmp(one["updated"], limit_time) < 0):
                print("已经发现有超过时间的数据")
                continue_flag = 0
                break
            else:
                writer.writerow([one["project"], one["branch"], one["subject"], one["owner"]["name"], one["updated"]])
                print(one["project"], one["branch"], one["subject"], one["owner"]["name"], one["updated"], one["_sortkey"])
    return continue_flag, DOWNLOAD_URL + "&N=" + data_json[-1]["_sortkey"]



#两个字符串转int 相减计算大小
def time_cmp(first_time, second_time):
    print(first_time)
    print(second_time)
    return int(first_time) - int(second_time)

#对时间"2017-12-11 02:07:27.000000000"格式化为20171211020727
def time_format(time):
    time = time.replace('.000000000', "")
    time = time.replace(' ', "")
    time = time.replace(':', "")
    time = time.replace('-', "")
    return time

#用正则表达式统计不符合规范的人员及其出现的个数  得到一个DataFrame
def subject_format_count():
    nonstandard_count={}
    #newline=' '可以防止两行之间出现空行
    with open(r"gerrit.csv",newline='') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            matchObj = re.match(r"^TFS_\d+:" + row[3] + "_\D+\w+:.+", row[2])
            if matchObj:
                pass
            else:
                if row[3] in nonstandard_count:
                    nonstandard_count[row[3]] += 1
                else:
                    nonstandard_count[row[3]] = 1
    #去掉统进来的标签
    nonstandard_count.pop('owner')
    #按出现次数递减排序
    sort_nonstandard_count = sorted(nonstandard_count.items(), key=lambda v: v[1], reverse=True)
    #这地方的设置可以先查看sort_nonstandard_count 然后看看具体要的是哪个值 根据这里再写可视化
    df = pandas.DataFrame(sort_nonstandard_count, index=[item[0] for item in sort_nonstandard_count])
    return df

##可视化处理###############
def view_format_count(df):
    # x为横坐标刻度
    x = np.arange(len(df.index))
    # 设置y轴的数值，取df的1列，0列为横坐标
    y = np.array(df[1])
    # 设置x横坐标显示为0列的名字
    xticks1 = np.array(df[0])
    # 设置横坐标格式 倾斜30°
    plt.xticks(x, xticks1, size='small', rotation=30)
    # 画出柱状图 appha为透明度
    plt.bar(x, y, width=0.35, align='center', color='c', alpha=0.8)
    # 在柱形图上方显示y值 zip（x,y）得到的是tuple列表 即各列顶点的坐标
    # 然后再各列的顶点上方0.05设置一个文本 ha水平对齐left,right,center va垂直对齐 'center' , 'top' , 'bottom' ,'baseline'
    for a, b in zip(x,y):
        plt.text(a, b + 0.05, '%.0f' %b, ha='center', va='bottom', fontsize=11)
    plt.show()



def main():
    limit_time = input("请输入截止时间  格式：20171211000000\n")
    url = DOWNLOAD_URL
    continue_flag = 1
    #写标题
    with open("gerrit.csv", "w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["project", "branch", "subject", "owner", "updated"])
    while (continue_flag):
        continue_flag, url = requesst(url,limit_time)
    #可视化
    view_format_count(subject_format_count())

if __name__ == '__main__':
    main()
