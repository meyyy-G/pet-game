# src/events/interaction_zones.py
"""交互区域定义"""

class InteractionZones:
    """房间场景的交互区域定义"""
    ZONES = {
        "bed": {
            "rect": (250, 185, 15, 65),
            "cat_pos": (257.5, 212.5),
            "action": "sleepy",
            "need_type": ["sleepy"],
            "recovery": {"health": 20, "mood": 15},
            "required_needs": ["sleepy"]
        },
        "toy": {
            "rect": (315, 150, 45, 110),
            "cat_pos": (327.5, 202),
            "action": "play",
            "need_type": ["play"],
            "recovery": {"mood": 25},
            "required_needs": ["play"]
        },
        "water_bowl": {
            "rect": (230, 295, 30, 25),
            "cat_pos": (245, 307.5),
            "action": "thirsty",
            "need_type": ["thirsty"],
            "recovery": {"health": 15},
            "required_needs": ["thirsty"]
        },
        "food_bowl": {
            "rect": (180, 300, 30, 30),
            "cat_pos": (195, 315),
            "action": "hungry",
            "need_type": ["hungry"],
            "recovery": {"health": 25},
            "required_needs": ["hungry"]
        }
    }