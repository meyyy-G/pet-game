# src/renderer/effect_renderer.py
"""特效渲染器"""

import pygame
from src.config.game_config import GameConfig
from src.config.ui_layout import UILayout
from src.config.text_config import TextConfig


class EffectRenderer:
    """特效渲染器"""

    @staticmethod
    def draw_loading_screen(window, loading_state, loading_timer):
        """绘制加载界面"""
        window.fill(GameConfig.LOADING_BACKGROUND_COLOR)

        # 获取窗口中心位置
        window_width, window_height = GameConfig.LOADING_WINDOW_SIZE
        center_x = window_width // 2
        center_y = window_height // 2

        # 绘制加载动画（猫咪）
        current_frame = loading_state.get_current_frame()
        if current_frame:
            # 计算猫咪绘制位置（居中）
            cat_rect = current_frame.get_rect()
            cat_x = center_x - cat_rect.width // 2
            cat_y = center_y - cat_rect.height // 2 - 20  # 稍微向上偏移
            window.blit(current_frame, (cat_x, cat_y))

        # 绘制"Loading..."文字
        font = pygame.font.SysFont(UILayout.FONT_NAME, 24, bold=True)
        text_surface = font.render(GameConfig.LOADING_TEXT, True, GameConfig.LOADING_TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_x = center_x - text_rect.width // 2
        text_y = center_y + 50  # 在猫咪下方
        window.blit(text_surface, (text_x, text_y))

        # 绘制加载进度点点
        dots = "." * ((loading_state.frame_index // 4) % 4)  # 0到3个点循环
        dots_surface = font.render(dots, True, GameConfig.LOADING_TEXT_COLOR)
        dots_x = text_x + text_rect.width + 5
        window.blit(dots_surface, (dots_x, text_y))

        # 绘制进度条
        progress = min(100, (loading_timer / 180) * 100)  # 基于计时器的进度
        bar_width = 200
        bar_height = 8
        bar_x = center_x - bar_width // 2
        bar_y = center_y + 100

        # 进度条背景
        pygame.draw.rect(window, (100, 50, 25), (bar_x, bar_y, bar_width, bar_height))
        # 进度条填充
        if progress > 0:
            fill_width = int(bar_width * (progress / 100))
            pygame.draw.rect(window, GameConfig.LOADING_TEXT_COLOR, (bar_x, bar_y, fill_width, bar_height))

        # 进度百分比
        progress_font = pygame.font.SysFont(UILayout.FONT_NAME, 16)
        progress_text = f"{progress:.0f}%"
        progress_surface = progress_font.render(progress_text, True, GameConfig.LOADING_TEXT_COLOR)
        progress_rect = progress_surface.get_rect()
        window.blit(progress_surface, (center_x - progress_rect.width // 2, bar_y + 15))

    @staticmethod
    def draw_need_clouds(window, cloud_img, cat_state, scene, mode="all"):
        """绘制所有云朵"""
        # 优先检查是否有无需求消息要显示
        if cat_state.no_need_message and cat_state.no_need_timer > 0:
            text = cat_state.no_need_message
            EffectRenderer.draw_single_cloud(window, cloud_img, text, cat_state, scene)
            return

        # 显示所有活跃需求
        if not cat_state.current_needs:
            return

        # 简单实现：轮流显示不同的需求
        # 可以根据帧数决定显示哪个需求
        display_index = (cat_state.frame_index // 20) % len(cat_state.current_needs)
        need = cat_state.current_needs[display_index]
        text = TextConfig.NEED_TEXTS.get(need, "")
        # 在需求文本后添加数量提示
        if len(cat_state.current_needs) > 1:
            text += f"({display_index + 1}/{len(cat_state.current_needs)})"
        EffectRenderer.draw_single_cloud(window, cloud_img, text, cat_state, scene)

    @staticmethod
    def draw_single_cloud(window, cloud_img, text, cat_state, scene):
        """绘制单个云朵"""
        font = pygame.font.SysFont(UILayout.FONT_NAME, UILayout.FONT_SIZE_CLOUD, bold=True)
        text_surface = font.render(text, True, UILayout.FONT_COLOR)
        text_width = text_surface.get_width()

        # 计算云朵大小
        cloud_width = max(GameConfig.CLOUD_MIN_WIDTH,
                          min(GameConfig.CLOUD_MAX_WIDTH, text_width + GameConfig.CLOUD_PADDING))
        x, y = cat_state.get_current_position(scene)
        screen_width = GameConfig.MAIN_WINDOW_SIZE[0] if scene.is_main_scene() else GameConfig.ROOM_WINDOW_SIZE[0]
        cloud_x = max(10, min(screen_width - cloud_width - 10, x - cloud_width // 2))
        cloud_y = y + GameConfig.CLOUD_OFFSET_Y

        # 绘制云朵
        cloud_scaled = pygame.transform.smoothscale(cloud_img, (cloud_width, GameConfig.CLOUD_HEIGHT))
        window.blit(cloud_scaled, (cloud_x, cloud_y))

        # 绘制文字
        text_x = cloud_x + (cloud_width - text_width) // 2
        text_y = cloud_y + (GameConfig.CLOUD_HEIGHT - text_surface.get_height()) // 2
        window.blit(text_surface, (text_x, text_y))
