import os.path

import pandas as pd
from PyQt5.QtWidgets import QMessageBox


# 计算弹幕在屏幕上出现时间的算法——通过计算弹幕文本长度占视频画面长度的比例确保每条弹幕显示的时间相同
def delta_calculation(textLen, textSpeed, textSize):
    textRate = textLen / textSize
    lenTotal = 1 + textRate
    timeDelta = lenTotal * textSpeed * 100
    return timeDelta


# 计算时间的函数，输入时间码（毫秒），输出用于写入的字符串（hh:mm:ss.ms）
def time_calculation(time):
    time_ms = int(time % 100)
    time_sec = int(((time - time_ms) / 100) % 60)
    time_min = int(((time - time_sec * 100 - time_ms) / 6000) % 60)
    time_hour = int(time // 360000)
    # 分别计算毫秒、秒、分钟、小时位上的数值大小
    write_ms = str(time_ms).zfill(2)
    write_sec = str(time_sec).zfill(2)
    write_min = str(time_min).zfill(2)
    write_hour = str(time_hour).zfill(2)
    # 将毫秒、秒、分钟、小时分别转换为两位的字符串
    return("%s:%s:%s.%s" % (write_hour , write_min , write_sec , write_ms))


# 弹幕位置的算法
def barrage_location(PlayResX, PlayResY, textLen, textSpeed, textSize, textSizeNumber, lines, time_start):
    X1 = int((textLen / textSize) * PlayResX / 2 + PlayResX)    # 弹幕出现的位置
    X2 = int(0 - (textLen / textSize) * PlayResX / 2)           # 弹幕消失的位置
    textRate = textLen / textSize
    timeDelta = textRate * textSpeed * 100
    for n in range(len(lines)):
        if time_start >= lines[n]:
            lines[n] = lines[n] + timeDelta + 50
            Y = int((n + 1) * textSizeNumber)
            break
        elif n == len(lines)-1:
            Y = PlayResY + textSizeNumber
    return "%s,%s,%s,%s" % (X1, Y, X2, Y)


# 用于生成ass文件的函数，输入本地视频文件的名称
def write_ass(movie_path_splited, PlayResX, PlayResY, textSpeed, textSize):
    df = pd.read_csv('temp.csv', encoding="UTF-8")
    time = df['time']
    text = df['text']
    color = df['color']
    if PlayResX/16 >= PlayResY/9:
        textSizeNumber = PlayResX // textSize
    else:
        textSizeNumber = (PlayResY / 9 * 16) // textSize
    lines = []
    line = PlayResY // textSizeNumber
    for i in range(line):
        lines.append(0)
    df_len = len(time)
    # 读取视频对应csv数据表中的数据，包括弹幕出现的时间码（毫秒）与文本及其颜色
    ass_name = movie_path_splited + '.ass'  
    try:
        ass=open(ass_name,"x", encoding='UTF-8')
        ass.write("[Script Info]\n") # 写入ass文件中的固定开头，一般不会改变
        ass.write("ScriptType: v4.00+\n")
        ass.write("Collisions: Normal\n")
        ass.write("PlayResX: %s\n" % (PlayResX))
        ass.write("PlayResY: %s\n\n" % (PlayResY))
        ass.write("[V4+ Styles]\n")
        ass.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        ass.write("Style: Default, Microsoft YaHei, %s, &H00FFFFFF, &H00FFFFFF, &H00000000, &H00000000, 0, 0, 0, 0, 100, 100, 0.00, 0.00, 1, 1, 0, 2, 20, 20, 20, 0\n\n" % (textSizeNumber))
        ass.write("[Events]\n")
        ass.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        for i in range(df_len):
            time_start = int(time[i])                   # 弹幕出现的时间码（毫秒）
            time_end = time_start+delta_calculation(len(text[i]), textSpeed, textSize)             # 弹幕消失的时间码（毫秒）
            write_start = time_calculation(time_start)
            write_end = time_calculation(time_end)
            ass.write("Dialogue: 0,%s,%s,Default,,0,0,0,,{\move(%s)\c&H%s}%s\n" % (write_start, write_end, barrage_location(PlayResX, PlayResY, len(text[i]), textSpeed, textSize, textSizeNumber, lines, time_start), color[i], text[i]))
    # 创建ass文件，并逐行写入每条弹幕对应的ass文件信息
        QMessageBox(QMessageBox.Information, '提醒', '生成成功').exec_()
    except FileExistsError:
        QMessageBox(QMessageBox.Warning, '警告', '已存在同名字幕文件，请删除或重命名后重试').exec_()


def main(movie_path, textSpeedIndex, textSizeIndex, PlayResX, PlayResY):
    textSizeList = [60, 40, 30, 20, 15]
    textSpeedList = [15, 12, 10, 8, 5]
    textSize = textSizeList[textSizeIndex]
    textSpeed = textSpeedList[textSpeedIndex]
    movie_path_splited = os.path.splitext(movie_path)[0]    # 去掉文件扩展名
    write_ass(movie_path_splited, PlayResX, PlayResY, textSpeed, textSize)

