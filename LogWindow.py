"""
祈愿 · 幸运观众：更新说明窗口

Copyright © 2024-2026 卡猫kat

"""

from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtCore import Qt
import os
import sys

from RoundShadow import RoundShadow
from MovableWindow import MovableWindow

from config import _iconpath, _default_lang

class LogWindow(MovableWindow):
    def __init__(self, parent=None):
        super(LogWindow, self).__init__(parent)
        self.round_shadow = RoundShadow(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        
        def get_resource_path(relative_path):
            """获取资源文件的绝对路径（兼容 PyInstaller 单文件打包环境）"""
            if hasattr(sys, '_MEIPASS'):
                # 打包后临时解压目录
                base_path = sys._MEIPASS
            else:
                # 本地开发时的根目录
                base_path = os.path.abspath('.')
            return os.path.join(base_path, relative_path)


        # 1. 获取字体的真实路径
        font_path = get_resource_path(
            os.path.join('.wish', 'fonts', 'HYWH-85w Heavy.ttf')
        ) 
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                _global_font = families[0]
            else:
                _global_font = 'Microsoft YaHei'  # 备用默认字体
        else:
            print(f'警告: 字体加载失败，路径: {font_path}')
            _global_font = 'Microsoft YaHei'  # 加载失败时降级使用系统字体，避免程序直接崩溃

        self.log_layout = QVBoxLayout(self)

        self.log_header_layout = QHBoxLayout()  # 标题栏
        title_label = '更新说明' if _default_lang == 0 else 'Release Notes'
        self.log_title_label = QLabel(title_label, self)
        self.log_title_label.setFont(QFont(_global_font, 11))
        self.log_close_button = QPushButton('', self)
        self.log_close_button.setIcon(QIcon(get_resource_path(os.path.join('.wish', 'assets', 'icon', 'close.png'))))
        self.log_close_button.setFont(QFont(_global_font, 12))
        self.log_close_button.clicked.connect(self.close)
        self.log_close_button.setFixedSize(30, 30)
        self.log_close_button.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: red;
                color: white; }""")
        self.log_header_layout.addWidget(self.log_title_label)
        self.log_header_layout.addStretch(1)
        self.log_header_layout.addWidget(self.log_close_button)

        self.log_table = QGridLayout()  # 更新说明表格

        changelog_path = get_resource_path('CHANGELOG.txt')

        with open(changelog_path, 'r', encoding='utf-8') as file:
            content_list = [line.strip() for line in file]

        for x in range(1, int(len(content_list)/3+1)):
            log_column1 = QLabel(content_list[x*3-3].split("    ")[0]+"    ", self)
            log_column1.setFont(QFont(_global_font, 12))
            log_column1.setFixedHeight(30)
            log_column2 = QLabel(content_list[x*3-3].split("    ")[1], self)
            log_column2.setFont(QFont(_global_font, 12))
            log_column2.setFixedHeight(30)
            log_column3 = QLabel(content_list[x*3-2]+"    ", self)
            log_column3.setFont(QFont(_global_font, 12))
            log_column3.setFixedHeight(30)
            self.log_table.addWidget(log_column1, x, 1)
            self.log_table.addWidget(log_column3, x, 2)
            self.log_table.addWidget(log_column2, x, 3)

        self.log_table.setContentsMargins(35, 5, 35, 10)

        self.log_layout.addLayout(self.log_header_layout)  # 更新说明窗口布局
        self.log_layout.addLayout(self.log_table)
        self.log_layout.setContentsMargins(30, 25, 30, 25)

        self.setWindowTitle("祈愿 · 幸运观众 - 更新说明")
        self.setWindowIcon(QIcon(_iconpath))
        self.setGeometry(300, 300, 400, 400)

