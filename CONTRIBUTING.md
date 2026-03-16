# Contributing

感谢你关注 QEasy DataHub。

## 贡献方式

欢迎以下类型的贡献：

- 修正文档错误与失效链接
- 完善连接器、方案与 API 说明
- 改进 `src/` 下的 FastAPI 示例能力
- 提交测试、脚本与开发体验优化

## 本地开发建议

1. 安装依赖：`pip install -e ".[dev]"`
2. 启动服务：`uvicorn app.main:app --app-dir src --reload`
3. 运行测试：`pytest`
4. 检查文档链接：`python scripts/check_markdown_links.py`

## Pull Request 建议

- 保持改动聚焦，避免无关重构
- 新增能力时同步补充文档
- 若修改接口，请说明兼容性影响
- 提交前确认基础测试与文档链接检查通过

## 文档规范

- 优先使用清晰、直接的中文说明
- 链接尽量指向已存在的文档入口
- 新增图片优先使用稳定的公开地址或仓库资源

## 行为准则

参与项目前，请先阅读 [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)。
