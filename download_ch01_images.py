import os
import re
import time
import requests
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler

# 创建目录
os.makedirs("assets/images/ch01", exist_ok=True)
source_log_file = "assets/images/ch01/ch01_image_sources.txt"
source_log = []

# 读取README文件，提取图片标题和图片路径
def extract_image_info(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式匹配图片链接和标题
    pattern = r'!\[(.*?)\]\((https://qishengle\.github\.io/MobileHouse/assets/images/ch01/(.*?))\)'
    matches = re.findall(pattern, content)
    
    image_info = []
    for match in matches:
        title = match[0]  # 图片标题
        url = match[1]    # 完整URL
        filename = match[2]  # 文件名
        
        # 提取图片描述（在图片链接后的斜体文本）
        img_pattern = f'!\\[{re.escape(title)}\\]\\({re.escape(url)}\\)\\s*\\*([^\\*]+)\\*'
        desc_match = re.search(img_pattern, content)
        description = desc_match.group(1).strip() if desc_match else ""
        
        image_info.append({
            'title': title,
            'filename': filename,
            'description': description
        })
    
    return image_info

# 根据图片标题优化搜索关键词
def optimize_search_keyword(title, description):
    # 去除"关系图"、"比较"等通用词，保留核心内容
    core_title = title.replace("关系图", "").replace("比较", "").replace("趋势", "")
    
    # 根据文件名确定图片类型（地图、图表、照片等）
    img_type = ""
    if "map" in description.lower() or "地图" in description:
        img_type = "map visualization"
    elif "chart" in description.lower() or "图表" in description or "趋势" in title:
        img_type = "chart data visualization"
    elif "diagram" in description.lower() or "框架" in title or "体系" in title or "模式" in title:
        img_type = "diagram infographic"
    elif "model" in description.lower() or "模型" in title:
        img_type = "model diagram"
    elif "planning" in description.lower() or "规划" in title:
        img_type = "urban planning map"
    else:
        img_type = "high quality visualization"
    
    # 提取描述中的关键信息
    keywords = []
    if description:
        # 提取冒号后的内容作为重要关键词
        if "：" in description or ":" in description:
            colon_parts = re.split(r'[：:]', description)
            if len(colon_parts) > 1:
                keywords.append(colon_parts[1].split("*")[0].strip())
    
    # 构建优化后的搜索关键词
    optimized = f"{core_title} {' '.join(keywords)} {img_type}"
    
    return optimized

# 根据文件名获取已下载的图片列表
def get_downloaded_images(directory):
    if not os.path.exists(directory):
        return []
    return [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# 使用三种搜索引擎尝试下载图片
def download_image_with_crawler(keyword, output_dir, filename, max_num=3):
    # 存储原始文件名，用于后续重命名
    target_filename = filename
    base_filename = os.path.splitext(target_filename)[0]
    
    # 临时创建目录存放下载的图片
    temp_dir = f"{output_dir}/temp_{base_filename}"
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"  搜索关键词: {keyword}")
    success = False
    
    # 尝试使用不同的搜索引擎
    crawlers = [
        (GoogleImageCrawler(storage={'root_dir': temp_dir}), "Google"),
        (BingImageCrawler(storage={'root_dir': temp_dir}), "Bing"),
        (BaiduImageCrawler(storage={'root_dir': temp_dir}), "Baidu")
    ]
    
    for crawler, engine_name in crawlers:
        if success:
            break
            
        print(f"  尝试使用 {engine_name} 搜索引擎...")
        try:
            # 从每个引擎最多获取3张图片
            crawler.crawl(keyword=keyword, max_num=max_num)
            
            # 检查是否下载了任何图片
            downloaded = get_downloaded_images(temp_dir)
            if downloaded:
                # 取第一张图片作为结果
                first_img = os.path.join(temp_dir, downloaded[0])
                target_path = os.path.join(output_dir, target_filename)
                
                # 读取并保存为指定的文件名
                with open(first_img, 'rb') as src_file:
                    with open(target_path, 'wb') as dest_file:
                        dest_file.write(src_file.read())
                
                source_log.append(f"{target_filename}\t{engine_name} 搜索\t{keyword}")
                print(f"  成功下载 {target_filename}，使用 {engine_name} 搜索结果")
                success = True
                break
            else:
                print(f"  从 {engine_name} 未找到匹配 '{keyword}' 的图片")
        except Exception as e:
            print(f"  使用 {engine_name} 爬虫时出错: {e}")
        
        # 搜索引擎之间等待一下
        time.sleep(3)
    
    # 清理临时目录
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        
    return success

# 主处理流程
def main():
    readme_path = "content/part1-背景理论/ch01-城市化进程/README.md"
    output_dir = "assets/images/ch01"
    
    print("开始根据图片标题下载匹配的图片...")
    
    # 提取图片信息
    image_info = extract_image_info(readme_path)
    print(f"从README中提取到 {len(image_info)} 张图片信息")
    
    # 获取已下载的图片
    existing_images = get_downloaded_images(output_dir)
    print(f"目录中已有 {len(existing_images)} 张图片")
    
    # 下载缺失的图片
    for img in image_info:
        filename = img['filename']
        if filename in existing_images:
            print(f"跳过已存在的图片: {filename}")
            continue
        
        print(f"处理图片: {filename} - {img['title']}")
        # 优化搜索关键词
        search_keyword = optimize_search_keyword(img['title'], img['description'])
        print(f"优化后的搜索关键词: {search_keyword}")
        
        # 使用爬虫下载图片
        success = download_image_with_crawler(search_keyword, output_dir, filename)
        
        if not success:
            print(f"尝试使用备用关键词下载 {filename}")
            # 备用关键词，使用更简单的术语
            backup_keyword = f"{img['title']} visualization high quality"
            success = download_image_with_crawler(backup_keyword, output_dir, filename)
            
            if not success:
                print(f"无法下载图片 {filename}，请手动处理")
        
        # 每次处理完一张图片（无论成功与否）都等待一下
        time.sleep(5)
    
    # 记录图片来源
    if source_log:
        with open(source_log_file, "a") as f:
            f.write(f"\n--- 图片下载记录 {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            for line in source_log:
                f.write(line + "\n")
    
    # 统计结果
    final_images = get_downloaded_images(output_dir)
    print(f"\n下载完成! 目录中现有 {len(final_images)} 张图片")
    print(f"下载记录已保存至 {source_log_file}")

if __name__ == "__main__":
    main() 