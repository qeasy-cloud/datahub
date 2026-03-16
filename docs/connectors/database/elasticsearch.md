# Elasticsearch 集成专题

本文档详细介绍轻易云 iPaaS 平台与 Elasticsearch 搜索引擎的集成配置方法，涵盖连接器配置、索引管理、数据写入策略以及全文检索最佳实践。

---

## 概述

Elasticsearch 是基于 Apache Lucene 构建的分布式全文搜索和分析引擎，广泛应用于日志分析、全文检索、业务数据分析、监控告警等场景。轻易云 iPaaS 提供专用的 Elasticsearch 连接器，支持以下核心能力：

- **数据写入**：支持单条和批量索引写入（Bulk API）
- **数据查询**：支持 DSL 查询语法，灵活检索数据
- **索引管理**：支持索引的创建、映射配置和别名管理
- **数据同步**：支持从关系型数据库实时同步至 Elasticsearch

### 适用版本

| Elasticsearch 版本 | 支持状态 | 说明 |
|-------------------|----------|------|
| ES 7.x | ✅ 推荐 | 主流版本，功能完善 |
| ES 8.x | ✅ 推荐 | 最新版本，性能最佳 |
| OpenSearch 1.x/2.x | ✅ 支持 | 兼容 ES 7.x API |

---

## 连接器配置

### 创建连接器

1. 登录轻易云 iPaaS 控制台，进入**连接器管理**页面
2. 点击**新建连接器**，选择**数据库**分类下的 **Elasticsearch**
3. 填写连接参数（详见下方参数说明）
4. 点击**测试连接**验证连通性
5. 连接成功后点击**保存**

### 连接参数说明

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `hosts` | string | ✅ | ES 节点地址，多个节点用逗号分隔，如 `http://es1:9200,http://es2:9200` |
| `username` | string | — | 认证用户名（启用安全认证时必填） |
| `password` | string | — | 认证密码 |
| `use_ssl` | boolean | — | 是否使用 HTTPS 连接 |
| `api_key` | string | — | API Key 认证（与用户名/密码二选一） |

#### 连接字符串示例

```json
{
  "hosts": "https://es.example.com:9200",
  "username": "elastic",
  "password": "your_secure_password",
  "use_ssl": true
}
```

> [!TIP]
> 生产环境建议启用 X-Pack Security 或 OpenSearch Security 插件，使用 HTTPS 加密通信。

---

## 典型应用场景

### 业务数据全文检索

将 ERP、CRM 等系统的业务数据同步至 Elasticsearch，构建企业级搜索引擎：

```mermaid
flowchart LR
    A[ERP/CRM 数据] --> B[轻易云 iPaaS]
    B --> C[Elasticsearch]
    C --> D[搜索服务 API]
    D --> E[前端搜索页面]
    
    style B fill:#fff3e0,stroke:#ef6c00
    style C fill:#e8f5e9,stroke:#2e7d32
```

### 日志与监控分析

将多个业务系统的日志集中写入 Elasticsearch，实现统一的日志检索和分析：

| 场景 | 数据来源 | 写入方式 | 说明 |
|------|----------|----------|------|
| 集成日志 | 轻易云 iPaaS | 实时写入 | 集成方案执行日志 |
| 业务审计 | ERP/OA 系统 | 定时同步 | 业务操作审计日志 |
| 异常监控 | 各业务系统 | 事件驱动 | 异常事件汇聚分析 |

---

## 写入优化

### Bulk 批量写入

对于大数据量场景，建议使用 Bulk API 批量写入：

| 参数 | 建议值 | 说明 |
|------|--------|------|
| 批量大小 | 500~2000 条 | 平衡内存占用和写入效率 |
| 刷新间隔 | `30s` | 写入密集时适当调大 `refresh_interval` |
| 副本数 | 批量导入时设为 `0` | 完成后恢复副本数 |

> [!WARNING]
> 批量导入大数据量时，建议临时关闭副本和调大刷新间隔，完成后恢复原设置。

---

## 常见问题

### Q: 写入报错 "mapper_parsing_exception"？

字段类型与索引映射不匹配。请检查目标索引的 Mapping 定义，确保写入数据的字段类型与映射一致。

### Q: 查询返回数据不全？

Elasticsearch 默认返回前 10000 条结果。如需检索更多数据，可使用 `scroll` API 或 `search_after` 分页方式。

---

## 相关资源

- [数据库类连接器概览](./README) — 查看所有支持的数据库连接器
- [配置连接器](../../guide/configure-connector) — 连接器基础配置指南
- [批量数据处理](../../advanced/batch-processing) — 大数据量处理最佳实践

---

> [!NOTE]
> 本文档持续更新中，如有疑问请联系轻易云技术支持团队。
