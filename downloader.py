import requests
import re
import json
import os

class DouyinDownloader:
    def __init__(self):
        # 模拟移动端 User-Agent，这对于获取 mobile 分享页面至关重要
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'Referer': 'https://www.douyin.com/?is_from_mobile_home=1&recommend=1'
        }

    def get_real_url(self, share_url):
        """获取重定向后的真实 URL"""
        try:
            # 允许重定向
            response = requests.get(share_url, headers=self.headers, allow_redirects=True)
            return response.url
        except Exception as e:
            print(f"获取真实链接失败: {e}")
            return None

    def get_video_id(self, url):
        """从 URL 中提取视频 ID"""
        try:
            # 1. 尝试从 modal_id 参数提取 (优先匹配这种显式的参数)
            match = re.search(r'modal_id=(\d+)', url)
            if match:
                return match.group(1)

            # 2. 匹配 /video/数字
            match = re.search(r'/video/(\d+)', url)
            if match:
                return match.group(1)

            # 3. 有时候可能是 /share/video/数字
            match = re.search(r'video/(\d+)', url)
            if match:
                return match.group(1)
                
            # 4. 尝试从 note_id 参数提取 (图文)
            match = re.search(r'note_id=(\d+)', url)
            if match:
                return match.group(1)

            return None
        except Exception as e:
            print(f"提取视频 ID 失败: {e}")
            return None

    def get_video_data(self, video_id):
        """请求视频详情页并提取 _ROUTER_DATA JSON 数据"""
        url = f'https://www.iesdouyin.com/share/video/{video_id}/'
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # 正则匹配 window._ROUTER_DATA
            match = re.search(r'window\._ROUTER_DATA\s*=\s*(.*?)</script>', response.text)
            if match:
                json_str = match.group(1).strip()
                return json.loads(json_str)
            else:
                print("在页面中未找到数据")
                return None
        except Exception as e:
            print(f"获取视频数据失败: {e}")
            return None

    def parse_video_info(self, data):
        """解析 JSON 数据获取视频信息"""
        try:
            # 数据结构路径: loaderData -> video_(id)/page -> videoInfoRes -> item_list -> [0]
            loader_data = data.get('loaderData', {})
            video_info_res = None
            
            # 动态查找 key，因为 key 包含 video_id
            for key, value in loader_data.items():
                if isinstance(value, dict) and 'videoInfoRes' in value:
                    video_info_res = value['videoInfoRes']
                    break
            
            if not video_info_res:
                print("未找到视频详细信息 (videoInfoRes)")
                return None
                
            item_list = video_info_res.get('item_list', [])
            if not item_list:
                print("item_list 为空")
                return None
                
            video_item = item_list[0]
            
            desc = video_item.get('desc', '无标题')
            nickname = video_item.get('author', {}).get('nickname', '未知作者')
            
            # 获取 play_addr uri
            play_addr = video_item.get('video', {}).get('play_addr', {})
            uri = play_addr.get('uri')
            
            if not uri:
                print("未找到视频 URI")
                return None
                
            # 构造无水印下载链接
            # 注意：这里使用 douyin.com 的接口
            download_url = f"https://www.douyin.com/aweme/v1/play/?video_id={uri}"
            
            return {
                'desc': desc,
                'nickname': nickname,
                'download_url': download_url
            }
            
        except Exception as e:
            print(f"解析视频信息出错: {e}")
            return None

    def download(self, url, filename):
        """下载视频文件"""
        try:
            print(f"正在下载: {filename}")
            print(f"下载链接: {url}")
            
            # 下载时也要带上 headers，防止 403
            response = requests.get(url, headers=self.headers, stream=True)
            
            if response.status_code == 403:
                print("下载链接返回 403 Forbidden，尝试不带 Referer 重试...")
                headers_no_ref = self.headers.copy()
                headers_no_ref.pop('Referer', None)
                response = requests.get(url, headers=headers_no_ref, stream=True)
                
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"下载完成！文件保存在: {os.path.abspath(filename)}")
            return True
        except Exception as e:
            print(f"下载失败: {e}")
            return False

    def run(self, share_url, output_dir='downloads'):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        print("正在解析链接...")
        real_url = self.get_real_url(share_url)
        if not real_url:
            return
            
        # print(f"真实链接: {real_url}")
        video_id = self.get_video_id(real_url)
        if not video_id:
            print("无法提取视频 ID")
            return
            
        # print(f"视频 ID: {video_id}")
        data = self.get_video_data(video_id)
        if not data:
            return
            
        info = self.parse_video_info(data)
        if not info:
            return
            
        print(f"发现视频: {info['desc']} - 作者: {info['nickname']}")
        
        # 处理文件名非法字符
        # 去除 Windows 文件名非法字符以及换行符等不可见字符
        safe_desc = re.sub(r'[\\/*?:"<>|\r\n\t]', "", info['desc'])
        if len(safe_desc) > 30:
            safe_desc = safe_desc[:30]
        filename = os.path.join(output_dir, f"{safe_desc}_{video_id}.mp4")
        
        self.download(info['download_url'], filename)

if __name__ == "__main__":
    print("=== 抖音视频下载器 (无水印版) ===")
    url = input("请输入抖音分享链接 (例如 https://v.douyin.com/xxxx/): ")
    if url:
        downloader = DouyinDownloader()
        downloader.run(url)
