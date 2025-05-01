import re

# 读取README文件
readme_path = "content/part1-背景理论/ch01-城市化进程/README.md"
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 在线URL前缀
online_prefix = "https://qishengle.github.io/MobileHouse/assets/images/ch01/"
# 本地相对路径前缀
local_prefix = "/assets/images/ch01/"  # 修改为以仓库根目录为基准的路径

# 替换图片路径
pattern = r'\]\(' + re.escape(online_prefix) + r'([^)]+)\)'
replacement = r'](' + local_prefix + r'\1)'

# 如果已经使用了../../../格式的相对路径，也将其替换为仓库根目录路径
old_relative_prefix = "../../../assets/images/ch01/"
if old_relative_prefix in content:
    content = content.replace(old_relative_prefix, local_prefix)
else:
    content = re.sub(pattern, replacement, content)

# 统计替换次数
replacement_count = content.count(local_prefix)

# 保存更新后的文件
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"更新完成！")
print(f"总共更新了 {replacement_count} 处图片引用路径")
print(f"图片路径已统一修改为: {local_prefix}") 