# Creato UGC 爆款生成器 🐾

> 一条龙批量生产 UGC 短视频广告：搜对标 → 复刻脚本 → 生图 → 生视频 → 审片 → 剪辑 → 成片交付

## 这是什么？

一个 OpenClaw Agent Skill，让你的 AI agent 变成一个懂投放的广告素材生产线。

适用于：
- 软件/SaaS/WebApp/App 产品
- TikTok / Instagram / 小红书等平台
- 真人 reaction / hook 类型的短视频广告
- 需要批量测试不同创意变量的团队

## 快速开始

### 1. 把 skill 放到你的 agent 里

```bash
# 复制整个文件夹到你的 skills 目录
cp -r creato-ugc-generator/ ~/.openclaw/workspace/.agent/skills/
```

### 2. 准备 API Keys

你需要以下服务的 API Key：

| 服务 | 用途 | 获取方式 |
|---|---|---|
| **Apify** | TikTok/Instagram 搜索 | https://console.apify.com/account/integrations |
| **Foreplay** | 广告素材数据库 | https://foreplay.co → Settings → API Keys |
| **OpenCreator** | AI 生文/生图/生视频 | 联系 OpenCreator 团队 |
| **fal** | 字幕/剪辑后期 | https://fal.ai/dashboard → API Keys |

### 3. 写入 TOOLS.md

在你的 `TOOLS.md` 中添加：

```markdown
### Creato UGC Generator 配置

- CREATO_APIFY_API_KEY: <你的 key>
- CREATO_FOREPLAY_API_KEY: <你的 key>
- OPENCREATOR_API_KEY: <你的 key>
- OPENCREATOR_TEXT_WORKFLOW_ID: <你的 workflow id>
- OPENCREATOR_IMAGE_WORKFLOW_ID: <你的 workflow id>
- OPENCREATOR_VIDEO_WORKFLOW_ID: <你的 workflow id>
- CREATO_FAL_API_KEY: <你的 key>

## 效果测试集（可选）
- CREATO_BITABLE_APP_TOKEN: <你的飞书多维表格 token>
- CREATO_BITABLE_TABLE_ID: <你的数据表 id>
```

### 4. 安装系统依赖

```bash
pip install yt-dlp requests
apt-get install -y ffmpeg zip  # macOS: brew install ffmpeg zip

# 审片工具依赖（可选，用于后期阶段）
pip install scenedetect[opencv] rapidocr-onnxruntime pysrt python-dotenv
```

### 5. 开始使用

跟你的 agent 说：
- "帮我做一条 [产品名] 的 TikTok 广告"
- "搜一下 [品类] 的爆款视频，帮我复刻一条"
- "我有个 SaaS 产品，想做 3 条 15 秒的 hook 视频"

## 文件结构

```
creato-ugc-generator/
├── SKILL.md                          # Skill 主文件（agent 读这个）
├── README.md                         # 你正在看的这个
├── scripts/
│   └── opencreator_workflow.py       # OpenCreator API 调用封装
└── references/                       # 参考资料（可选）
```

## 完整流程

1. **搜索推荐** — 搜 TikTok/Instagram/Foreplay，推荐 3 个可复刻的对标视频
2. **生成脚本** — 用 OpenCreator 复刻对标视频的脚本结构
3. **匹配角色/场景** — 从 Avatar/Situation 库做结构化匹配
4. **生成关键图** — AI 生成角色+场景的关键图
5. **生成视频素材** — AI 生成视频素材
6. **审片** — 五维评分，过滤废镜头
7. **剪辑后期** — 停顿剪裁、录屏嵌入、字幕、合成
8. **成片交付** — 成片 + 原始素材包，可选写入效果测试集

支持 **Batch Mode**：选多个对标视频，每条独立跑完整闭环。

## 注意事项

- 三次确认不可跳过（脚本 → 关键图 → 视频素材）
- 所有媒体输入必须是真实文件，不是页面链接
- 审片是必须步骤，不能跳过直接剪辑
- 字幕最后做，不要提前烧

## License

内部使用，随便传。
