import pygame
import os
import math
import random
import json
import time

class GameConfig:
    """游戏配置常量-所有可能需要调整的数值"""
    #窗口设置
    MAIN_WINDOW_SIZE = (300, 450)
    ROOM_WINDOW_SIZE = (400,400)
    WINDOW_TITLE = "ELECTRIC_PAT"
    FPS = 6

    #加载动画配置
    LOADING_FRAME_COUNT = 12
    LOADING_ANIMATION_SPEED = 8
    LOADING_WINDOW_SIZE = (300,450)
    LOADING_TEXT = "Loading..."
    LOADING_BACKGROUND_COLOR = (139,69,19)
    LOADING_TEXT_COLOR = (255, 255, 255)
    LOADING_CAT_SIZE = 80

    # 场景过渡配置
    TRANSITION_DURATION = 30  # 过渡持续帧数
    TRANSITION_FADE_SPEED = 8  # 淡入淡出速度

    #猫咪默认位置和速度
    CAT_DEFAULT_X = 235
    CAT_DEFAULT_Y = 330
    CAT_TARGET_SIZE = 100
    CAT_ROOM_SIZE = 60
    CAT_MOVE_SPEED = 8

    #云朵设置
    CLOUD_MIN_WIDTH = 80
    CLOUD_MAX_WIDTH = 200
    CLOUD_HEIGHT = 60
    CLOUD_SPACING = 10
    CLOUD_OFFSET_Y = -80 #云朵上方多少像素
    CLOUD_PADDING = 20 #文字两边的内边距

    #游戏逻辑数值
    MAX_CONCURRENT_NEEDS = 3 #最多同时存在3个需求
    NEED_GENERATION_INTERVAL = 60 #每10（60帧） 检查是否生成新需求
    NEED_COOLDOWN_TIME = 180  # 单个需求冷却时间（3秒 = 180帧）

    #状态值衰减速度
    HEALTH_DECAY_RATE = 0.4 #健康值每秒掉落速度
    MOOD_DECAY_RATE = 0.6   #心情值每秒掉落速度
    DECAY_INTERVAL = 6      #每6帧（1秒）掉一次

    # 需求优先级权重（数值越高越容易被选中）
    NEED_WEIGHTS = {
        "hungry": 30,
        "thirsty": 25,
        "play": 20,
        "sleepy": 15,
        "touch": 25
    }
    #需求生成条件
    NEED_THRESHOLDS = {
        "hungry":{"health":88},
        "thirsty":{"health":85},
        "play":{"mood":80},
        "touch":{},
        "sleepy":{"special":True}
    }

    #时间系统
    GAME_HOUR_DURATION = 12 #游戏内1h = 10sec
    GAME_START_HOUR = 8
    DAY_START_HOUR = 6
    NIGHT_START_HOUR = 20
    SLEEP_DURATION_HOURS = 8
    SLEEP_TIME_SPEED_MULTIPLIER = 4

    #睡觉需求配置
    SLEEPY_NIGHT_MULTIPLIER = 5 # 夜晚睡觉需求概率倍数
    SLEEPY_LATE_NIGHT_MULTIPLIER = 10 # 深夜（22点后）概率倍数
    HOURS_AWAKE_THRESHOLD = 12 # 清醒超过12小时后增加困倦

    #消息显示时间设置
    NO_NEED_MESSAGE_FRAMES = 18

    #按钮设置
    BUTTON_SIZE = (50,50)
    BUTTON_Y = 200 #按钮Y坐标
    RIGHT_BUTTON_X = 250 #右箭头按钮X坐标
    LEFT_BUTTON_X = 10

    # Touch系统配置 - 改进版
    TOUCH_DETECTION_RADIUS = 50  # 检测鼠标是否在猫咪附近的半径
    TOUCH_MIN_MOVEMENT = 5  # 最小移动距离
    TOUCH_SATISFACTION_THRESHOLD = 20  # 降低到20次，让它更容易达成
    TOUCH_PROGRESS_DECAY = 0.2  # 降低衰减速度，让进度保持更久
    TOUCH_MOOD_RECOVERY = 30
    TOUCH_HEALTH_RECOVERY = 10
    TOUCH_PROGRESS_LOSS_DELAY = 30  # 松开鼠标后30帧（5秒）开始掉进度

    #存档系统
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

class UILayout:
    """UI布局常量 - 界面元素的位置"""
    #主场景进度条位置
    MAIN_PROGRESS_BAR_X = 200
    MAIN_HEALTH_BAR_Y = 53
    MAIN_MOOD_BAR_Y = 79

    #房间场景进度条位置
    ROOM_PROGRESS_BAR_X = 310
    ROOM_HEALTH_BAR_Y = 30
    ROOM_MOOD_BAR_Y = 60

    #时间显示位置
    TIME_DISPLAY_X = 10
    TIME_DISPLAY_Y = 10

    #字体设置
    FONT_NAME = "Comic Sans MS"
    FONT_SIZE_UI = 13
    FONT_SIZE_CLOUD = 14
    FONT_SIZE_TIME = 16
    LABEL_OFFSET_Y = -16
    #颜色
    FONT_COLOR = (60, 30, 0)
    TIME_COLOR_DAY = (60,30,0)
    TIME_COLOR_NIGHT = (150,150,200)

class InteractionZones:
    """房间场景的交互区域定义"""
    ZONES = {
        "bed": {
            "rect": (250, 185, 15, 65),
            "cat_pos": (257.5, 212.5),
            "action": "sleepy",
            "need_type": ["sleepy"],
            "recovery": {"health": 20, "mood": 15},
            "required_needs":["sleepy"]
        },
        "toy": {
            "rect": (315, 150, 45, 110),
            "cat_pos": (327.5, 202),
            "action": "play",
            "need_type": ["play"],
            "recovery": {"mood": 25},
            "required_needs":["play"]
        },
        "water_bowl": {
            "rect": (230, 295, 30, 25),
            "cat_pos": (245, 307.5),
            "action": "thirsty",
            "need_type": ["thirsty"],
            "recovery": {"health": 15},
            "required_needs":["thirsty"]
        },
        "food_bowl": {
            "rect": (180, 300, 30, 30),
            "cat_pos": (195, 315),
            "action": "hungry",
            "need_type": ["hungry"],
            "recovery": {"health": 25},
            "required_needs":["hungry"]
        }
    }

class TextConfig:
    """文本配置 - 游戏中所有文本统一管理"""
    # 窗口名称
    WINDOW_TITLE = "ELECTRIC_PAT"

    #UI标签文本
    HEALTH_LABEL = "Health"
    MOOD_LABEL = "Mood"

    #需求文本
    NEED_TEXTS = {
        "hungry": "Hungry!",
        "thirsty":"Thirsty!",
        "play": "We play!",
        "sleepy": "Sleep!",
        "touch":"Touch me!"
    }

    #无需求提示文本
    NO_NEED_TEXTS = {
        "food_bowl":"I'm not hungry!",
        "water_bowl":"I'm not thirsty!",
        "toy":"I'm not boring!",
        "bed":"I'm not sleepy!"
    }

    #存档系统文本
    SAVE_SUCCESS = "Game Saved!"
    LOAD_SUCCESS = "Game Loaded!"
    SAVE_FAILED = "Save Failed!"
    LOAD_FAILED = "Load Failed!"
    NO_SAVE_FILE = "No save file found!"
    AUTO_SAVE_TEXT = "Auto saving..."

class AnimationConfig:
    """动画配置 - 所有动画文件的信息"""
    ANIMATION ={
        "normal": {"folder":"normal_cat","prefix":"cat_","count":10},
        #加载动画
        "loading":{"folder":"loading","prefix":"load_frame_","count":12},

        #需求动画
        "hungry": {"folder": "hungry_cat", "prefix": "hry_cat_", "count": 8},
        "play": {"folder": "play_cat", "prefix": "ply_cat_", "count": 12},
        "sleepy": {"folder": "sleepy_cat", "prefix": "slpy_cat_", "count": 9},
        "touch":{"folder":"touched_cat","prefix":"tch_cat_","count":12},

        #执行动画
        "eating":{"folder":"hungry_cat","prefix":"eat_rect_","count":15},
        "playing": {"folder": "play_cat", "prefix": "ply_rect_", "count": 4},
        "sleeping": {"folder": "sleepy_cat", "prefix": "slpy_rect_", "count": 4},
        "touched":{"folder":"touched_cat","prefix":"tch_rect_","count":12}
    }

class GameTime:
    """游戏时间管理系统"""
    def __init__(self):
        self.current_hour = GameConfig.GAME_START_HOUR
        self.frame_counter = 0
        self.time_speed_multiplier = 1 # 时间流逝速度倍数
        self.is_sleeping = False

    def update(self):
        """游戏更新时间"""
        self.frame_counter += self.time_speed_multiplier
        frames_per_hour = GameConfig.GAME_HOUR_DURATION * GameConfig.FPS

        if self.frame_counter >= frames_per_hour:
            self.frame_counter = 0
            self.current_hour = (self.current_hour + 1 ) % 24
            print(f"时间更新:{self.get_time_string()}")

    def is_daytime(self):
        return GameConfig.DAY_START_HOUR <= self.current_hour < GameConfig.NIGHT_START_HOUR
    def is_nighttime(self):
        return not self.is_daytime()
    def is_late_night(self):
        return self.current_hour >= 22 or self.current_hour < 6

    def get_time_string(self):
        """获取时间字符串提示"""
        period = "AM" if self.current_hour < 12 else "PM"
        display_hour = self.current_hour % 12 or 12
        return f"{display_hour:02d}:00 {period}"

    def start_sleeping(self):
        """开始睡觉，加速时间流逝"""
        self.is_sleeping = True
        self.time_speed_multiplier = GameConfig.SLEEP_TIME_SPEED_MULTIPLIER
        print(f"开始睡觉，时间加上{self.time_speed_multiplier}倍")

    def stop_sleeping(self):
        """结束睡觉，恢复正常时间流逝"""
        self.is_sleeping = False
        self.time_speed_multiplier = 1
        print(f"🌞 睡醒了，时间恢复正常速度")

    def get_sleep_hours_passed(self,star_hour):
        """计算睡眠时长"""
        if self.current_hour >= star_hour:
            return self.current_hour - star_hour
        else:
            return  (24 - star_hour) + self.current_hour

class ResourceManager:
    """资源管理器 - 负责加载和管理所有游戏资源"""
    @staticmethod
    def load_loading_animation():
        print("🔄 开始加载loading动画...")
        loading_frames = ResourceManager.load_png_frames(
            "loading","load_frame_",
            GameConfig.LOADING_FRAME_COUNT,GameConfig.LOADING_CAT_SIZE
        )
        if loading_frames:
            print(f"✅ Loading动画加载成功：{len(loading_frames)}帧")
            return loading_frames
        else:
            print("❌ Loading动画加载失败")
            return []

    @staticmethod
    def load_png_frames(folder,prefix,frame_count,target_size):
        """安全地加载PNG动画帧序列，带错误的处理"""
        frames = []
        print(f"🔄 加载动画：{folder}")
        for i in range(1,frame_count + 1):
            filename = f"{prefix}{i:02d}.png"
            path = os.path.join(folder, filename)
            try:
                #加载图片
                img = pygame.image.load(path).convert_alpha()
                #等比例缩放
                orig_w, orig_h = img.get_size()
                scale = min(target_size / orig_w, target_size / orig_h) #选择最小缩放比
                new_size = (int(orig_w * scale),int(orig_h * scale))
                frame_image = pygame.transform.scale(img,new_size) #把一张图放大或缩小成你指定的尺寸，返回一个新的 Surface 对象。
                frames.append(frame_image)
            except pygame.error as e:
                print(f"❌ 无法加载{path}:{e}")
            except FileNotFoundError:
                print(f"❌ 文件不存在:{path}")
        print(f"✅ 成功加载{len(frames)}帧动画")
        return frames

    @staticmethod
    def load_all_animations():
        """加载所有动画，为主场景和房间分别加载不同大小"""
        animations = {"main":{},"room":{}}
        print("开始加载所有动画")

        for status,config in AnimationConfig.ANIMATION.items():
            main_frames = ResourceManager.load_png_frames(
                config["folder"],
                config["prefix"],
                config["count"],
                GameConfig.CAT_TARGET_SIZE
            )

            #房间加载小尺寸猫
            room_frames = ResourceManager.load_png_frames(
                config["folder"],
                config["prefix"],
                config["count"],
                GameConfig.CAT_ROOM_SIZE
            )

            if main_frames and room_frames:
                animations["main"][status]= main_frames #加载到动画，存进字典
                animations["room"][status]= room_frames
                print(f"{status}动画加载成功 - 主场景：{len(main_frames)}帧,房间：{len(room_frames)}")
            else:
                print(f"{status}动画加载失败，将使用默认动画")

        #确保至少有normal动画，否则游戏无法运行
        if ("normal" not in animations["main"] or not animations["main"]["normal"] or
                "normal" not in animations["room"] or not animations["room"]["normal"]):
            print("关键错误：无法加载normal动画，游戏无法启动")
            return None

        #用normal动画作为所有失败动画的备用
        for scene_type in ["main", "room"]:
            for status in AnimationConfig.ANIMATION.keys():
                if status not in animations[scene_type]:
                    animations[scene_type][status] = animations[scene_type]["normal"]
                    print(f"{status}使用normal 动画作为备用")

        print("所有动画加载完成！")
        return animations

    @staticmethod
    def load_ui_images():
        """加载所有UI相关图片"""
        print("开始加载UI图片...")

        ui_images = {}

        #需要加载的图片列表
        image_files ={
            "main_background": "main_background.jpg",
            "room_background": "room_background.png",  # 房间背景图
            "cloud": "cloud.png",
            "right_button": "right_arrow.png",  # 你的右箭头图片
            "left_button": "left_arrow.png"
        }

        for name,filename in image_files.items():
            try:
                img = pygame.image.load(filename).convert_alpha()
                #处理不同类型的图片
                if name == "main_background":
                    img = pygame.transform.scale(img,GameConfig.MAIN_WINDOW_SIZE)
                elif name == "room_background":
                    img = pygame.transform.scale(img,GameConfig.ROOM_WINDOW_SIZE)
                elif "button" in name:
                    img = pygame.transform.scale(img,GameConfig.BUTTON_SIZE)

                ui_images[name] = img
                print(f"加载图片{filename}")
            except pygame.error as e:
                print(f"无法加载图片{filename}:{e}")
                return None
            except FileNotFoundError:
                print(f"图片不存在{filename}")
                return None

        print("所有UI图片加载完成！")
        return ui_images

class SaveManager:
    @staticmethod
    def save_game_data(cat_state, game_time, play_time=0, slot=0):
        """保存游戏数据到指定槽位"""
        try:
            # 确保Save文件夹存在
            save_dir = "Save"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                print(f"📁 创建存档文件夹: {save_dir}")
            #构建存档数据
            save_data ={
                "version":"1.0",
                "player_name":"player",
                "play_time":play_time,
                "cat_health":cat_state.health,
                "cat_mood":cat_state.mood,
                "game_hour":game_time.current_hour,
                "last_sleep_hour":cat_state.last_sleep_hour,
                "satisfied_needs_history": cat_state.satisfied_needs.copy(),
                "created_time": time.time(),
                "last_saved_time": time.time(),
                "slot": slot
            }
            #生成文件名
            if slot == 0:
                filename = os.path.join(save_dir, GameConfig.SAVE_FILE_NAME)
            else:
                filename = f"electric_pat_save_slot{slot}.json"

            #保存到文件
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            print(f"✅ 游戏已保存到槽位 {slot}")
            return True
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False

    @staticmethod
    def load_game_data(slot=0):
        """从指定槽位加载游戏数据"""
        try:
            save_dir = "Save"
            # 生成文件名
            if slot == 0:
                filename = os.path.join(save_dir, GameConfig.SAVE_FILE_NAME)
            else:
                filename = os.path.join(save_dir, f"electric_pat_save_slot{slot}.json")

            # 读取文件
            with open(filename, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            print(f"✅ 从槽位 {slot} 加载游戏数据")
            return save_data

        except FileNotFoundError:
            print(f"❌ 槽位 {slot} 没有存档文件")
            return None
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return None

    @staticmethod
    def has_save_file(slot=0):
        """检查指定槽位是否有存档"""
        save_dir = "Save"
        if slot == 0:
            filename = os.path.join(save_dir, GameConfig.SAVE_FILE_NAME)
        else:
            filename = os.path.join(save_dir, f"electric_pat_save_slot{slot}.json")
        return os.path.exists(filename)

    @staticmethod
    def get_save_info(slot=0):
        """获取存档信息（用于显示存档列表）"""
        save_data = SaveManager.load_game_data(slot)
        if save_data:
            return {
                "slot": slot,
                "player_name": save_data.get("player_name", "Player"),
                "play_time": save_data.get("play_time", 0),
                "game_hour": save_data.get("game_hour", 8),
                "cat_health": save_data.get("cat_health", 100),
                "cat_mood": save_data.get("cat_mood", 100),
                "last_saved": save_data.get("last_saved_time", 0)
            }
        return None

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
        #根据配置的速度切换动画帧
        if self.animation_timer >= GameConfig.LOADING_ANIMATION_SPEED:
            self.animation_timer = 0
            if self.loading_frames:
                self.frame_index = (self.frame_index + 1) % len(self.loading_frames)

    def get_current_frame(self):
        """获取当前动画帧"""
        if self.loading_frames and len(self.loading_frames) > 0:
            return self.loading_frames[self.frame_index]
        return None

class GameScene:
    """游戏场景管理器"""
    def __init__(self):
        self.current_scene = "loading"
        self.target_scene = "loading"
        self.window = None
        self.transition_timer = 0
        self.is_transitioning = False
        self.create_window()

    def start_transition_to_main(self):
        """开始过渡到主界面"""
        self.target_scene = "main"
        self.is_transitioning = True
        self.transition_timer = GameConfig.TRANSITION_DURATION
        print("🎬 开始场景过渡动画...")

    def update_transition(self):
        """更新过渡状态"""
        if self.is_transitioning and self.transition_timer > 0:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                # 过渡完成，真正切换场景
                self.current_scene = self.target_scene
                self.create_window()
                self.is_transitioning = False
                print("✨ 场景过渡完成！")

    def get_transition_alpha(self):
        """获取过渡透明度"""
        if not self.is_transitioning:
            return 255
        # 创建淡出效果
        progress = self.transition_timer / GameConfig.TRANSITION_DURATION
        return int(255 * progress)

    def create_window(self):
        """根据当前场景创建窗口"""
        if self.current_scene == "loading":
            size = GameConfig.LOADING_WINDOW_SIZE
        elif self.current_scene == "main":
            size = GameConfig.MAIN_WINDOW_SIZE
        else:
            size = GameConfig.ROOM_WINDOW_SIZE

        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption(TextConfig.WINDOW_TITLE)

    def switch_to_main(self):
        self.current_scene = "main"
        self.create_window()

    def switch_to_room(self):
        self.current_scene = "room"
        self.create_window()

    def is_loading_scene(self):
        return self.current_scene == "loading"

    def is_main_scene(self):
        return self.current_scene == "main"

    def is_room_scene(self):
        return self.current_scene == "room"

class TouchSystem:
    """抚摸管理系统"""
    def __init__(self):
        self.is_touching = False
        self.last_mouse_x = None
        self.movement_count = 0
        self.touch_progress = 0
        self.last_direction = 0
        self.not_touching_timer = 0  # 松开鼠标后的计时器

    def start_touch(self,mouse_x):
        """开始抚摸"""
        self.is_touching = True
        self.last_mouse_x = mouse_x
        self.last_direction = 0
        self.not_touching_timer = 0
        print(f"开始抚摸，当前进度：{self.touch_progress:.1f}%")
        print(f"开始抚摸，is_touching = {self.is_touching}")

    def stop_touch(self):
        """停止抚摸"""
        self.is_touching = False
        self.last_mouse_x = None
        print(f"暂停抚摸，进度保留在：{self.touch_progress:.1f}%")

    def update(self,mouse_x, cat_state):
        """更新抚摸状态"""
        # 如果已经满足（100%）且正在播放动画，不再更新
        if self.touch_progress >= 100 and (cat_state.current_action == "touch" or cat_state.is_being_touched):
            return False
        if self.touch_progress >= 100:
            return True

        if not self.is_touching:
            self.not_touching_timer += 1

            #超越延迟时间才开始掉进度
            if self.not_touching_timer > GameConfig.TOUCH_PROGRESS_LOSS_DELAY:
                self.touch_progress = max(0,self.touch_progress - GameConfig.TOUCH_PROGRESS_DECAY * 2)
            return False

        if self.last_mouse_x is None:
            return False

        #计算移动距离
        movement = mouse_x - self.last_mouse_x
        #检测方向变化(左右摇摆）
        if abs(movement) > GameConfig.TOUCH_MIN_MOVEMENT:
            current_direction = 1 if movement> 0 else -1

            #如果方向改变，记为一次有效摇动
            if current_direction != self.last_direction and self.last_direction != 0:
                self.movement_count += 1
                self.touch_progress = min(100, self.touch_progress + (100 / GameConfig.TOUCH_SATISFACTION_THRESHOLD))
                print(f"摇动次数：{self.movement_count}, 进度：{self.touch_progress:.1f}%")

            self.last_direction = current_direction
            self.last_mouse_x = mouse_x
        #进度衰减
        if self.touch_progress < 100:
            self.touch_progress = max(0, self.touch_progress - GameConfig.TOUCH_PROGRESS_DECAY)
        #检查是否满足需求
        return self.touch_progress >= 100

    def reset(self):
        """重置抚摸系统（满足需求后调用）"""
        self.touch_progress = 0
        self.movement_count = 0
        self.not_touching_timer = 0
        print("抚摸需求已满足，进度重置")

class CatState:
    """猫咪状态管理"""
    ANIMATION_STATES = ["hungry", "play", "sleepy","touch"]
    def __init__(self,game_time):
        #位置系统
        self.main_x = GameConfig.CAT_DEFAULT_X
        self.main_y = GameConfig.CAT_DEFAULT_Y
        self.room_x = 205
        self.room_y = 255
        self.default_room_x = 205
        self.default_room_y = 255
        self.target_x = self.room_x
        self.target_y = self.room_y

        #动画
        self.frame_index = 0
        self.status = "normal"
        self.temp_status = None

        #状态值
        self.health = 100
        self.mood = 100
        self.decay_timer = 0 #控制掉状态频率
        #需求系统
        self.current_needs = []    #当前唯一的活跃需求
        self.need_cooldowns = {}      #检查冷却计时器
        self.need_generation_timer = 0   #检查新需求的计时器
        self.satisfied_needs = []   #最近满足的需求

        #时间系统
        self.game_time = game_time
        self.last_sleep_hour = None
        self.awake_hours = 0
        self.sleep_start_hour = None

        #交互系统
        self.is_moving = False
        self.current_action = None
        self.action_timer = 0      #动作持续的时间
        self.move_speed = GameConfig.CAT_MOVE_SPEED
        #待执行的恢复数据
        self.pending_action_type = None
        self.pending_recovery =None

        #无需求提示系统
        self.no_need_message = None
        self.no_need_timer = 0

        #抚摸系统
        self.touch_system = TouchSystem()
        self.is_being_touched = False

        #存档属性
        self.play_time = 0  # 游戏总时长（秒）
        self.auto_save_timer = 0  # 自动存档计时器
        self.last_save_message = None  # 保存消息
        self.save_message_timer = 0  # 保存消息显示时间

    def update_play_time(self):
        """更新游戏时长"""
        self.play_time += 1 / GameConfig.FPS  # 每帧增加对应的秒数

    def auto_save_check(self, game_time):
        """检查是否需要自动存档"""
        self.auto_save_timer += 1
        if self.auto_save_timer >= GameConfig.AUTO_SAVE_INTERVAL:
            self.auto_save_timer = 0
            if SaveManager.save_game_data(self, game_time, self.play_time):
                self.show_save_message(TextConfig.AUTO_SAVE_TEXT)
                return True
        return False

    def save_game(self, game_time, slot=0):
        """手动保存游戏"""
        if SaveManager.save_game_data(self, game_time, self.play_time, slot):
            self.show_save_message(TextConfig.SAVE_SUCCESS)
            return True
        else:
            self.show_save_message(TextConfig.SAVE_FAILED)
            return False

    def load_game(self, game_time, slot=0):
        """加载游戏"""
        save_data = SaveManager.load_game_data(slot)
        if save_data:
            # 恢复数据
            self.health = save_data.get("cat_health", 100)
            self.mood = save_data.get("cat_mood", 100)
            self.last_sleep_hour = save_data.get("last_sleep_hour")
            self.satisfied_needs = save_data.get("satisfied_needs_history", [])
            self.play_time = save_data.get("play_time", 0)

            # 恢复时间
            game_time.current_hour = save_data.get("game_hour", 8)

            self.show_save_message(TextConfig.LOAD_SUCCESS)
            print(f"🎮 游戏加载完成 - 游戏时长: {self.play_time:.1f}秒")
            return True
        else:
            self.show_save_message(TextConfig.LOAD_FAILED)
            return False

    def show_save_message(self, message):
        """显示存档消息"""
        self.last_save_message = message
        self.save_message_timer = 90  # 显示1.5秒
        print(f"💾 {message}")

    def update_save_message(self):
        """更新存档消息显示"""
        if self.save_message_timer > 0:
            self.save_message_timer -= 1
            if self.save_message_timer <= 0:
                self.last_save_message = None

    def check_need_condition(self,need_type):
        """检查某个需求类型是否满足生成条件"""
        conditions = GameConfig.NEED_THRESHOLDS.get(need_type,{})
        #特殊条件处理
        if conditions.get("special"):
            if need_type == "sleepy":
                return self.should_add_sleepy_need()
            return False
        #通用条件检查
        if "health" in conditions and self.health >= conditions["health"]:
            return False
        if "mood" in conditions and self.mood >= conditions["mood"]:
            return False
        return True

    def should_add_sleepy_need(self):
        """判断是否应该困倦"""
        if self.last_sleep_hour is not None:
            hours_since_sleep = self.game_time.get_sleep_hours_passed(self.last_sleep_hour)
            if hours_since_sleep < 6:
                return False

        self.update_awake_hours()
        #深夜必困
        if self.game_time.is_late_night():
            return True
        elif self.game_time.is_nighttime() and self.awake_hours > 8:
            return True
        elif self.awake_hours > GameConfig.HOURS_AWAKE_THRESHOLD:
            return True
        return False

    def update_awake_hours(self):
        """清醒时间"""
        if self.last_sleep_hour is None:
            self.awake_hours = 4
        else:
            self.awake_hours = self.game_time.get_sleep_hours_passed(self.last_sleep_hour)

    def generate_new_need(self):
        """生成新需求"""
        #如果已达到最大需求数，不生成
        if len(self.current_needs) >= GameConfig.MAX_CONCURRENT_NEEDS:
            return None
        # 收集可用的需求类型
        available_needs = []
        # 根据权重随机选择需求
        weighted_needs =[]

        for need_type, base_weight in GameConfig.NEED_WEIGHTS.items():
            #检查冷却
            if self.need_cooldowns.get(need_type,0) > 0:
                continue
            #检查是否已经在当前需求中
            if need_type in self.current_needs:
                continue
            #检查生成条件
            if not self.check_need_condition(need_type):
                continue

            #动态调整权重
            weight = base_weight
            if need_type == "hungry" and self.health <50:
                weight *= 2 #健康值很低时饥饿权重翻倍
            elif need_type == "thirsty" and self.health <40:
                weight *= 1.5
            elif need_type == "touch" and self.mood < 40:
                weight *= 2
            elif need_type == "play" and self.mood < 50:
                weight *= 1.5
            elif need_type == "sleepy":
                #根据时间段调整睡觉需求权重
                if self.game_time.is_late_night():
                    weight *= GameConfig.SLEEPY_LATE_NIGHT_MULTIPLIER
                elif self.game_time.is_nighttime():
                    weight *= GameConfig.SLEEPY_NIGHT_MULTIPLIER

            weighted_needs.extend([need_type] * int(weight))

        #随机选择一个需求
        if weighted_needs:
            selected = random.choice(weighted_needs)
            self.current_needs.append(selected)
            print(f"选择新需求：{selected}(当前需求数：{len(self.current_needs)}/{ GameConfig.MAX_CONCURRENT_NEEDS})")
            return selected
        return None

    def update_need_system(self):
        """更新需求系统 - 核心逻辑"""
        #更新所有冷却时间
        for need_type in list(self.need_cooldowns.keys()):
            self.need_cooldowns[need_type] -= 1
            if self.need_cooldowns[need_type] <= 0:
                del self.need_cooldowns[need_type]
        #更新需求生成计时器
        self.need_generation_timer += 1

        #定期尝试生成新需求
        if self.need_generation_timer >= GameConfig.NEED_GENERATION_INTERVAL:
            self.need_generation_timer = 0
            #如果需求值未满，尝试生成
            if (len(self.current_needs) < GameConfig.MAX_CONCURRENT_NEEDS and
                    not self.current_action and not self.is_moving and not self.is_being_touched):
                self.generate_new_need()

    def satisfy_need(self,need_type):
        """满足需求"""
        if need_type == "sleepy":
            #处理睡觉需求
            self.last_sleep_hour = self.game_time.current_hour
            self.awake_hours = 0
            print(f"💤 猫咪在 {self.game_time.get_time_string()} 睡觉了")

        #从当前需求中移除
        if need_type in self.current_needs:
            self.current_needs.remove(need_type)
            print(f"✅ 满足需求：{need_type} (剩余需求：{self.current_needs})")

            #记录满足的需求
            self.satisfied_needs.append(need_type)
            if len(self.satisfied_needs) > 5:
                self.satisfied_needs.pop(0)

            #设置冷却时间
            self.need_cooldowns[need_type] = GameConfig.NEED_COOLDOWN_TIME

    def move_to_target(self,target_x,target_y):
        """移动目标位置"""
        self.target_x = target_x
        self.target_y = target_y
        self.is_moving = True

    def get_current_position(self,scene):
        """根据当前场景获取猫咪位置"""
        if scene.is_main_scene():
            return self.main_x, self.main_y
        else:
            return self.room_x, self.room_y

    def show_no_need_message(self,zone_name):
        """显示无需求消息"""
        self.no_need_message = TextConfig.NO_NEED_TEXTS.get(zone_name,"I don't need this!")
        self.no_need_timer = GameConfig.NO_NEED_MESSAGE_FRAMES
        print(f"猫咪说：{self.no_need_message}")

    def update_position(self):
        """更新猫咪位置"""
        if not self.is_moving:
            return
        dx = self.target_x - self.room_x
        dy = self.target_y - self.room_y
        distance = math.sqrt(dx*dx + dy*dy)

        if distance < self.move_speed:
            #到达目标位置
            self.room_x = self.target_x
            self.room_y = self.target_y
            self.is_moving = False

            #开始执行动作
            if self.pending_action_type:
                action_to_animation = {
                    "hungry": "eating",
                    "thirsty": "eating",
                    "play": "playing",
                    "sleepy": "sleeping"
                }
                self.status = action_to_animation.get(self.pending_action_type,"normal")
                if self.pending_action_type == "sleepy":
                    self.sleep_start_hour = self.game_time.current_hour
                    self.game_time.start_sleeping()

                #开始动作计时器
                self.current_action = self.pending_action_type
                self.action_timer = 120
                self.pending_action_type = None
                print(f"达到目标，开始执行动作：{self.current_action}")
        else:
            #继续移动
            self.room_x += (dx / distance) * self.move_speed #每次走一小段
            self.room_y += (dy / distance) * self.move_speed

    def update_stats_decay(self):
        """更新状态值衰减"""
        if self.current_action:
            return  #执行动作时不掉血
        self.decay_timer += 1
        if self.decay_timer >= GameConfig.DECAY_INTERVAL:
            self.decay_timer = 0

            #健康值和心情值持续下降
            self.health = max(0, self.health -GameConfig.HEALTH_DECAY_RATE)
            self.mood = max(0, self.mood - GameConfig.MOOD_DECAY_RATE)
            # 有需求时掉得更快
            if self.current_needs:
                extra_decay = len(self.current_needs) * 0.1  # 每个需求额外0.1
                self.health = max(0, self.health - extra_decay)
                self.mood = max(0, self.mood - extra_decay)

    def handle_touch_satisfaction(self):
        """处理抚摸满足"""
        # 恢复数值
        self.health = min(100, self.health + GameConfig.TOUCH_HEALTH_RECOVERY)
        self.mood = min(100, self.mood + GameConfig.TOUCH_MOOD_RECOVERY)

        #播放满足后的动画
        self.status = "touched"
        self.current_action = "touch"
        self.action_timer = 30
        self.is_being_touched = True

        #调用satisfy_need来移除touch需求
        self.satisfy_need("touch")

        #重置抚摸系统
        self.touch_system.reset()
        print(f"😊 抚摸完成！Health+{GameConfig.TOUCH_HEALTH_RECOVERY}, Mood+{GameConfig.TOUCH_MOOD_RECOVERY}")

    def get_current_status_for_animation(self):
        """获取当前应该播放的动画状态"""
        # 调试信息
        if self.temp_status == "touch":
            print(f"返回抚摸动画：{self.temp_status}")

        #如果有临时状态，优先显示
        if self.temp_status:
            return self.temp_status

        # 如果正在执行动作或移动，保持当前状态
        if self.current_action or self.is_moving or self.is_being_touched:
            return self.status

        # 如果有需求，显示与云朵同步的需求动画
        if self.current_needs:
            # 修复：与云朵显示逻辑保持一致，轮流显示不同需求的动画
            display_index = (self.frame_index // 20) % len(self.current_needs)
            need = self.current_needs[display_index]
            if need in self.ANIMATION_STATES:
                return need

        return "normal"

    def update(self,cat_animation,scene):
        """更新所有状态，统一管理 - 每帧都会调用"""
        self.update_stats_decay() #持续的状态值衰减

        #重置临时状态
        self.temp_status = None
        #每帧都检查抚摸状态
        if scene.is_main_scene() and "touch" in self.current_needs:
            if self.touch_system.is_touching:
                self.temp_status = "touch"
                print(f"设置抚摸动画：temp_status = touch")

        #只有在room里处理移动和交互
        if scene.is_room_scene():
            self.update_position()
            #处理动作完成
            if self.current_action and self.action_timer > 0:
                self.action_timer -= 1
                #检查睡眠时长
                if self.current_action == "sleepy" and self.game_time.is_sleeping:
                    sleep_hours = self.game_time.get_sleep_hours_passed(self.sleep_start_hour)
                    if sleep_hours >= GameConfig.SLEEP_DURATION_HOURS:
                        self.action_timer = 0
                        print(f"睡够{sleep_hours}小时了，该起床了!")

                if self.action_timer <= 0:
                    #动作完成时恢复数值
                    if self.pending_recovery:
                        recovery= self.pending_recovery
                        self.health = min(100,self.health + recovery.get("health",0))
                        self.mood = min(100,self.mood + recovery.get("mood",0))

                        # 睡觉额外恢复
                        if self.current_action == "sleepy":
                            sleep_hours = self.game_time.get_sleep_hours_passed(self.sleep_start_hour)
                            extra_health = min(sleep_hours * 5, 30)  # 每小时额外恢复5点，最多30点
                            extra_mood = min(sleep_hours * 3, 20)  # 每小时额外恢复3点，最多20点
                            self.health = min(100, self.health + extra_health)
                            self.mood = min(100, self.mood + extra_mood)
                            self.game_time.stop_sleeping()  # 停止时间加速
                            print(f"😊 睡了{sleep_hours}小时，额外恢复 Health+{extra_health}, Mood+{extra_mood}")

                        self.pending_recovery = None
                    #处理抚摸动作结束
                    if self.current_action is not None:
                        #非touch动作才调用satisfy_need
                        if self.current_action != "touch":
                            self.satisfy_need(self.current_action)
                        if self.current_action == "touch":
                            self.is_being_touched = False

                    self.current_action = None
                    self.status = "normal"
        #处理main中抚摸动作的完成
        elif scene.is_main_scene():
            if self.current_action == "touch" and self.action_timer > 0:
                self.action_timer -= 1
                if self.action_timer <=0:
                    self.current_action = None
                    self.status = "normal"
                    self.is_being_touched = False
        #将需求系统更新移到动作处理之后
        #这样确保在动作刚结束的帧不会立即生成新需求
        self.update_need_system()

        #更新无需求消息计时器
        if self.no_need_timer > 0:
            self.no_need_timer -= 1
            if self.no_need_timer <= 0:
                self.no_need_message = None

        #更新动画状态
        self.status = self.get_current_status_for_animation()

        #更新动画帧
        scene_type = "main" if scene.is_main_scene() else "room"
        current_frames = cat_animation[scene_type][self.status]
        self.frame_index = (self.frame_index + 1) % len(current_frames)

def handle_click(mouse_pos, cat_state, scene, ui_images):
    mouse_x, mouse_y = mouse_pos

    #主场景切换按钮
    if scene.is_main_scene():
        button_rect = pygame.Rect(
            GameConfig.RIGHT_BUTTON_X, GameConfig.BUTTON_Y, *GameConfig.BUTTON_SIZE)
        if button_rect.collidepoint(mouse_x,mouse_y):
            print("点击右键头，切换房间场景")
            scene.switch_to_room()
            return
    #房间场景：检查左箭头按钮
    else:
        button_rect = pygame.Rect(GameConfig.LEFT_BUTTON_X,GameConfig.BUTTON_Y - 50, *GameConfig.BUTTON_SIZE)
        if button_rect.collidepoint(mouse_x,mouse_y):
            print("点击左键头，切换主场景")
            scene.switch_to_main()
            return

        #如做动作时，忽略点击
        if cat_state.is_moving or cat_state.current_action:
            return

        #遍历所有交互区域
        for zone_name, zone_data in InteractionZones.ZONES.items():
            rect = zone_data["rect"] #拿出每个物品的区域矩形
            #判断你点的地方是否在这个区域里
            if(rect[0] <= mouse_x <= rect[0] + rect[2] and
               rect[1] <= mouse_y <= rect[1] + rect[3]):
                print(f"点击了{zone_name}")

                #检查需求匹配
                action = zone_data["action"]
                if action not in cat_state.current_needs: # 检查需求列表
                    #没有这个需求
                    message = TextConfig.NO_NEED_TEXTS.get(zone_name, "I don't need this!")
                    cat_state.no_need_message = message
                    cat_state.no_need_timer = GameConfig.NO_NEED_MESSAGE_FRAMES
                    print(f"猫咪说：{message}")
                    return

                #有需求，开始移动
                target_pos = zone_data["cat_pos"]
                cat_state.move_to_target(target_pos[0],target_pos[1])
                #保存待执行的动作数据
                cat_state.pending_action_type = action
                cat_state.pending_recovery = zone_data["recovery"]
                print(f"开始移动到 {zone_name}，准备执行 {zone_data['action']} 动作")
                return

def draw_cat(window,cat_animation,cat_state,scene):
    """绘制猫咪（位置由cat_status决定）"""
    # 根据场景选择对应的动画合集
    scene_type = "main" if scene.is_main_scene() else "room"
    frames = cat_animation[scene_type].get(cat_state.status,cat_animation[scene_type]["normal"])

    #确保动画状态存在
    if frames:
        current_frames = frames[cat_state.frame_index]
        cat_rect = current_frames.get_rect()
        x,y = cat_state.get_current_position(scene)
        window.blit(current_frames,(x - cat_rect.width // 2, y - cat_rect.height // 2))

def draw_loading_screen(window,loading_state,loading_timer):
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

def draw_progress_bar(window, value, prefix, pos):
    """进度条绘制函数"""
    #根据数值范围直接觉得用哪张照片
    percent = 100 if value >= 90 else 80 if value >= 70 else 50 if value >= 45 else 30 if value >= 25 else 15
    img_path = f"UI/{prefix}_{percent}.png"

    try:
        bar_img = pygame.image.load(img_path).convert_alpha()
        bar_img= pygame.transform.scale(bar_img, (70,15))
        window.blit(bar_img,pos)
    except Exception as e:
        print(f"进度条图片加载失败：{img_path},{e}")

def draw_fixed_ui(window, ui_images,cat_state,scene):
    """绘制UI界面"""
    #根据场景选择UI位置
    if scene.is_main_scene():
        bar_x = UILayout.MAIN_PROGRESS_BAR_X
        health_y = UILayout.MAIN_HEALTH_BAR_Y
        mood_y = UILayout.MAIN_MOOD_BAR_Y
    else:
        bar_x = UILayout.ROOM_PROGRESS_BAR_X
        health_y = UILayout.ROOM_HEALTH_BAR_Y
        mood_y = UILayout.ROOM_MOOD_BAR_Y

    draw_progress_bar(window,cat_state.health,"health_bar",(bar_x,health_y))
    draw_progress_bar(window,cat_state.mood,"mood_bar",(bar_x,mood_y))

    #创建字体对象
    font = pygame.font.SysFont(UILayout.FONT_NAME,UILayout.FONT_SIZE_UI,bold=True)
    window.blit(font.render(TextConfig.HEALTH_LABEL,True, UILayout.FONT_COLOR),
                (bar_x,health_y + UILayout.LABEL_OFFSET_Y))
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
    window.blit(font.render(status,True,color),
                (UILayout.TIME_DISPLAY_X, UILayout.TIME_DISPLAY_Y + 20))

def draw_buttons(window,ui_images,scene):
    """绘制按钮"""
    if scene.is_main_scene():
        window.blit(ui_images["right_button"], (GameConfig.RIGHT_BUTTON_X, GameConfig.BUTTON_Y))
    else:
        window.blit(ui_images["left_button"], (GameConfig.LEFT_BUTTON_X, GameConfig.BUTTON_Y - 50))

def draw_need_clouds(window,cloud_img,cat_state,scene,mode="all"):
    """绘制所有云朵"""
    #优先检查是否有无需求消息要显示
    if cat_state.no_need_message and cat_state.no_need_timer > 0:
        text = cat_state.no_need_message
        draw_single_cloud(window, cloud_img, text, cat_state, scene)
        return
    #显示所有活跃需求
    if not  cat_state.current_needs:
        return

    #简单实现：轮流显示不同的需求
    #可以根据帧数觉得显示哪个需求
    display_index = (cat_state.frame_index // 20) % len(cat_state.current_needs)
    need = cat_state.current_needs[display_index]
    text = TextConfig.NEED_TEXTS.get(need, "")
    #在需求文本后添加数量提示
    if len(cat_state.current_needs) > 1:
        text += f"({display_index + 1}/{len(cat_state.current_needs)})"
    draw_single_cloud(window, cloud_img, text, cat_state, scene)

def draw_single_cloud(window, cloud_img, text, cat_state, scene):
    """绘制单个云朵"""
    font = pygame.font.SysFont(UILayout.FONT_NAME,UILayout.FONT_SIZE_CLOUD,bold=True)
    text_surface = font.render(text,True,UILayout.FONT_COLOR)
    text_width = text_surface.get_width()

    #计算云朵大小
    cloud_width = max(GameConfig.CLOUD_MIN_WIDTH,
                      min(GameConfig.CLOUD_MAX_WIDTH,text_width + GameConfig.CLOUD_PADDING))
    x,y = cat_state.get_current_position(scene)
    screen_width = GameConfig.MAIN_WINDOW_SIZE[0] if scene.is_main_scene() else GameConfig.ROOM_WINDOW_SIZE[0]
    cloud_x = max(10, min(screen_width - cloud_width - 10, x - cloud_width // 2))
    cloud_y = y + GameConfig.CLOUD_OFFSET_Y

    #绘制云朵
    cloud_scaled = pygame.transform.smoothscale(cloud_img,(cloud_width,GameConfig.CLOUD_HEIGHT))
    window.blit(cloud_scaled,(cloud_x,cloud_y))

    #绘制文字
    text_x = cloud_x + (cloud_width - text_width) // 2
    text_y = cloud_y + (GameConfig.CLOUD_HEIGHT - text_surface.get_height()) // 2
    window.blit(text_surface,(text_x,text_y))

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

def draw_game_info(window, cat_state):
    """绘制游戏信息（时长等）"""
    if cat_state is None:
        return

    font = pygame.font.SysFont(UILayout.FONT_NAME, 12)

    #显示游戏时长
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

def main():
    """主循环,专注于游戏逻辑"""
    print("📦 加载游戏资源...")

    #初始化pygame
    pygame.init()

    #创建场景管理器
    scene = GameScene()

    # 创建加载状态管理器
    loading_state = LoadingState()

    # 先加载loading动画
    loading_frames = ResourceManager.load_loading_animation()
    loading_state.loading_frames = loading_frames

    # 游戏状态变量
    game_time = None
    cat_animation = None
    ui_images = None
    cat_state = None
    clock = pygame.time.Clock()
    running = True
    is_near_cat = False

    # 资源加载计数器
    loading_timer = 0

    #游戏主循环
    while running:
        if scene.is_loading_scene():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            loading_state.update()
            loading_timer += 1

            # 模拟加载过程并实际加载资源
            if loading_timer > 180:  # 3秒后开始加载资源
                if game_time is None:
                    print("🔄 加载游戏资源...")
                    game_time = GameTime()
                    cat_animation = ResourceManager.load_all_animations()
                    ui_images = ResourceManager.load_ui_images()

                    if cat_animation and ui_images:
                        cat_state = CatState(game_time)
                        loading_state.is_loading_complete = True
                        print("✅ 资源加载完成，开始过渡到主界面")
                        scene.start_transition_to_main()
                    else:
                        print("❌ 资源加载失败，游戏退出")
                        running = False

            draw_loading_screen(scene.window, loading_state, loading_timer)
            # 如果正在过渡，添加淡出效果
            if scene.is_transitioning:
                alpha = scene.get_transition_alpha()
                fade_surface = pygame.Surface(GameConfig.LOADING_WINDOW_SIZE)
                fade_surface.set_alpha(255 - alpha)
                fade_surface.fill((0, 0, 0))
                scene.window.blit(fade_surface, (0, 0))
        else:
            # 只有在cat_state存在时才处理游戏逻辑
            if cat_state is None:
                running = False
                break
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if cat_state:
                        cat_state.save_game(game_time, slot=0)
                        print("🎮 游戏退出前自动保存完成")
                    running = False
                elif event.type == pygame.KEYDOWN:  # 键盘事件处理
                    if event.key == pygame.K_F5:  # F5 快速保存
                        if cat_state:
                            cat_state.save_game(game_time, slot=0)
                    elif event.key == pygame.K_F9:  # F9 快速加载
                        if cat_state:
                            cat_state.load_game(game_time, slot=0)
                    elif event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):  # Ctrl+S 保存
                        if cat_state:
                            cat_state.save_game(game_time, slot=0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #左键按下
                        mouse_x,mouse_y = event.pos

                        #在主场景检查是否点击猫咪附近
                        if scene.is_main_scene():
                            cat_x ,cat_y = cat_state.get_current_position(scene)
                            distance = math.sqrt((mouse_x - cat_x) ** 2 + (mouse_y - cat_y) ** 2)
                            if (distance < GameConfig.TOUCH_DETECTION_RADIUS and
                                "touch" in cat_state.current_needs and
                                not cat_state.is_being_touched):
                                cat_state.touch_system.start_touch(mouse_x)
                            else:# 处理其他点击（如按钮）
                                handle_click(event.pos, cat_state,scene,ui_images)
                        else: # 房间场景的正常点击处理
                            handle_click(event.pos, cat_state, scene,ui_images)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if cat_state.touch_system.is_touching:
                            cat_state.touch_system.stop_touch()
                elif event.type == pygame.MOUSEMOTION:
                        mouse_x, mouse_y = event.pos

                        #检查鼠标是否在猫咪附近
                        if scene.is_main_scene() and "touch" in cat_state.current_needs:
                            cat_x, cat_y = cat_state.get_current_position(scene)
                            distance = math.sqrt((mouse_x - cat_x) ** 2 + (mouse_y - cat_y) ** 2)

                            # 根据距离改变鼠标光标
                            if distance < GameConfig.TOUCH_DETECTION_RADIUS:
                                if not is_near_cat:
                                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                                    is_near_cat = True
                            else:
                                if is_near_cat:
                                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                                    is_near_cat = False
                        else:
                            if is_near_cat:
                                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                                is_near_cat = False

                            # 鼠标移动时更新抚摸状态
                        if cat_state.touch_system.is_touching:
                            if cat_state.touch_system.update(mouse_x, cat_state):
                                # 抚摸满足
                                cat_state.handle_touch_satisfaction()
                                cat_state.touch_system.stop_touch()

            #更新游戏时间
            game_time.update()
            #更新游戏状态
            cat_state.update(cat_animation,scene)
            # 更新存档相关状态
            cat_state.update_play_time()
            cat_state.update_save_message()
            cat_state.auto_save_check(game_time)

            # 绘制游戏界面
            bg_name = "main_background" if scene.is_main_scene() else "room_background"
            scene.window.blit(ui_images[bg_name], (0, 0))

            draw_cat(scene.window, cat_animation, cat_state, scene)
            draw_fixed_ui(scene.window, ui_images, cat_state, scene)
            draw_buttons(scene.window, ui_images, scene)
            draw_time_display(scene.window, game_time)
            draw_need_clouds(scene.window, ui_images["cloud"], cat_state, scene)
            draw_game_info(scene.window, cat_state)  # 游戏时长和提示
            draw_save_message(scene.window, cat_state)  # 存档消息

        # 更新场景过渡
        scene.update_transition()
        #更新显示
        pygame.display.flip()
        clock.tick(GameConfig.FPS)

    pygame.quit()
    print("游戏结束，感谢游玩")

if __name__ == "__main__":
    main()