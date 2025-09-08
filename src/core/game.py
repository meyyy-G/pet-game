# src/core/game.py - 修正版本
"""主游戏类"""

import pygame
from src.config.game_config import GameConfig
from src.core.game_time import GameTime
from src.core.scene_manager import GameScene
from src.core.cat_state import CatState
from src.systems.resource_manager import ResourceManager
from src.systems.loading_state import LoadingState
from src.events.event_handler import EventHandler
from src.renderer.ui_renderer import UIRenderer
from src.renderer.cat_renderer import CatRenderer
from src.renderer.effect_renderer import EffectRenderer


class Game:
    """主游戏类，专注于游戏逻辑"""

    def __init__(self):
        print("📦 初始化游戏...")

        # 初始化pygame
        pygame.init()

        # 创建场景管理器
        self.scene = GameScene()

        # 创建加载状态管理器
        self.loading_state = LoadingState()

        # 游戏状态变量
        self.game_time = None
        self.cat_animation = None
        self.ui_images = None
        self.cat_state = None
        self.clock = pygame.time.Clock()
        self.running = True

        # 事件处理器
        self.event_handler = EventHandler()

        # 资源加载计数器
        self.loading_timer = 0

        # 先加载loading动画
        loading_frames = ResourceManager.load_loading_animation()
        self.loading_state.loading_frames = loading_frames

    def run(self):
        """游戏主循环"""
        print("🎮 游戏开始运行...")

        while self.running:
            if self.scene.is_loading_scene():
                self._handle_loading_scene()
            else:
                self._handle_game_scene()

            # 更新场景过渡
            self.scene.update_transition()
            # 更新显示
            pygame.display.flip()
            self.clock.tick(GameConfig.FPS)

        pygame.quit()
        print("游戏结束，感谢游玩")

    def _handle_loading_scene(self):
        """处理加载场景"""
        # 处理基本事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.loading_state.update()
        self.loading_timer += 1

        # 模拟加载过程并实际加载资源
        if self.loading_timer > 180:  # 3秒后开始加载资源
            if self.game_time is None:
                print("🔄 加载游戏资源...")
                self.game_time = GameTime()
                self.cat_animation = ResourceManager.load_all_animations()
                self.ui_images = ResourceManager.load_ui_images()

                if self.cat_animation and self.ui_images:
                    self.cat_state = CatState(self.game_time)
                    self.loading_state.is_loading_complete = True
                    print("✅ 资源加载完成，开始过渡到主界面")
                    self.scene.start_transition_to_main()
                else:
                    print("❌ 资源加载失败，游戏退出")
                    self.running = False

        # 绘制加载界面
        EffectRenderer.draw_loading_screen(self.scene.window, self.loading_state, self.loading_timer)

        # 如果正在过渡，添加淡出效果
        if self.scene.is_transitioning:
            alpha = self.scene.get_transition_alpha()
            fade_surface = pygame.Surface(GameConfig.LOADING_WINDOW_SIZE)
            fade_surface.set_alpha(255 - alpha)
            fade_surface.fill((0, 0, 0))
            self.scene.window.blit(fade_surface, (0, 0))

    def _handle_game_scene(self):
        """处理游戏场景"""
        # 只有在cat_state存在时才处理游戏逻辑
        if self.cat_state is None:
            self.running = False
            return

        # 处理事件
        events = pygame.event.get()
        self.running = self.event_handler.handle_events(events, self.cat_state, self.scene, self.game_time)

        if not self.running:
            return

        # 更新游戏时间
        self.game_time.update()
        # 更新游戏状态
        self.cat_state.update(self.cat_animation, self.scene)
        # 更新存档相关状态
        self.cat_state.update_play_time()
        self.cat_state.update_save_message()
        self.cat_state.auto_save_check(self.game_time)

        # 绘制游戏界面
        self._render_game()

    def _render_game(self):
        """渲染游戏界面"""
        # 绘制背景
        bg_name = "main_background" if self.scene.is_main_scene() else "room_background"
        self.scene.window.blit(self.ui_images[bg_name], (0, 0))

        # 绘制猫咪
        CatRenderer.draw_cat(self.scene.window, self.cat_animation, self.cat_state, self.scene)

        # 绘制UI元素
        UIRenderer.draw_fixed_ui(self.scene.window, self.ui_images, self.cat_state, self.scene)
        UIRenderer.draw_buttons(self.scene.window, self.ui_images, self.scene)
        UIRenderer.draw_time_display(self.scene.window, self.game_time)
        UIRenderer.draw_game_info(self.scene.window, self.cat_state)
        UIRenderer.draw_save_message(self.scene.window, self.cat_state)

        # 绘制特效
        EffectRenderer.draw_need_clouds(self.scene.window, self.ui_images["cloud"], self.cat_state, self.scene)
