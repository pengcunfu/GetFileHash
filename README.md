# 文件 SHA-256 计算工具

一个基于 PySide6 的图形界面工具，用于计算文件的 SHA-256 哈希值。

## 功能特性

- 🎨 现代化的图形用户界面
- 📊 大文件计算进度显示
- 📋 一键复制哈希值到剪贴板
- 🚀 支持任意大小的文件
- 💻 跨平台支持（Windows、Linux、macOS）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

### 直接运行 Python 脚本

```bash
python get_file_sha256.py
```

### 打包成可执行文件

使用提供的 build.py 脚本进行打包：

```bash
python build.py
```

打包完成后，可执行文件将位于 `dist` 目录中。

## 打包说明

`build.py` 脚本会自动：
1. 检查 PyInstaller 是否已安装
2. 清理之前的构建文件
3. 使用 PyInstaller 打包程序
4. 生成单文件可执行程序（无需 Python 环境即可运行）

### 自定义打包选项

编辑 `build.py` 中的 `pyinstaller_args` 列表来修改打包选项：

- `--name`: 可执行文件名称
- `--onefile`: 打包成单个文件
- `--windowed`: Windows GUI 程序（不显示控制台）
- `--icon`: 指定图标文件（.ico 格式）

## 使用方法

1. 点击"选择文件"按钮选择要计算哈希值的文件
2. 点击"计算 SHA-256"按钮开始计算
3. 等待计算完成（大文件会显示进度条）
4. 点击"复制到剪贴板"按钮复制哈希值

## 技术栈

- Python 3.x
- PySide6 (Qt for Python)
- PyInstaller (打包工具)

## 许可证

MIT License
