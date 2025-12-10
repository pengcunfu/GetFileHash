import subprocess
import sys
import os
from pathlib import Path

def build_installer():
    """构建 Windows 安装程序"""
    print("开始构建安装程序...")

    # 检查是否已构建应用程序
    app_path = Path("dist/main.dist/GetFileHash.exe")
    if not app_path.exists():
        print("错误: 未找到构建的应用程序，请先运行 python scripts/deploy.py")
        return False

    # 查找 Inno Setup 编译器
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]

    inno_path = None
    for path in inno_paths:
        if Path(path).exists():
            inno_path = path
            break

    if not inno_path:
        print("错误: 未找到 Inno Setup 编译器")
        print("请从 https://jrsoftware.org/isdl.php 下载并安装 Inno Setup")
        return False

    # 创建安装程序输出目录
    installer_dir = Path("installer")
    installer_dir.mkdir(exist_ok=True)

    print(f"使用 Inno Setup 编译器: {inno_path}")

    # 运行 Inno Setup
    cmd = [inno_path, "scripts/installer.iss"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("安装程序构建成功！")
        print(f"输出目录: {installer_dir.absolute()}")

        # 显示生成的文件
        for file in installer_dir.glob("*.exe"):
            print(f"生成文件: {file}")

        return True
    else:
        print(f"安装程序构建失败: {result.stderr}")
        return False

if __name__ == "__main__":
    success = build_installer()
    sys.exit(0 if success else 1)