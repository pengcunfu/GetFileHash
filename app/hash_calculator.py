#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈希计算模块
包含文件和文本哈希计算的线程类
"""

import hashlib
from PySide6.QtCore import QThread, Signal


class HashCalculator(QThread):
    """文件哈希计算线程"""
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

            # 获取文件大小用于计算进度
            file_size = self.file_path.stat().st_size
            processed_bytes = 0

            # 读取文件并更新哈希值
            with open(self.file_path, 'rb') as f:
                while True:
                    chunk = f.read(8192)  # 每次读取8KB
                    if not chunk:
                        break
                    hash_obj.update(chunk)
                    processed_bytes += len(chunk)

                    # 发送进度信号
                    if file_size > 0:
                        progress_percent = int((processed_bytes / file_size) * 100)
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