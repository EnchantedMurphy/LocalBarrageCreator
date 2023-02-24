from socket import *
import struct
import json
import os
import sys
import time


def download(video_name, video_ep):
    # 创建客户端
    client = socket(AF_INET, SOCK_STREAM)
    ip_port = ('127.0.0.1', 21463)
    buffSize = 1024
    client.connect(ip_port)
    print("connecting...")

    # 开始通信
    while True:
        # 文件信息发送给服务器
        video_ep = video_ep.zfill(3)
        filePath = 'barrages/'+video_name+'/'
        client.send(bytes(filePath, "utf-8"))
        fileName = video_ep+'.csv'
        client.send(bytes(fileName, "utf-8"))

        # 默认文件存在，接受并解析报头的长度，接受报头的内容
        head_struct = client.recv(4)
        head_len = struct.unpack('i', head_struct)[0]
        data = client.recv(head_len)

        # 解析报头字典
        head_dir = json.loads(data.decode('utf-8'))
        filesize_b = head_dir["fileSize"]
        filename = head_dir["fileName"]

        # 接受真实的文件内容
        recv_len = 0
        recv_mesg = b''

        f = open("temp.csv", "wb")

        while recv_len < filesize_b:
            if filesize_b - recv_len > buffSize:
                # 假设未上传的文件数据大于最大传输数据
                recv_mesg = client.recv(buffSize)
                f.write(recv_mesg)
                recv_len += len(recv_mesg)
            else:
                # 需要传输的文件数据小于最大传输数据大小
                recv_mesg = client.recv(filesize_b - recv_len)
                recv_len += len(recv_mesg)
                f.write(recv_mesg)
                f.close()
                print("文件接收完毕！")

        # 向服务器发送信号，文件已经上传完毕
        completed = "1"
        client.send(bytes(completed, "utf-8"))

        print("退出系统！")
        client.close()
        break
