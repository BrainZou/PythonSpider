import multiprocessing
import re
import socket
import time
import requests
from bs4 import BeautifulSoup

#第三方接入弹幕服务器列表：
#IP地址：openbarrage.douyutv.com端口：8601
host = socket.gethostbyname("openbarrage.douyutv.com")
port = 8601

# socket 实例化
# 参数一：地址簇 socket.AF_INET  表示IPV4(默认)
#              socket.AF_INET6 表示IPV6
#              socket.AF_UNIX   只能用于单一的Unix系统进程间的通信
# 参数二：类型   socket.SOCK_STREAM  流式socket for TCP（默认）
#              socket.SOCK_DGRAM   数据格式socket,for UDP
#              socket.SOCK_RAW     原始套接字，普通的套接字无法处理ICMP,IGMP等网络报文，可以通过IP_HDRINCL套接字选项由用户构造IP头
#              socket.SOCK_RDM      是一种可靠的UDP形式，即保证交付数据报但不保证顺序，SOCK_RDM用来提供对原始协议的低级访问，
#                                   在需要执行某些特殊操作时使用，如发送ICMP报文，SOCK_RAM通常仅限于高级用户或管理员运行的程序使用
#              socket.SOCK_SEQPACKET  可靠的连续数据包服务
# 参数三：协议
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#client.connect 连接到address处的socket，一般，address的格式为元组（hostname,port）,如果连接出错，返回socket,error错误
#client.connect_ex(address) 同上的client.connect只不过会有返回值，连接成功时返回0，连接失败时返回编码
client.connect((host, port))


danmu = re.compile(b'txt@=(.+?)/cid@')

def sendmsg(msgstr):
    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    #689客户端发送给弹幕服务器的文本格式数据
    #690弹幕服务器发送给客户端的文本格式数据
    code = 689

    # 消息长度+消息长度+4字节code（消息类型+加密字段+保留字段）
    # 等价于msgHead = int.to_bytes(data_length, 4, 'little') \
    #         + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 2, 'little')+int.to_bytes(0,1,'little')+int.to_bytes(0,1,'little')

    msgHead = int.to_bytes(data_length, 4, 'little') \
              + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 4, 'little')

    #发送协议头
    client.send(msgHead)

    #发送消息
    #sent = 0
    #while sent < len(msg):
    #    tn = client.send(msg[sent:])
    #    sent = sent + tn
    #确保发送完整

    client.sendall(msg[0:])

def start(roomid):
    #登陆请求信息 房间id
    msg = 'type@=loginreq/roomid@={}/\0'.format(roomid)
    sendmsg(msg)
    #入组信息 -9999代表海量弹幕模式
    msg_more = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
    sendmsg(msg_more)

    print('---------------欢迎连接到{}的直播间---------------'.format(get_name(roomid)))
    while True:
        # client.recv(bufsize[,flag])
        # 接收socket的数据，数据以字符串形式返回，bufsize指定最多可以接收的数量，flag提供有关消息的其他信息，通常可以忽略
        data = client.recv(1024)
        danmu_more = danmu.findall(data)
        if not data:
            print("===========================客户端已经断开正在尝试重新连接=================================")
            multiprocessing.Process(target=start, args=(roomid,)).start()
        else:
            for i in range(0, len(danmu_more)):
                with open('danmu_1.txt', 'a') as fo:
                    try:
                        print(danmu_more[i].decode(encoding='utf-8'))
                        txt = danmu_more[i].decode(encoding='utf-8') + '\n'
                        fo.writelines(txt)
                    except:
                        print('-----------------出错了------------------------')


def keeplive():
    while True:
        #心跳信息
        msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
        sendmsg(msg)
        print("❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥❥")
        time.sleep(30)


def get_name(roomid):
    r = requests.get("http://www.douyu.com/" + roomid)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find('a', {'class', 'zb-name'}).string


if __name__ == '__main__':
    room_id = input('请输入房间ID： ')
    #606118 453751
    p1 = multiprocessing.Process(target=start, args=(room_id,))
    p2 = multiprocessing.Process(target=keeplive)
    p1.start()
    p2.start()
