#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件哈希值计算工具
支持多种哈希算法：MD5, SHA-1, SHA-256, SHA-384, SHA-512
使用 PySide6 图形界面
"""

import sys
import hashlib
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTextEdit, QLabel,
    QFileDialog, QProgressBar, QComboBox, QGridLayout, QStatusBar
)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calculator_thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("文件哈希值计算工具")
        self.setMinimumSize(600, 400)
        self.resize(700, 450)

        # 创建状态栏并设置标题
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusLabel = QLabel("文件哈希值计算工具 - 支持多种算法")
        self.statusBar.addWidget(self.statusLabel)

        # 在右侧添加永久提示信息
        self.tipLabel = QLabel("提示：支持任意大小的文件，大文件会显示计算进度")
        self.tipLabel.setStyleSheet("color: #666; font-size: 11px;")
        self.statusBar.addPermanentWidget(self.tipLabel)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # 控制区域 - 将算法选择、文件选择和计算按钮放在一行
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        # 哈希算法选择
        algo_label = QLabel("算法:")
        control_layout.addWidget(algo_label)

        self.hash_combo = QComboBox()
        self.hash_combo.setMinimumWidth(100)
        self.hash_combo.addItems([
            "MD5",
            "SHA-1",
            "SHA-256",
            "SHA-384",
            "SHA-512"
        ])
        self.hash_combo.setCurrentText("SHA-256")
        control_layout.addWidget(self.hash_combo)

        
        # 添加间隔
        control_layout.addSpacing(20)

        # 文件选择按钮
        self.select_button = QPushButton("选择文件")
        self.select_button.setMinimumWidth(80)
        self.select_button.setMinimumHeight(32)
        self.select_button.clicked.connect(self.select_file)
        control_layout.addWidget(self.select_button)

        # 计算按钮
        self.calculate_button = QPushButton("计算哈希值")
        self.calculate_button.setEnabled(False)
        self.calculate_button.clicked.connect(self.calculate_hash)
        self.calculate_button.setMinimumHeight(32)
        control_layout.addWidget(self.calculate_button)

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

        # 结果显示区域
        layout.addSpacing(8)
        result_label = QLabel("计算结果:")
        layout.addWidget(result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("计算结果将显示在这里...")
        self.result_text.setMinimumHeight(120)
        layout.addWidget(self.result_text)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.copy_button = QPushButton("复制到剪贴板")
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setMinimumWidth(100)
        self.copy_button.setMinimumHeight(30)
        button_layout.addWidget(self.copy_button)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # 不再需要提示信息标签，改为在状态栏显示

        self.selected_file = None

        # 设置窗口接受拖拽
        self.setAcceptDrops(True)

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
                    self.calculate_button.setEnabled(True)
                    self.result_text.clear()
                    self.copy_button.setEnabled(False)

                    # 自动开始计算
                    self.calculate_hash()

                    self.statusBar.showMessage(f"已处理文件: {Path(file_path).name}", 3000)
                    return
        event.ignore()

    
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
            self.calculate_button.setEnabled(True)
            self.result_text.clear()
            self.copy_button.setEnabled(False)

    def calculate_hash(self):
        if not self.selected_file:
            return

        # 获取选择的哈希算法
        algorithm = self.hash_combo.currentText().lower().replace("-", "")

        # 禁用按钮
        self.select_button.setEnabled(False)
        self.calculate_button.setEnabled(False)
        self.copy_button.setEnabled(False)
        self.hash_combo.setEnabled(False)

        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # 清空结果
        self.result_text.clear()
        self.result_text.setPlainText("正在计算中...")

        # 创建并启动计算线程
        self.calculator_thread = HashCalculator(self.selected_file, algorithm)
        self.calculator_thread.progress.connect(self.update_progress)
        self.calculator_thread.finished.connect(self.on_calculation_finished)
        self.calculator_thread.error.connect(self.on_calculation_error)
        self.calculator_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_calculation_finished(self, hash_name, hash_value):
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
        self.select_button.setEnabled(True)
        self.calculate_button.setEnabled(True)
        self.copy_button.setEnabled(True)
        self.hash_combo.setEnabled(True)

        # 隐藏进度条
        self.progress_bar.setVisible(False)

    def on_calculation_error(self, error_msg):
        self.result_text.setPlainText(f"错误: {error_msg}")

        # 恢复按钮状态
        self.select_button.setEnabled(True)
        self.calculate_button.setEnabled(True)
        self.hash_combo.setEnabled(True)

        # 隐藏进度条
        self.progress_bar.setVisible(False)

    def copy_to_clipboard(self):
        text = self.result_text.toPlainText()
        # 查找哈希值行
        for line in text.split('\n'):
            if ':' in line and not line.startswith('文件名:') and not line.startswith('文件大小:'):
                hash_value = line.split(':', 1)[1].strip()
                if len(hash_value) > 16:  # 确保是哈希值
                    QApplication.clipboard().setText(hash_value)
                    self.result_text.append(f"\n{self.hash_combo.currentText()} 哈希值已复制到剪贴板！")
                    break


def main():
    app = QApplication(sys.argv)
    app.setStyle("windowsvista")
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

