# 产品概览

轻易云 iPaaS 是企业级数据集成平台，帮助企业快速实现异构系统之间的数据打通与业务协同。

## 核心能力

```mermaid
mindmap
  root((轻易云 iPaaS))
    数据集成
      多源异构数据接入
      实时与批量同步
      数据质量管理
    应用集成
      500+ 预置连接器
      API 编排
      流程自动化
    业务协同
      ERP 与电商集成
      OA 审批集成
      业财一体化
```

## 产品架构

```mermaid
flowchart TB
    subgraph 数据源层
        A[ERP 系统]
        B[OA 系统]
        C[电商平台]
        D[数据库]
    end

    subgraph 轻易云 iPaaS
        E[连接器引擎]
        F[数据处理引擎]
        G[流程编排引擎]
        H[调度监控中心]
    end

    subgraph 数据目标层
        I[数据仓库]
        J[业务系统]
        K[BI 平台]
    end

    A --> E
    B --> E
    C --> E
    D --> E
    E --> F
    F --> G
    G --> H
    G --> I
    G --> J
    G --> K

    style E fill:#e3f2fd
    style F fill:#e3f2fd
    style G fill:#e3f2fd
```

## 快速导航

| 模块 | 说明 | 链接 |
|-----|------|------|
| 产品介绍 | 了解产品定位、能力和优势 | [查看详情](./introduction/overview) |
| 快速开始 | 5 分钟上手，创建第一个集成方案 | [立即开始](./quick-start/introduction) |
| 使用指南 | 详细的功能使用说明 | [查看指南](./guide) |
| 连接器 | 已支持的 500+ 系统连接 | [查看连接器](./connectors) |
| 解决方案 | 行业场景解决方案 | [查看方案](./solutions) |
| API 参考 | 完整的 OpenAPI 文档 | [查看 API](./api-reference) |

## 开始使用

> [!TIP]
> 初次使用轻易云 iPaaS？建议从 [快速开始](./quick-start/introduction) 章节开始。

### 1. 注册账号

访问 [轻易云官网](https://www.qeasy.cloud) 注册账号。

### 2. 创建连接器

配置与您的业务系统的连接。

### 3. 设计集成方案

使用可视化设计器配置数据映射和转换规则。

### 4. 运行监控

启动方案并监控执行状态。
