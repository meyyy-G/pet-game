# src/systems/resource_manager.py - 绝对路径修正版本
"""资源管理器 - 修正路径问题"""

import pygame
import os
from pathlib import Path
from src.config.game_config import GameConfig
from src.config.animation_config import AnimationConfig


class ResourceManager:
    """资源管理器 - 负责加载和管理所有游戏资源"""

    @staticmethod
    def get_project_root():
        """获取项目根目录的绝对路径"""
        # 从当前文件向上找到项目根目录
        current_file = Path(__file__)  # 当前是 src/systems/resource_manager.py
        project_root = current_file.parent.parent.parent  # 向上三级到项目根目录
        return project_root.resolve()  # 返回绝对路径

    @staticmethod
    def load_loading_animation():
        """加载loading动画"""
        print("🔄 开始加载loading动画...")
        project_root = ResourceManager.get_project_root()
        loading_path = project_root / "assets" / "animations" / "loading"

        print(f"📁 项目根目录: {project_root}")
        print(f"📁 Loading路径: {loading_path}")

        loading_frames = ResourceManager.load_png_frames(
            str(loading_path), "load_frame_",
            GameConfig.LOADING_FRAME_COUNT, GameConfig.LOADING_CAT_SIZE
        )
        if loading_frames:
            print(f"✅ Loading动画加载成功：{len(loading_frames)}帧")
            return loading_frames
        else:
            print("❌ Loading动画加载失败")
            return []

    @staticmethod
    def load_png_frames(folder, prefix, frame_count, target_size):
        """安全地加载PNG动画帧序列，带错误处理"""
        frames = []
        folder_path = Path(folder)
        print(f"🔄 加载动画：{folder_path}")
        print(f"📁 文件夹是否存在: {folder_path.exists()}")

        if not folder_path.exists():
            print(f"❌ 文件夹不存在: {folder_path}")
            return frames

        # 列出文件夹中的所有文件进行调试
        all_files = list(folder_path.glob("*.png"))
        print(f"📄 文件夹中的PNG文件: {[f.name for f in all_files]}")

        for i in range(1, frame_count + 1):
            filename = f"{prefix}{i:02d}.png"
            file_path = folder_path / filename
            print(f"🔍 尝试加载: {file_path}")

            try:
                if not file_path.exists():
                    print(f"❌ 文件不存在: {file_path}")
                    continue

                # 加载图片
                img = pygame.image.load(str(file_path)).convert_alpha()
                # 等比例缩放
                orig_w, orig_h = img.get_size()
                scale = min(target_size / orig_w, target_size / orig_h)
                new_size = (int(orig_w * scale), int(orig_h * scale))
                frame_image = pygame.transform.scale(img, new_size)
                frames.append(frame_image)
                print(f"✅ 成功加载: {filename}")
            except pygame.error as e:
                print(f"❌ Pygame错误 {file_path}: {e}")
            except Exception as e:
                print(f"❌ 其他错误 {file_path}: {e}")

        print(f"✅ 总共加载了{len(frames)}帧动画")
        return frames

    @staticmethod
    def load_all_animations():
        """加载所有动画，为主场景和房间分别加载不同大小"""
        animations = {"main": {}, "room": {}}
        print("开始加载所有动画")
        project_root = ResourceManager.get_project_root()

        for status, config in AnimationConfig.ANIMATION.items():
            # 根据动画类型选择不同的基础路径
            if status == "loading":
                folder_path = project_root / "assets" / "animations" / config['folder']
            else:
                folder_path = project_root / "assets" / "animations" / "cat" / config['folder']

            print(f"🔄 处理动画: {status}, 路径: {folder_path}")

            main_frames = ResourceManager.load_png_frames(
                str(folder_path),
                config["prefix"],
                config["count"],
                GameConfig.CAT_TARGET_SIZE
            )

            # 房间加载小尺寸猫
            room_frames = ResourceManager.load_png_frames(
                str(folder_path),
                config["prefix"],
                config["count"],
                GameConfig.CAT_ROOM_SIZE
            )

            if main_frames and room_frames:
                animations["main"][status] = main_frames
                animations["room"][status] = room_frames
                print(f"✅ {status}动画加载成功 - 主场景：{len(main_frames)}帧, 房间：{len(room_frames)}帧")
            else:
                print(f"⚠️  {status}动画加载失败，将使用默认动画")

        # 确保至少有normal动画，否则游戏无法运行
        if ("normal" not in animations["main"] or not animations["main"]["normal"] or
                "normal" not in animations["room"] or not animations["room"]["normal"]):
            print("❌ 关键错误：无法加载normal动画，游戏无法启动")
            return None

        # 用normal动画作为所有失败动画的备用
        for scene_type in ["main", "room"]:
            for status in AnimationConfig.ANIMATION.keys():
                if status not in animations[scene_type] or not animations[scene_type][status]:
                    animations[scene_type][status] = animations[scene_type]["normal"]
                    print(f"🔄 {status}使用normal动画作为备用")

        print("✅ 所有动画加载完成！")
        return animations

    @staticmethod
    def load_ui_images():
        """加载所有UI相关图片"""
        print("🔄 开始加载UI图片...")
        project_root = ResourceManager.get_project_root()
        ui_images = {}

        # 需要加载的图片列表（使用相对于项目根目录的路径）
        image_files = {
            "main_background": "assets/images/backgrounds/main_background.jpg",
            "room_background": "assets/images/backgrounds/room_background.png",
            "cloud": "assets/images/ui/cloud.png",
            "right_button": "assets/images/ui/right_arrow.png",
            "left_button": "assets/images/ui/left_arrow.png"
        }

        for name, relative_path in image_files.items():
            full_path = project_root / relative_path
            print(f"🔍 尝试加载: {full_path}")

            try:
                if not full_path.exists():
                    print(f"❌ 文件不存在: {full_path}")
                    return None

                img = pygame.image.load(str(full_path)).convert_alpha()
                # 处理不同类型的图片
                if name == "main_background":
                    img = pygame.transform.scale(img, GameConfig.MAIN_WINDOW_SIZE)
                elif name == "room_background":
                    img = pygame.transform.scale(img, GameConfig.ROOM_WINDOW_SIZE)
                elif "button" in name:
                    img = pygame.transform.scale(img, GameConfig.BUTTON_SIZE)

                ui_images[name] = img
                print(f"✅ 加载图片成功: {relative_path}")
            except pygame.error as e:
                print(f"❌ Pygame错误 {full_path}: {e}")
                return None
            except Exception as e:
                print(f"❌ 其他错误 {full_path}: {e}")
                return None

        print("✅ 所有UI图片加载完成！")
        return ui_images
