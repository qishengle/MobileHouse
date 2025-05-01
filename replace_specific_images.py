import os
import logging
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_image_with_crawler(keyword, output_dir, filename, max_num=5):
    """使用多个搜索引擎下载图片"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 记录下载来源
    sources = []
    
    # 1. 尝试使用Google搜索
    try:
        logger.info(f"尝试使用Google搜索下载图片: {keyword}")
        google_crawler = GoogleImageCrawler(
            storage={'root_dir': output_dir},
            feeder_threads=1,
            parser_threads=1,
            downloader_threads=2
        )
        google_crawler.crawl(keyword=keyword, max_num=max_num, file_idx_offset=0)
        # 检查是否下载成功
        downloaded_files = [f for f in os.listdir(output_dir) if f.startswith('000')]
        if downloaded_files:
            # 重命名第一个文件为目标文件名
            os.rename(os.path.join(output_dir, downloaded_files[0]), 
                      os.path.join(output_dir, filename))
            # 删除其他下载的文件
            for f in downloaded_files[1:]:
                try:
                    os.remove(os.path.join(output_dir, f))
                except:
                    pass
            sources.append(f"Google搜索: {keyword}")
            logger.info(f"成功使用Google下载图片: {filename}")
            return sources
    except Exception as e:
        logger.warning(f"Google搜索下载失败: {str(e)}")
    
    # 2. 尝试使用Bing搜索
    try:
        logger.info(f"尝试使用Bing搜索下载图片: {keyword}")
        bing_crawler = BingImageCrawler(
            storage={'root_dir': output_dir},
            feeder_threads=1,
            parser_threads=1,
            downloader_threads=2
        )
        bing_crawler.crawl(keyword=keyword, max_num=max_num, file_idx_offset=0)
        # 检查是否下载成功
        downloaded_files = [f for f in os.listdir(output_dir) if f.startswith('000')]
        if downloaded_files:
            # 重命名第一个文件为目标文件名
            os.rename(os.path.join(output_dir, downloaded_files[0]), 
                      os.path.join(output_dir, filename))
            # 删除其他下载的文件
            for f in downloaded_files[1:]:
                try:
                    os.remove(os.path.join(output_dir, f))
                except:
                    pass
            sources.append(f"Bing搜索: {keyword}")
            logger.info(f"成功使用Bing下载图片: {filename}")
            return sources
    except Exception as e:
        logger.warning(f"Bing搜索下载失败: {str(e)}")
    
    # 3. 尝试使用百度搜索
    try:
        logger.info(f"尝试使用百度搜索下载图片: {keyword}")
        baidu_crawler = BaiduImageCrawler(
            storage={'root_dir': output_dir},
            feeder_threads=1,
            parser_threads=1,
            downloader_threads=2
        )
        baidu_crawler.crawl(keyword=keyword, max_num=max_num, file_idx_offset=0)
        # 检查是否下载成功
        downloaded_files = [f for f in os.listdir(output_dir) if f.startswith('000')]
        if downloaded_files:
            # 重命名第一个文件为目标文件名
            os.rename(os.path.join(output_dir, downloaded_files[0]), 
                      os.path.join(output_dir, filename))
            # 删除其他下载的文件
            for f in downloaded_files[1:]:
                try:
                    os.remove(os.path.join(output_dir, f))
                except:
                    pass
            sources.append(f"百度搜索: {keyword}")
            logger.info(f"成功使用百度下载图片: {filename}")
            return sources
    except Exception as e:
        logger.warning(f"百度搜索下载失败: {str(e)}")
    
    return []

def main():
    # 设置图片保存路径
    output_dir = "assets/images/ch01"
    os.makedirs(output_dir, exist_ok=True)
    
    # 图片信息和优化的搜索关键词
    images_to_replace = [
        {
            "filename": "china_housing_system.png",
            "keyword": "中国多层次住房保障体系 保障性住房 商品房 人才住房 框架图 高清",
            "backup_keyword": "中国住房保障体系 多层次住房 体系架构 清晰图表"
        },
        {
            "filename": "housing_affordability_trend.png",
            "keyword": "全球主要城市房价收入比变化趋势 2000-2023 数据图表 高清",
            "backup_keyword": "主要城市房价收入比 国际城市房价对比 清晰图表 统计数据"
        }
    ]
    
    # 下载并替换图片
    sources_log = []
    for img in images_to_replace:
        logger.info(f"开始下载图片: {img['filename']}")
        
        # 如果文件已存在，先备份
        if os.path.exists(os.path.join(output_dir, img['filename'])):
            backup_name = img['filename'] + '.bak'
            try:
                os.rename(
                    os.path.join(output_dir, img['filename']),
                    os.path.join(output_dir, backup_name)
                )
                logger.info(f"已备份原图片为: {backup_name}")
            except Exception as e:
                logger.warning(f"备份原图片失败: {str(e)}")
        
        # 尝试使用优化的关键词下载
        sources = download_image_with_crawler(
            img['keyword'], output_dir, img['filename'], max_num=5
        )
        
        # 如果主关键词失败，尝试备用关键词
        if not sources:
            logger.info(f"主关键词下载失败，尝试备用关键词: {img['backup_keyword']}")
            sources = download_image_with_crawler(
                img['backup_keyword'], output_dir, img['filename'], max_num=5
            )
        
        # 记录下载结果
        if sources:
            sources_log.append(f"{img['filename']}: {', '.join(sources)}")
            logger.info(f"成功下载图片: {img['filename']}")
        else:
            logger.error(f"下载图片失败: {img['filename']}")
    
    # 保存下载日志
    log_file = os.path.join(output_dir, "replaced_images_sources.txt")
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"替换的图片来源记录：\n")
        f.write("\n".join(sources_log))
    
    logger.info(f"图片替换完成，共替换 {len(sources_log)} 张图片")
    logger.info(f"下载记录已保存至: {log_file}")

if __name__ == "__main__":
    main() 