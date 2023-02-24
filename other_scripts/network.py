import json
import socket
from PyQt5.QtWidgets import QMessageBox


def get_video_names(search_name):
    s = socket.socket()
    host = socket.gethostname()  # 获取本地主机名
    port = 21463  # 设置端口号

    try:
        s.connect((host, port))
        s.send(search_name.encode())
        receive = s.recv(2048).decode("unicode-escape")
        searched_video_list = json.loads(receive)
        s.close()
        return searched_video_list
    except ConnectionRefusedError:
        QMessageBox(QMessageBox.Warning, '警告', '无法连接至服务器，请检查网络连接！').exec_()
        return []


def get_episode_number(video_name):
    if video_name != '':
        s = socket.socket()
        host = socket.gethostname()
        port = 21464

        try:
            s.connect((host, port))
            s.send(video_name.encode())
            receive = s.recv(2048).decode("unicode-escape")
            episode_number_list = json.loads(receive)
            s.close()
            return episode_number_list
        except ConnectionRefusedError:
            QMessageBox(QMessageBox.Warning, '警告', '无法连接至服务器，请检查网络连接！').exec_()
            return []


def sendBarrage(video_name, episode_number, text, time, textColor):
    data = {'video_name': video_name,
            "episode_number": episode_number,
            'text': text,
            "time": time,
            "textColor": textColor}
    data_json = json.dumps(data)
    s = socket.socket()
    host = socket.gethostname()  # 获取本地主机名
    port = 21461  # 设置端口号
    try:
        s.connect((host, port))
        s.send(data_json.encode())
        QMessageBox(QMessageBox.Information, '提醒', '发送成功').exec_()
    except ConnectionRefusedError:
        QMessageBox(QMessageBox.Warning, '警告', '无法连接至服务器，请检查网络连接！').exec_()