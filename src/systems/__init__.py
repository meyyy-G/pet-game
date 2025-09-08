# src/systems/__init__.py - 修正版本
"""系统模块"""

from .resource_manager import ResourceManager
from .save_manager import SaveManager
from .touch_system import TouchSystem
from .loading_state import LoadingState

__all__ = ['ResourceManager', 'SaveManager', 'TouchSystem', 'LoadingState']