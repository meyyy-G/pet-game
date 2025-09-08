# src/config/game_config.py
"""游戏配置常量"""


class GameConfig:
    """游戏配置常量-所有可能需要调整的数值"""
    # 窗口设置
    MAIN_WINDOW_SIZE = (300, 450)
    ROOM_WINDOW_SIZE = (400, 400)
    WINDOW_TITLE = "ELECTRIC_PAT"
    FPS = 6

    # 加载动画配置
    LOADING_FRAME_COUNT = 12
    LOADING_ANIMATION_SPEED = 8
    LOADING_WINDOW_SIZE = (300, 450)
    LOADING_TEXT = "Loading..."
    LOADING_BACKGROUND_COLOR = (139, 69, 19)
    LOADING_TEXT_COLOR = (255, 255, 255)
    LOADING_CAT_SIZE = 80

    # 场景过渡配置
    TRANSITION_DURATION = 30  # 过渡持续帧数
    TRANSITION_FADE_SPEED = 8  # 淡入淡出速度

    # 猫咪默认位置和速度
    CAT_DEFAULT_X = 235
    CAT_DEFAULT_Y = 330
    CAT_TARGET_SIZE = 100
    CAT_ROOM_SIZE = 60
    CAT_MOVE_SPEED = 8

    # 云朵设置
    CLOUD_MIN_WIDTH = 80
    CLOUD_MAX_WIDTH = 200
    CLOUD_HEIGHT = 60
    CLOUD_SPACING = 10
    CLOUD_OFFSET_Y = -80  # 云朵上方多少像素
    CLOUD_PADDING = 20  # 文字两边的内边距

    # 游戏逻辑数值
    MAX_CONCURRENT_NEEDS = 3  # 最多同时存在3个需求
    NEED_GENERATION_INTERVAL = 60  # 每60帧检查是否生成新需求
    NEED_COOLDOWN_TIME = 180  # 单个需求冷却时间（3秒 = 180帧）

    # 状态值衰减速度
    HEALTH_DECAY_RATE = 0.4  # 健康值每秒掉落速度
    MOOD_DECAY_RATE = 0.6  # 心情值每秒掉落速度
    DECAY_INTERVAL = 6  # 每6帧（1秒）掉一次

    # 需求优先级权重（数值越高越容易被选中）
    NEED_WEIGHTS = {
        "hungry": 30,
        "thirsty": 25,
        "play": 20,
        "sleepy": 15,
        "touch": 25
    }

    # 需求生成条件
    NEED_THRESHOLDS = {
        "hungry": {"health": 88},
        "thirsty": {"health": 85},
        "play": {"mood": 80},
        "touch": {},
        "sleepy": {"special": True}
    }

    # 时间系统
    GAME_HOUR_DURATION = 12  # 游戏内1h = 12秒
    GAME_START_HOUR = 8
    DAY_START_HOUR = 6
    NIGHT_START_HOUR = 20
    SLEEP_DURATION_HOURS = 8
    SLEEP_TIME_SPEED_MULTIPLIER = 4

    # 睡觉需求配置
    SLEEPY_NIGHT_MULTIPLIER = 5  # 夜晚睡觉需求概率倍数
    SLEEPY_LATE_NIGHT_MULTIPLIER = 10  # 深夜（22点后）概率倍数
    HOURS_AWAKE_THRESHOLD = 12  # 清醒超过12小时后增加困倦

    # 消息显示时间设置
    NO_NEED_MESSAGE_FRAMES = 18

    # 按钮设置
    BUTTON_SIZE = (50, 50)
    BUTTON_Y = 200  # 按钮Y坐标
    RIGHT_BUTTON_X = 250  # 右箭头按钮X坐标
    LEFT_BUTTON_X = 10

    # Touch系统配置
    TOUCH_DETECTION_RADIUS = 50  # 检测鼠标是否在猫咪附近的半径
    TOUCH_MIN_MOVEMENT = 5  # 最小移动距离
    TOUCH_SATISFACTION_THRESHOLD = 20  # 降低到20次，让它更容易达成
    TOUCH_PROGRESS_DECAY = 0.2  # 降低衰减速度，让进度保持更久
    TOUCH_MOOD_RECOVERY = 30
    TOUCH_HEALTH_RECOVERY = 10
    TOUCH_PROGRESS_LOSS_DELAY = 30  # 松开鼠标后30帧（5秒）开始掉进度

    # 存档系统
    SAVE_FILE_NAME = "electric_pat_save.json"  # 存档文件名
    AUTO_SAVE_INTERVAL = 600  # 自动存档间隔（100秒 = 600帧）
    SAVE_SLOTS = 3  # 支持3个存档槽
    DEFAULT_SAVE_DATA = {  # 默认存档数据结构
        "version": "1.0",
        "player_name": "Player",
        "play_time": 0,
        "cat_health": 100,
        "cat_mood": 100,
        "game_hour": 8,
        "last_sleep_hour": None,
        "satisfied_needs_history": [],
        "created_time": None,
        "last_saved_time": None
    }