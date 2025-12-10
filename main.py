#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GetFileHash - 哈希值计算工具
程序入口点
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from app.main_window import MainWindow


def main():
    """主函数"""
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