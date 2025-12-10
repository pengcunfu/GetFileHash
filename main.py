#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈希值计算工具
支持计算文件和文本的哈希值
支持多种哈希算法：MD5, SHA-1, SHA-256, SHA-384, SHA-512
使用 PySide6 图形界面
"""

import sys
import hashlib
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTextEdit, QLabel,
    QFileDialog, QProgressBar, QComboBox, QGridLayout, QStatusBar,
    QTabWidget, QGroupBox, QRadioButton, QButtonGroup, QMessageBox, QMenuBar
)
from PySide6.QtCore import QThread, Signal, Qt, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDesktopServices, QIcon


class HashCalculator(QThread):
    """哈希计算线程"""
    progress = Signal(int)
    finished = Signal(str, str)  # hash_name, hash_value
    error = Signal(str)

    def __init__(self, file_path, hash_algorithm):
        super().__init__()
        self.file_path = file_path
        self.hash_algorithm = hash_algorithm

    def run(self):
        try:
            # 获取哈希算法对象
            hash_obj = hashlib.new(self.hash_algorithm)
            file_size = Path(self.file_path).stat().st_size
            bytes_read = 0

            with open(self.file_path, "rb") as f:
                # 每次读取 8KB
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_obj.update(chunk)
                    bytes_read += len(chunk)
                    # 更新进度
                    if file_size > 0:
                        progress_percent = int((bytes_read / file_size) * 100)
                        self.progress.emit(progress_percent)

            result = hash_obj.hexdigest()
            self.finished.emit(self.hash_algorithm.upper(), result)
        except Exception as e:
            self.error.emit(str(e))


class TextHashCalculator(QThread):
    """文本哈希计算线程"""
    finished = Signal(str, str)  # hash_name, hash_value
    error = Signal(str)

    def __init__(self, text, hash_algorithm):
        super().__init__()
        self.text = text
        self.hash_algorithm = hash_algorithm

    def run(self):
        try:
            # 获取哈希算法对象
            hash_obj = hashlib.new(self.hash_algorithm)

            # 将文本编码为 UTF-8
            text_bytes = self.text.encode('utf-8')
            hash_obj.update(text_bytes)

            result = hash_obj.hexdigest()
            self.finished.emit(self.hash_algorithm.upper(), result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calculator_thread = None
        self.text_calculator_thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("哈希值计算工具")
        self.setMinimumSize(600, 500)
        self.resize(700, 550)

        # 创建状态栏并设置标题
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusLabel = QLabel("哈希值计算工具 - 支持文件和文本")
        self.statusBar.addWidget(self.statusLabel)

        # 在右侧添加永久提示信息
        self.tipLabel = QLabel("提示：支持文件拖拽 | 文本支持 UTF-8 编码")
        self.tipLabel.setStyleSheet("color: #666; font-size: 11px;")
        self.statusBar.addPermanentWidget(self.tipLabel)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # 创建标签页
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # 文件标签页
        self.init_file_tab()

        # 文本标签页
        self.init_text_tab()

        # 通用结果显示区域
        self.init_result_area()

        self.selected_file = None
        self.selected_text = None

        # 创建菜单栏
        self.create_menu_bar()

        # 设置窗口接受拖拽
        self.setAcceptDrops(True)

    def init_file_tab(self):
        """初始化文件标签页"""
        file_tab = QWidget()
        layout = QVBoxLayout(file_tab)
        layout.setSpacing(10)

        # 控制区域
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        # 哈希算法选择
        algo_label = QLabel("算法:")
        control_layout.addWidget(algo_label)

        self.file_hash_combo = QComboBox()
        self.file_hash_combo.setMinimumWidth(100)
        self.file_hash_combo.addItems([
            "MD5",
            "SHA-1",
            "SHA-256",
            "SHA-384",
            "SHA-512"
        ])
        self.file_hash_combo.setCurrentText("SHA-256")
        control_layout.addWidget(self.file_hash_combo)

        # 添加间隔
        control_layout.addSpacing(20)

        # 文件选择按钮
        self.select_file_button = QPushButton("选择文件")
        self.select_file_button.setMinimumWidth(80)
        self.select_file_button.setMinimumHeight(32)
        self.select_file_button.clicked.connect(self.select_file)
        control_layout.addWidget(self.select_file_button)

        # 计算按钮
        self.calculate_file_button = QPushButton("计算哈希值")
        self.calculate_file_button.setEnabled(False)
        self.calculate_file_button.clicked.connect(self.calculate_file_hash)
        self.calculate_file_button.setMinimumHeight(32)
        control_layout.addWidget(self.calculate_file_button)

        control_layout.addStretch()
        layout.addLayout(control_layout)

        # 文件路径显示
        self.file_path_label = QLabel("未选择文件")
        self.file_path_label.setWordWrap(True)
        layout.addWidget(self.file_path_label)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(18)
        layout.addWidget(self.progress_bar)

        # 添加说明
        info_label = QLabel("提示：可以直接拖拽文件到此处")
        info_label.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(info_label)

        layout.addStretch()
        self.tab_widget.addTab(file_tab, "📁 文件哈希")

    def init_text_tab(self):
        """初始化文本标签页"""
        text_tab = QWidget()
        layout = QVBoxLayout(text_tab)
        layout.setSpacing(10)

        # 控制区域
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        # 哈希算法选择
        algo_label = QLabel("算法:")
        control_layout.addWidget(algo_label)

        self.text_hash_combo = QComboBox()
        self.text_hash_combo.setMinimumWidth(100)
        self.text_hash_combo.addItems([
            "MD5",
            "SHA-1",
            "SHA-256",
            "SHA-384",
            "SHA-512"
        ])
        self.text_hash_combo.setCurrentText("SHA-256")
        control_layout.addWidget(self.text_hash_combo)

        # 添加间隔
        control_layout.addSpacing(20)

        # 计算按钮
        self.calculate_text_button = QPushButton("计算哈希值")
        self.calculate_text_button.setMinimumHeight(32)
        self.calculate_text_button.clicked.connect(self.calculate_text_hash)
        control_layout.addWidget(self.calculate_text_button)

        control_layout.addStretch()
        layout.addLayout(control_layout)

        # 文本输入区域
        text_input_group = QGroupBox("输入文本")
        text_input_layout = QVBoxLayout(text_input_group)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("在此输入要计算哈希值的文本...")
        self.text_input.setMinimumHeight(100)
        self.text_input.setMaximumHeight(150)
        self.text_input.textChanged.connect(self.on_text_changed)
        text_input_layout.addWidget(self.text_input)

        # 文本信息
        self.text_info_label = QLabel("字符数: 0 | 行数: 0")
        self.text_info_label.setStyleSheet("color: #888; font-size: 12px;")
        text_input_layout.addWidget(self.text_info_label)

        layout.addWidget(text_input_group)

        # 快速操作按钮
        quick_layout = QHBoxLayout()
        quick_layout.setSpacing(10)

        clear_text_btn = QPushButton("清空文本")
        clear_text_btn.clicked.connect(self.clear_text)
        quick_layout.addWidget(clear_text_btn)

        paste_text_btn = QPushButton("粘贴文本")
        paste_text_btn.clicked.connect(self.paste_text)
        quick_layout.addWidget(paste_text_btn)

        quick_layout.addStretch()
        layout.addLayout(quick_layout)

        self.tab_widget.addTab(text_tab, "📝 文本哈希")

    def init_result_area(self):
        """初始化结果显示区域"""
        # 结果显示区域
        result_group = QGroupBox("计算结果")
        result_layout = QVBoxLayout(result_group)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("计算结果将显示在这里...")
        self.result_text.setMinimumHeight(180)
        result_layout.addWidget(self.result_text)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.copy_button = QPushButton("复制到剪贴板")
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setMinimumWidth(100)
        self.copy_button.setMinimumHeight(30)
        button_layout.addWidget(self.copy_button)

        clear_result_btn = QPushButton("清空结果")
        clear_result_btn.clicked.connect(self.clear_result)
        clear_result_btn.setMinimumWidth(100)
        clear_result_btn.setMinimumHeight(30)
        button_layout.addWidget(clear_result_btn)

        button_layout.addStretch()
        result_layout.addLayout(button_layout)

        # 将结果区域添加到主布局
        self.tab_widget.parent().layout().addWidget(result_group)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            # 检查是否是文件（不是目录）
            urls = event.mimeData().urls()
            if urls and urls[0].isLocalFile():
                file_path = urls[0].toLocalFile()
                if Path(file_path).is_file():
                    event.acceptProposedAction()
                    self.statusBar.showMessage(f"拖拽文件: {Path(file_path).name}", 2000)
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        """文件放下事件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].isLocalFile():
                file_path = urls[0].toLocalFile()
                if Path(file_path).is_file():
                    self.selected_file = file_path
                    self.file_path_label.setText(f"已选择: {file_path}")
                    self.calculate_file_button.setEnabled(True)
                    self.result_text.clear()
                    self.copy_button.setEnabled(False)

                    # 自动开始计算
                    self.calculate_file_hash()

                    self.statusBar.showMessage(f"已处理文件: {Path(file_path).name}", 3000)
                    return
        event.ignore()

    
    # 文件相关方法
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择文件",
            "",
            "所有文件 (*.*)"
        )

        if file_path:
            self.selected_file = file_path
            self.file_path_label.setText(f"已选择: {file_path}")
            self.calculate_file_button.setEnabled(True)
            self.result_text.clear()
            self.copy_button.setEnabled(False)

    def calculate_file_hash(self):
        if not self.selected_file:
            return

        # 获取选择的哈希算法
        algorithm = self.file_hash_combo.currentText().lower().replace("-", "")

        # 禁用按钮
        self.select_file_button.setEnabled(False)
        self.calculate_file_button.setEnabled(False)
        self.copy_button.setEnabled(False)
        self.file_hash_combo.setEnabled(False)

        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # 清空结果
        self.result_text.clear()
        self.result_text.setPlainText("正在计算中...")

        # 创建并启动计算线程
        self.calculator_thread = HashCalculator(self.selected_file, algorithm)
        self.calculator_thread.progress.connect(self.update_progress)
        self.calculator_thread.finished.connect(self.on_file_calculation_finished)
        self.calculator_thread.error.connect(self.on_calculation_error)
        self.calculator_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_file_calculation_finished(self, hash_name, hash_value):
        # 显示结果
        file_name = Path(self.selected_file).name
        file_size = Path(self.selected_file).stat().st_size
        size_mb = file_size / (1024 * 1024)

        result_text = f"""文件名: {file_name}
文件大小: {size_mb:.2f} MB ({file_size:,} 字节)
{hash_name}: {hash_value}

格式化输出:
{hash_value.upper()}
"""
        self.result_text.setPlainText(result_text)

        # 恢复按钮状态
        self.select_file_button.setEnabled(True)
        self.calculate_file_button.setEnabled(True)
        self.copy_button.setEnabled(True)
        self.file_hash_combo.setEnabled(True)

        # 隐藏进度条
        self.progress_bar.setVisible(False)

    # 文本相关方法
    def on_text_changed(self):
        """文本内容变化时的处理"""
        text = self.text_input.toPlainText()
        char_count = len(text)
        line_count = len(text.split('\n')) if text else 0
        self.text_info_label.setText(f"字符数: {char_count} | 行数: {line_count}")

        # 启用/禁用计算按钮
        self.calculate_text_button.setEnabled(len(text.strip()) > 0)
        self.selected_text = text

    def calculate_text_hash(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            return

        # 获取选择的哈希算法
        algorithm = self.text_hash_combo.currentText().lower().replace("-", "")

        # 禁用按钮
        self.calculate_text_button.setEnabled(False)
        self.copy_button.setEnabled(False)
        self.text_hash_combo.setEnabled(False)

        # 清空结果
        self.result_text.clear()
        self.result_text.setPlainText("正在计算中...")

        # 创建并启动计算线程
        self.text_calculator_thread = TextHashCalculator(text, algorithm)
        self.text_calculator_thread.finished.connect(self.on_text_calculation_finished)
        self.text_calculator_thread.error.connect(self.on_calculation_error)
        self.text_calculator_thread.start()

    def on_text_calculation_finished(self, hash_name, hash_value):
        text = self.selected_text
        char_count = len(text)
        byte_count = len(text.encode('utf-8'))

        result_text = f"""文本长度: {char_count} 字符
UTF-8 字节数: {byte_count} 字节
{hash_name}: {hash_value}

格式化输出:
{hash_value.upper()}
"""
        self.result_text.setPlainText(result_text)

        # 恢复按钮状态
        self.calculate_text_button.setEnabled(True)
        self.copy_button.setEnabled(True)
        self.text_hash_combo.setEnabled(True)

    def on_calculation_error(self, error_msg):
        self.result_text.setPlainText(f"错误: {error_msg}")

        # 恢复所有按钮状态
        if hasattr(self, 'select_file_button'):
            self.select_file_button.setEnabled(True)
        if hasattr(self, 'calculate_file_button') and self.selected_file:
            self.calculate_file_button.setEnabled(True)
        if hasattr(self, 'calculate_text_button') and self.selected_text:
            self.calculate_text_button.setEnabled(True)

        self.copy_button.setEnabled(False)

        # 恢复下拉框状态
        if hasattr(self, 'file_hash_combo'):
            self.file_hash_combo.setEnabled(True)
        if hasattr(self, 'text_hash_combo'):
            self.text_hash_combo.setEnabled(True)

        # 隐藏进度条
        self.progress_bar.setVisible(False)

    def copy_to_clipboard(self):
        text = self.result_text.toPlainText()
        # 查找哈希值行
        for line in text.split('\n'):
            if ':' in line and not line.startswith('文件名:') and not line.startswith('文件大小:') and not line.startswith('文本长度:') and not line.startswith('UTF-8'):
                hash_value = line.split(':', 1)[1].strip()
                if len(hash_value) > 16:  # 确保是哈希值
                    QApplication.clipboard().setText(hash_value)
                    self.result_text.append(f"\n✅ 哈希值已复制到剪贴板！")
                    break

    def clear_text(self):
        """清空文本输入"""
        self.text_input.clear()
        self.result_text.clear()
        self.copy_button.setEnabled(False)

    def paste_text(self):
        """粘贴文本"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            self.text_input.setPlainText(text)
            # 移动光标到末尾
            cursor = self.text_input.textCursor()
            cursor.movePosition(cursor.End)
            self.text_input.setTextCursor(cursor)

    def clear_result(self):
        """清空结果显示"""
        self.result_text.clear()
        self.copy_button.setEnabled(False)

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")

        # 关于菜单项
        about_action = help_menu.addAction("关于(&A)")
        about_action.setShortcut("F1")
        about_action.triggered.connect(self.show_about)

        help_menu.addSeparator()

        # 访问仓库菜单项
        repo_action = help_menu.addAction("访问 GitHub 仓库(&G)")
        repo_action.triggered.connect(self.open_repository)

    def show_about(self):
        """显示关于对话框"""
        about_text = """<h2>GetFileHash - 哈希值计算工具</h2>
<p><b>版本:</b> 0.0.1</p>
<p><b>作者:</b> pengcunfu</p>
<p><b>描述:</b></p>
<ul>
<li>支持计算文件的哈希值</li>
<li>支持计算文本的哈希值</li>
<li>支持多种哈希算法：MD5, SHA-1, SHA-256, SHA-384, SHA-512</li>
<li>支持文件拖拽</li>
<li>支持大文件进度显示</li>
<li>一键复制哈希值到剪贴板</li>
</ul>
<p><b>技术栈:</b> Python + PySide6 (Qt for Python)</p>
<p><b>许可证:</b> MIT License</p>
<br>
<p>如有问题或建议，欢迎访问 GitHub 仓库。</p>"""

        QMessageBox.about(self, "关于 GetFileHash", about_text)

    def open_repository(self):
        """打开 GitHub 仓库"""
        url = QUrl("https://github.com/pengcunfu/GetFileHash.git")
        QDesktopServices.openUrl(url)


def main():
    app = QApplication(sys.argv)
    app.setStyle("windowsvista")

    # 设置应用程序图标
    icon_path = Path(__file__).parent / "resources" / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    # 设置窗口图标（与应用程序图标相同）
    if icon_path.exists():
        window.setWindowIcon(QIcon(str(icon_path)))

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

