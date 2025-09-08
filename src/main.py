# src/main.py - 智能路径检测版本
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电子宠物猫游戏 - 主入口文件（智能路径检测）
"""

import sys
import os
from pathlib import Path


def find_project_root():
    """智能查找项目根目录"""
    # 方法1：从当前文件位置计算
    current_file = Path(__file__)  # src/main.py
    project_root_from_file = current_file.parent.parent  # 向上两级

    # 方法2：从工作目录开始查找
    current_dir = Path.cwd()

    # 检查可能的项目根目录位置
    possible_roots = [
        project_root_from_file,  # 从文件位置计算的路径
        current_dir,  # 当前工作目录
        current_dir / "My Pet",  # 如果在父目录运行的情况
    ]

    for root in possible_roots:
        assets_dir = root / "assets"
        src_dir = root / "src"
        if assets_dir.exists() and src_dir.exists():
            print(f"✅ 找到项目根目录: {root}")
            return root.resolve()

    # 如果都找不到，显示调试信息
    print("❌ 无法找到项目根目录!")
    print("调试信息:")
    print(f"  当前文件位置: {current_file}")
    print(f"  计算的项目根目录: {project_root_from_file}")
    print(f"  当前工作目录: {current_dir}")

    for i, root in enumerate(possible_roots, 1):
        assets_exists = (root / "assets").exists()
        src_exists = (root / "src").exists()
        print(f"  选项{i}: {root}")
        print(f"    assets存在: {assets_exists}")
        print(f"    src存在: {src_exists}")

    return None


# 查找并设置项目根目录
project_root = find_project_root()
if project_root is None:
    print("❌ 无法找到项目根目录，请检查文件结构")
    sys.exit(1)

# 设置工作目录和Python路径
os.chdir(project_root)
sys.path.insert(0, str(project_root))

print(f"📁 设置工作目录: {os.getcwd()}")
print(f"📁 项目根目录: {project_root}")

try:
    import pygame

    print("✅ Pygame 导入成功")
except ImportError:
    print("❌ 错误：请先安装 pygame")
    print("运行：pip install pygame")
    sys.exit(1)

# 验证资源文件
assets_dir = project_root / "assets"
loading_dir = assets_dir / "animations" / "loading"

print(f"📁 Assets目录: {assets_dir}")
print(f"📁 Loading目录: {loading_dir}")

if not assets_dir.exists():
    print(f"❌ 资源文件夹不存在: {assets_dir}")
    sys.exit(1)

if loading_dir.exists():
    loading_files = list(loading_dir.glob("load_frame_*.png"))
    print(f"📄 找到 {len(loading_files)} 个loading动画文件")
    if len(loading_files) >= 12:
        print("✅ Loading动画文件充足")
    else:
        print("⚠️  Loading动画文件不足，但继续运行")
else:
    print(f"❌ Loading动画文件夹不存在: {loading_dir}")

try:
    print("🔄 导入游戏模块...")
    from src.core.game import Game

    print("✅ 游戏模块导入成功")
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)


def main():
    """游戏主入口"""
    print("🎮 启动电子宠物猫游戏...")

    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"❌ 游戏运行错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()