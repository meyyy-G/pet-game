# src/systems/save_manager.py
"""存档管理器"""

import os
import json
import time
from src.config.game_config import GameConfig


class SaveManager:
    """存档管理器"""

    @staticmethod
    def save_game_data(cat_state, game_time, play_time=0, slot=0):
        """保存游戏数据到指定槽位"""
        try:
            # 确保Save文件夹存在
            save_dir = "data/saves"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                print(f"📁 创建存档文件夹: {save_dir}")

            # 构建存档数据
            save_data = {
                "version": "1.0",
                "player_name": "player",
                "play_time": play_time,
                "cat_health": cat_state.health,
                "cat_mood": cat_state.mood,
                "game_hour": game_time.current_hour,
                "last_sleep_hour": cat_state.last_sleep_hour,
                "satisfied_needs_history": cat_state.satisfied_needs.copy(),
                "created_time": time.time(),
                "last_saved_time": time.time(),
                "slot": slot
            }

            # 生成文件名
            if slot == 0:
                filename = os.path.join(save_dir, GameConfig.SAVE_FILE_NAME)
            else:
                filename = os.path.join(save_dir, f"electric_pat_save_slot{slot}.json")

            # 保存到文件
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
            save_dir = "data/saves"
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
        save_dir = "data/saves"
        if slot == 0:
            filename = os.path.join(save_dir, GameConfig.SAVE_FILE_NAME)
        else:
            filename = os.path.join(save_dir, f"electric_pat_save_slot{slot}.json")
        return os.path.exists(filename)
