# src/systems/touch_system.py
"""抚摸系统"""

from src.config.game_config import GameConfig


class TouchSystem:
    """抚摸管理系统"""

    def __init__(self):
        self.is_touching = False
        self.last_mouse_x = None
        self.movement_count = 0
        self.touch_progress = 0
        self.last_direction = 0
        self.not_touching_timer = 0  # 松开鼠标后的计时器

    def start_touch(self, mouse_x):
        """开始抚摸"""
        self.is_touching = True
        self.last_mouse_x = mouse_x
        self.last_direction = 0
        self.not_touching_timer = 0
        print(f"开始抚摸，当前进度：{self.touch_progress:.1f}%")

    def stop_touch(self):
        """停止抚摸"""
        self.is_touching = False
        self.last_mouse_x = None
        print(f"暂停抚摸，进度保留在：{self.touch_progress:.1f}%")

    def update(self, mouse_x, cat_state):
        """更新抚摸状态"""
        # 如果已经满足（100%）且正在播放动画，不再更新
        if self.touch_progress >= 100 and (cat_state.current_action == "touch" or cat_state.is_being_touched):
            return False
        if self.touch_progress >= 100:
            return True

        if not self.is_touching:
            self.not_touching_timer += 1

            # 超过延迟时间才开始掉进度
            if self.not_touching_timer > GameConfig.TOUCH_PROGRESS_LOSS_DELAY:
                self.touch_progress = max(0, self.touch_progress - GameConfig.TOUCH_PROGRESS_DECAY * 2)
            return False

        if self.last_mouse_x is None:
            return False

        # 计算移动距离
        movement = mouse_x - self.last_mouse_x
        # 检测方向变化(左右摇摆）
        if abs(movement) > GameConfig.TOUCH_MIN_MOVEMENT:
            current_direction = 1 if movement > 0 else -1

            # 如果方向改变，记为一次有效摇动
            if current_direction != self.last_direction and self.last_direction != 0:
                self.movement_count += 1
                self.touch_progress = min(100, self.touch_progress +
                                          (100 / GameConfig.TOUCH_SATISFACTION_THRESHOLD))
                print(f"摇动次数：{self.movement_count}, 进度：{self.touch_progress:.1f}%")

            self.last_direction = current_direction
            self.last_mouse_x = mouse_x

        # 进度衰减
        if self.touch_progress < 100:
            self.touch_progress = max(0, self.touch_progress - GameConfig.TOUCH_PROGRESS_DECAY)

        # 检查是否满足需求
        return self.touch_progress >= 100

    def reset(self):
        """重置抚摸系统（满足需求后调用）"""
        self.touch_progress = 0
        self.movement_count = 0
        self.not_touching_timer = 0
        print("抚摸需求已满足，进度重置")