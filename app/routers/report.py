"""
周报生成路由
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from app.models.schemas import (
    GenerateRequest, 
    GenerateResponse,
    ReportType,
    WritingStyle,
    ExportFormat
)
from app.services.generator import generate_report_with_ai, format_report_for_export
from app.services.billing import check_quota, get_or_create_user


router = APIRouter(prefix="/api/report", tags=["周报生成"])


@router.post("/generate", response_model=GenerateResponse)
async def generate_report(
    request: GenerateRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID")
):
    """
    生成工作周报/日报/月报
    
    - 输入工作要点，选择报告类型和风格
    - 自动生成格式化报告
    """
    # 获取或创建用户
    user_id, user_info = get_or_create_user(x_user_id)
    
    # 检查配额
    can_use, remaining = check_quota(user_id)
    
    if not can_use:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "免费额度已用完",
                "message": "您本月的免费次数(3次)已用完",
                "upgrade_url": "/#/upgrade",
                "user_id": user_id
            }
        )
    
    # 调用AI生成报告
    result = await generate_report_with_ai(
        work_points=request.work_points,
        report_type=request.report_type,
        style=request.style,
        user_api_key=request.user_api_key,
        previous_report=request.previous_report,
        next_week_plan=request.next_week_plan,
        auto_expand=request.auto_expand
    )
    
    if result["success"]:
        return GenerateResponse(
            success=True,
            report=result["report"],
            remaining_free=remaining,
            is_pro=user_info["is_pro"],
            tokens_used=result.get("tokens_used")
        )
    else:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "生成失败",
                "message": result["error"],
                "user_id": user_id
            }
        )


@router.post("/export")
async def export_report(
    report: str,
    format: ExportFormat = ExportFormat.MARKDOWN
):
    """
    导出报告为不同格式
    """
    formatted = format_report_for_export(report, format)
    return {
        "success": True,
        "content": formatted,
        "format": format
    }


@router.get("/types")
async def get_report_types():
    """获取支持的报告类型"""
    return {
        "types": [
            {"value": "daily", "label": "日报", "description": "简洁的单日工作汇报"},
            {"value": "weekly", "label": "周报", "description": "标准的一周工作总结"},
            {"value": "monthly", "label": "月报", "description": "详细的一个月工作汇总"}
        ]
    }


@router.get("/styles")
async def get_writing_styles():
    """获取支持的写作风格"""
    return {
        "styles": [
            {
                "value": "concise",
                "label": "简洁务实型",
                "description": "工程师风格，短句为主，突出完成项"
            },
            {
                "value": "data_driven",
                "label": "数据驱动型",
                "description": "产品/运营风格，强调量化成果"
            },
            {
                "value": "executive",
                "label": "向上汇报型",
                "description": "给领导看的风格，突出战略价值"
            },
            {
                "value": "achievement",
                "label": "自我包装型",
                "description": "绩效季加分风格，STAR法则包装"
            }
        ]
    }
