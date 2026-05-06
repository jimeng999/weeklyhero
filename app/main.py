"""
周报侠 (WeeklyHero) - FastAPI主应用
AI智能周报助手
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.routers import report, user


# 创建FastAPI应用
app = FastAPI(
    title="周报侠 (WeeklyHero)",
    description="AI智能周报助手 - 输入几个关键词，30秒生成一份漂亮的工作周报",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(report.router)
app.include_router(user.router)


# 静态文件路径
static_path = Path(__file__).parent.parent / "static"


@app.get("/", response_class=HTMLResponse)
async def root():
    """返回前端页面"""
    index_file = static_path / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return HTMLResponse(content="""
    <html>
        <head><title>周报侠</title></head>
        <body>
            <h1>周报侠 (WeeklyHero)</h1>
            <p>AI智能周报助手</p>
            <p>访问 <a href="/docs">API文档</a></p>
        </body>
    </html>
    """)


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "WeeklyHero"}


@app.get("/api/info")
async def api_info():
    """API信息"""
    return {
        "name": "周报侠 (WeeklyHero)",
        "version": "1.0.0",
        "description": "AI智能周报助手",
        "features": [
            "日报生成",
            "周报生成", 
            "月报生成",
            "多种写作风格",
            "自动补全",
            "上周周报衔接"
        ],
        "pricing": {
            "free": "3次/月",
            "pro": "¥29/月 无限次"
        }
    }


# 挂载静态文件（如果需要直接访问静态资源）
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
