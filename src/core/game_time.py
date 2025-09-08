# src/core/game_time.py
"""游戏时间系统"""

from src.config.game_config import GameConfig


class GameTime:
    """游戏时间管理系统"""

    def __init__(self):
        self.current_hour = GameConfig.GAME_START_HOUR
        self.frame_counter = 0
        self.time_speed_multiplier = 1  # 时间流逝速度倍数
        self.is_sleeping = False

    def update(self):
        """更新游戏时间"""
        self.frame_counter += self.time_speed_multiplier
        frames_per_hour = GameConfig.GAME_HOUR_DURATION * GameConfig.FPS

        if self.frame_counter >= frames_per_hour:
            self.frame_counter = 0
            self.current_hour = (self.current_hour + 1) % 24
            print(f"时间更新:{self.get_time_string()}")

    def is_daytime(self):
        return GameConfig.DAY_START_HOUR <= self.current_hour < GameConfig.NIGHT_START_HOUR

    def is_nighttime(self):
        return not self.is_daytime()

    def is_late_night(self):
        return self.current_hour >= 22 or self.current_hour < 6

    def get_time_string(self):
        """获取时间字符串"""
        period = "AM" if self.current_hour < 12 else "PM"
        display_hour = self.current_hour % 12 or 12
        return f"{display_hour:02d}:00 {period}"

    def start_sleeping(self):
        """开始睡觉，加速时间流逝"""
        self.is_sleeping = True
        self.time_speed_multiplier = GameConfig.SLEEP_TIME_SPEED_MULTIPLIER
        print(f"开始睡觉，时间加速{self.time_speed_multiplier}倍")

    def stop_sleeping(self):
        """结束睡觉，恢复正常时间流逝"""
        self.is_sleeping = False
        self.time_speed_multiplier = 1
        print(f"🌞 睡醒了，时间恢复正常速度")

    def get_sleep_hours_passed(self, start_hour):
        """计算睡眠时长"""
        if self.current_hour >= start_hour:
            return self.current_hour - start_hour
        else:
            return (24 - start_hour) + self.current_hour