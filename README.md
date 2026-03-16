<p align="center">
    <a href="https://www.qeasy.cloud/">
        <img src="https://static.qeasy.cloud/common/logo/qeasy_logo_v3.png" alt="轻易云 QEasy Logo" width="300" />
    </a>
</p>

# QEasy DataHub

<p align="center">广东轻亿云软件科技有限公司 · 轻易云开源项目</p>

<p align="center">
    <a href="https://img.shields.io/badge/license-Apache%202.0-blue.svg"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="Apache 2.0" /></a>
    <a href="https://img.shields.io/badge/python-3.11%2B-3776AB.svg"><img src="https://img.shields.io/badge/python-3.11%2B-3776AB.svg" alt="Python 3.11+" /></a>
    <a href="https://img.shields.io/badge/FastAPI-starter-009688.svg"><img src="https://img.shields.io/badge/FastAPI-starter-009688.svg" alt="FastAPI Starter" /></a>
    <a href="https://img.shields.io/badge/docs-ready-6f42c1.svg"><img src="https://img.shields.io/badge/docs-ready-6f42c1.svg" alt="Docs Ready" /></a>
</p>

<p align="center">
    <a href="https://www.qeasy.cloud/">轻易云官网</a> ·
    <a href="./docs/README.md">完整文档中心</a> ·
    <a href="./docs/quick-start/README.md">快速开始</a> ·
    <a href="./docs/api-reference/README.md">API 参考</a>
</p>

> QEasy DataHub 是轻易云 iPaaS 生态中的开源项目，聚焦企业级数据集成、流程自动化、连接器能力沉淀与开放接口实践。本首页仅保留项目概览与快速入口，完整产品文档请进入 [docs/README.md](./docs/README.md)。

<p align="center">
    <img src="https://static.qeasy.cloud/common/static/data_integration_flow_dark.png" alt="轻易云数据集成流程图" width="920" />
</p>

## 项目简介

轻易云 iPaaS（Integration Platform as a Service）由广东轻亿云软件科技有限公司研发，面向企业提供异构系统连接、数据采集与转换、流程编排、调度监控以及开放集成能力。

这个仓库当前包含两部分核心内容：

- **文档中心**：覆盖平台介绍、快速开始、使用指南、连接器、开发者文档、API 参考与行业解决方案。
- **FastAPI 起步工程**：位于 `src/`，提供一个可直接启动的 Python 服务骨架，便于扩展开放接口、状态检测与项目元信息服务。

## 为什么使用 QEasy DataHub

- **500+ 预置连接器**：覆盖 ERP、CRM、OA、电商、数据库与 SaaS 系统。
- **可视化集成能力**：支持低代码配置、字段映射、流程编排与任务调度。
- **实时同步机制**：支持 CDC、断点续传、双队列池与异常重试。
- **企业级安全体系**：支持权限隔离、审计追踪与加密传输。
- **开放扩展友好**：支持 API、Webhook、自定义连接器与脚本扩展。

## 仓库内容

| 路径 | 说明 |
|------|------|
| `docs/` | 轻易云 DataHub 全量文档中心 |
| `src/` | 基础 FastAPI 项目骨架 |
| `tests/` | FastAPI 示例测试 |
| `scripts/` | 文档链接检查脚本等辅助工具 |
| `pyproject.toml` | Python 项目依赖与开发配置 |

## 文档入口

为避免与 [docs/README.md](./docs/README.md) 重复，首页只保留高频入口：

- [文档总览](./docs/README.md)
- [快速开始](./docs/quick-start/README.md)
- [使用指南](./docs/guide/README.md)
- [连接器文档](./docs/connectors/README.md)
- [解决方案](./docs/solutions/README.md)
- [开发者文档](./docs/developer/README.md)
- [API 参考](./docs/api-reference/README.md)
- [FAQ](./docs/faq/README.md)

## FastAPI 起步工程

仓库已在 `src/` 下初始化一个最小可运行的 FastAPI 项目，提供以下基础能力：

- `/`：项目欢迎页与入口信息
- `/api/v1/health`：健康检查
- `/api/v1/project`：项目元信息接口
- `/docs`：Swagger UI
- `/redoc`：ReDoc

### 本地启动

```bash
pip install -e ".[dev]"
uvicorn app.main:app --app-dir src --reload
```

启动后可访问：

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/api/v1/health`

## 架构展示

<p align="center">
    <img src="https://static.qeasy.cloud/common/static/qeasy_architecture_v3.jpg" alt="轻易云架构图" width="920" />
</p>

## 开源协作

为便于社区协作，仓库已补充常见开源项目配套文件：

- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)
- [SECURITY.md](./SECURITY.md)
- [NOTICE](./NOTICE)

欢迎通过 Issue、Pull Request 或文档修订参与共建。

## 品牌与支持

- **官网**：[https://www.qeasy.cloud/](https://www.qeasy.cloud/)
- **联系页面**：[https://www.qeasy.cloud/contact](https://www.qeasy.cloud/contact)
- **文档中心**：[docs/README.md](./docs/README.md)
- **版本协议**：[LICENSE](./LICENSE)

## License

本项目采用 [Apache License 2.0](./LICENSE) 开源。
