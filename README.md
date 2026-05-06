# 周报侠 (WeeklyHero) - AI智能周报助手

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-purple?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.109-green?style=for-the-badge" alt="FastAPI">
</p>

<p align="center">
  <strong>输入几个关键词，30秒生成一份漂亮的工作周报</strong>
</p>

---

## 🎯 产品定位

- **名称**：周报侠（WeeklyHero）
- **Slogan**：输入几个关键词，30秒生成一份漂亮的工作周报
- **目标用户**：所有需要写周报/日报/月报的职场人
- **商业模式**：免费3次/月 → Pro ¥29/月无限次

---

## ✨ 功能特性

### 核心功能
- 📝 **智能生成**：输入工作要点，自动生成格式化周报
- 🎨 **4种写作风格**：
  - 简洁务实型（工程师风格）
  - 数据驱动型（产品/运营风格）
  - 向上汇报型（给领导看的风格）
  - 自我包装型（绩效季加分风格）
- 📅 **3种报告类型**：日报、周报、月报

### 高级功能
- 🔗 **上周衔接**：自动延续上周周报内容
- ✨ **自动补全**：输入关键词，AI帮你扩充成完整描述
- 📤 **多格式导出**：Markdown / 纯文本 / 一键复制

### 商业模式
- **免费层**：3次/月
- **Pro会员**：¥29/月，无限次使用

---

## 🚀 快速开始

### 本地开发

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd AI-WeeklyHero

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 设置环境变量（可选，用于兜底API）
export DEEPSEEK_API_KEY="your-api-key-here"

# 5. 启动服务
python3 -m uvicorn app.main:app --reload --port 8000
```

访问 http://localhost:8000 即可使用！

### 一键启动（使用Docker）

```bash
docker build -t weeklyhero .
docker run -p 8000:8000 -e DEEPSEEK_API_KEY="your-key" weeklyhero
```

---

## 📁 项目结构

```
AI-WeeklyHero/
├── api/
│   ├── index.py          # Vercel Serverless入口
│   └── __init__.py
├── app/
│   ├── main.py           # FastAPI主应用
│   ├── routers/
│   │   ├── report.py     # 周报生成路由
│   │   └── user.py       # 用户管理路由
│   ├── services/
│   │   ├── generator.py  # 周报生成核心逻辑（Prompt Engineering）
│   │   └── billing.py    # 计费逻辑（SimpleStore内存存储）
│   └── models/
│       └── schemas.py    # 数据模型
├── static/
│   └── index.html        # 前端单页应用（深色科技风格）
├── vercel.json           # Vercel部署配置
├── requirements.txt      # Python依赖
└── README.md
```

---

## 🔌 API文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 主要接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `POST /api/report/generate` | 生成周报 | 输入工作要点，获取生成的报告 |
| `GET /api/user/status` | 用户状态 | 获取当前用户配额信息 |
| `POST /api/user/upgrade` | 升级Pro | 升级为Pro会员 |
| `GET /api/report/types` | 报告类型 | 获取支持的报告类型列表 |
| `GET /api/report/styles` | 写作风格 | 获取支持的写作风格列表 |

### 请求示例

```bash
# 生成周报
curl -X POST http://localhost:8000/api/report/generate \
  -H "Content-Type: application/json" \
  -H "X-User-ID: your-user-id" \
  -d '{
    "work_points": [
      "完成用户登录模块开发",
      "修复了3个线上bug",
      "参与产品需求评审"
    ],
    "report_type": "weekly",
    "style": "concise"
  }'
```

---

## 🎨 Prompt Engineering

周报生成器内置4套精心设计的Prompt模板：

### 1. 简洁务实型
- 短句为主，突出完成项和待办
- 不用形容词和废话
- 结构清晰，按优先级排列

### 2. 数据驱动型
- 强调量化成果
- "完成X个需求"、"提升Y%指标"
- 突出可衡量成果

### 3. 向上汇报型
- 突出战略价值和业务影响
- 先说结论再展开
- 简洁有力，让领导快速获取关键信息

### 4. 自我包装型
- 用STAR法则(Situation-Task-Action-Result)包装每个事项
- 突出个人贡献和能力
- 展示主动性和成长

---

## 🌐 部署

### Vercel部署

```bash
# 1. 安装Vercel CLI
npm install -g vercel

# 2. 登录
vercel login

# 3. 部署
vercel

# 4. 设置环境变量
vercel env add DEEPSEEK_API_KEY
```

或在Vercel Dashboard中：
1. Import your GitHub repository
2. Add Environment Variable: `DEEPSEEK_API_KEY`
3. Deploy!

### 其他平台

由于是标准FastAPI应用，可以部署到：
- Railway
- Render  
- Fly.io
- 任何支持Python的Paas

---

## 💡 使用技巧

### 1. BYOK模式（推荐高频用户）
使用自己的DeepSeek API Key，完全不受免费次数限制：
1. 点击"高级选项"
2. 勾选"使用自己的API Key"
3. 输入你的API Key

### 2. 上周衔接
粘贴上周周报内容，AI会自动衔接，保持工作连续性。

### 3. 自动补全
只输入关键词如"登录模块"，AI会帮你扩充成完整描述。

---

## 🔧 配置

### 环境变量

| 变量名 | 必需 | 描述 |
|--------|------|------|
| `DEEPSEEK_API_KEY` | 是 | DeepSeek API Key（用于兜底） |

### 获取DeepSeek API Key

1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 充值或使用免费额度

---

## 📝 License

MIT License - 欢迎使用和修改！

---

<p align="center">
  <strong>让工作汇报更轻松 ✨</strong>
</p>
