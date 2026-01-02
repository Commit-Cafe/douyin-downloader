from downloader import DouyinDownloader
import os
import sys

def main():
    print("=== 抖音无水印视频批量下载工具 ===")
    
    # 构建链接文件路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    link_file_path = os.path.join(base_dir, 'shipin_lianjie', 'shipinglianjie')
    
    if not os.path.exists(link_file_path):
        print(f"错误: 找不到链接文件: {link_file_path}")
        return

    print(f"正在读取链接文件: {link_file_path}")
    
    lines = []
    # 尝试不同编码读取文件
    for encoding in ['utf-8', 'gbk', 'utf-16']:
        try:
            with open(link_file_path, 'r', encoding=encoding) as f:
                temp_lines = f.readlines()
            if temp_lines:
                lines = temp_lines
                print(f"成功使用 {encoding} 编码读取文件")
                break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"使用 {encoding} 读取时出错: {e}")
            
    urls = [line.strip() for line in lines if line.strip()]
    
    if not urls:
        print("文件中没有找到有效的链接 (或文件为空/读取失败)")
        try:
            print(f"文件大小: {os.path.getsize(link_file_path)} 字节")
        except:
            pass
        return
            
    print(f"找到 {len(urls)} 个链接，准备开始下载...")
    
    downloader = DouyinDownloader()
    
    for index, url in enumerate(urls, 1):
        print(f"\n[{index}/{len(urls)}] 正在处理: {url}")
        try:
            downloader.run(url)
        except Exception as e:
            print(f"处理链接时出错: {e}")
            
    print("\n所有任务处理完成！")

if __name__ == "__main__":
    main()
