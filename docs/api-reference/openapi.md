# OpenAPI 文档

本文档介绍轻易云 iPaaS 平台的 OpenAPI 规范文档，帮助开发者快速了解接口定义、自动生成客户端代码，并与主流 API 工具集成。

---

## 概述

轻易云 iPaaS 提供符合 OpenAPI 3.0 规范的接口描述文件，支持开发者通过标准化的 API 定义文档快速接入平台能力。你可以利用 OpenAPI 文档完成以下操作：

- **API 文档浏览**：通过 Swagger UI 在线浏览和测试接口
- **客户端代码生成**：使用 OpenAPI Generator 自动生成多语言 SDK
- **接口测试**：导入 Postman、Insomnia 等工具进行接口调试
- **API 网关集成**：将 OpenAPI 文档导入企业 API 网关

## OpenAPI 规范版本

| 规范版本 | 支持状态 | 说明 |
|---------|----------|------|
| OpenAPI 3.0 | ✅ 当前版本 | 主要接口文档格式 |
| Swagger 2.0 | ✅ 兼容导出 | 向下兼容旧版工具 |

## 接口分类

轻易云 iPaaS 的开放接口按功能模块分为以下几类：

| 模块 | 路径前缀 | 说明 |
|------|----------|------|
| **认证授权** | `/v2/oauth` | Token 获取与管理 |
| **数据推送** | `/v2/open-api/business/{scheme_id}/store` | 向集成方案推送数据 |
| **数据查询** | `/v2/open-api/business/{scheme_id}/query` | 从集成方案查询数据 |
| **方案管理** | `/v2/open-api/scheme` | 集成方案的查询与管理 |
| **日志查询** | `/v2/open-api/log` | 集成执行日志查询 |

## 使用方式

### Swagger UI 在线浏览

访问以下地址可在线查看和测试 API：

```text
https://api.qeasy.cloud/swagger-ui/
```

### Postman 导入

1. 打开 Postman，点击 **Import**
2. 选择 **Link** 标签页
3. 输入 OpenAPI 文档地址
4. 点击 **Continue**，完成导入
5. 在生成的 Collection 中设置环境变量（`base_url`、`access_token` 等）

### 代码生成

使用 OpenAPI Generator 自动生成客户端代码：

```bash
openapi-generator-cli generate \
  -i https://api.qeasy.cloud/v2/openapi.json \
  -g python \
  -o ./qeasy-client
```

支持的语言包括：Python、Java、TypeScript、Go、C# 等。

> [!TIP]
> 生成的客户端代码已包含认证、请求签名等基础逻辑，可直接用于项目开发。

## 认证说明

所有业务接口均需要 Bearer Token 认证。在 OpenAPI 文档中，认证方式定义为：

```yaml
securitySchemes:
  BearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT
```

详细的认证流程请参阅 [认证指南](./authentication)。

## 常见问题

### Q: OpenAPI 文档多久更新一次？

API 文档随平台版本同步更新。每次发布新版本时，OpenAPI 文档会自动生成并部署。

### Q: 如何获取特定版本的 API 文档？

可通过版本号访问历史版本文档，如 `/v2/openapi.json`。建议始终使用最新版本的 API。

---

## 相关资源

- [API 概览](./README) — API 使用入门
- [认证指南](./authentication) — 认证授权详细说明
- [接口列表](./endpoints) — 完整接口端点文档
- [错误码](./error-codes) — 错误码与排查指南
