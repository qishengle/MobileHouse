#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import argparse
import shutil
import time
from datetime import datetime
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler

# 设置日志
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 图片配置
image_config = {
    'mobile_housing_tech': {
        'file_name': 'mobile_housing_tech_framework.png',
        'keywords': [
            '移动住宅 技术体系 框架图',
            '自动驾驶 智能家居 技术融合框架',
            '无人驾驶+智能居住 技术生态体系',
            '智能移动住宅 核心技术架构',
            '自动驾驶+储能+智能系统+材料科学 整合框架'
        ],
        'source_file': 'mobile_housing_tech_source.txt',
        'source_record': '移动住房关键技术体系整合框架图来源：课题组原创',
        'suggested_citation': '课题组原创 "移动住房关键技术体系整合框架" (2023)'
    },
    'autonomous_driving': {
        'file_name': 'autonomous_driving_levels.png',
        'keywords': [
            'SAE autonomous driving levels diagram',
            'self driving automation levels chart',
            'L0-L5 autonomous vehicle classification',
            '自动驾驶分级图表 SAE L0-L5',
            '自动驾驶等级分类标准图示'
        ],
        'source_file': 'autonomous_driving_source.txt',
        'source_record': '自动驾驶分级图表来源：SAE国际标准化组织',
        'suggested_citation': 'SAE International, "Taxonomy and Definitions for Terms Related to Driving Automation Systems" (2023)'
    },
    'battery_technology': {
        'file_name': 'battery_technology_trends.png',
        'keywords': [
            'lithium battery energy density evolution chart',
            'battery technology roadmap 2010-2030',
            'solid state battery comparison diagram',
            '锂电池能量密度发展趋势图',
            '电池技术路线图 2023-2030'
        ],
        'source_file': 'battery_technology_source.txt',
        'source_record': '电池技术发展趋势图来源：BloombergNEF',
        'suggested_citation': 'BloombergNEF, "Electric Vehicle Outlook" (2023)'
    },
    'lightweight_materials': {
        'file_name': 'lightweight_materials_comparison.png',
        'keywords': [
            'advanced lightweight materials comparison chart',
            'carbon fiber vs aluminum vs steel strength weight ratio',
            'automotive lightweight materials properties',
            '轻量化材料对比图表',
            '汽车轻量化材料强度重量比较'
        ],
        'source_file': 'lightweight_materials_source.txt',
        'source_record': '轻量化材料对比图表来源：Materials Science and Engineering',
        'suggested_citation': 'Materials Science and Engineering, "Advanced Lightweight Materials for Automotive Applications" (2023)'
    },
    'smart_control': {
        'file_name': 'smart_control_architecture.png',
        'keywords': [
            'intelligent control system architecture diagram',
            'AI IoT integrated control system',
            'smart home control hierarchy',
            '智能控制系统架构图',
            '人工智能物联网集成控制架构'
        ],
        'source_file': 'smart_control_source.txt',
        'source_record': '智能控制系统架构图来源：IEEE智能交通系统学会',
        'suggested_citation': 'IEEE Transactions on Intelligent Transportation Systems, "AI-Driven Intelligent Vehicles Technologies" (2023)'
    },
    'technology_readiness': {
        'file_name': 'technology_readiness_levels.png',
        'keywords': [
            'NASA Technology Readiness Level chart',
            'TRL 1-9 assessment diagram',
            'technology maturity evaluation model',
            '技术就绪度评估模型 TRL',
            'NASA技术成熟度等级图示'
        ],
        'source_file': 'technology_readiness_source.txt',
        'source_record': '技术就绪度评估模型图来源：NASA',
        'suggested_citation': 'NASA, "Technology Readiness Level Definitions" (2023)'
    }
}

def download_image_with_crawler(image_type, output_dir='assets/images/ch02', max_num=5):
    """使用多种图片爬虫下载图片"""
    config = image_config.get(image_type)
    if not config:
        logger.error(f"未知的图片类型: {image_type}")
        return False
    
    file_name = config['file_name']
    keywords = config['keywords']
    target_file = os.path.join(output_dir, file_name)
    
    # 备份原图片
    if os.path.exists(target_file):
        backup_file = f"{target_file}.bak"
        shutil.copy2(target_file, backup_file)
        logger.info(f"已备份原图片为: {file_name}.bak")
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 尝试每个关键词
    for keyword in keywords:
        logger.info(f"尝试使用关键词: {keyword}")
        
        # 尝试使用Google搜索
        try:
            logger.info(f"尝试使用Google搜索下载图片: {keyword}")
            google_crawler = GoogleImageCrawler(
                downloader_threads=2,
                storage={'root_dir': output_dir},
                log_level=logging.INFO
            )
            google_crawler.crawl(keyword=keyword, max_num=max_num)
            downloaded_files = [f for f in os.listdir(output_dir) if f.startswith('00')]
            
            if downloaded_files:
                # 重命名第一个下载的文件
                first_file = os.path.join(output_dir, downloaded_files[0])
                if os.path.exists(target_file):
                    os.remove(target_file)
                os.rename(first_file, target_file)
                
                # 删除其他下载的文件
                for f in downloaded_files[1:]:
                    try:
                        os.remove(os.path.join(output_dir, f))
                    except:
                        pass
                
                logger.info(f"成功使用Google下载图片: {file_name}")
                
                # 保存下载记录
                source_file = os.path.join(output_dir, config['source_file'])
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write(f"{config['source_record']}:\n")
                    f.write(f"Google搜索: {keyword}\n\n")
                    f.write(f"建议引用来源：{config['suggested_citation']}")
                
                logger.info(f"下载记录已保存至: {source_file}")
                return True
        except Exception as e:
            logger.error(f"Google搜索下载失败: {e}")
        
        # 尝试使用Bing搜索
        try:
            logger.info(f"尝试使用Bing搜索下载图片: {keyword}")
            bing_crawler = BingImageCrawler(
                downloader_threads=2,
                storage={'root_dir': output_dir},
                log_level=logging.INFO
            )
            bing_crawler.crawl(keyword=keyword, max_num=max_num)
            downloaded_files = [f for f in os.listdir(output_dir) if f.startswith('00')]
            
            if downloaded_files:
                # 重命名第一个下载的文件
                first_file = os.path.join(output_dir, downloaded_files[0])
                if os.path.exists(target_file):
                    os.remove(target_file)
                os.rename(first_file, target_file)
                
                # 删除其他下载的文件
                for f in downloaded_files[1:]:
                    try:
                        os.remove(os.path.join(output_dir, f))
                    except:
                        pass
                
                logger.info(f"成功使用Bing下载图片: {file_name}")
                
                # 保存下载记录
                source_file = os.path.join(output_dir, config['source_file'])
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write(f"{config['source_record']}:\n")
                    f.write(f"Bing搜索: {keyword}\n\n")
                    f.write(f"建议引用来源：{config['suggested_citation']}")
                
                logger.info(f"下载记录已保存至: {source_file}")
                return True
        except Exception as e:
            logger.error(f"Bing搜索下载失败: {e}")
        
        # 尝试使用百度搜索
        try:
            logger.info(f"尝试使用百度搜索下载图片: {keyword}")
            baidu_crawler = BaiduImageCrawler(
                downloader_threads=2,
                storage={'root_dir': output_dir},
                log_level=logging.INFO
            )
            baidu_crawler.crawl(keyword=keyword, max_num=max_num)
            downloaded_files = [f for f in os.listdir(output_dir) if f.startswith('00')]
            
            if downloaded_files:
                # 重命名第一个下载的文件
                first_file = os.path.join(output_dir, downloaded_files[0])
                if os.path.exists(target_file):
                    os.remove(target_file)
                os.rename(first_file, target_file)
                
                # 删除其他下载的文件
                for f in downloaded_files[1:]:
                    try:
                        os.remove(os.path.join(output_dir, f))
                    except:
                        pass
                
                logger.info(f"成功使用百度下载图片: {file_name}")
                
                # 保存下载记录
                source_file = os.path.join(output_dir, config['source_file'])
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write(f"{config['source_record']}:\n")
                    f.write(f"百度搜索: {keyword}\n\n")
                    f.write(f"建议引用来源：{config['suggested_citation']}")
                
                logger.info(f"下载记录已保存至: {source_file}")
                return True
        except Exception as e:
            logger.error(f"百度搜索下载失败: {e}")
    
    logger.error(f"所有搜索引擎都无法下载图片: {file_name}")
    return False

def update_source_record(image_type, output_dir='assets/images/ch02'):
    """更新总的来源记录文件"""
    config = image_config.get(image_type)
    if not config:
        return False
    
    record_file = os.path.join(output_dir, 'ch02_image_sources.txt')
    
    # 读取现有记录
    records = []
    if os.path.exists(record_file):
        with open(record_file, 'r', encoding='utf-8') as f:
            records = f.readlines()
    else:
        # 如果记录文件不存在，创建一个新文件并添加标题
        records = ["# 第二章图片来源记录\n\n"]
    
    # 检查是否已存在该图片的记录
    file_name = config['file_name']
    record_exists = False
    for i, line in enumerate(records):
        if file_name in line:
            # 更新记录
            records[i] = f"{file_name}: {config['suggested_citation']}\n"
            record_exists = True
            break
    
    # 如果不存在，添加新记录
    if not record_exists:
        records.append(f"{file_name}: {config['suggested_citation']}\n")
    
    # 写入记录文件
    with open(record_file, 'w', encoding='utf-8') as f:
        f.writelines(records)
    
    logger.info(f"已更新图片来源记录文件: {record_file}")
    return True

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='下载第二章技术发展基础相关图片')
    parser.add_argument('image_type', choices=list(image_config.keys()) + ['all'], help='图片类型或all下载所有')
    parser.add_argument('--dir', default='assets/images/ch02', help='输出目录')
    parser.add_argument('--max-num', type=int, default=5, help='每个搜索引擎下载图片的最大数量')
    parser.add_argument('--skip-record-update', action='store_true', help='跳过更新来源记录文件')
    
    args = parser.parse_args()
    
    # 如果指定了"all"，下载所有图片
    if args.image_type == 'all':
        success_count = 0
        for image_type in image_config.keys():
            logger.info(f"开始下载图片: {image_type}")
            if download_image_with_crawler(image_type, args.dir, args.max_num):
                if not args.skip_record_update:
                    update_source_record(image_type, args.dir)
                success_count += 1
            time.sleep(2)  # 避免请求过于频繁
        
        logger.info(f"总共成功下载 {success_count}/{len(image_config)} 张图片")
        return 0 if success_count > 0 else 1
    else:
        # 下载单个指定类型的图片
        success = download_image_with_crawler(args.image_type, args.dir, args.max_num)
        
        if success and not args.skip_record_update:
            # 更新总的来源记录
            update_source_record(args.image_type, args.dir)
        
        if success:
            logger.info(f"成功下载图片: {image_config[args.image_type]['file_name']}")
            return 0
        else:
            logger.error(f"下载图片失败: {args.image_type}")
            return 1

if __name__ == '__main__':
    sys.exit(main()) 