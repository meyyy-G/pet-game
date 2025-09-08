# src/systems/loading_state.py
"""加载状态管理"""

from src.config.game_config import GameConfig


class LoadingState:
    """加载状态管理器"""

    def __init__(self):
        self.frame_index = 0
        self.animation_timer = 0
        self.loading_frames = []
        self.is_loading_complete = False

    def update(self):
        """更新加载动画"""
        self.animation_timer += 1
        # 根据配置的速度切换动画帧
        if self.animation_timer >= GameConfig.LOADING_ANIMATION_SPEED:
            self.animation_timer = 0
            if self.loading_frames:
                self.frame_index = (self.frame_index + 1) % len(self.loading_frames)

    def get_current_frame(self):
        """获取当前动画帧"""
        if self.loading_frames and len(self.loading_frames) > 0:
            return self.loading_frames[self.frame_index]
        return None
