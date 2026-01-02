# 抖音无水印视频批量下载器 (Douyin No-Watermark Downloader)

Python 编写的轻量级抖音视频无水印批量下载工具。支持解析多种分享链接格式，自动去重，批量下载。

## ✨ 功能特点

*   **无水印下载**：自动解析并下载无水印的高清视频原文件。
*   **批量处理**：支持从文件中读取多个链接进行批量下载。
*   **智能解析**：兼容长链接、短链接、图文链接等多种分享格式。
*   **自动重试**：针对 403 禁止访问等网络问题包含自动重试机制。
*   **文件名净化**：自动处理文件名中的非法字符，防止保存失败。

## 🛠️ 安装依赖

确保你的电脑已安装 Python 3.x。

1.  克隆或下载本项目。
2.  安装所需的第三方库：

```bash
pip install -r requirements.txt
```

## 🚀 使用方法

### 1. 准备链接
打开 `shipin_lianjie/shipinglianjie` 文件，将需要下载的抖音分享链接粘贴进去，一行一个。

示例：
```text
https://v.douyin.com/xxxx/
https://www.douyin.com/video/xxxx
```

### 2. 运行下载
在终端中运行 `main.py`：

```bash
python main.py
```

### 3. 查看结果
下载完成的视频将自动保存在 `downloads` 文件夹中。

## 📂 项目结构

```
douyin_downloader/
├── downloader.py      # 核心下载逻辑类
├── main.py            # 批量下载入口脚本
├── requirements.txt   # 项目依赖
├── shipin_lianjie/    # 链接存放目录
│   └── shipinglianjie # 在此文件中放入链接
└── downloads/         # (自动创建) 视频保存目录
```

## ⚠️ 免责声明

本项目仅供学习和研究 Python 爬虫技术使用。请勿用于商业用途或侵犯他人版权。使用者应对使用本工具产生的一切后果负责。
