from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtCore import Qt
import string
import random
from copy import deepcopy


class ChildWindow(QDialog):
    def __init__(self, word_vocab, hash_map):
        super().__init__()

        self.current_en = "sldfjlk"
        self.current_ch = "slkdfjsldk"
        self.word_vocab = word_vocab
        self.hash_map = hash_map
        print("wv", word_vocab)
        print("hm", hash_map)

        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        self.set_label()

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.label)
        # self.vbox.addWidget(self.label_2)
        vbox.addStretch()

        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("单词测试")

        self.button1 = self.set_button_next()
        self.button2 = self.set_button_get_answer()
        self.setWindowTitle('单词检测')

    def set_label(self):
        self.label = QLabel(self)
        self.get_word()
        # label.setText(word)
        self.label.setFont(QFont("Consolas", 35))
        self.label.setAutoFillBackground(True)
        # label.move(130, 30)
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.gray)
        self.label.setPalette(palette)
        # 居中必须要设置布局才能显示
        self.label.setAlignment(Qt.AlignCenter)

    def set_button_next(self):
        button = QPushButton("下一个", self)
        button.resize(120, 100)
        button.move(250, 160)  # (30, 160)
        button.setFont(QFont("Consolas", 15))

        button.clicked.connect(self.get_word)

        return button

    def set_button_get_answer(self):
        button = QPushButton("查看译义", self)
        button.resize(120, 100)
        button.move(30, 160)
        button.setFont(QFont("Consolas", 15))

        button.clicked.connect(self.get_answer)

        return button

    def get_word(self, rand=False):
        if rand:  # 测试
            chars = string.ascii_lowercase
            word_len = random.choice(list(range(4, 9)))
            word = ''.join(random.choices(chars, k=word_len))
            return word

        # 如果单词都遍历完了
        if all(self.hash_map):
            # 初始化标记数据结构
            self.label.setText(self.current_en)
            self.hash_map = self.hash_map = dict([(item[0], 0)
                                                  for item in self.word_vocab])
            random.shuffle(self.word_vocab)

        flag = 0

        for row in self.word_vocab:
            en, ch = row
            if not self.hash_map[en]:
                self.hash_map[en] = 1
                flag = 1
                self.current_en = en
                self.current_ch = ch
                break

        print("flag", flag)
        print("hash_map", self.hash_map)

        if flag:
            self.label.setText(self.current_en)

    def get_answer(self):
        if self.button2.text() == "查看译义":
            self.label.setText(self.current_ch)
            self.button2.setText("查看单词")
        else:
            self.label.setText(self.current_en)
            self.button2.setText("查看译义")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(330, 250)
        self.had_opened_new_win = False
        # self.word_matrix = list()

    def set_btn1(self):
        btn1 = QPushButton("单词测试", self)
        btn1.resize(120, 100)
        btn1.move(30, 70)
        btn1.setFont(QFont("Consolas", 15))
        btn1.setToolTip("<b>无情地进行单词测试吧</b>")

        # 触发事件
        btn1.clicked.connect(self.new_window)
        return btn1

    def set_btn2(self):
        btn2 = QPushButton("导入单词", self)
        btn2.resize(120, 100)
        btn2.move(180, 70)
        btn2.setFont(QFont("Consolas", 15))
        btn2.setToolTip("<b>无情地导入你的单词吧</b>")

        # 触发事件
        btn2.clicked.connect(self.open_file)

        return btn2

    def new_window(self):
        global word_matrix
        # 如果未导入
        if word_matrix:
            child_window = ChildWindow(self.word_vocab, self.hash_map)
            child_window.show()
            child_window.exec_()
        # 如果都所有单词都遍历过一遍了
        # elif self.had_opened_new_win and all(self.hash_map.values()):
        #     self.word_vocab = deepcopy(word_matrix)
        #     random.shuffle(self.word_vocab)
        #     self.hash_map = dict([(item[0], 0) for item in self.word_vocab])
        else:
            # 提示框
            self.messageDialog_error2()

    def open_file(self):
        self.message_reminding()
        global word_matrix
        openfile_name = QFileDialog.getOpenFileNames(self, '选择文件吧！')
        # (list, str)
        if openfile_name[0]:
            abs_file_path = openfile_name[0][0]
            # print(openfile_name[0][0].split('/')[-1])
            with open(abs_file_path, 'r', encoding="utf-8") as f:
                content = f.readlines()
                print(content)
                for line in content:
                    if len(line.split()) < 2:
                        self.messageDialog_error1()
                        word_matrix = list()
                        break
                    else:
                        En, Ch = line.split()
                        word_matrix.append([En, Ch])
                    # if len(line) < 2:
                    #     continue
                    # try:
                    #     En, Ch = line.split()
                    #     word_matrix.append([En, Ch])
                    # except ValueError:  # 文件格式错误
                    #     self.messageDialog_error1()  # 弹出提示框
                    #     # 还原数据
                    #     word_matrix = list()
                    #     break  # 注意break，不然错误的行数是多少行，就弹出多少次提示窗口

            print(word_matrix)
            # deep copy, word_vocab: 2D matrix [[en, ch], ...]
            self.word_vocab = deepcopy(word_matrix)
            random.shuffle(self.word_vocab)

            # 使用散列表记录已经出现过的单词
            self.hash_map = dict([(item[0], 0) for item in self.word_vocab])
            self.had_opened_new_win = True

    def message_reminding(self):
        render_text = "<b>请将导入文件的格式设置为：<p>英文单词 中文译义</p>中间用空格隔开<p>不同行之间用\\n换行</b>"
        msg = QMessageBox.information(self, "提示", render_text, QMessageBox.Ok)

    def messageDialog_error1(self):
        # 核心功能代码就两行，可以加到需要的地方
        msg_box = QMessageBox(QMessageBox.Warning, '警告', '文件格式错误', QMessageBox.Ok)
        msg_box.exec_()

    def messageDialog_error2(self):
        # 核心功能代码就两行，可以加到需要的地方
        msg = QMessageBox.warning(self, "警告", "请先导入单词", QMessageBox.Ok)

    def closeEvent(self, event):
        # 重写关闭事件，确认是否真的要关闭：
        message = QMessageBox()
        # message.resize(400, 200)
        # 置顶显示对话框：
        message.setWindowFlag(Qt.WindowStaysOnTopHint)
        message.setIcon(QMessageBox.Warning)
        message.setText("这都撤了？")
        # 自定义对话框按钮：
        # 必须要指定按钮的 Role 属性，不能忘
        message.addButton("溜溜球!", QMessageBox.AcceptRole)
        msg_no = message.addButton("再玩会", QMessageBox.NoRole)
        # 设置默认按钮：
        message.setDefaultButton(msg_no)
        # 接收按下对话框按钮的信息：
        reply = message.exec_()
        # 第一个按钮返回 0 ，第二个返回 1 ，以此类推：
        if reply == 0:
            event.accept()
        if reply == 1:
            event.ignore()

    def initUI(self):
        # 顺序不可反
        btn2 = self.set_btn2()
        btn1 = self.set_btn1()
        # 全局设置
        # self.setGeometry(400, 300, 300, 200)
        self.setWindowTitle('无情单词检测器')
        self.setWindowIcon(QIcon("icon.jpg"))
        self.show()


if __name__ == "__main__":
    word_matrix = list()

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
