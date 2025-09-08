# src/config/ui_layout.py
"""UI布局配置"""


class UILayout:
    """UI布局常量 - 界面元素的位置"""
    # 主场景进度条位置
    MAIN_PROGRESS_BAR_X = 200
    MAIN_HEALTH_BAR_Y = 53
    MAIN_MOOD_BAR_Y = 79

    # 房间场景进度条位置
    ROOM_PROGRESS_BAR_X = 310
    ROOM_HEALTH_BAR_Y = 30
    ROOM_MOOD_BAR_Y = 60

    # 时间显示位置
    TIME_DISPLAY_X = 10
    TIME_DISPLAY_Y = 10

    # 字体设置
    FONT_NAME = "Comic Sans MS"
    FONT_SIZE_UI = 13
    FONT_SIZE_CLOUD = 14
    FONT_SIZE_TIME = 16
    LABEL_OFFSET_Y = -16

    # 颜色
    FONT_COLOR = (60, 30, 0)
    TIME_COLOR_DAY = (60, 30, 0)
    TIME_COLOR_NIGHT = (150, 150, 200)
