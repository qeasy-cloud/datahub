# 平台简介

轻易云 iPaaS 集成平台是一款企业级数据集成与流程自动化平台，致力于帮助企业打破数据孤岛，实现异构系统间的无缝连接与数据实时同步。平台采用云原生架构设计，支持可视化配置、低代码开发，让复杂的系统集成变得简单高效。

通过轻易云，你可以轻松连接 ERP、CRM、OA、电商平台、数据库等 500+ 主流系统，构建企业级的数据集成解决方案。无论是制造业的 MES 与 ERP 对接、零售业的电商与财务系统同步，还是 SaaS 应用之间的数据流转，轻易云都能提供稳定、安全、高效的集成能力。

## 平台架构

轻易云 iPaaS 采用分层架构设计，从底层数据源到上层应用服务，形成完整的数据集成生态体系。

```mermaid
flowchart TB
    subgraph 数据源层
        ERP[ERP 系统<br/>金蝶/用友/SAP]
        CRM[CRM 系统<br/>Salesforce/纷享销客]
        OA[OA 系统<br/>钉钉/飞书/企业微信]
        EC[电商平台<br/>淘宝/京东/拼多多]
        DB[数据库<br/>MySQL/Oracle/MongoDB]
        API[第三方 API]
    end

    subgraph 连接层
        CONN[连接器引擎<br/>Connector Engine]
        AUTH[认证中心<br/>OAuth/Token/密钥]
        PROTO[协议适配<br/>REST/SOAP/JDBC]
    end

    subgraph 处理层
        QUEUE[队列池<br/>Queue Pool]
        MAPPING[数据映射<br/>Data Mapping]
        TRANS[数据转换<br/>Transformation]
        SCRIPT[自定义脚本<br/>Groovy/Python]
    end

    subgraph 存储层
        MONGO[MongoDB<br/>数据缓存]
        REDIS[Redis<br/>队列/状态]
        LOG[日志存储<br/>Elasticsearch]
    end

    subgraph 服务层
        SCHEDULER[任务调度<br/>Scheduler]
        MONITOR[监控告警<br/>Monitoring]
        DEBUG[调试器<br/>Debugger]
        WEBHOOK[事件驱动<br/>Webhook]
    end

    ERP --> CONN
    CRM --> CONN
    OA --> CONN
    EC --> CONN
    DB --> CONN
    API --> CONN

    CONN --> QUEUE
    AUTH --> CONN
    PROTO --> CONN

    QUEUE --> MAPPING
    MAPPING --> TRANS
    TRANS --> SCRIPT

    SCRIPT --> MONGO
    QUEUE --> REDIS
    TRANS --> LOG

    MONGO --> SCHEDULER
    REDIS --> SCHEDULER
    SCHEDULER --> MONITOR
    MONITOR --> DEBUG
    WEBHOOK --> QUEUE

    style CONN fill:#e3f2fd,stroke:#1565c0
    style QUEUE fill:#fff3e0,stroke:#ef6c00
    style MAPPING fill:#e8f5e9,stroke:#2e7d32
    style SCHEDULER fill:#f3e5f5,stroke:#7b1fa2
```

### 核心组件说明

| 组件 | 功能描述 | 技术特点 |
|------|----------|----------|
| 连接器引擎 | 统一管理各类系统连接 | 支持 500+ 系统，标准化接口定义 |
| 队列池 | 任务调度与负载均衡 | 基于 Redis 的高性能队列，支持优先级 |
| 数据映射 | 字段映射与值转换 | 可视化配置，支持复杂嵌套结构 |
| 数据缓存 | 中间数据存储 | MongoDB 文档存储，支持海量数据 |
| 调试器 | 方案调试与问题定位 | 实时日志、单步调试、命令行工具 |

## 数据流向

轻易云的数据集成遵循标准的 ETL（Extract-Transform-Load）流程，同时支持实时 CDC（Change Data Capture）模式，满足不同业务场景的需求。

```mermaid
sequenceDiagram
    participant S as 源系统
    participant C as 连接器
    participant Q as 队列池
    participant P as 数据加工厂
    participant M as 数据映射
    participant T as 目标系统

    Note over S,T: 定时调度或事件触发
    
    S->>C: 1. 发起数据查询请求
    C->>S: 返回原始数据
    C->>Q: 2. 生成源队列任务
    
    loop 队列调度
        Q->>P: 3. 取出任务进行处理
        P->>P: 数据清洗/格式转换
        P->>P: 字段映射与计算
        P->>M: 值格式化与解析
        M->>Q: 4. 生成目标写入队列
    end
    
    loop 写入调度
        Q->>C: 5. 执行目标写入
        C->>T: 写入业务数据
        T-->>C: 返回写入结果
        C->>Q: 6. 更新任务状态
    end
    
    Note over S,T: 完成数据同步
```

### 数据处理流程

```mermaid
flowchart LR
    A[数据抽取<br/>Extract] --> B[数据清洗<br/>Clean]
    B --> C[字段映射<br/>Map]
    C --> D[值转换<br/>Transform]
    D --> E[数据加载<br/>Load]
    E --> F[结果回写<br/>Writeback]

    A -->|查询接口| SRC[源系统]
    E -->|写入接口| TGT[目标系统]

    style A fill:#e3f2fd,stroke:#1565c0
    style C fill:#fff3e0,stroke:#ef6c00
    style E fill:#e8f5e9,stroke:#2e7d32
```

1. **数据抽取（Extract）**：通过连接器从源系统获取数据，支持全量同步和增量同步两种模式
2. **数据清洗（Clean）**：对原始数据进行过滤、去重、验证，确保数据质量
3. **字段映射（Map）**：将源系统字段映射到目标系统字段，支持一对一、一对多、多对一映射
4. **值转换（Transform）**：对字段值进行格式化、计算、解析等处理
5. **数据加载（Load）**：将处理后的数据写入目标系统
6. **结果回写（Writeback）**：将写入结果回传至源系统或数据管理模块

## 核心术语表

### 连接器（Connector）

连接器是轻易云平台与外部系统建立通信的桥梁，用于配置和管理与特定系统的连接信息。

```mermaid
flowchart LR
    subgraph 连接器配置
        ENV[运行环境]
        AUTH[认证信息]
        PARAM[连接参数]
    end

    subgraph 支持的环境
        PROD[生产环境<br/>env_production]
        TEST[测试环境<br/>env_test]
        DEV[开发环境<br/>env_development]
    end

    ENV --> PROD
    ENV --> TEST
    ENV --> DEV

    style PROD fill:#ffebee,stroke:#c62828
    style TEST fill:#fff3e0,stroke:#ef6c00
    style DEV fill:#e3f2fd,stroke:#1565c0
```

连接器支持多环境隔离，你可以分别为开发、测试、生产环境配置不同的连接参数，确保数据安全。在方案正式上线前，务必切换至生产环境。

### 集成方案（Integration Strategy）

集成方案是轻易云平台的核心概念，代表一种具体的业务数据对接策略。每个方案定义了从哪个源系统获取数据、如何处理数据、最终写入哪个目标系统的完整流程。

> [!TIP]
> 一个集成方案对应一种业务场景，例如：
> - 金蝶云星空 → 旺店通：销售订单同步
> - 钉钉审批 → 金蝶云星空：费用报销单对接
> - MySQL → MongoDB：数据归档迁移

### 数据映射（Data Mapping）

数据映射用于解决不同系统间基础数据编码不一致的问题。当源系统的「客户编码」与目标系统的「客户编码」存在差异时，通过数据映射关系实现准确转换。

```mermaid
flowchart LR
    A[源系统<br/>客户编码: C001] -->|映射关系| MAP[数据映射表]
    MAP -->|转换| B[目标系统<br/>客户编码: 10001]

    style MAP fill:#fff3e0,stroke:#ef6c00
```

数据映射支持 Excel 批量导入，格式如下：

| 源值 | 源标签 | 目标值 | 目标标签 |
|------|--------|--------|----------|
| C001 | 张三科技 | 10001 | 张三科技有限公司 |
| C002 | 李四贸易 | 10002 | 李四贸易有限公司 |

### 值格式化（Value Formatter）

值格式化用于对字段值进行格式转换和处理，满足目标系统的数据格式要求。

支持的标准格式类型：

| 格式类型 | 说明 | 示例 |
|----------|------|------|
| `date` | 日期格式 | `2024-03-15` |
| `dateTime` | 日期时间格式 | `2024-03-15 14:30:00` |
| `amount` | 金额千分位 | `¥1,000.00` |
| `intval` | 整数转换 | `100` |
| `round(2)` | 浮点精度控制 | `99.99` |
| `implode(',')` | 数组转字符串 | `a,b,c` |

```json
{
  "formatResponse": [
    {
      "old": "delivery_date",
      "new": "formatted_date",
      "format": "date"
    }
  ]
}
```

### 队列（Queue）

队列是轻易云平台实现异步任务调度的核心机制，采用先进先出（FIFO）原则管理集成任务。

```mermaid
flowchart TB
    subgraph 队列池架构
        RQ[请求队列池<br/>Request Queue]
        WQ[写入队列池<br/>Write Queue]
        REDIS[(Redis<br/>分布式队列)]
    end

    subgraph 队列状态
        PENDING[等待中]
        PROCESSING[处理中]
        COMPLETED[已完成]
        FAILED[失败重试]
    end

    RQ --> REDIS
    WQ --> REDIS
    REDIS --> PENDING
    PENDING --> PROCESSING
    PROCESSING --> COMPLETED
    PROCESSING --> FAILED
    FAILED -->|重试机制| PENDING

    style REDIS fill:#fff3e0,stroke:#ef6c00
    style FAILED fill:#ffebee,stroke:#c62828
    style COMPLETED fill:#e8f5e9,stroke:#2e7d32
```

队列的主要特性：
- **异步处理**：解耦数据查询与写入操作，提升系统吞吐量
- **负载均衡**：根据系统负载动态调整并发数
- **失败重试**：自动重试失败任务，支持自定义重试次数
- **优先级调度**：支持任务优先级设置，确保关键业务优先处理

### 调试器（Debugger）

调试器是集成方案开发与运维阶段的重要工具，提供命令行接口用于测试连接、手动触发任务、查看系统状态等操作。

常用调试命令：

| 命令 | 简写 | 功能描述 |
|------|------|----------|
| `connect-source` | `cs` | 测试源系统连接 |
| `connect-target` | `ct` | 测试目标系统连接 |
| `invoke-source` | `is` | 手动调用源系统查询 |
| `invoke-target` | `it` | 手动调用目标系统写入 |
| `dispatch-source` | `ds` | 生成源查询队列 |
| `dispatch-target` | `dt` | 生成目标写入队列 |
| `db-info` | `dbi` | 查看 MongoDB 数据库信息 |
| `db-reset-status` | `dbrs` | 重置异常数据状态 |

> [!WARNING]
> `db-clean-data`、`db-clean-job`、`db-clean-all` 等清空操作会永久删除数据，请谨慎使用。

## 产品优势

```mermaid
mindmap
  root((轻易云<br/>iPaaS 平台))
    高效集成
      500+ 预置连接器
      可视化配置
      2 小时快速上线
    稳定可靠
      分布式架构
      自动故障转移
      数据一致性保障
    灵活扩展
      自定义脚本
      开放 API
      插件化架构
    安全合规
      军工级加密
      多环境隔离
      操作审计
```

- **开箱即用**：预置 500+ 主流系统连接器，无需额外开发
- **低代码配置**：可视化界面操作，降低技术门槛
- **高性能处理**：分布式队列架构，支持百万级数据同步
- **灵活扩展**：支持 Groovy、Python 自定义脚本，满足个性化需求
- **安全可靠**：多层次安全防护，企业级数据加密

## 下一步

- [账号注册](./registration) - 创建轻易云账号，开通数据集成服务
- [环境配置](./environment-setup) - 配置开发与生产环境
- [第一个集成流程](./first-integration) - 快速上手，完成首个数据同步方案
