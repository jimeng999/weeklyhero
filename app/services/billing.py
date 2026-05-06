"""
计费服务
使用SimpleStore内存存储实现简单的订阅和用量追踪
"""

from typing import Optional, Dict
from datetime import datetime, timedelta
import uuid


# ============ 内存存储 (SimpleStore) ============
# 在生产环境中，这些应该存储在数据库中
# 这里使用内存字典模拟，便于开发和测试

class SimpleStore:
    """简单的内存数据存储"""
    
    def __init__(self):
        # 用户数据: {user_id: {"is_pro": bool, "usage_count": int, "last_reset": str}}
        self.users: Dict[str, dict] = {}
        
        # 全局计数器: {"count": int, "last_reset": str}
        self.global_usage: Dict[str, any] = {
            "count": 0,
            "last_reset": datetime.now().strftime("%Y-%m")
        }
        
        # API Key管理: {api_key: user_id}
        self.api_keys: Dict[str, str] = {}
    
    def get_user(self, user_id: str) -> dict:
        """获取用户数据，不存在则创建"""
        if user_id not in self.users:
            self.users[user_id] = {
                "is_pro": False,
                "usage_count": 0,
                "created_at": datetime.now().isoformat(),
                "last_reset": datetime.now().strftime("%Y-%m")
            }
        return self.users[user_id]
    
    def create_user(self, user_id: Optional[str] = None) -> str:
        """创建新用户"""
        if not user_id:
            user_id = str(uuid.uuid4())
        
        self.get_user(user_id)  # 确保用户存在
        return user_id
    
    def check_and_increment_usage(self, user_id: str) -> tuple[bool, int]:
        """
        检查并增加用量
        
        Returns:
            (can_use: bool, remaining: int)
            - can_use: 是否可以使用
            - remaining: 剩余免费次数（Pro用户返回-1）
        """
        user = self.get_user(user_id)
        
        # Pro用户无限使用
        if user["is_pro"]:
            return True, -1
        
        # 检查是否需要重置（每月重置）
        current_month = datetime.now().strftime("%Y-%m")
        if user["last_reset"] != current_month:
            # 新月份，重置计数
            user["usage_count"] = 0
            user["last_reset"] = current_month
        
        # 检查免费额度
        FREE_LIMIT = 3
        if user["usage_count"] < FREE_LIMIT:
            user["usage_count"] += 1
            remaining = FREE_LIMIT - user["usage_count"]
            return True, remaining
        else:
            return False, 0
    
    def upgrade_to_pro(self, user_id: str) -> bool:
        """升级为Pro用户"""
        user = self.get_user(user_id)
        user["is_pro"] = True
        return True
    
    def is_pro(self, user_id: str) -> bool:
        """检查是否为Pro用户"""
        return self.get_user(user_id)["is_pro"]
    
    def get_remaining_free(self, user_id: str) -> int:
        """获取剩余免费次数"""
        user = self.get_user(user_id)
        if user["is_pro"]:
            return -1
        
        FREE_LIMIT = 3
        remaining = FREE_LIMIT - user["usage_count"]
        return max(0, remaining)
    
    def get_usage_info(self, user_id: str) -> dict:
        """获取用户用量信息"""
        user = self.get_user(user_id)
        return {
            "user_id": user_id,
            "is_pro": user["is_pro"],
            "usage_count": user["usage_count"],
            "free_limit": 3,
            "remaining_free": self.get_remaining_free(user_id)
        }
    
    def reset_usage(self, user_id: str) -> bool:
        """重置用户用量（管理员用）"""
        user = self.get_user(user_id)
        user["usage_count"] = 0
        user["last_reset"] = datetime.now().strftime("%Y-%m")
        return True


# 全局单例
store = SimpleStore()


# ============ 计费相关函数 ============

def get_or_create_user(user_id: Optional[str] = None) -> tuple[str, dict]:
    """
    获取或创建用户
    
    Args:
        user_id: 可选的用户ID
        
    Returns:
        (user_id, user_info)
    """
    if user_id:
        user_info = store.get_user(user_id)
    else:
        user_id = store.create_user()
        user_info = store.get_user(user_id)
    
    return user_id, user_info


def check_quota(user_id: str) -> tuple[bool, int]:
    """
    检查用户配额
    
    Returns:
        (can_use: bool, remaining: int)
    """
    return store.check_and_increment_usage(user_id)


def upgrade_user_to_pro(user_id: str) -> dict:
    """
    升级用户为Pro
    
    在实际场景中，这里应该集成支付网关（如Stripe）
    """
    success = store.upgrade_to_pro(user_id)
    return {
        "success": success,
        "is_pro": True,
        "message": "升级成功！您现在可以无限次使用周报侠Pro" if success else "升级失败"
    }


def simulate_payment_callback(user_id: str, plan: str) -> dict:
    """
    模拟支付回调（实际应该由支付网关调用）
    
    在生产环境中：
    1. 接收Stripe/WebPay等支付通知
    2. 验证签名
    3. 更新用户订阅状态
    """
    if plan == "pro":
        return upgrade_user_to_pro(user_id)
    return {"success": False, "message": "未知的订阅计划"}
