"""
用户管理路由
"""

from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.services.billing import (
    get_or_create_user, 
    upgrade_user_to_pro, 
    store,
    simulate_payment_callback
)


router = APIRouter(prefix="/api/user", tags=["用户管理"])


@router.get("/status")
async def get_user_status(x_user_id: Optional[str] = Header(None, alias="X-User-ID")):
    """
    获取用户状态和用量信息
    """
    user_id, user_info = get_or_create_user(x_user_id)
    usage_info = store.get_usage_info(user_id)
    
    return {
        "success": True,
        "user_id": user_id,
        **usage_info
    }


@router.post("/init")
async def init_user():
    """
    初始化新用户
    """
    user_id, user_info = get_or_create_user()
    
    return {
        "success": True,
        "user_id": user_id,
        "message": "用户初始化成功"
    }


@router.post("/upgrade")
async def upgrade_to_pro(x_user_id: Optional[str] = Header(None, alias="X-User-ID")):
    """
    升级为Pro用户（模拟支付流程）
    
    实际生产环境应该：
    1. 返回支付链接（Stripe等）
    2. 等待支付回调确认
    """
    user_id, _ = get_or_create_user(x_user_id)
    
    # 模拟支付流程 - 实际应该跳转到支付页面
    # 这里直接模拟支付成功
    result = upgrade_user_to_pro(user_id)
    
    return {
        "success": result["success"],
        "user_id": user_id,
        "is_pro": result["is_pro"],
        "message": result["message"],
        "payment_url": "/api/payment/simulate"  # 模拟支付接口
    }


@router.post("/payment/simulate")
async def simulate_payment(x_user_id: Optional[str] = Header(None, alias="X-User-ID")):
    """
    模拟支付成功回调（开发测试用）
    
    实际环境中，支付网关会在支付成功后调用此接口
    """
    user_id, _ = get_or_create_user(x_user_id)
    result = simulate_payment_callback(user_id, "pro")
    
    return {
        "success": result["success"],
        "user_id": user_id,
        "is_pro": result.get("is_pro", False),
        "message": "模拟支付成功！您已成为Pro用户"
    }


@router.post("/reset-usage")
async def reset_usage(x_user_id: Optional[str] = Header(None, alias="X-User-ID")):
    """
    重置用户用量（管理员功能）
    """
    user_id, _ = get_or_create_user(x_user_id)
    success = store.reset_usage(user_id)
    
    return {
        "success": success,
        "user_id": user_id,
        "message": "用量已重置"
    }
