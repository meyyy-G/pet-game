# src/renderer/ui_renderer.py
"""UI渲染器"""

import pygame
from src.config.game_config import GameConfig
from src.config.ui_layout import UILayout
from src.config.text_config import TextConfig


class UIRenderer:
    """UI渲染器"""

    @staticmethod
    def draw_progress_bar(window, value, prefix, pos):
        """进度条绘制函数"""
        # 根据数值范围直接决定用哪张图片
        percent = 100 if value >= 90 else 80 if value >= 70 else 50 if value >= 45 else 30 if value >= 25 else 15
        img_path = f"assets/images/ui/progress_bars/{prefix}_{percent}.png"

        try:
            bar_img = pygame.image.load(img_path).convert_alpha()
            bar_img = pygame.transform.scale(bar_img, (70, 15))
            window.blit(bar_img, pos)
        except Exception as e:
            print(f"进度条图片加载失败：{img_path},{e}")

    @staticmethod
    def draw_fixed_ui(window, ui_images, cat_state, scene):
        """绘制UI界面"""
        # 根据场景选择UI位置
        if scene.is_main_scene():
            bar_x = UILayout.MAIN_PROGRESS_BAR_X
            health_y = UILayout.MAIN_HEALTH_BAR_Y
            mood_y = UILayout.MAIN_MOOD_BAR_Y
        else:
            bar_x = UILayout.ROOM_PROGRESS_BAR_X
            health_y = UILayout.ROOM_HEALTH_BAR_Y
            mood_y = UILayout.ROOM_MOOD_BAR_Y

        UIRenderer.draw_progress_bar(window, cat_state.health, "health_bar", (bar_x, health_y))
        UIRenderer.draw_progress_bar(window, cat_state.mood, "mood_bar", (bar_x, mood_y))

        # 创建字体对象
        font = pygame.font.SysFont(UILayout.FONT_NAME, UILayout.FONT_SIZE_UI, bold=True)
        window.blit(font.render(TextConfig.HEALTH_LABEL, True, UILayout.FONT_COLOR),
                    (bar_x, health_y + UILayout.LABEL_OFFSET_Y))
        window.blit(font.render(TextConfig.MOOD_LABEL, True, UILayout.FONT_COLOR),
                    (bar_x, mood_y + UILayout.LABEL_OFFSET_Y))

        # 在主场景显示抚摸进度条（如果正在抚摸）
        if scene.is_main_scene() and "touch" in cat_state.current_needs:
            progress_text = f"Touch: {cat_state.touch_system.touch_progress:.0f}%"
            text_surface = font.render(progress_text, True, UILayout.FONT_COLOR)
            window.blit(text_surface, (150, 200))

            # 小巧的进度条
            bar_width = 100
            bar_height = 15
            bar_x = 150
            bar_y = 220

            # 背景
            pygame.draw.rect(window, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height))

            # 进度
            progress_width = int(bar_width * (cat_state.touch_system.touch_progress / 100))
            if progress_width > 0:
                pygame.draw.rect(window, (100, 200, 100), (bar_x, bar_y, progress_width, bar_height))
            # 边框
            pygame.draw.rect(window, (60, 30, 0), (bar_x, bar_y, bar_width, bar_height), 2)

    @staticmethod
    def draw_time_display(window, game_time):
        """绘制时间显示"""
        font = pygame.font.SysFont(UILayout.FONT_NAME, UILayout.FONT_SIZE_TIME, bold=True)
        # 根据白天/夜晚选择颜色
        color = UILayout.TIME_COLOR_DAY if game_time.is_daytime() else UILayout.TIME_COLOR_NIGHT

        time_string = game_time.get_time_string()
        # 如果在睡觉，显示特殊效果
        if game_time.is_sleeping:
            time_string += " 💤"

        window.blit(font.render(time_string, True, color),
                    (UILayout.TIME_DISPLAY_X, UILayout.TIME_DISPLAY_Y))

        # 显示白天/夜晚状态
        status = "☀️ Day" if game_time.is_daytime() else "🌙 Night"
        window.blit(font.render(status, True, color),
                    (UILayout.TIME_DISPLAY_X, UILayout.TIME_DISPLAY_Y + 20))

    @staticmethod
    def draw_buttons(window, ui_images, scene):
        """绘制按钮"""
        if scene.is_main_scene():
            window.blit(ui_images["right_button"], (GameConfig.RIGHT_BUTTON_X, GameConfig.BUTTON_Y))
        else:
            window.blit(ui_images["left_button"], (GameConfig.LEFT_BUTTON_X, GameConfig.BUTTON_Y - 50))

    @staticmethod
    def draw_save_message(window, cat_state):
        """绘制存档消息"""
        if cat_state is None:
            return
        if cat_state.last_save_message and cat_state.save_message_timer > 0:
            # 创建半透明背景
            font = pygame.font.SysFont(UILayout.FONT_NAME, 18, bold=True)
            text_surface = font.render(cat_state.last_save_message, True, (255, 255, 255))
            text_rect = text_surface.get_rect()

            # 计算位置（屏幕右上角）
            window_width = window.get_width()
            message_x = window_width - text_rect.width - 20
            message_y = 10

            # 绘制背景框
            bg_rect = pygame.Rect(message_x - 10, message_y - 5, text_rect.width + 20, text_rect.height + 10)

            # 根据消息类型选择颜色
            if "Success" in cat_state.last_save_message or "Saved" in cat_state.last_save_message:
                bg_color = (34, 139, 34, 180)  # 绿色
            elif "Failed" in cat_state.last_save_message:
                bg_color = (220, 20, 60, 180)  # 红色
            else:
                bg_color = (70, 130, 180, 180)  # 蓝色（自动保存）

            # 创建半透明表面
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill(bg_color)
            window.blit(bg_surface, (bg_rect.x, bg_rect.y))

            # 绘制文字
            window.blit(text_surface, (message_x, message_y))

    @staticmethod
    def draw_game_info(window, cat_state):
        """绘制游戏信息（时长等）"""
        if cat_state is None:
            return

        font = pygame.font.SysFont(UILayout.FONT_NAME, 12)

        # 显示游戏时长
        play_time_minutes = int(cat_state.play_time // 60)
        play_time_seconds = int(cat_state.play_time % 60)
        time_text = f"Time: {play_time_minutes:02d}:{play_time_seconds:02d}"
        time_surface = font.render(time_text, True, UILayout.FONT_COLOR)

        # 根据场景选择位置
        if window.get_width() == GameConfig.MAIN_WINDOW_SIZE[0]:  # 主场景
            window.blit(time_surface, (10, 50))
        else:  # 房间场景
            window.blit(time_surface, (10, 80))

        # 显示存档提示
        hint_text = "F5:Save F9:Load"
        hint_surface = font.render(hint_text, True, (128, 128, 128))
        window.blit(hint_surface, (10, window.get_height() - 20))
