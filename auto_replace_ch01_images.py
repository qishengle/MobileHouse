import os
import requests
import time
import re
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler

# 仅针对上次失败的图片，尝试新的关键词和下载策略
failed_images_map = {
    "china_regional_urbanization.png": "China regional urbanization level map data visualization alternative source",
    "jobs_housing_balance.png": "jobs housing balance index commuting time relationship graph visualization",
    "shenzhen_housing_innovation.png": "Shenzhen ecosystem innovation model diagram visualization alternative source"
}

# # 重点替换可能不符的图片，使用更精确的关键词
# target_replace_map = {
#     "china_urban_clusters.png": "China urban clusters metropolitan areas map official",
#     "china_regional_urbanization.png": "China regional urbanization level differences map data visualization",
#     "china_housing_system.png": "China multi level housing security system diagram chart",
#     "jobs_housing_balance.png": "jobs housing balance index commuting time relationship chart graph",
#     "land_use_efficiency.png": "urban land use efficiency population density relationship chart graph",
#     "mobile_housing_solution.png": "mobile housing solution framework diagram schematic",
#     "shenzhen_housing_evolution.png": "Shenzhen housing supply system evolution timeline chart",
#     "shenzhen_housing_innovation.png": "Shenzhen housing innovation model diagram chart",
#     "xiong_an_planning.png": "Xiong'an new area urban planning smart housing map official plan",
#     "hangzhou_housing_innovation.png": "Hangzhou innovation corridor housing model diagram chart"
# }

# # 图片标题与英文关键词映射 (保留备用)
# title_query_map = {
#     "urban_housing_challenge.png": "urbanization housing challenge infographic",
#     "population_density_trend.png": "global city population density trend chart",
#     "sustainable_city_models.png": "sustainable city development models comparison",
#     "china_urbanization_trend.png": "China urbanization rate trend 1978-2023 graph",
#     "china_urban_clusters.png": "China urban clusters metropolitan areas map",
#     "china_regional_urbanization.png": "China regional urbanization level differences map",
#     "china_housing_system.png": "China multi-level housing security system diagram",
#     "housing_affordability_trend.png": "global cities housing price to income ratio trend chart",
#     "commute_time_comparison.png": "global cities average commuting time comparison chart",
#     "jobs_housing_balance.png": "jobs housing balance index commuting time chart",
#     "land_use_efficiency.png": "urban land use efficiency population density chart",
#     "mobile_housing_solution.png": "mobile housing solution framework diagram",
#     "tokyo_case_study.png": "Tokyo micro apartment transit oriented development photo",
#     "shenzhen_housing_evolution.png": "Shenzhen housing supply system evolution chart",
#     "shenzhen_housing_innovation.png": "Shenzhen housing innovation model diagram",
#     "xiong_an_planning.png": "Xiong'an new area urban planning smart housing map",
#     "amsterdam_floating_houses.png": "Amsterdam floating houses community photo",
#     "hangzhou_housing_innovation.png": "Hangzhou innovation corridor housing model diagram"
# }

os.makedirs("assets/images/ch01", exist_ok=True)
source_log_file = "assets/images/ch01/ch01_image_sources_replaced.txt"
source_log = []

print(f"Attempting to find alternative sources for {len(failed_images_map)} items...")

def is_problematic_domain(url):
    # 简单检查是否是 ResearchGate 或已知有问题的域
    problematic_domains = ["researchgate.net"]
    for domain in problematic_domains:
        if domain in url:
            return True
    return False

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
    
    print(f"  Searching for: {keyword}")
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
            
        print(f"  Trying {engine_name} search engine...")
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
                
                source_log.append(f"{target_filename}\t{engine_name} search\t{keyword}")
                print(f"  Successfully replaced {target_filename} with {engine_name} result.")
                success = True
                break
            else:
                print(f"  No images found from {engine_name} for: {keyword}")
        except Exception as e:
            print(f"  Error with {engine_name} crawler: {e}")
        
        # 搜索引擎之间等待一下
        time.sleep(3)
    
    # 清理临时目录
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        
    return success

# 主处理流程
for fname, query in failed_images_map.items():
    img_path = f"assets/images/ch01/{fname}"
    print(f"Processing: {query} -> {fname}")
    
    # 使用图片爬虫下载
    success = download_image_with_crawler(query, "assets/images/ch01", fname)
    
    if not success:
        print(f"Failed to find and download an alternative for {fname} after trying multiple search engines.")
    
    # 每次处理完一张图片（无论成功与否）都等待一下
    time.sleep(5)

# 记录本次替换的来源
if source_log:
    with open(source_log_file, "a") as f: # 追加模式
        f.write(f"\n--- Alternative Source Log {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        for line in source_log:
            f.write(line + "\n")

print(f"Alternative source finding process completed. Check {source_log_file} for details.") 