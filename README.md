# GetFileHash - 哈希值计算工具

一个基于 PySide6 的现代化图形界面工具，用于计算文件和文本的哈希值。

## ✨ 功能特性

- 🎨 **现代化图形用户界面** - 基于 PySide6 (Qt for Python)
- 🔄 **多哈希算法支持** - MD5、SHA-1、SHA-256、SHA-384、SHA-512
- 📊 **大文件进度显示** - 实时显示计算进度
- 📋 **一键复制功能** - 快速复制哈希值到剪贴板
- 📝 **文本哈希计算** - 支持计算文本内容的哈希值
- 🖱️ **文件拖拽操作** - 直接拖拽文件到界面进行计算
- 🚀 **高性能** - 支持任意大小的文件
- 💻 **跨平台支持** - Windows、Linux、macOS
- 📦 **便捷分发** - 提供安装程序和便携版本

## 🚀 快速开始

### 下载和安装

#### 📦 推荐下载：安装程序版本
- **文件名**: `GetFileHash-Setup-{VERSION}.exe`
- **说明**: 完整的Windows安装程序，包含卸载功能
- **优点**: 自动创建桌面快捷方式、开始菜单项，支持程序卸载

#### 🗂️ 便携版本
- **文件名**: `GetFileHash-{VERSION}.zip`
- **说明**: 绿色便携版，解压即可使用
- **优点**: 无需安装，不写入注册表，适合U盘使用

从 [Releases 页面](https://github.com/pengcunfu/GetFileHash/releases) 下载最新版本。

### 系统要求
- Windows 10 及以上版本
- **推荐**: 安装程序版本需要管理员权限进行安装
- **便携**: 无需特殊权限

## 💻 开发环境

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

### 构建可执行文件

```bash
# 构建 Windows 可执行文件
python scripts/build.py

# 构建 Windows 安装程序
python scripts/build_installer.py
```

## 📖 使用说明

### 文件哈希计算
1. 点击"选择文件"按钮或直接拖拽文件到界面
2. 选择需要的哈希算法（默认 SHA-256）
3. 点击"计算哈希值"按钮
4. 等待计算完成（大文件会显示进度条）
5. 点击"复制到剪贴板"复制结果

### 文本哈希计算
1. 切换到"文本哈希"标签页
2. 在文本框中输入或粘贴要计算哈希值的文本
3. 选择哈希算法
4. 点击"计算哈希值"按钮
5. 复制计算结果

## 🛠️ 技术栈

- **Python 3.9** - 核心开发语言
- **PySide6** - GUI 框架 (Qt for Python)
- **Nuitka** - 编译工具，生成高性能可执行文件
- **Inno Setup** - Windows 安装程序制作

## 📁 项目结构

```
GetFileHash/
├── main.py                 # 主程序入口
├── requirements.txt        # Python 依赖
├── resources/             # 资源文件
│   └── icon.png          # 应用图标
├── scripts/               # 构建脚本
│   ├── build.py          # 构建可执行文件
│   └── build_installer.py # 构建安装程序
├── scripts/installer.iss  # Inno Setup 配置
└── .github/workflows/     # CI/CD 工作流
    ├── ci.yml            # 持续集成
    └── release.yml       # 自动发布
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [PySide6](https://doc.qt.io/qtforpython/) - 优秀的 Python GUI 框架
- [Nuitka](https://nuitka.net/) - 强大的 Python 编译器
- [Inno Setup](https://jrsoftware.org/isinfo.php) - 专业的安装程序制作工具

---

<p align="center">
  <strong>如果这个项目对您有帮助，请给个 ⭐ Star 支持一下！</strong>
</p>