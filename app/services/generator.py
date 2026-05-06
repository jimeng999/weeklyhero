"""
周报生成器核心服务
包含精心设计的Prompt Engineering模板
"""

import json
from typing import List, Optional
from app.models.schemas import ReportType, WritingStyle


# ============ Prompt 模板定义 ============

PROMPT_TEMPLATES = {
    WritingStyle.CONCISE: {
        ReportType.DAILY: """你是一个专业的职场周报助手，风格简洁务实。
## 要求
- 使用短句，突出完成项和待办
- 不用形容词和废话
- 结构清晰，分区明确

## 输出格式
【今日完成】
- [具体事项]

【明日计划】
- [具体事项]

【需协助/风险】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成日报：""",

        ReportType.WEEKLY: """你是一个专业的职场周报助手，风格简洁务实。
## 要求
- 使用短句，突出完成项和待办
- 不用形容词和废话
- 结构清晰，按优先级排列
- 按整手（100股/港股）计算

## 输出格式
【本周完成】(按优先级)
- [具体事项]

【下周计划】
- [具体事项]

【需协助/风险】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成周报：""",

        ReportType.MONTHLY: """你是一个专业的职场周报助手，风格简洁务实。
## 要求
- 使用短句，突出完成项和待办
- 不用形容词和废话
- 结构清晰，按优先级排列

## 输出格式
【本月完成】(按优先级)
- [具体事项]

【下月计划】
- [具体事项]

【需协助/风险】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成月报："""
    },

    WritingStyle.DATA_DRIVEN: {
        ReportType.DAILY: """你是一个专业的职场周报助手，风格数据驱动。
## 要求
- 强调量化成果
- 用"完成X个需求"、"提升Y%指标"等表述
- 突出可衡量成果

## 输出格式
【今日成果】
- [量化成果描述]

【关键指标变化】
- [如有数据则写]

【明日目标】
- [量化目标]

【需协助/风险】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成日报：""",

        ReportType.WEEKLY: """你是一个专业的职场周报助手，风格数据驱动。
## 要求
- 强调量化成果
- 用"完成X个需求"、"提升Y%指标"、"覆盖Z个用户"等表述
- 突出可衡量成果和业务价值

## 输出格式
【本周量化成果】
1. [量化成果1]
2. [量化成果2]
...

【关键指标变化】
| 指标 | 变化 |
|------|------|
| ... | ... |

【下周量化目标】
- [目标1]
- [目标2]

【需协助/风险】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成周报：""",

        ReportType.MONTHLY: """你是一个专业的职场周报助手，风格数据驱动。
## 要求
- 强调量化成果
- 用"完成X个需求"、"提升Y%指标"等表述
- 突出可衡量成果和业务价值
- 可用表格展示数据

## 输出格式
【本月量化成果】
1. [量化成果1]
2. [量化成果2]
...

【核心指标】
| 指标 | 本月 | 环比 | 同比 |
|------|------|------|------|
| ... | ... | ... | ... |

【下月量化目标】
- [目标1]
- [目标2]

【需协助/风险】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成月报："""
    },

    WritingStyle.EXECUTIVE: {
        ReportType.DAILY: """你是一个专业的职场周报助手，风格向上汇报型。
## 要求
- 突出战略价值和业务影响
- 先说结论再展开
- 简洁有力，让领导快速获取关键信息

## 输出格式
【核心成果】
> [一句话总结今日最重要成果]

【详情】
- [事项1]
- [事项2]

【明日重点】
- [最重要的一件事]

【需要领导知晓/决策】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成日报：""",

        ReportType.WEEKLY: """你是一个专业的职场周报助手，风格向上汇报型。
## 要求
- 突出战略价值和业务影响
- 先说结论再展开
- 简洁有力，让领导快速获取关键信息
- 按整手（100股/港股）计算买入量

## 输出格式
【本周核心成果】
> [一句话总结本周最重要成果]

【业务价值】
1. [价值点1]
2. [价值点2]

【详情】
- [事项1]
- [事项2]
...

【下周重点】
- [最重要的一件事/目标]

【需要领导知晓/决策】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成周报：""",

        ReportType.MONTHLY: """你是一个专业的职场周报助手，风格向上汇报型。
## 要求
- 突出战略价值和业务影响
- 先说结论再展开
- 简洁有力，让领导快速获取关键信息
- 强调对整体目标/OKR的贡献

## 输出格式
【本月核心成果】
> [一句话总结本月最重要成果]

【战略贡献】
1. [战略贡献1]
2. [战略贡献2]

【业务价值】
- [价值点]
...

【风险与挑战】
- [如有]

【下月重点】
- [最重要的一件事/目标]

【需要领导知晓/决策】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成月报："""
    },

    WritingStyle.ACHIEVEMENT: {
        ReportType.DAILY: """你是一个专业的职场周报助手，风格自我包装型。
## 要求
- 用STAR法则(Situation-Task-Action-Result)包装每个事项
- 突出个人贡献和能力
- 展示主动性和成长
- 让绩效季加分

## 输出格式
【今日成就】
- **[任务]**：[情境]→[行动]→[结果，含量化收益]

【能力展现】
- [展示的技能/新学到的东西]

【明日挑战】
- [计划挑战的目标]

【所需支持】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成日报：""",

        ReportType.WEEKLY: """你是一个专业的职场周报助手，风格自我包装型。
## 要求
- 用STAR法则(Situation-Task-Action-Result)包装每个事项
- 突出个人贡献和能力
- 展示主动性和成长
- 让绩效季加分
- 突出影响范围和个人独特贡献

## 输出格式
【本周成就】(STAR法则)
1. **[成果标题]**
   - Situation(情境)：[背景]
   - Task(任务)：[目标]
   - Action(行动)：[你的具体行动]
   - Result(结果)：[量化成果+影响]

【个人成长】
- [本周学到的技能/突破]
- [展示的专业能力]

【下周挑战目标】
- [计划挑战的目标]

【所需支持】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成周报：""",

        ReportType.MONTHLY: """你是一个专业的职场周报助手，风格自我包装型。
## 要求
- 用STAR法则(Situation-Task-Action-Result)包装每个事项
- 突出个人贡献和能力
- 展示主动性和成长
- 让绩效季加分
- 突出影响范围和个人独特贡献
- 可加入项目背景和团队协作描述

## 输出格式
【本月成就】(STAR法则)
1. **[核心成果标题]**
   - Situation(情境)：[背景+挑战]
   - Task(任务)：[目标+难度]
   - Action(行动)：[你的具体行动+创新点]
   - Result(结果)：[量化成果+业务影响+他人反馈]

【里程碑】
- [本月达成的重要里程碑]

【个人成长】
- [本月学到的技能/突破]
- [展示的专业能力]
- [跨团队协作亮点]

【下月挑战目标】
- [计划挑战的目标+期望成果]

【所需支持】
- [如无则写"无"]

## 工作要点
{work_points}

{previous_context}

请生成月报："""
    }
}


# 自动补全Prompt
AUTO_EXPAND_PROMPT = """你是一个专业的职场周报助手，擅长将工作关键词扩充为完整描述。

## 要求
- 将用户提供的关键词扩充成完整、专业的句子
- 保持原意，适当添加合理的上下文
- 使用专业但不做作的职场用语
- 每个要点扩充为1-3句话

## 输入格式
{keywords}

## 输出格式
请直接输出扩充后的工作要点列表，每行一个，用"-"开头：
- [扩充后的完整描述]
- [扩充后的完整描述]

不要添加其他说明文字。"""


def build_system_prompt(style: WritingStyle, report_type: ReportType) -> str:
    """构建系统提示词"""
    return """你是一个专业的职场周报助手。你的任务是帮助用户生成高质量的工作报告。

## 核心原则
1. 专业但不夸张
2. 突出价值，不过度包装
3. 结构清晰，便于阅读
4. 根据用户选择的风格调整表达方式"""

def build_user_prompt(
    work_points: List[str],
    report_type: ReportType,
    style: WritingStyle,
    previous_report: Optional[str] = None,
    next_week_plan: Optional[List[str]] = None
) -> str:
    """构建用户提示词"""
    
    # 获取对应模板
    template = PROMPT_TEMPLATES[style][report_type]
    
    # 格式化工作要点
    formatted_points = "\n".join([f"- {point}" for point in work_points])
    
    # 格式化上周周报上下文
    previous_context = ""
    if previous_report:
        if report_type == ReportType.DAILY:
            previous_context = f"\n## 昨日延续\n{previous_report}"
        else:
            previous_context = f"\n## 上期报告延续\n{previous_report}"
    
    # 格式化下周计划
    next_plan = ""
    if next_week_plan:
        plan_items = "\n".join([f"- {item}" for item in next_week_plan])
        if report_type == ReportType.DAILY:
            next_plan = f"\n## 明日计划要点\n{plan_items}"
        else:
            next_plan = f"\n## 下期计划要点\n{plan_items}"
    
    # 填充模板
    prompt = template.format(
        work_points=formatted_points,
        previous_context=previous_context + next_plan
    )
    
    return prompt


async def generate_report_with_ai(
    work_points: List[str],
    report_type: ReportType,
    style: WritingStyle,
    user_api_key: Optional[str] = None,
    previous_report: Optional[str] = None,
    next_week_plan: Optional[List[str]] = None,
    auto_expand: bool = False
) -> dict:
    """
    使用AI生成报告
    
    Returns:
        dict: {"success": bool, "report": str, "error": str, "tokens_used": int}
    """
    import httpx
    
    # 决定使用哪个API
    if user_api_key:
        # BYOK模式：使用用户提供的API
        base_url = "https://api.deepseek.com"
        api_key = user_api_key
    else:
        # 兜底模式：使用DeepSeek官方API（需要配置DEEPSEEK_API_KEY）
        base_url = "https://api.deepseek.com"
        api_key = None  # 将在headers中使用应用级key
    
    # 构建消息
    system_prompt = build_system_prompt(style, report_type)
    
    # 如果需要自动补全，先处理工作要点
    processed_points = work_points
    if auto_expand:
        expand_messages = [
            {"role": "system", "content": AUTO_EXPAND_PROMPT.format(keywords="\n".join(work_points))},
            {"role": "user", "content": "请扩充以上工作要点"}
        ]
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                headers = {
                    "Authorization": f"Bearer {api_key or 'dummy'}",
                    "Content-Type": "application/json"
                }
                if not api_key:
                    # 使用默认API key
                    from os import getenv
                    api_key = getenv("DEEPSEEK_API_KEY", "")
                    headers["Authorization"] = f"Bearer {api_key}"
                
                expand_response = await client.post(
                    f"{base_url}/chat/completions",
                    headers=headers,
                    json={
                        "model": "deepseek-chat",
                        "messages": expand_messages,
                        "temperature": 0.7,
                        "max_tokens": 500
                    }
                )
                
                if expand_response.status_code == 200:
                    expand_result = expand_response.json()
                    expanded_text = expand_result["choices"][0]["message"]["content"]
                    # 解析扩充后的要点
                    processed_points = [
                        line.strip("- ").strip() 
                        for line in expanded_text.split("\n") 
                        if line.strip().startswith("-")
                    ]
                else:
                    # 自动补全失败，继续使用原始要点
                    pass
        except Exception:
            # 网络错误，继续使用原始要点
            pass
    
    # 构建生成报告的消息
    user_prompt = build_user_prompt(
        work_points=processed_points,
        report_type=report_type,
        style=style,
        previous_report=previous_report,
        next_week_plan=next_week_plan
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # 调用AI
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            headers = {
                "Content-Type": "application/json"
            }
            if not api_key:
                from os import getenv
                api_key = getenv("DEEPSEEK_API_KEY", "")
            headers["Authorization"] = f"Bearer {api_key}"
            
            response = await client.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json={
                    "model": "deepseek-chat",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                report = result["choices"][0]["message"]["content"]
                tokens_used = result.get("usage", {}).get("total_tokens", 0)
                
                return {
                    "success": True,
                    "report": report,
                    "tokens_used": tokens_used,
                    "error": None
                }
            else:
                error_detail = response.text
                return {
                    "success": False,
                    "report": None,
                    "tokens_used": 0,
                    "error": f"AI API错误: {response.status_code} - {error_detail}"
                }
                
    except Exception as e:
        return {
            "success": False,
            "report": None,
            "tokens_used": 0,
            "error": f"网络错误: {str(e)}"
        }


def format_report_for_export(report: str, format: str) -> str:
    """格式化报告为不同导出格式"""
    if format == "markdown":
        return report
    elif format == "plain_text":
        # 移除markdown格式符号
        lines = report.split("\n")
        formatted = []
        for line in lines:
            # 移除粗体
            line = line.replace("**", "")
            # 移除表格markdown
            line = line.replace("|", "  ")
            formatted.append(line)
        return "\n".join(formatted)
    elif format == "html":
        # 简单转换为HTML
        html = report.replace("\n", "<br>")
        html = html.replace("**", "<strong>").replace("**", "</strong>")
        html = html.replace("- ", "<li>")
        return f"<div style='font-family: sans-serif; line-height: 1.6;'>{html}</div>"
    return report
