# src/core/cat_state.py
"""猫咪状态管理"""

import random
import math
from src.config.game_config import GameConfig
from src.config.text_config import TextConfig
from src.systems.touch_system import TouchSystem
from src.systems.save_manager import SaveManager


class CatState:
    """猫咪状态管理"""
    ANIMATION_STATES = ["hungry", "play", "sleepy", "touch"]

    def __init__(self, game_time):
        # 位置系统
        self.main_x = GameConfig.CAT_DEFAULT_X
        self.main_y = GameConfig.CAT_DEFAULT_Y
        self.room_x = 205
        self.room_y = 255
        self.default_room_x = 205
        self.default_room_y = 255
        self.target_x = self.room_x
        self.target_y = self.room_y

        # 动画
        self.frame_index = 0
        self.status = "normal"
        self.temp_status = None

        # 状态值
        self.health = 100
        self.mood = 100
        self.decay_timer = 0  # 控制掉状态频率

        # 需求系统
        self.current_needs = []  # 当前活跃需求
        self.need_cooldowns = {}  # 检查冷却计时器
        self.need_generation_timer = 0  # 检查新需求的计时器
        self.satisfied_needs = []  # 最近满足的需求

        # 时间系统
        self.game_time = game_time
        self.last_sleep_hour = None
        self.awake_hours = 0
        self.sleep_start_hour = None

        # 交互系统
        self.is_moving = False
        self.current_action = None
        self.action_timer = 0  # 动作持续的时间
        self.move_speed = GameConfig.CAT_MOVE_SPEED
        # 待执行的恢复数据
        self.pending_action_type = None
        self.pending_recovery = None

        # 无需求提示系统
        self.no_need_message = None
        self.no_need_timer = 0

        # 抚摸系统
        self.touch_system = TouchSystem()
        self.is_being_touched = False

        # 存档属性
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

    def check_need_condition(self, need_type):
        """检查某个需求类型是否满足生成条件"""
        conditions = GameConfig.NEED_THRESHOLDS.get(need_type, {})
        # 特殊条件处理
        if conditions.get("special"):
            if need_type == "sleepy":
                return self.should_add_sleepy_need()
            return False
        # 通用条件检查
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
        # 深夜必困
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
        # 如果已达到最大需求数，不生成
        if len(self.current_needs) >= GameConfig.MAX_CONCURRENT_NEEDS:
            return None

        # 根据权重随机选择需求
        weighted_needs = []

        for need_type, base_weight in GameConfig.NEED_WEIGHTS.items():
            # 检查冷却
            if self.need_cooldowns.get(need_type, 0) > 0:
                continue
            # 检查是否已经在当前需求中
            if need_type in self.current_needs:
                continue
            # 检查生成条件
            if not self.check_need_condition(need_type):
                continue

            # 动态调整权重
            weight = base_weight
            if need_type == "hungry" and self.health < 50:
                weight *= 2  # 健康值很低时饥饿权重翻倍
            elif need_type == "thirsty" and self.health < 40:
                weight *= 1.5
            elif need_type == "touch" and self.mood < 40:
                weight *= 2
            elif need_type == "play" and self.mood < 50:
                weight *= 1.5
            elif need_type == "sleepy":
                # 根据时间段调整睡觉需求权重
                if self.game_time.is_late_night():
                    weight *= GameConfig.SLEEPY_LATE_NIGHT_MULTIPLIER
                elif self.game_time.is_nighttime():
                    weight *= GameConfig.SLEEPY_NIGHT_MULTIPLIER

            weighted_needs.extend([need_type] * int(weight))

        # 随机选择一个需求
        if weighted_needs:
            selected = random.choice(weighted_needs)
            self.current_needs.append(selected)
            print(f"选择新需求：{selected}(当前需求数：{len(self.current_needs)}/{GameConfig.MAX_CONCURRENT_NEEDS})")
            return selected
        return None

    def update_need_system(self):
        """更新需求系统 - 核心逻辑"""
        # 更新所有冷却时间
        for need_type in list(self.need_cooldowns.keys()):
            self.need_cooldowns[need_type] -= 1
            if self.need_cooldowns[need_type] <= 0:
                del self.need_cooldowns[need_type]

        # 更新需求生成计时器
        self.need_generation_timer += 1

        # 定期尝试生成新需求
        if self.need_generation_timer >= GameConfig.NEED_GENERATION_INTERVAL:
            self.need_generation_timer = 0
            # 如果需求值未满，尝试生成
            if (len(self.current_needs) < GameConfig.MAX_CONCURRENT_NEEDS and
                    not self.current_action and not self.is_moving and not self.is_being_touched):
                self.generate_new_need()

    def satisfy_need(self, need_type):
        """满足需求"""
        if need_type == "sleepy":
            # 处理睡觉需求
            self.last_sleep_hour = self.game_time.current_hour
            self.awake_hours = 0
            print(f"💤 猫咪在 {self.game_time.get_time_string()} 睡觉了")

        # 从当前需求中移除
        if need_type in self.current_needs:
            self.current_needs.remove(need_type)
            print(f"✅ 满足需求：{need_type} (剩余需求：{self.current_needs})")

            # 记录满足的需求
            self.satisfied_needs.append(need_type)
            if len(self.satisfied_needs) > 5:
                self.satisfied_needs.pop(0)

            # 设置冷却时间
            self.need_cooldowns[need_type] = GameConfig.NEED_COOLDOWN_TIME

    def move_to_target(self, target_x, target_y):
        """移动到目标位置"""
        self.target_x = target_x
        self.target_y = target_y
        self.is_moving = True

    def get_current_position(self, scene):
        """根据当前场景获取猫咪位置"""
        if scene.is_main_scene():
            return self.main_x, self.main_y
        else:
            return self.room_x, self.room_y

    def show_no_need_message(self, zone_name):
        """显示无需求消息"""
        self.no_need_message = TextConfig.NO_NEED_TEXTS.get(zone_name, "I don't need this!")
        self.no_need_timer = GameConfig.NO_NEED_MESSAGE_FRAMES
        print(f"猫咪说：{self.no_need_message}")

    def update_position(self):
        """更新猫咪位置"""
        if not self.is_moving:
            return

        dx = self.target_x - self.room_x
        dy = self.target_y - self.room_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < self.move_speed:
            # 到达目标位置
            self.room_x = self.target_x
            self.room_y = self.target_y
            self.is_moving = False

            # 开始执行动作
            if self.pending_action_type:
                action_to_animation = {
                    "hungry": "eating",
                    "thirsty": "eating",
                    "play": "playing",
                    "sleepy": "sleeping"
                }
                self.status = action_to_animation.get(self.pending_action_type, "normal")
                if self.pending_action_type == "sleepy":
                    self.sleep_start_hour = self.game_time.current_hour
                    self.game_time.start_sleeping()

                # 开始动作计时器
                self.current_action = self.pending_action_type
                self.action_timer = 120
                self.pending_action_type = None
                print(f"达到目标，开始执行动作：{self.current_action}")
        else:
            # 继续移动
            self.room_x += (dx / distance) * self.move_speed
            self.room_y += (dy / distance) * self.move_speed

    def update_stats_decay(self):
        """更新状态值衰减"""
        if self.current_action:
            return  # 执行动作时不掉血

        self.decay_timer += 1
        if self.decay_timer >= GameConfig.DECAY_INTERVAL:
            self.decay_timer = 0

            # 健康值和心情值持续下降
            self.health = max(0, self.health - GameConfig.HEALTH_DECAY_RATE)
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

        # 播放满足后的动画
        self.status = "touched"
        self.current_action = "touch"
        self.action_timer = 30
        self.is_being_touched = True

        # 调用satisfy_need来移除touch需求
        self.satisfy_need("touch")

        # 重置抚摸系统
        self.touch_system.reset()
        print(f"😊 抚摸完成！Health+{GameConfig.TOUCH_HEALTH_RECOVERY}, Mood+{GameConfig.TOUCH_MOOD_RECOVERY}")

    def get_current_status_for_animation(self):
        """获取当前应该播放的动画状态"""
        # 如果有临时状态，优先显示
        if self.temp_status:
            return self.temp_status

        # 如果正在执行动作或移动，保持当前状态
        if self.current_action or self.is_moving or self.is_being_touched:
            return self.status

        # 如果有需求，显示与云朵同步的需求动画
        if self.current_needs:
            # 与云朵显示逻辑保持一致，轮流显示不同需求的动画
            display_index = (self.frame_index // 20) % len(self.current_needs)
            need = self.current_needs[display_index]
            if need in self.ANIMATION_STATES:
                return need

        return "normal"

    def update(self, cat_animation, scene):
        """更新所有状态，统一管理 - 每帧都会调用"""
        self.update_stats_decay()  # 持续的状态值衰减

        # 重置临时状态
        self.temp_status = None
        # 每帧都检查抚摸状态
        if scene.is_main_scene() and "touch" in self.current_needs:
            if self.touch_system.is_touching:
                self.temp_status = "touch"

        # 只有在room里处理移动和交互
        if scene.is_room_scene():
            self.update_position()
            # 处理动作完成
            if self.current_action and self.action_timer > 0:
                self.action_timer -= 1
                # 检查睡眠时长
                if self.current_action == "sleepy" and self.game_time.is_sleeping:
                    sleep_hours = self.game_time.get_sleep_hours_passed(self.sleep_start_hour)
                    if sleep_hours >= GameConfig.SLEEP_DURATION_HOURS:
                        self.action_timer = 0
                        print(f"睡够{sleep_hours}小时了，该起床了!")

                if self.action_timer <= 0:
                    # 动作完成时恢复数值
                    if self.pending_recovery:
                        recovery = self.pending_recovery
                        self.health = min(100, self.health + recovery.get("health", 0))
                        self.mood = min(100, self.mood + recovery.get("mood", 0))

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

                    # 处理抚摸动作结束
                    if self.current_action is not None:
                        # 非touch动作才调用satisfy_need
                        if self.current_action != "touch":
                            self.satisfy_need(self.current_action)
                        if self.current_action == "touch":
                            self.is_being_touched = False

                    self.current_action = None
                    self.status = "normal"

        # 处理main中抚摸动作的完成
        elif scene.is_main_scene():
            if self.current_action == "touch" and self.action_timer > 0:
                self.action_timer -= 1
                if self.action_timer <= 0:
                    self.current_action = None
                    self.status = "normal"
                    self.is_being_touched = False

        # 将需求系统更新移到动作处理之后
        self.update_need_system()

        # 更新无需求消息计时器
        if self.no_need_timer > 0:
            self.no_need_timer -= 1
            if self.no_need_timer <= 0:
                self.no_need_message = None

        # 更新动画状态
        self.status = self.get_current_status_for_animation()

        # 更新动画帧
        scene_type = "main" if scene.is_main_scene() else "room"
        current_frames = cat_animation[scene_type][self.status]
        self.frame_index = (self.frame_index + 1) % len(current_frames)
