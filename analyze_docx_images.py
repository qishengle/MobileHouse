#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PIL import Image
import shutil

def analyze_images():
    """分析docx图片并选择适合第1章的图片"""
    
    docx_images_dir = 'assets/images/chapter01/docx_images'
    selected_images_dir = 'assets/images/chapter01/selected'
    
    # 创建选择图片目录
    os.makedirs(selected_images_dir, exist_ok=True)
    
    # 获取所有图片文件
    image_files = []
    for filename in os.listdir(docx_images_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(docx_images_dir, filename)
            try:
                with Image.open(filepath) as img:
                    width, height = img.size
                    file_size = os.path.getsize(filepath)
                    
                    image_files.append({
                        'filename': filename,
                        'filepath': filepath,
                        'width': width,
                        'height': height,
                        'size': file_size,
                        'aspect_ratio': width / height if height > 0 else 0
                    })
            except Exception as e:
                print(f"无法处理图片 {filename}: {e}")
    
    # 按文件大小排序，选择质量较好的图片
    image_files.sort(key=lambda x: x['size'], reverse=True)
    
    print(f"找到 {len(image_files)} 张有效图片")
    print("\n前20张最大的图片:")
    
    # 选择适合的图片
    selected_images = []
    
    for i, img in enumerate(image_files[:20]):
        print(f"{i+1:2d}. {img['filename']:<25} "
              f"尺寸: {img['width']}x{img['height']} "
              f"大小: {img['size']//1024}KB "
              f"比例: {img['aspect_ratio']:.2f}")
        
        # 根据图片特征选择适合的图片
        if img['size'] > 100000:  # 大于100KB的高质量图片
            if 1.2 <= img['aspect_ratio'] <= 2.0:  # 适合的宽高比
                selected_images.append(img)
    
    print(f"\n选择了 {len(selected_images)} 张适合的图片")
    
    # 复制选择的图片到新目录
    chapter1_images = [
        {'name': '01-housing-evolution', 'desc': '住房发展史概览'},
        {'name': '02-traditional-house', 'desc': '传统住房'},
        {'name': '03-courtyard-house', 'desc': '四合院'},
        {'name': '04-modern-apartment', 'desc': '现代公寓'},
        {'name': '05-mobile-home', 'desc': '移动住房'},
        {'name': '06-wall-structure', 'desc': '墙体结构'},
        {'name': '07-rural-application', 'desc': '农村应用'},
        {'name': '08-community-layout', 'desc': '社区布局'},
        {'name': '09-solar-system', 'desc': '太阳能系统'},
        {'name': '10-chassis-design', 'desc': '底盘设计'}
    ]
    
    # 为每个主题选择最合适的图片
    for i, theme in enumerate(chapter1_images):
        if i < len(selected_images):
            src_path = selected_images[i]['filepath']
            ext = os.path.splitext(selected_images[i]['filename'])[1]
            dst_filename = f"{theme['name']}{ext}"
            dst_path = os.path.join(selected_images_dir, dst_filename)
            
            shutil.copy2(src_path, dst_path)
            print(f"复制 {selected_images[i]['filename']} -> {dst_filename} ({theme['desc']})")
    
    return selected_images

if __name__ == '__main__':
    analyze_images() 