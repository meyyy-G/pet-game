# src/core/scene_manager.py
"""场景管理器"""

import pygame
from src.config.game_config import GameConfig
from src.config.text_config import TextConfig


class GameScene:
    """游戏场景管理器"""

    def __init__(self):
        self.current_scene = "loading"
        self.target_scene = "loading"
        self.window = None
        self.transition_timer = 0
        self.is_transitioning = False
        self.create_window()

    def start_transition_to_main(self):
        """开始过渡到主界面"""
        self.target_scene = "main"
        self.is_transitioning = True
        self.transition_timer = GameConfig.TRANSITION_DURATION
        print("🎬 开始场景过渡动画...")

    def update_transition(self):
        """更新过渡状态"""
        if self.is_transitioning and self.transition_timer > 0:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                # 过渡完成，真正切换场景
                self.current_scene = self.target_scene
                self.create_window()
                self.is_transitioning = False
                print("✨ 场景过渡完成！")

    def get_transition_alpha(self):
        """获取过渡透明度"""
        if not self.is_transitioning:
            return 255
        # 创建淡出效果
        progress = self.transition_timer / GameConfig.TRANSITION_DURATION
        return int(255 * progress)

    def create_window(self):
        """根据当前场景创建窗口"""
        if self.current_scene == "loading":
            size = GameConfig.LOADING_WINDOW_SIZE
        elif self.current_scene == "main":
            size = GameConfig.MAIN_WINDOW_SIZE
        else:
            size = GameConfig.ROOM_WINDOW_SIZE

        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption(TextConfig.WINDOW_TITLE)

    def switch_to_main(self):
        self.current_scene = "main"
        self.create_window()

    def switch_to_room(self):
        self.current_scene = "room"
        self.create_window()

    def is_loading_scene(self):
        return self.current_scene == "loading"

    def is_main_scene(self):
        return self.current_scene == "main"

    def is_room_scene(self):
        return self.current_scene == "room"
