#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile
import os
from pathlib import Path

def extract_images_from_docx(docx_path, output_dir):
    """从docx文档中提取图片"""
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 打开docx文件（实际上是zip文件）
        with zipfile.ZipFile(docx_path, 'r') as docx:
            # 列出所有文件
            file_list = docx.namelist()
            
            # 查找图片文件
            image_files = [f for f in file_list if f.startswith('word/media/') and 
                          f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.emf', '.wmf'))]
            
            print(f'在文档中找到 {len(image_files)} 张图片:')
            
            extracted_images = []
            
            for i, img_file in enumerate(image_files, 1):
                print(f'{i}. {img_file}')
                
                # 提取图片
                img_data = docx.read(img_file)
                
                # 获取文件扩展名
                ext = Path(img_file).suffix
                original_name = Path(img_file).name
                
                # 保存图片
                output_path = os.path.join(output_dir, f'docx_{i:02d}_{original_name}')
                
                with open(output_path, 'wb') as f:
                    f.write(img_data)
                
                print(f'   已保存到: {output_path}')
                print(f'   文件大小: {len(img_data)} bytes')
                
                extracted_images.append({
                    'index': i,
                    'original_path': img_file,
                    'output_path': output_path,
                    'size': len(img_data),
                    'extension': ext
                })
            
            return extracted_images
            
    except Exception as e:
        print(f'提取图片时出错: {e}')
        return []

if __name__ == '__main__':
    docx_file = '移动住房时代，凤凰来仪- 简体.docx'
    output_directory = 'assets/images/chapter01/docx_images'
    
    print(f'开始从 {docx_file} 提取图片...')
    images = extract_images_from_docx(docx_file, output_directory)
    
    if images:
        print(f'\n成功提取 {len(images)} 张图片到 {output_directory}')
        
        # 生成图片清单
        print('\n图片清单:')
        for img in images:
            print(f'- {img["output_path"]} ({img["size"]} bytes)')
    else:
        print('未找到图片或提取失败') 