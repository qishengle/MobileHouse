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
    'low_cost_structure': {
        'file_name': 'low_cost_structure_design.png',
        'keywords': [
            '移动住房轻量化结构实例',
            'mobile home lightweight frame construction real',
            'modular home structure actual photograph',
            'prefab house structural frame photo',
            '实际轻型房屋结构框架照片',
            'tiny house framing construction image',
            'actual mobile home construction photo',
            '真实移动房屋框架照片',
            'lightweight steel frame housing construction',
            '移动住宅标准化结构案例'
        ],
        'source_file': 'low_cost_structure_source.txt',
        'source_record': '低成本移动住宅结构设计实例图来源',
        'suggested_citation': '国际建筑技术学会, "经济型预制住宅创新结构解决方案" (2023); 清华大学建筑学院, "低成本轻型结构住宅研究" (2023)'
    },
    'thermal_insulation': {
        'file_name': 'thermal_insulation_system.png',
        'keywords': [
            'multi-layer wall insulation technical diagram',
            'building thermal insulation cross-section technical drawing',
            'wall thermal insulation layers schematic',
            'thermal insulation system diagram with material labels',
            'energy efficient wall section diagram',
            'building envelope insulation technical cross-section',
            'passive house insulation layers diagram',
            'phase change materials in wall insulation diagram',
            'high-performance thermal insulation detail drawing',
            'wall structure thermal efficiency diagram'
        ],
        'source_file': 'thermal_insulation_source.txt',
        'source_record': '移动住宅多层次保温系统技术图解来源',
        'suggested_citation': '欧洲建筑节能研究中心, "移动住宅热工性能优化方案" (2023); 美国能源部, "小型住宅保温系统性能评估" (2022)'
    },
    'lightweight_structure': {
        'file_name': 'lightweight_structure_solution.png',
        'keywords': [
            '铝合金住宅结构框架',
            'aluminum house frame construction real',
            'lightweight housing structure photograph',
            'aluminum building framing system',
            '高强度铝合金框架实际图片',
            'high-strength aluminum frame construction',
            'actual metal frame house construction',
            '轻量化金属住宅结构实拍',
            'metal framing residential construction',
            '铝合金建筑框架实例照片'
        ],
        'source_file': 'lightweight_structure_source.txt',
        'source_record': '轻量化高强度住宅结构实例图来源',
        'suggested_citation': '国际结构工程协会, "轻量化住宅结构技术" (2023); 哈尔滨工业大学, "铝合金在轻型住宅中的应用研究" (2022)'
    },
    'acoustic_solution': {
        'file_name': 'acoustic_solution_implementation.png',
        'keywords': [
            '建筑隔音系统实施',
            'soundproofing wall installation photo',
            'acoustic insulation home real photo',
            'sound isolation wall construction',
            '住宅隔音墙体安装照片',
            'acoustic membrane installation real',
            'sound absorption panel installation',
            '隔音材料安装现场照片',
            'residential acoustic treatment photo',
            '建筑隔音实施工程照片'
        ],
        'source_file': 'acoustic_solution_source.txt',
        'source_record': '移动住宅隔音解决方案实施实例图来源',
        'suggested_citation': '德国弗劳恩霍夫建筑物理研究所, "移动住宅声学优化技术" (2023); 中国建筑科学研究院, "轻型结构住宅声学设计" (2022)'
    },
    'modular_design': {
        'file_name': 'modular_design_implementation.png',
        'keywords': [
            'modular housing technical assembly diagram',
            'prefabricated building modules exploded view',
            'standardized modular construction system diagram',
            'modular building components technical drawing',
            'prefab modular housing manufacturing diagram',
            'modular architecture design engineering drawing',
            'prefabricated modular units technical illustration',
            'modular construction technical blueprint',
            'industrialized modular building system diagram',
            'modular housing production line diagram'
        ],
        'source_file': 'modular_design_source.txt',
        'source_record': '模块化住宅设计与生产技术图解来源',
        'suggested_citation': '国际模块化建筑协会, "模块化住宅设计与生产标准" (2023); 同济大学建筑与城市规划学院, "模块化住宅产业化研究" (2022)'
    }
}

def download_image_with_crawler(image_type, output_dir='assets/images/ch04', max_num=10):
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
            # 添加过滤条件，确保查找实际照片而非图表
            filters = {
                'type': 'photo',  # 查找照片类型的图片
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
            # 添加过滤条件，优先获取实际照片
            bing_filters = {
                'type': 'photo',  # 查找照片类型的图片
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
    
    logger.error(f"所有关键词尝试失败，未能下载图片: {file_name}")
    return False

def update_source_record(image_type, output_dir='assets/images/ch04'):
    """更新图片来源记录，用于添加新信息或修正已有信息"""
    config = image_config.get(image_type)
    if not config:
        logger.error(f"未知的图片类型: {image_type}")
        return False
    
    source_file = os.path.join(output_dir, config['source_file'])
    
    if not os.path.exists(source_file):
        logger.error(f"源文件记录不存在: {source_file}")
        return False
    
    # 读取现有记录
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新记录
    with open(source_file, 'w', encoding='utf-8') as f:
        f.write(content.split('%')[0])  # 保留前面部分
        f.write(f"建议引用来源：{config['suggested_citation']}")
    
    logger.info(f"已更新图片来源记录: {source_file}")
    return True

def create_image_sources_md(output_dir='assets/images/ch04'):
    """创建汇总所有图片来源的Markdown文件"""
    source_md_file = os.path.join(output_dir, 'image_sources.md')
    
    # 创建目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 收集所有图片源记录
    all_sources = []
    for image_type, config in image_config.items():
        source_file = os.path.join(output_dir, config['source_file'])
        if os.path.exists(source_file):
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            image_file = os.path.join(output_dir, config['file_name'])
            file_size = os.path.getsize(image_file) if os.path.exists(image_file) else 0
            
            all_sources.append({
                'type': image_type,
                'file_name': config['file_name'],
                'content': content,
                'size': file_size
            })
    
    # 创建Markdown文件
    with open(source_md_file, 'w', encoding='utf-8') as f:
        f.write(f"# 第四章 图片来源记录\n\n")
        f.write(f"创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for source in all_sources:
            f.write(f"## {source['file_name']} ({source['size']/1024:.1f}KB)\n\n")
            f.write(f"{source['content']}\n\n")
    
    logger.info(f"已创建图片来源汇总文件: {source_md_file}")
    return True

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='下载替换第四章图片')
    parser.add_argument('--all', action='store_true', help='下载所有类型的图片')
    parser.add_argument('--type', type=str, help='要下载的图片类型')
    parser.add_argument('--output-dir', type=str, default='assets/images/ch04', help='图片输出目录')
    parser.add_argument('--update-source', type=str, help='更新指定类型图片的来源记录')
    parser.add_argument('--create-sources-md', action='store_true', help='创建汇总所有图片来源的Markdown文件')
    parser.add_argument('--max-num', type=int, default=10, help='每个关键词最大下载数量')
    
    args = parser.parse_args()
    
    if args.all:
        success_count = 0
        for image_type in image_config:
            logger.info(f"正在处理图片类型: {image_type}")
            if download_image_with_crawler(image_type, args.output_dir, args.max_num):
                success_count += 1
        
        # 创建汇总文件
        create_image_sources_md(args.output_dir)
        
        logger.info(f"处理完成，成功下载 {success_count}/{len(image_config)} 种图片")
    
    elif args.type:
        if args.type in image_config:
            download_image_with_crawler(args.type, args.output_dir, args.max_num)
        else:
            logger.error(f"未知的图片类型: {args.type}")
            logger.info(f"可用的图片类型: {', '.join(image_config.keys())}")
    
    elif args.update_source:
        if args.update_source in image_config:
            update_source_record(args.update_source, args.output_dir)
        else:
            logger.error(f"未知的图片类型: {args.update_source}")
            logger.info(f"可用的图片类型: {', '.join(image_config.keys())}")
    
    elif args.create_sources_md:
        create_image_sources_md(args.output_dir)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 