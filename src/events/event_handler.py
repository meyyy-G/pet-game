# src/events/event_handler.py
"""事件处理器"""

import pygame
import math
from src.config.game_config import GameConfig
from src.config.text_config import TextConfig
from .interaction_zones import InteractionZones


class EventHandler:
    """游戏事件处理器"""

    def __init__(self):
        self.is_near_cat = False

    def handle_events(self, events, cat_state, scene, game_time):
        """处理所有游戏事件"""
        for event in events:
            if event.type == pygame.QUIT:
                if cat_state:
                    cat_state.save_game(game_time, slot=0)
                    print("🎮 游戏退出前自动保存完成")
                return False

            elif event.type == pygame.KEYDOWN:
                self._handle_keyboard_events(event, cat_state, game_time)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_button_down(event, cat_state, scene)

            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_button_up(event, cat_state)

            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event, cat_state, scene)

        return True

    def _handle_keyboard_events(self, event, cat_state, game_time):
        """处理键盘事件"""
        if event.key == pygame.K_F5:  # F5 快速保存
            if cat_state:
                cat_state.save_game(game_time, slot=0)
        elif event.key == pygame.K_F9:  # F9 快速加载
            if cat_state:
                cat_state.load_game(game_time, slot=0)
        elif event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):  # Ctrl+S 保存
            if cat_state:
                cat_state.save_game(game_time, slot=0)

    def _handle_mouse_button_down(self, event, cat_state, scene):
        """处理鼠标按下事件"""
        if event.button == 1:  # 左键按下
            mouse_x, mouse_y = event.pos

            # 在主场景检查是否点击猫咪附近
            if scene.is_main_scene():
                cat_x, cat_y = cat_state.get_current_position(scene)
                distance = math.sqrt((mouse_x - cat_x) ** 2 + (mouse_y - cat_y) ** 2)
                if (distance < GameConfig.TOUCH_DETECTION_RADIUS and
                        "touch" in cat_state.current_needs and
                        not cat_state.is_being_touched):
                    cat_state.touch_system.start_touch(mouse_x)
                else:
                    # 处理其他点击（如按钮）
                    self._handle_click(event.pos, cat_state, scene)
            else:
                # 房间场景的正常点击处理
                self._handle_click(event.pos, cat_state, scene)

    def _handle_mouse_button_up(self, event, cat_state):
        """处理鼠标释放事件"""
        if event.button == 1:
            if cat_state.touch_system.is_touching:
                cat_state.touch_system.stop_touch()

    def _handle_mouse_motion(self, event, cat_state, scene):
        """处理鼠标移动事件"""
        mouse_x, mouse_y = event.pos

        # 检查鼠标是否在猫咪附近
        if scene.is_main_scene() and "touch" in cat_state.current_needs:
            cat_x, cat_y = cat_state.get_current_position(scene)
            distance = math.sqrt((mouse_x - cat_x) ** 2 + (mouse_y - cat_y) ** 2)

            # 根据距离改变鼠标光标
            if distance < GameConfig.TOUCH_DETECTION_RADIUS:
                if not self.is_near_cat:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    self.is_near_cat = True
            else:
                if self.is_near_cat:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.is_near_cat = False
        else:
            if self.is_near_cat:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.is_near_cat = False

        # 鼠标移动时更新抚摸状态
        if cat_state.touch_system.is_touching:
            if cat_state.touch_system.update(mouse_x, cat_state):
                # 抚摸满足
                cat_state.handle_touch_satisfaction()
                cat_state.touch_system.stop_touch()

    def _handle_click(self, mouse_pos, cat_state, scene):
        """处理点击事件"""
        mouse_x, mouse_y = mouse_pos

        # 主场景切换按钮
        if scene.is_main_scene():
            button_rect = pygame.Rect(
                GameConfig.RIGHT_BUTTON_X, GameConfig.BUTTON_Y, *GameConfig.BUTTON_SIZE)
            if button_rect.collidepoint(mouse_x, mouse_y):
                print("点击右箭头，切换房间场景")
                scene.switch_to_room()
                return

        # 房间场景：检查左箭头按钮
        else:
            button_rect = pygame.Rect(GameConfig.LEFT_BUTTON_X, GameConfig.BUTTON_Y - 50,
                                      *GameConfig.BUTTON_SIZE)
            if button_rect.collidepoint(mouse_x, mouse_y):
                print("点击左箭头，切换主场景")
                scene.switch_to_main()
                return

            # 如果正在做动作时，忽略点击
            if cat_state.is_moving or cat_state.current_action:
                return

            # 遍历所有交互区域
            for zone_name, zone_data in InteractionZones.ZONES.items():
                rect = zone_data["rect"]
                # 判断点击位置是否在这个区域里
                if (rect[0] <= mouse_x <= rect[0] + rect[2] and
                        rect[1] <= mouse_y <= rect[1] + rect[3]):
                    print(f"点击了{zone_name}")

                    # 检查需求匹配
                    action = zone_data["action"]
                    if action not in cat_state.current_needs:
                        # 没有这个需求
                        message = TextConfig.NO_NEED_TEXTS.get(zone_name, "I don't need this!")
                        cat_state.no_need_message = message
                        cat_state.no_need_timer = GameConfig.NO_NEED_MESSAGE_FRAMES
                        print(f"猫咪说：{message}")
                        return

                    # 有需求，开始移动
                    target_pos = zone_data["cat_pos"]
                    cat_state.move_to_target(target_pos[0], target_pos[1])
                    # 保存待执行的动作数据
                    cat_state.pending_action_type = action
                    cat_state.pending_recovery = zone_data["recovery"]
                    print(f"开始移动到 {zone_name}，准备执行 {zone_data['action']} 动作")
                    return