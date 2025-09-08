# src/config/animation_config.py - 确保配置正确
"""动画配置"""

class AnimationConfig:
    """动画配置 - 所有动画文件的信息"""
    ANIMATION = {
        "normal": {"folder": "normal", "prefix": "cat_", "count": 10},
        # 加载动画 - 现在直接在 animations 文件夹下
        "loading": {"folder": "loading", "prefix": "load_frame_", "count": 12},

        # 需求动画 - 在 animations/cat 子文件夹下
        "hungry": {"folder": "hungry", "prefix": "hry_cat_", "count": 8},
        "play": {"folder": "play", "prefix": "ply_cat_", "count": 12},
        "sleepy": {"folder": "sleepy", "prefix": "slpy_cat_", "count": 9},
        "touch": {"folder": "touched", "prefix": "tch_cat_", "count": 12},

        # 执行动画 - 也在 animations/cat 子文件夹下
        "eating": {"folder": "hungry", "prefix": "eat_rect_", "count": 15},
        "playing": {"folder": "play", "prefix": "ply_rect_", "count": 4},
        "sleeping": {"folder": "sleepy", "prefix": "slpy_rect_", "count": 4},
        "touched": {"folder": "touched", "prefix": "tch_rect_", "count": 12}
    }
