# src/renderer/cat_renderer.py
"""猫咪渲染器"""

import pygame


class CatRenderer:
    """猫咪渲染器"""

    @staticmethod
    def draw_cat(window, cat_animation, cat_state, scene):
        """绘制猫咪（位置由cat_state决定）"""
        # 根据场景选择对应的动画合集
        scene_type = "main" if scene.is_main_scene() else "room"
        frames = cat_animation[scene_type].get(cat_state.status, cat_animation[scene_type]["normal"])

        # 确保动画状态存在
        if frames:
            current_frame = frames[cat_state.frame_index]
            cat_rect = current_frame.get_rect()
            x, y = cat_state.get_current_position(scene)
            window.blit(current_frame, (x - cat_rect.width // 2, y - cat_rect.height // 2))