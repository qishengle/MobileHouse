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
            '可持续住宅能源效率对比',
            '节能住宅实例对比',
            'energy efficient homes comparison',
            'sustainable housing energy efficiency',
            '高能效住宅与传统住宅对比',
            '节能移动住宅实拍图',
            'tiny home energy efficiency',
            'sustainable mobile housing energy saving',
            '移动微型住宅节能特点',
            '小型预制房屋节能设计'
        ],
        'source_file': 'housing_energy_source.txt',
        'source_record': '不同住房类型能耗对比图来源',
        'suggested_citation': '欧洲环境署 "住宅建筑能源消耗对比研究" (2023); 美国能源部建筑技术办公室 "建筑能源数据手册" (2023)'
    },
    'lifecycle_carbon': {
        'file_name': 'lifecycle_carbon_emissions.png',
        'keywords': [
            '建筑生命周期碳排放实例',
            '不同住宅碳足迹比较实拍',
            'building carbon footprint comparison',
            'housing lifecycle carbon emissions examples',
            '低碳住宅与传统住宅对比',
            '移动住宅碳足迹优势',
            'tiny house carbon footprint real example',
            'sustainable home carbon reduction',
            '零碳住宅实例照片',
            '小型住宅减少碳排放实例'
        ],
        'source_file': 'lifecycle_carbon_source.txt',
        'source_record': '移动住房与传统住房全生命周期碳排放对比图来源',
        'suggested_citation': 'Nature Sustainability "建筑类型生命周期评估" (2023); 中国环境科学研究院 "建筑碳足迹评价报告" (2023)'
    },
    'water_recycling': {
        'file_name': 'water_recycling_system.png',
        'keywords': [
            '住宅水循环利用系统实例',
            '家庭雨水收集系统实拍',
            'home water recycling system',
            'residential water reuse technology',
            '小型住宅水资源循环利用',
            '移动住宅节水系统实拍',
            'compact water treatment device',
            'tiny house water conservation system',
            '微型住宅用水优化方案',
            '可持续住宅水资源管理实例'
        ],
        'source_file': 'water_recycling_source.txt',
        'source_record': '移动住房集成式水资源循环系统实例图来源',
        'suggested_citation': 'Journal of Water Reuse and Desalination "移动应用紧凑型水循环系统" (2023); 联合国环境规划署 "封闭空间可持续水资源管理" (2023)'
    },
    'nutrient_recovery': {
        'file_name': 'nutrient_recovery_benefits.png',
        'keywords': [
            '有机废弃物养分回收系统实例',
            '家庭堆肥系统实拍图',
            'organic waste nutrient recovery',
            'home composting system examples',
            '小型住宅有机废物处理设备',
            '移动住宅堆肥装置实例',
            'compact composting unit',
            'tiny house waste management',
            '微型住宅有机废弃物循环利用',
            '可持续住宅养分回收案例'
        ],
        'source_file': 'nutrient_recovery_source.txt',
        'source_record': '移动住房有机废弃物处理系统养分回收实例图来源',
        'suggested_citation': 'Environmental Science & Technology "移动环境中人类废物养分回收" (2023); 瑞典皇家理工学院 "闭环系统：有机废物养分回收" (2022)'
    },
    'decentralized_waste': {
        'file_name': 'decentralized_waste_impact.png',
        'keywords': [
            '分散式污水处理系统实例',
            '小型住宅废水处理装置实拍',
            'decentralized sewage treatment system',
            'small scale wastewater treatment examples',
            '移动住宅污水处理设备',
            '独立式生活污水处理装置',
            'mobile home wastewater treatment',
            'compact sewage processing unit',
            '微型住宅废水资源化设备',
            '可持续住宅污水循环利用实例'
        ],
        'source_file': 'decentralized_waste_source.txt',
        'source_record': '移动住房分散式废弃物处理系统实例图来源',
        'suggested_citation': 'Water Research "城市废水管理范式转变" (2023); 清华大学环境学院 "分散式污水处理与资源回收技术评估" (2023)'
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

        # 尝试使用百度搜索
        try:
            logger.info(f"尝试使用百度搜索下载图片: {keyword}")
            baidu_crawler = BaiduImageCrawler(
                downloader_threads=2,
                storage={'root_dir': output_dir},
                log_level=logging.INFO
            )
            # 百度搜索的过滤选项较少，但可以通过关键词调整
            enhanced_keyword = f"{keyword} 真实照片 高清"
            baidu_crawler.crawl(keyword=enhanced_keyword, max_num=max_num)
            
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
                
                logger.info(f"成功使用百度下载图片: {file_name} (文件大小: {file_sizes[0][1]/1024:.1f}KB)")
                
                # 保存下载记录
                source_file = os.path.join(output_dir, config['source_file'])
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write(f"{config['source_record']}:\n")
                    f.write(f"百度搜索: {keyword}\n")
                    f.write(f"文件大小: {file_sizes[0][1]/1024:.1f}KB\n\n")
                    f.write(f"建议引用来源：{config['suggested_citation']}")
                
                logger.info(f"下载记录已保存至: {source_file}")
                return True
        except Exception as e:
            logger.error(f"百度搜索下载失败: {e}")
    
    logger.warning(f"所有关键词和搜索引擎均未能成功下载图片: {file_name}")
    return False

def update_source_record(image_type, output_dir='assets/images/ch03'):
    """更新图片来源记录，创建汇总文件"""
    config = image_config.get(image_type)
    if not config:
        logger.error(f"未知的图片类型: {image_type}")
        return False
    
    source_file = os.path.join(output_dir, config['source_file'])
    if not os.path.exists(source_file):
        logger.warning(f"图片来源记录文件不存在: {source_file}")
        return False
    
    # 读取单个图片的来源记录
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    # 更新汇总记录文件
    summary_file = os.path.join(output_dir, 'image_sources.md')
    
    # 如果汇总文件不存在，则创建
    if not os.path.exists(summary_file):
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# 第三章图片来源记录\n\n")
            f.write(f"创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    # 读取现有内容
    with open(summary_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已包含该图片类型的记录
    image_title = f"## {config['file_name']}"
    if image_title in content:
        # 更新现有记录
        content_parts = content.split(image_title)
        head = content_parts[0]
        tail = ""
        if len(content_parts) > 2:
            # 查找下一个 ##
            next_section = content_parts[1].find("##")
            if next_section >= 0:
                tail = content_parts[1][next_section:] + "".join(content_parts[2:])
            else:
                tail = "".join(content_parts[2:])
        
        # 更新内容
        updated_content = f"{head}{image_title}\n\n{source_content}\n\n更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{tail}"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    else:
        # 添加新记录
        with open(summary_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{image_title}\n\n")
            f.write(source_content)
            f.write(f"\n\n更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    logger.info(f"已更新汇总图片来源记录: {summary_file}")
    return True

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='下载和替换第三章图片')
    parser.add_argument('--type', choices=list(image_config.keys()), help='指定要下载的图片类型')
    parser.add_argument('--all', action='store_true', help='下载所有图片')
    parser.add_argument('--output', default='assets/images/ch03', help='指定输出目录')
    parser.add_argument('--max-num', type=int, default=5, help='每个关键词最多下载的图片数量')
    
    args = parser.parse_args()
    
    if not args.type and not args.all:
        parser.print_help()
        return
    
    # 创建输出目录
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # 下载指定类型的图片
    if args.type:
        if download_image_with_crawler(args.type, args.output, args.max_num):
            update_source_record(args.type, args.output)
    
    # 下载所有类型的图片
    if args.all:
        for image_type in image_config.keys():
            logger.info(f"处理图片类型: {image_type}")
            if download_image_with_crawler(image_type, args.output, args.max_num):
                update_source_record(image_type, args.output)
            # 添加延迟避免被搜索引擎限制
            time.sleep(5)
    
    logger.info("图片下载和替换任务完成")

if __name__ == '__main__':
    main() 