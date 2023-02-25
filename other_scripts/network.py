import json
import socket
from PyQt5.QtWidgets import QMessageBox


def get_video_names(search_name, host):
    s = socket.socket()
    port = 21463  # 设置端口号

    try:
        s.connect((host, port))
        s.send(search_name.encode())
        receive = s.recv(2048).decode("unicode-escape")
        searched_video_list = json.loads(receive)
        s.close()
        return searched_video_list
    except socket.error as er:
        QMessageBox(QMessageBox.Warning, '错误', str(er)).exec_()
        return []


def get_episode_number(video_name, host):
    s = socket.socket()
    port = 21464

    try:
        s.connect((host, port))
        s.send(video_name.encode())
        receive = s.recv(2048).decode("unicode-escape")
        episode_number_list = json.loads(receive)
        s.close()
        return episode_number_list
    except socket.error as er:
        QMessageBox(QMessageBox.Warning, '错误', str(er)).exec_()
        return []


def sendBarrage(video_name, episode_number, text, time, textColor, host):
    data = {'video_name': video_name,
            "episode_number": episode_number,
            'text': text,
            "time": time,
            "textColor": textColor}
    data_json = json.dumps(data)
    s = socket.socket()
    port = 21461  # 设置端口号

    try:
        s.connect((host, port))
        s.send(data_json.encode())
        QMessageBox(QMessageBox.Information, '提醒', '发送成功').exec_()
    except socket.error as er:
        QMessageBox(QMessageBox.Warning, '错误', str(er)).exec_()


def receive_csv(video_name, episode_number, host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 21462

    try:
        s.connect((host, port))
        csv_file = open('temp.csv', 'wb')
        file_name = 'barrages/' + video_name + '/' + episode_number.zfill(3) + '.csv'
        s.send(file_name.encode())
        while True:
            data_utf8 = s.recv(4096)
            data = data_utf8.decode()
            if data == 'EOF':
                break
            csv_file.write(data_utf8)
        s.close()
    except socket.error as er:
        QMessageBox(QMessageBox.Warning, '错误', str(er)).exec_()
