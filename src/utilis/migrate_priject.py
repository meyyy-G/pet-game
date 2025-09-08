#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电子宠物猫项目自动化迁移脚本
运行此脚本来自动整理项目文件夹结构
"""

import os
import shutil
import json
from pathlib import Path


class ProjectMigrator:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / "backup_before_migration"

    def create_backup(self):
        """创建备份"""
        print("创建备份...")
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)

        # 备份重要文件和文件夹
        important_items = [
            "My Pet.py",
            "pygame实时调整工具.py",
            "Save",
            "UI",
            "normal_cat",
            "hungry_cat",
            "sleepy_cat",
            "play_cat",
            "touched_cat",
            "loading",
            "cut素材"
        ]

        self.backup_dir.mkdir(exist_ok=True)
        for item in important_items:
            item_path = self.project_root / item
            if item_path.exists():
                if item_path.is_dir():
                    shutil.copytree(item_path, self.backup_dir / item)
                else:
                    shutil.copy2(item_path, self.backup_dir / item)

        print("备份完成！")

    def create_directory_structure(self):
        """创建新的目录结构"""
        print("创建新目录结构...")

        directories = [
            "src",
            "src/config",
            "src/core",
            "src/systems",
            "src/renderer",
            "src/events",
            "src/utils",
            "assets",
            "assets/animations",
            "assets/animations/cat",
            "assets/animations/cat/normal",
            "assets/animations/cat/hungry",
            "assets/animations/cat/sleepy",
            "assets/animations/cat/play",
            "assets/animations/cat/touched",
            "assets/animations/ui",
            "assets/animations/ui/loading",
            "assets/images",
            "assets/images/backgrounds",
            "assets/images/ui",
            "assets/images/ui/progress_bars",
            "assets/images/raw_materials",
            "assets/audio",
            "assets/audio/sfx",
            "assets/audio/music",
            "data",
            "data/saves",
            "data/configs",
            "data/logs",
            "tests",
            "docs"
        ]

        for directory in directories:
            (self.project_root / directory).mkdir(parents=True, exist_ok=True)

        print("目录结构创建完成！")

    def create_init_files(self):
        """创建__init__.py文件"""
        print("创建__init__.py文件...")

        init_dirs = [
            "src",
            "src/config",
            "src/core",
            "src/systems",
            "src/renderer",
            "src/events",
            "src/utils",
            "tests"
        ]

        for directory in init_dirs:
            init_file = self.project_root / directory / "__init__.py"
            init_file.touch()

        print("__init__.py文件创建完成！")

    def migrate_assets(self):
        """迁移资源文件"""
        print("迁移资源文件...")

        # 定义迁移映射
        migrations = {
            # 动画文件夹
            "normal_cat": "assets/animations/cat/normal",
            "hungry_cat": "assets/animations/cat/hungry",
            "sleepy_cat": "assets/animations/cat/sleepy",
            "play_cat": "assets/animations/cat/play",
            "touched_cat": "assets/animations/cat/touched",
            "loading": "assets/animations/ui/loading",

            # UI素材
            "UI": "assets/images/ui/progress_bars",
            "cut素材": "assets/images/raw_materials",

            # 存档
            "Save": "data/saves"
        }

        # 单个文件迁移
        file_migrations = {
            "main_background.jpg": "assets/images/backgrounds/",
            "room_background.png": "assets/images/backgrounds/",
            "cloud.png": "assets/images/ui/",
            "left_arrow.png": "assets/images/ui/",
            "right_arrow.png": "assets/images/ui/",
            "pygame实时调整工具.py": "src/utils/debug_tools.py"
        }

        # 迁移文件夹
        for source, target in migrations.items():
            source_path = self.project_root / source
            target_path = self.project_root / target

            if source_path.exists():
                if target_path.exists():
                    shutil.rmtree(target_path)

                if source_path.is_dir():
                    shutil.copytree(source_path, target_path)
                    print(f"  文件夹 {source} -> {target}")

        # 迁移单个文件
        for source, target in file_migrations.items():
            source_path = self.project_root / source
            if source_path.exists():
                if target.endswith('.py'):
                    # 特殊处理：重命名文件
                    target_path = self.project_root / target
                else:
                    # 移动到目录
                    target_path = self.project_root / target / source

                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, target_path)
                print(f"  文件 {source} -> {target}")

        print("资源文件迁移完成！")

    def create_config_files(self):
        """创建配置文件"""
        print("创建配置文件...")

        # requirements.txt
        requirements = """pygame>=2.1.0
pillow>=8.0.0
"""
        with open(self.project_root / "requirements.txt", 'w', encoding='utf-8') as f:
            f.write(requirements)

        # .gitignore
        gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/

# 游戏数据
data/saves/*.json
data/logs/*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# 备份文件
backup_before_migration/
"""
        with open(self.project_root / ".gitignore", 'w', encoding='utf-8') as f:
            f.write(gitignore)

        # README.md
        readme = """# 电子宠物猫游戏

一个使用 Python 和 Pygame 开发的电子宠物猫游戏。

## 安装和运行

1. 创建虚拟环境：`python -m venv .venv`
2. 激活虚拟环境：
   - Windows: `.venv\\Scripts\\activate`
   - macOS/Linux: `source .venv/bin/activate`
3. 安装依赖：`pip install -r requirements.txt`
4. 运行游戏：`python src/main.py`

## 功能特色

- 猫咪状态管理（健康、心情）
- 多种互动系统（喂食、玩耍、抚摸、睡觉）
- 昼夜循环系统
- 自动保存功能
- 精美的像素艺术动画

## 项目结构

```
├── src/          # 源代码
├── assets/       # 游戏资源
├── data/         # 游戏数据和存档
├── tests/        # 测试代码
└── docs/         # 文档
```

## 开发说明

本项目已经重构为模块化结构，便于维护和扩展。

### 代码结构

- `src/config/`: 游戏配置
- `src/core/`: 核心游戏逻辑
- `src/systems/`: 游戏系统（资源管理、存档等）
- `src/renderer/`: 渲染模块
- `src/events/`: 事件处理

### 添加新功能

1. 在相应模块添加代码
2. 更新配置文件
3. 添加相应的资源文件
4. 编写测试用例

## 许可证

MIT License
"""
        with open(self.project_root / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme)

        print("配置文件创建完成！")

    def create_sample_main(self):
        """创建示例主文件"""
        print("创建示例主文件...")

        main_py = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电子宠物猫游戏 - 主入口文件
重构后的模块化版本
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import pygame
    print("Pygame 导入成功")
except ImportError:
    print("错误：请先安装 pygame")
    print("运行：pip install pygame")
    sys.exit(1)

def main():
    """游戏主入口"""
    print("启动电子宠物猫游戏...")
    print("项目根目录:", project_root)

    # 检查资源文件
    assets_dir = project_root / "assets"
    if not assets_dir.exists():
        print("错误：资源文件夹不存在")
        print("请确保已正确运行迁移脚本")
        return

    print("资源文件夹检查通过")

    # TODO: 在这里导入重构后的游戏模块
    # from src.core.game import Game
    # game = Game()
    # game.run()

    print("游戏正在重构中...")
    print("请参考原始的 backup_before_migration/My Pet.py 进行模块化拆分")

if __name__ == "__main__":
    main()
'''
        with open(self.project_root / "src" / "main.py", 'w', encoding='utf-8') as f:
            f.write(main_py)

        print("示例主文件创建完成！")

    def clean_old_files(self):
        """清理旧文件（可选）"""
        print("检查可清理的旧文件...")

        # 这里不自动删除，只是列出可以删除的文件
        old_items = [
            "normal_cat", "hungry_cat", "sleepy_cat", "play_cat",
            "touched_cat", "loading", "UI", "cut素材", "Save",
            "My Pet.py", "pygame实时调整工具.py",
            "main_background.jpg", "room_background.png",
            "cloud.png", "left_arrow.png", "right_arrow.png"
        ]

        existing_old = []
        for item in old_items:
            if (self.project_root / item).exists():
                existing_old.append(item)

        if existing_old:
            print("以下旧文件/文件夹可以删除（已迁移到新位置）：")
            for item in existing_old:
                print(f"  - {item}")
            print("\n建议先测试游戏正常运行后再删除这些文件")
        else:
            print("没有发现需要清理的旧文件")

    def run_migration(self):
        """运行完整的迁移流程"""
        print("开始项目迁移...")
        print("=" * 50)

        try:
            self.create_backup()
            self.create_directory_structure()
            self.create_init_files()
            self.migrate_assets()
            self.create_config_files()
            self.create_sample_main()
            self.clean_old_files()

            print("=" * 50)
            print("迁移完成！")
            print("\n下一步：")
            print("1. 检查 assets/ 目录下的资源文件是否正确")
            print("2. 开始拆分 backup_before_migration/My Pet.py 到各个模块")
            print("3. 测试游戏功能是否正常")
            print("4. 提交代码到版本控制系统")

        except Exception as e:
            print(f"迁移过程中出现错误: {e}")
            print("建议检查备份文件夹恢复项目")


def main():
    """主函数"""
    print("电子宠物猫项目迁移工具")
    print("=" * 30)

    # 检查是否在正确的目录
    current_dir = Path("")
    expected_files = ["My Pet.py", ".venv"]

    if not any((current_dir / f).exists() for f in expected_files):
        print("错误：请在项目根目录运行此脚本")
        print("应该包含 'My Pet.py' 文件的目录")
        return

    # 确认迁移
    response = input("这将重新组织你的项目结构。是否继续？(y/N): ")
    if response.lower() != 'y':
        print("取消迁移")
        return

    migrator = ProjectMigrator()
    migrator.run_migration()


if __name__ == "__main__":
    main()