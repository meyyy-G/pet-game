# src/config/text_config.py
"""文本配置"""

class TextConfig:
    """文本配置 - 游戏中所有文本统一管理"""
    # 窗口名称
    WINDOW_TITLE = "ELECTRIC_PAT"

    # UI标签文本
    HEALTH_LABEL = "Health"
    MOOD_LABEL = "Mood"

    # 需求文本
    NEED_TEXTS = {
        "hungry": "Hungry!",
        "thirsty": "Thirsty!",
        "play": "We play!",
        "sleepy": "Sleep!",
        "touch": "Touch me!"
    }

    # 无需求提示文本
    NO_NEED_TEXTS = {
        "food_bowl": "I'm not hungry!",
        "water_bowl": "I'm not thirsty!",
        "toy": "I'm not boring!",
        "bed": "I'm not sleepy!"
    }

    # 存档系统文本
    SAVE_SUCCESS = "Game Saved!"
    LOAD_SUCCESS = "Game Loaded!"
    SAVE_FAILED = "Save Failed!"
    LOAD_FAILED = "Load Failed!"
    NO_SAVE_FILE = "No save file found!"
    AUTO_SAVE_TEXT = "Auto saving..."
