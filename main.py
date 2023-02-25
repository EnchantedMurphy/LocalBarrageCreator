import sys
from os import startfile
from random import randint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from other_scripts import network, standardoptions, csvTOass
from ui import ui, ui_barrage_options, ui_about


class MyWidget(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setupUi(self)

        global textSpeedIndex, textSizeIndex, PlayResX, PlayResY, native_video, video_name, video_ep, textColor, host

        textSpeedIndex, textSizeIndex, PlayResX, PlayResY, host = standardoptions.get_options()  # 获取默认设置
        native_video = ''
        video_name = ''
        video_ep = 1
        textColor = 'ffffff'

        # 打开帮助文档
        self.action_help.triggered.connect(self.help)

        # 点击搜索按钮
        self.pushButton_Search.clicked.connect(self.search)
        # 列表内容切换
        self.comboBox_chosen.currentTextChanged.connect(self.choose)
        # 集数内容切换
        self.comboBox_episode.currentTextChanged.connect(self.choose_ep)

        # 生成弹幕
        # 选择本地视频
        self.pushButton_nativeVideo.clicked.connect(self.native_video)
        # 选择弹幕大小
        self.comboBox_textSize.addItems(['小', '较小', '中等', '较大', '大'])
        self.comboBox_textSize.setCurrentIndex(textSizeIndex)
        self.comboBox_textSize.currentTextChanged.connect(self.text_size)
        # 选择弹幕速度
        self.comboBox_textSpeed.addItems(['慢', '较慢', '中等', '较快', '快'])
        self.comboBox_textSpeed.setCurrentIndex(textSpeedIndex)
        self.comboBox_textSpeed.currentTextChanged.connect(self.text_speed)
        # 点击生成按钮
        self.pushButton_generate.clicked.connect(self.generate)

        # 发送弹幕
        # 选择弹幕颜色
        self.pushButton_color.clicked.connect(self.color)
        # 点击发送按钮
        self.pushButton_send.clicked.connect(self.send)

    def help(self):
        startfile('帮助文档.txt')

    def search(self):
        search_name = self.lineEdit_Search.text()
        if search_name != '':
            result = network.get_video_names(search_name, host)
            self.comboBox_chosen.clear()
            self.comboBox_chosen.addItems(result)

    def choose(self):
        global video_name
        video_name = self.comboBox_chosen.currentText()
        if video_name != '':
            episode_list = network.get_episode_number(video_name, host)
            self.comboBox_episode.clear()
            self.comboBox_episode.addItems(episode_list)

    def choose_ep(self):
        global video_ep
        video_ep = self.comboBox_episode.currentText()

    def native_video(self):
        global native_video
        native_video = QFileDialog.getOpenFileName(None, "选择本地视频文件")[0]
        self.lineEdit_nativeVideo.setText(native_video)

    def text_size(self):
        global textSizeIndex
        textSizeIndex = self.comboBox_textSize.currentIndex()

    def text_speed(self):
        global textSpeedIndex
        textSpeedIndex = self.comboBox_textSpeed.currentIndex()

    def generate(self):
        network.receive_csv(video_name, video_ep, host)
        csvTOass.main(native_video, textSpeedIndex, textSizeIndex, PlayResX, PlayResY)

    def color(self):
        global textColor
        selectedColor = QColorDialog.getColor()
        textColor = selectedColor.name()[1:7]
        palette = QPalette()
        palette.setColor(QPalette.Window, selectedColor)
        self.widget_color.setPalette(palette)

    def send(self):
        text = self.lineEdit_textSend.text()
        selectedTime = self.timeEdit.time()
        hour = selectedTime.toString('hh')
        minute = selectedTime.toString('mm')
        second = selectedTime.toString('ss')
        barrage_time = int(hour)*360000 + int(minute)*6000 + int(second)*100 + randint(0, 99)
        network.sendBarrage(video_name, video_ep, text, barrage_time, textColor, host)


class ChildWin_barrage_options(QDialog, ui_barrage_options.Ui_Dialog_barrage_options):
    def __init__(self):
        super(ChildWin_barrage_options, self).__init__()
        self.setupUi(self)

        self.comboBox_textSize.addItems(['小', '较小', '中等', '较大', '大'])
        self.comboBox_textSize.setCurrentIndex(textSizeIndex)

        self.comboBox_textSpeed.addItems(['慢', '较慢', '中等', '较快', '快'])
        self.comboBox_textSpeed.setCurrentIndex(textSpeedIndex)

        self.lineEdit_PlayResX.setText(str(PlayResX))
        self.lineEdit_PlayResY.setText(str(PlayResY))

        self.pushButton_confirm.clicked.connect(self.confirm)
        self.pushButton_cancel.clicked.connect(self.cancel)

    def confirm(self):
        global PlayResX, PlayResY
        options_textSizeIndex = self.comboBox_textSize.currentIndex()
        options_textSpeedIndex = self.comboBox_textSpeed.currentIndex()
        options_PlayResX = int(self.lineEdit_PlayResX.text())
        options_PlayResY = int(self.lineEdit_PlayResY.text())
        PlayResX = options_PlayResX
        PlayResY = options_PlayResY
        standardoptions.set_options(options_textSpeedIndex, options_textSizeIndex, options_PlayResX, options_PlayResY, host)
        self.close()

    def cancel(self):
        self.close()


class ChildWin_about(QDialog, ui_about.Ui_Dialog_about):
    def __init__(self):
        super(ChildWin_about, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 支持高分辨率显示器
    app = QApplication(sys.argv)
    widget = MyWidget()
    child_barrage_options = ChildWin_barrage_options()
    child_about = ChildWin_about()
    widget.setFixedSize(widget.width(), widget.height())  # 固定窗口大小
    child_barrage_options.setFixedSize(child_barrage_options.width(), child_barrage_options.height())
    child_about.setFixedSize(child_about.width(), child_about.height())
    widget.action_barrage_options.triggered.connect(child_barrage_options.show)
    widget.action_about.triggered.connect(child_about.show)
    widget.show()
    sys.exit(app.exec_())
