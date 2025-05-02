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
    'housing_energy': {
        'file_name': 'housing_energy_comparison.png',
        'keywords': [
            '不同住房类型能耗对比图表数据',
            '住宅类型年度能耗比较柱状图',
            '传统住宅与移动住宅能耗对比数据图',
            '各类型住宅单位面积能耗对比数据',
            '建筑能耗比较分析图表',
            'housing energy consumption comparison chart',
            'residential building energy use comparison graph'
        ],
        'source_file': 'housing_energy_source.txt',
        'source_record': '不同住房类型年度单位面积能耗对比图表来源',
        'suggested_citation': '欧洲环境署 "Energy Consumption in Residential Buildings" (2022); 美国能源部建筑技术办公室 "Building Energy Data Book" (2023)'
    },
    'lifecycle_carbon': {
        'file_name': 'lifecycle_carbon_emissions.png',
        'keywords': [
            '建筑生命周期碳排放对比图表',
            '移动住宅传统住宅碳足迹比较图',
            '住房类型碳排放量化分析图表',
            '建筑碳排放生命周期评估数据',
            '住宅全生命周期碳排放对比图',
            'building lifecycle carbon emissions chart',
            'housing carbon footprint comparison diagram'
        ],
        'source_file': 'lifecycle_carbon_source.txt',
        'source_record': '移动住房与传统住房全生命周期碳排放对比图表来源',
        'suggested_citation': 'Nature Sustainability "Life-cycle Assessment of Housing Types" (2023); 中国环境科学研究院 "建筑碳足迹评价报告" (2023)'
    },
    'water_recycling': {
        'file_name': 'water_recycling_system.png',
        'keywords': [
            '水资源循环利用系统流程图',
            '移动住宅水循环处理系统示意图',
            '水资源回收再利用流程示意图',
            '小型水处理循环系统图表',
            '集成式水资源循环系统图',
            'water recycling system flow chart',
            'water reuse process diagram'
        ],
        'source_file': 'water_recycling_source.txt',
        'source_record': '移动住房集成式水资源循环系统流程图来源',
        'suggested_citation': 'Journal of Water Reuse and Desalination "Compact Water Recycling Systems for Mobile Applications" (2022); 联合国环境规划署 "Sustainable Water Management in Confined Spaces" (2023)'
    },
    'nutrient_recovery': {
        'file_name': 'nutrient_recovery_benefits.png',
        'keywords': [
            '有机废弃物养分回收效益图表',
            '废弃物处理养分回收数据图',
            '养分循环利用系统效益分析图',
            '有机废物资源化利用效益图',
            '粪便厨余养分回收系统图表',
            'nutrient recovery from organic waste diagram',
            'organic waste nutrient recycling benefits chart'
        ],
        'source_file': 'nutrient_recovery_source.txt',
        'source_record': '移动住房有机废弃物处理系统养分回收及环境效益图表来源',
        'suggested_citation': 'Environmental Science & Technology "Nutrient Recovery from Human Waste in Mobile Settings" (2023); 瑞典皇家理工学院 "Closing the Loop: Nutrient Recovery from Organic Waste" (2022)'
    },
    'decentralized_waste': {
        'file_name': 'decentralized_waste_impact.png',
        'keywords': [
            '分散式废弃物处理系统影响评估图',
            '移动住宅废弃物处理城市影响图表',
            '分布式污水处理系统效益分析图',
            '分散式处理对市政系统影响数据',
            '污水处理系统范式转变图表',
            'decentralized waste treatment urban impact chart',
            'distributed wastewater system impact assessment'
        ],
        'source_file': 'decentralized_waste_source.txt',
        'source_record': '移动住房分散式废弃物处理对城市基础设施影响评估图表来源',
        'suggested_citation': 'Water Research "Paradigm Shift in Urban Wastewater Management" (2023); 清华大学环境学院 "分散式污水处理与资源回收技术评估" (2023)'
    }
}

def download_image_with_crawler(image_type, output_dir='assets/images/ch03', max_num=10):
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
            # 添加过滤条件，确保查找图表而非实际照片
            filters = {
                'type': 'clipart',  # 使用clipart类型可以找到更多图表和示意图
                'license': 'commercial,modify',  # 搜索可商用和修改的图片
                'size': 'large',  # 搜索大尺寸图片
                'color': 'color'  # 搜索彩色图片
            }
            google_crawler.crawl(keyword=keyword, max_num=max_num, filters=filters)
            
            # 检查下载的文件
            downloaded_files = [f for f in os.listdir(output_dir) if f.startswith('00')]
            
            if downloaded_files:
                # 选择文件大小最大的图片（可能质量更高）
                file_sizes = [(f, os.path.getsize(os.path.join(output_dir, f))) for f in downloaded_files]
                file_sizes.sort(key=lambda x: x[1], reverse=True)
                best_file = file_sizes[0][0]
                
                # 重命名选中的文件
                best_file_path = os.path.join(output_dir, best_file)
                if os.path.exists(target_file):
                    os.remove(target_file)
                os.rename(best_file_path, target_file)
                
                # 删除其他下载的文件
                for f in downloaded_files:
                    if f != best_file:
                        try:
                            os.remove(os.path.join(output_dir, f))
                        except:
                            pass
                
                logger.info(f"成功使用Google下载图片: {file_name} (文件大小: {file_sizes[0][1]/1024:.1f}KB)")
                
                # 保存下载记录
                source_file = os.path.join(output_dir, config['source_file'])
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write(f"{config['source_record']}:\n")
                    f.write(f"Google搜索: {keyword}\n")
                    f.write(f"文件大小: {file_sizes[0][1]/1024:.1f}KB\n\n")
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
            # 添加过滤条件，优先获取图表和示意图
            bing_filters = {
                'type': 'clipart',  # 使用clipart类型可以找到更多图表和示意图
                'license': 'commercial',  # 搜索可商用的图片
                'size': 'large'  # 搜索大尺寸图片
            }
            bing_crawler.crawl(keyword=keyword, max_num=max_num, filters=bing_filters)
            
            # 检查下载的文件
            downloaded_files = [f for f in os.listdir(output_dir) if f.startswith('00')]
            
            if downloaded_files:
                # 选择文件大小最大的图片（可能质量更高）
                file_sizes = [(f, os.path.getsize(os.path.join(output_dir, f))) for f in downloaded_files]
                file_sizes.sort(key=lambda x: x[1], reverse=True)
                best_file = file_sizes[0][0]
                
                # 重命名选中的文件
                best_file_path = os.path.join(output_dir, best_file)
                if os.path.exists(target_file):
                    os.remove(target_file)
                os.rename(best_file_path, target_file)
                
                # 删除其他下载的文件
                for f in downloaded_files:
                    if f != best_file:
                        try:
                            os.remove(os.path.join(output_dir, f))
                        except:
                            pass
                
                logger.info(f"成功使用Bing下载图片: {file_name} (文件大小: {file_sizes[0][1]/1024:.1f}KB)")
                
                # 保存下载记录
                source_file = os.path.join(output_dir, config['source_file'])
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write(f"{config['source_record']}:\n")
                    f.write(f"Bing搜索: {keyword}\n")
                    f.write(f"文件大小: {file_sizes[0][1]/1024:.1f}KB\n\n")
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
            # 百度搜索的过滤选项较少，但可以通过关键词调整
            enhanced_keyword = f"{keyword} 数据图表 高清"
            baidu_crawler.crawl(keyword=enhanced_keyword, max_num=max_num)
            
            # 检查下载的文件
            downloaded_files = [f for f in os.listdir(output_dir) if f.startswith('00')]
            
            if downloaded_files:
                # 选择文件大小最大的图片（可能质量更高）
                file_sizes = [(f, os.path.getsize(os.path.join(output_dir, f))) for f in downloaded_files]
                file_sizes.sort(key=lambda x: x[1], reverse=True)
                
                # 过滤掉太小的图片（可能是缩略图）
                valid_files = [(f, size) for f, size in file_sizes if size > 50*1024]  # 至少50KB
                
                if valid_files:
                    best_file = valid_files[0][0]
                    
                    # 重命名选中的文件
                    best_file_path = os.path.join(output_dir, best_file)
                    if os.path.exists(target_file):
                        os.remove(target_file)
                    os.rename(best_file_path, target_file)
                    
                    # 删除其他下载的文件
                    for f in downloaded_files:
                        if f != best_file:
                            try:
                                os.remove(os.path.join(output_dir, f))
                            except:
                                pass
                    
                    logger.info(f"成功使用百度下载图片: {file_name} (文件大小: {valid_files[0][1]/1024:.1f}KB)")
                    
                    # 保存下载记录
                    source_file = os.path.join(output_dir, config['source_file'])
                    with open(source_file, 'w', encoding='utf-8') as f:
                        f.write(f"{config['source_record']}:\n")
                        f.write(f"百度搜索: {enhanced_keyword}\n")
                        f.write(f"文件大小: {valid_files[0][1]/1024:.1f}KB\n\n")
                        f.write(f"建议引用来源：{config['suggested_citation']}")
                    
                    logger.info(f"下载记录已保存至: {source_file}")
                    return True
        except Exception as e:
            logger.error(f"百度搜索下载失败: {e}")
    
    logger.error(f"所有搜索引擎都无法下载合适的图片: {file_name}")
    return False

def update_source_record(image_type, output_dir='assets/images/ch03'):
    """更新总的来源记录文件"""
    config = image_config.get(image_type)
    if not config:
        return False
    
    source_file = os.path.join(output_dir, config['source_file'])
    if not os.path.exists(source_file):
        return False
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新总的记录文件
    record_file = os.path.join(output_dir, 'image_sources.md')
    with open(record_file, 'a+', encoding='utf-8') as f:
        f.seek(0)
        old_content = f.read()
        
        # 检查是否已存在记录
        if config['file_name'] not in old_content:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n\n## {config['file_name']} (更新时间: {timestamp})\n")
            f.write(content)
        else:
            # 替换已有记录
            lines = old_content.split('\n')
            new_lines = []
            start_index = -1
            end_index = -1
            
            for i, line in enumerate(lines):
                if f"## {config['file_name']}" in line:
                    start_index = i
                elif start_index != -1 and i > start_index and line.startswith('## '):
                    end_index = i
                    break
            
            if start_index != -1:
                if end_index == -1:
                    end_index = len(lines)
                
                # 更新记录
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_record = [f"## {config['file_name']} (更新时间: {timestamp})"]
                new_record.extend(content.split('\n'))
                
                new_lines = lines[:start_index] + new_record + lines[end_index:]
                
                # 清空文件并写入新内容
                f.seek(0)
                f.truncate()
                f.write('\n'.join(new_lines))
    
    logger.info(f"更新总记录文件: {record_file}")
    return True

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='下载和替换第三章图片')
    parser.add_argument('--type', type=str, help='指定要下载的图片类型', 
                        choices=list(image_config.keys()))
    parser.add_argument('--all', action='store_true', help='下载所有图片')
    parser.add_argument('--output', type=str, default='assets/images/ch03', 
                        help='指定输出目录')
    parser.add_argument('--max-num', type=int, default=10, 
                        help='每个关键词最多下载的图片数量')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    if args.type:
        # 下载单个类型的图片
        success = download_image_with_crawler(args.type, args.output, args.max_num)
        if success:
            update_source_record(args.type, args.output)
    elif args.all:
        # 下载所有类型的图片
        for image_type in image_config.keys():
            logger.info(f"\n开始下载图片类型: {image_type}")
            success = download_image_with_crawler(image_type, args.output, args.max_num)
            if success:
                update_source_record(image_type, args.output)
            # 避免过快请求
            time.sleep(2)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 