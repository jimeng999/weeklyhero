# 周报侠 (WeeklyHero) - AI智能周报助手

from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from enum import Enum


class ReportType(str, Enum):
    """报告类型"""
    DAILY = "daily"      # 日报
    WEEKLY = "weekly"    # 周报
    MONTHLY = "monthly"  # 月报


class WritingStyle(str, Enum):
    """写作风格"""
    CONCISE = "concise"              # 简洁务实型
    DATA_DRIVEN = "data_driven"      # 数据驱动型
    EXECUTIVE = "executive"          # 向上汇报型
    ACHIEVEMENT = "achievement"      # 自我包装型


class GenerateRequest(BaseModel):
    """周报生成请求"""
    work_points: List[str] = Field(
        ..., 
        description="本周工作要点列表",
        min_length=1,
        max_length=20
    )
    report_type: ReportType = Field(
        default=ReportType.WEEKLY,
        description="报告类型"
    )
    style: WritingStyle = Field(
        default=WritingStyle.CONCISE,
        description="写作风格"
    )
    user_api_key: Optional[str] = Field(
        None,
        description="用户自己的API Key（BYOK模式）"
    )
    previous_report: Optional[str] = Field(
        None,
        description="上周周报内容（用于自动衔接）"
    )
    next_week_plan: Optional[List[str]] = Field(
        None,
        description="下周计划要点"
    )
    auto_expand: bool = Field(
        default=False,
        description="是否自动补全要点"
    )


class GenerateResponse(BaseModel):
    """周报生成响应"""
    success: bool
    report: Optional[str] = None
    remaining_free: Optional[int] = None
    is_pro: Optional[bool] = None
    error: Optional[str] = None
    tokens_used: Optional[int] = None


class UserStatus(BaseModel):
    """用户状态"""
    user_id: str
    is_pro: bool
    usage_count: int
    free_limit: int = 3
    remaining_free: int


class SubscriptionRequest(BaseModel):
    """订阅请求"""
    user_id: str
    plan: Literal["pro"] = "pro"


class SubscriptionResponse(BaseModel):
    """订阅响应"""
    success: bool
    is_pro: bool
    message: str


class ExportFormat(str, Enum):
    """导出格式"""
    MARKDOWN = "markdown"
    PLAIN_TEXT = "plain_text"
    HTML = "html"
