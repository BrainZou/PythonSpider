import requests
import json
import re
import csv
import matplotlib.pyplot as plt
import pandas
import numpy as np

gerrit_list = []
# DOWNLOAD_URL = 'http://192.168.8.40:8080/changes/?q=status:merged&n=25&O=1&N=0049b98c0000f3b8'
DOWNLOAD_URL = 'http://192.168.8.40:8080/changes/?q=status:merged&n=25&O=1'


def requesst(url,limit_time):
    finish_flag = 0
    # while(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Cookie': 'GerritAccount=aRqdfi-RiZW85kCc4mqqwpXUxlHXe-hp'
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
                finish_flag = 1
                break
            else:
                writer.writerow([one["project"], one["branch"], one["subject"], one["owner"]["name"], one["updated"]])
                print(one["project"], one["branch"], one["subject"], one["owner"]["name"], one["updated"], one["_sortkey"])
        return finish_flag,data_json[-1]["updated"], DOWNLOAD_URL + "&N=" + data_json[-1]["_sortkey"]



#两个时间字符型转int 相减计算大小
def time_cmp(first_time, second_time):
    print(first_time)
    print(second_time)
    return int(first_time) - int(second_time)

#对时间格式化为20171212101720
def time_format(time):
    time = time.replace('.000000000', "")
    time = time.replace(' ', "")
    time = time.replace(':', "")
    time = time.replace('-', "")
    return time

#统计不符合标准的人员及其不标准格式的个数  得到一个DataFrame
def subject_format_count():
    nonstandard_count={}
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
    #print(nonstandard_count)
    nonstandard_count.pop('owner')
    sort_nonstandard_count = sorted(nonstandard_count.items(), key=lambda v: v[1], reverse=True)
    #print (sort_nonstandard_count)
    df = pandas.DataFrame(sort_nonstandard_count, index=[item[0] for item in sort_nonstandard_count])
    return df

def view_format_count(df):
##可视化处理######################
    # x为横坐标刻度
    x = np.arange(len(df.index))
    # 设置y轴的数值，取df的1列，0列为横坐标
    y = np.array(df[1])
    xticks1 = np.array(df[0])  # 0列为横坐标
    plt.xticks(x, xticks1, size='small', rotation=30)
    # 画出柱状图
    plt.bar(x, y, width=0.35, align='center', color='c', alpha=0.8)
    for a, b in zip(x,y):
        plt.text(a, b + 0.05, '%.0f' %b, ha='center', va='bottom', fontsize=11)
    plt.show()



def main():
    limit_time = input("请输入截止时间  格式：20171211000000\n")
    # url = DOWNLOAD_URL+'#/q/status:merged,n,0049b98c0000f3b8'
    url = DOWNLOAD_URL
    #写标题
    with open("gerrit.csv", "w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["project", "branch", "subject", "owner", "updated"])
    while (url):
        finish_flag,last_time, url = requesst(url,limit_time)
        #print(url)
        time_format(last_time)
        #print(last_time)
        # last_time = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')

        if finish_flag:
            print("已完成")
            break
        else:
            pass

        view_format_count(subject_format_count())

if __name__ == '__main__':
    main()
