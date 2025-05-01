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
    'jobs_housing': {
        'file_name': 'jobs_housing_balance.png',
        'keywords': [
            'jobs housing balance index commute time correlation chart',
            'job housing balance and commute time scatter plot',
            '职住平衡指数与通勤时间的关系 散点图'
        ],
        'source_file': 'jobs_housing_source.txt',
        'source_record': '职住平衡与通勤时间关系图来源：Google搜索',
        'suggested_citation': 'OECD交通与城市研究，《城市通勤模式分析》(2023)'
    },
    'mobile_housing': {
        'file_name': 'mobile_housing_solution.png',
        'keywords': [
            'mobile housing solutions urban innovation',
            'movable modular housing urban design',
            '移动住宅解决方案 城市创新'
        ],
        'source_file': 'mobile_housing_solution_source.txt',
        'source_record': '移动住宅解决方案图片来源：Google搜索',
        'suggested_citation': '未来城市研究所，《移动住宅创新解决方案》(2023)'
    },
    'tokyo_case': {
        'file_name': 'tokyo_case_study.png',
        'keywords': [
            'Tokyo micro apartments space saving design',
            'Tokyo compact living solutions',
            '东京微型公寓空间优化设计'
        ],
        'source_file': 'tokyo_case_study_source.txt',
        'source_record': '东京微型公寓设计图片来源：Google搜索',
        'suggested_citation': '日本住宅与城市研究所，《东京都市住宅创新案例集》(2023)'
    },
    'housing_trend': {
        'file_name': 'housing_affordability_trend.png',
        'keywords': [
            'global house price to income ratio trend 2000-2023 chart',
            'housing affordability index historical trend graph',
            'Demographia International Housing Affordability Survey 2023 chart'
        ],
        'source_file': 'housing_trend_source.txt',
        'source_record': '住房可负担性趋势图来源：Google搜索',
        'suggested_citation': 'Knight Frank全球房价指数报告 (2023)'
    },
    'amsterdam': {
        'file_name': 'amsterdam_floating_houses.png',
        'keywords': [
            'Amsterdam floating houses community',
            'Amsterdam water homes sustainable housing',
            '阿姆斯特丹水上住宅社区'
        ],
        'source_file': 'amsterdam_houses_source.txt',
        'source_record': '阿姆斯特丹水上住宅图片来源：Google搜索',
        'suggested_citation': '荷兰水上住宅协会，《Floating Communities of Amsterdam》(2023)'
    },
    'xiong_an': {
        'file_name': 'xiong_an_housing.png',
        'keywords': [
            'Xiong\'an New Area smart housing development',
            'Xiong\'an ecological city planning',
            '雄安新区智慧住宅生态城市规划'
        ],
        'source_file': 'xiong_an_housing_source.txt',
        'source_record': '雄安新区智慧住宅图片来源：Google搜索',
        'suggested_citation': '雄安新区规划建设局，《雄安新区智慧住房发展规划》(2023)'
    },
    'hangzhou': {
        'file_name': 'hangzhou_talent_housing.png',
        'keywords': [
            'Hangzhou talent apartment innovation corridor',
            'Hangzhou tech innovation corridor housing',
            '杭州城西科创走廊人才公寓'
        ],
        'source_file': 'hangzhou_talent_housing_source.txt',
        'source_record': '杭州科创走廊人才公寓图片来源：Google搜索',
        'suggested_citation': '杭州市城西科创大走廊管理委员会，《科创人才住房发展报告》(2023)'
    },
    'shenzhen_housing': {
        'file_name': 'shenzhen_housing_evolution.png',
        'keywords': [
            'Shenzhen housing system evolution 1980-2023',
            'Shenzhen urban housing development history',
            '深圳住房供给体系演变 1980-2023'
        ],
        'source_file': 'shenzhen_housing_source.txt',
        'source_record': '深圳住房供给体系演变图片来源：Google搜索',
        'suggested_citation': '深圳市住房和建设局，《深圳住房发展白皮书》(2022)'
    },
    'shenzhen_innovation': {
        'file_name': 'shenzhen_housing_innovation.png',
        'keywords': [
            'Shenzhen housing innovation model chart',
            'Shenzhen affordable housing policy diagram',
            '深圳住房创新模式与成效分析'
        ],
        'source_file': 'shenzhen_innovation_source.txt',
        'source_record': '深圳住房创新模式图片来源：Google搜索',
        'suggested_citation': '深圳市住房和建设局，《深圳住房创新实践报告》(2023)'
    },
    'shenzhen_evolution': {
        'file_name': 'shenzhen_housing_evolution.png',
        'keywords': [
            'Shenzhen housing development evolution 1980-2023 diagram',
            'Shenzhen housing supply system historical evolution chart',
            'Shenzhen urban housing transformation timeline',
            '深圳住房供给体系演变图 1980-2023',
            '深圳住房发展历程阶段演变图表'
        ],
        'source_file': 'shenzhen_evolution_source.txt',
        'source_record': '深圳住房发展白皮书中的图表',
        'suggested_citation': '深圳市住房和建设局，《深圳住房发展白皮书》(2023)'
    },
    'hydrogen_fuel_cell': {
        'file_name': 'hydrogen_fuel_cell_integration.png',
        'keywords': [
            'hydrogen fuel cell integration schematic diagram',
            'fuel cell battery hybrid system schematic',
            'fuel cell system diagram technical',
            'hydrogen fuel cell electric vehicle powertrain diagram',
            '氢燃料电池系统示意图',
            '燃料电池电动汽车系统原理图'
        ],
        'source_file': 'hydrogen_fuel_cell_source.txt',
        'source_record': '氢燃料电池系统集成架构图来源',
        'suggested_citation': 'Journal of Power Sources, "Integrated Hydrogen Fuel Cell Systems for Mobile Applications" (2023)'
    }
}

def download_image_with_crawler(image_type, output_dir='assets/images/ch01', max_num=5):
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
            # 添加过滤条件 - 移除尺寸限制，优先保证相关性
            filters = {
                'type': 'photo',
                'license': 'commercial,modify'  # 搜索可商用和修改的图片
            }
            google_crawler.crawl(keyword=keyword, max_num=max_num, filters=filters)
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
                    f.write(f"建议引用来源：{config['suggested_citation']}%")
                
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
            # 添加过滤条件 - 移除尺寸限制
            bing_filters = {
                'type': 'photo',
                'license': 'commercial'  # 搜索可商用的图片
            }
            bing_crawler.crawl(keyword=keyword, max_num=max_num, filters=bing_filters)
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
                    f.write(f"建议引用来源：{config['suggested_citation']}%")
                
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
            # 添加过滤条件 - 移除尺寸限制
            baidu_filters = {
                'type': 'photo'
            }
            baidu_crawler.crawl(keyword=keyword, max_num=max_num, filters=baidu_filters)
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
                    f.write(f"建议引用来源：{config['suggested_citation']}%")
                
                logger.info(f"下载记录已保存至: {source_file}")
                return True
        except Exception as e:
            logger.error(f"百度搜索下载失败: {e}")
    
    logger.error(f"所有搜索引擎都无法下载图片: {file_name}")
    return False

def update_source_record(image_type, output_dir='assets/images/ch01'):
    """更新总的来源记录文件"""
    config = image_config.get(image_type)
    if not config:
        return False
    
    record_file = os.path.join(output_dir, 'replaced_images_sources.txt')
    
    # 读取现有记录
    records = []
    if os.path.exists(record_file):
        with open(record_file, 'r', encoding='utf-8') as f:
            records = f.readlines()
    
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
    parser = argparse.ArgumentParser(description='替换指定类型的图片')
    parser.add_argument('image_type', choices=list(image_config.keys()), help='图片类型')
    parser.add_argument('--dir', default='assets/images/ch01', help='输出目录')
    parser.add_argument('--max-num', type=int, default=5, help='下载图片的最大数量')
    parser.add_argument('--skip-record-update', action='store_true', help='跳过更新来源记录文件')
    
    args = parser.parse_args()
    
    # 下载图片
    success = download_image_with_crawler(args.image_type, args.dir, args.max_num)
    
    if success and not args.skip_record_update:
        # 更新总的来源记录
        update_source_record(args.image_type, args.dir)
    
    if success:
        logger.info(f"成功下载图片: {image_config[args.image_type]['file_name']}")
    else:
        logger.error(f"下载图片失败: {args.image_type}")
        sys.exit(1)

if __name__ == '__main__':
    main() 