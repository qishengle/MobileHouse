#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_joby_image():
    """下载Joby Aviation的eVTOL电动飞行器图片"""
    
    # 设置输出目录
    output_dir = "assets/images/ch02"
    os.makedirs(output_dir, exist_ok=True)
    
    # 目标文件名
    filename = "joby_aviation_evtol.png"
    target_file = os.path.join(output_dir, filename)
    
    # 关键词列表尝试多种搜索
    keywords = [
        "Joby Aviation electric aircraft",
        "Joby eVTOL air taxi",
        "Joby Aviation flying taxi"
    ]
    
    logger.info(f"开始下载Joby Aviation电动飞行器图片")
    
    # 尝试每个关键词
    for keyword in keywords:
        # 使用Google图片搜索下载
        try:
            logger.info(f"使用Google搜索关键词: {keyword}")
            google_crawler = GoogleImageCrawler(
                storage={'root_dir': output_dir},
                feeder_threads=1,
                parser_threads=1,
                downloader_threads=2
            )
            
            google_crawler.crawl(keyword=keyword, max_num=5)
            
            # 检查是否下载成功
            downloaded_files = [f for f in os.listdir(output_dir) if f.startswith('000')]
            
            if downloaded_files:
                # 重命名第一个下载的文件为目标文件名
                os.rename(
                    os.path.join(output_dir, downloaded_files[0]),
                    target_file
                )
                
                # 删除其他下载的文件
                for f in downloaded_files[1:]:
                    try:
                        os.remove(os.path.join(output_dir, f))
                    except:
                        pass
                
                # 创建图片来源文件
                source_file = os.path.join(output_dir, "joby_aviation_source.txt")
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write("Joby Aviation电动垂直起降飞行器图片来源:\n")
                    f.write(f"Google搜索: {keyword}\n\n")
                    f.write("建议引用来源：Joby Aviation官方网站 (2023)")
                
                logger.info(f"成功下载图片: {filename}")
                logger.info(f"来源信息已保存至: {source_file}")
                
                # 更新主图片来源记录文件
                main_source_file = os.path.join(output_dir, "ch02_image_sources.txt")
                with open(main_source_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n{filename}: Joby Aviation官方网站 (2023)")
                
                return True
        except Exception as e:
            logger.error(f"Google搜索下载失败: {str(e)}")
        
        # 尝试使用Bing搜索
        try:
            logger.info(f"使用Bing搜索关键词: {keyword}")
            bing_crawler = BingImageCrawler(
                storage={'root_dir': output_dir},
                feeder_threads=1,
                parser_threads=1,
                downloader_threads=2
            )
            
            bing_crawler.crawl(keyword=keyword, max_num=5)
            
            # 检查是否下载成功
            downloaded_files = [f for f in os.listdir(output_dir) if f.startswith('000')]
            
            if downloaded_files:
                # 重命名第一个下载的文件为目标文件名
                os.rename(
                    os.path.join(output_dir, downloaded_files[0]),
                    target_file
                )
                
                # 删除其他下载的文件
                for f in downloaded_files[1:]:
                    try:
                        os.remove(os.path.join(output_dir, f))
                    except:
                        pass
                
                # 创建图片来源文件
                source_file = os.path.join(output_dir, "joby_aviation_source.txt")
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write("Joby Aviation电动垂直起降飞行器图片来源:\n")
                    f.write(f"Bing搜索: {keyword}\n\n")
                    f.write("建议引用来源：Joby Aviation官方网站 (2023)")
                
                logger.info(f"成功下载图片: {filename}")
                logger.info(f"来源信息已保存至: {source_file}")
                
                # 更新主图片来源记录文件
                main_source_file = os.path.join(output_dir, "ch02_image_sources.txt")
                with open(main_source_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n{filename}: Joby Aviation官方网站 (2023)")
                
                return True
        except Exception as e:
            logger.error(f"Bing搜索下载失败: {str(e)}")
    
    logger.error("所有尝试都未能找到满足条件的图片")
    return False

if __name__ == "__main__":
    download_joby_image() 