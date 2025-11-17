#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件 SHA-256 计算工具
使用 PySide6 图形界面
"""

import sys
import hashlib
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QTextEdit, QLabel,
    QFileDialog, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont


class SHA256Calculator(QThread):
    """SHA-256 计算线程"""
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        try:
            sha256_hash = hashlib.sha256()
            file_size = Path(self.file_path).stat().st_size
            bytes_read = 0
            
            with open(self.file_path, "rb") as f:
                # 每次读取 8KB
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256_hash.update(chunk)
                    bytes_read += len(chunk)
                    # 更新进度
                    if file_size > 0:
                        progress_percent = int((bytes_read / file_size) * 100)
                        self.progress.emit(progress_percent)
            
            result = sha256_hash.hexdigest()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calculator_thread = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("文件 SHA-256 计算工具")
        self.setMinimumSize(700, 500)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("📁 文件 SHA-256 哈希值计算")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 文件路径显示
        self.file_path_label = QLabel("未选择文件")
        self.file_path_label.setWordWrap(True)
        self.file_path_label.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ddd;
            }
        """)
        layout.addWidget(self.file_path_label)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 选择文件按钮
        self.select_button = QPushButton("📂 选择文件")
        self.select_button.setMinimumHeight(40)
        self.select_button.clicked.connect(self.select_file)
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        button_layout.addWidget(self.select_button)
        
        # 计算按钮
        self.calculate_button = QPushButton("🔐 计算 SHA-256")
        self.calculate_button.setMinimumHeight(40)
        self.calculate_button.setEnabled(False)
        self.calculate_button.clicked.connect(self.calculate_hash)
        self.calculate_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0a6bc2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        button_layout.addWidget(self.calculate_button)
        
        layout.addLayout(button_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 5px;
                text-align: center;
                background-color: #f5f5f5;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # 结果显示
        result_label = QLabel("SHA-256 哈希值：")
        result_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        layout.addWidget(result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("计算结果将显示在这里...")
        self.result_text.setMinimumHeight(150)
        self.result_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                background-color: #fafafa;
            }
        """)
        layout.addWidget(self.result_text)
        
        # 复制按钮
        self.copy_button = QPushButton("📋 复制到剪贴板")
        self.copy_button.setMinimumHeight(35)
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
            QPushButton:pressed {
                background-color: #cc7a00;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        layout.addWidget(self.copy_button)
        
        # 提示信息
        tip_label = QLabel("💡 提示：支持任意大小的文件，大文件会显示计算进度")
        tip_label.setStyleSheet("color: #666; font-size: 11px; font-style: italic;")
        tip_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(tip_label)
        
        self.selected_file = None
    
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
        
        # 禁用按钮
        self.select_button.setEnabled(False)
        self.calculate_button.setEnabled(False)
        self.copy_button.setEnabled(False)
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 清空结果
        self.result_text.clear()
        self.result_text.setPlainText("正在计算中...")
        
        # 创建并启动计算线程
        self.calculator_thread = SHA256Calculator(self.selected_file)
        self.calculator_thread.progress.connect(self.update_progress)
        self.calculator_thread.finished.connect(self.on_calculation_finished)
        self.calculator_thread.error.connect(self.on_calculation_error)
        self.calculator_thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def on_calculation_finished(self, hash_value):
        # 显示结果
        file_name = Path(self.selected_file).name
        file_size = Path(self.selected_file).stat().st_size
        size_mb = file_size / (1024 * 1024)
        
        result_text = f"""文件名: {file_name}
文件大小: {size_mb:.2f} MB ({file_size:,} 字节)
SHA-256: {hash_value}

格式化输出:
{hash_value.upper()}
"""
        self.result_text.setPlainText(result_text)
        
        # 恢复按钮状态
        self.select_button.setEnabled(True)
        self.calculate_button.setEnabled(True)
        self.copy_button.setEnabled(True)
        
        # 隐藏进度条
        self.progress_bar.setVisible(False)
    
    def on_calculation_error(self, error_msg):
        self.result_text.setPlainText(f"❌ 错误: {error_msg}")
        
        # 恢复按钮状态
        self.select_button.setEnabled(True)
        self.calculate_button.setEnabled(True)
        
        # 隐藏进度条
        self.progress_bar.setVisible(False)
    
    def copy_to_clipboard(self):
        text = self.result_text.toPlainText()
        if "SHA-256:" in text:
            # 提取 SHA-256 值
            for line in text.split('\n'):
                if line.startswith('SHA-256:'):
                    hash_value = line.split(':', 1)[1].strip()
                    QApplication.clipboard().setText(hash_value)
                    self.result_text.append("\n✅ SHA-256 值已复制到剪贴板！")
                    break


def main():
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
