# 进阶应用

本章介绍轻易云 iPaaS 平台的高级功能与进阶使用技巧，帮助你应对复杂的业务集成场景，提升数据集成效率与可靠性。适用于已完成基础学习、需要深入掌握平台高级能力的用户。

> [!IMPORTANT]
> 本章内容需要登录平台账号后查看完整文档。部分功能（如 CDC 实时同步、高可用配置）需要企业版授权。

## 本章内容概览

```mermaid
mindmap
  root((进阶应用))
    数据转换与处理
      高级数据转换
      自定义函数
      解析器应用
      字段格式化
    集成策略与调度
      集成策略模式
      链式触发方案
      事件驱动架构
    数据查询与过滤
      高级查询条件引擎
      自定义查询条件
      数据联查关系
    复杂数据处理
      [数据聚合写入](./data-aggregation)
      批量数据处理
      多维数据拍扁
    数据一致性
      写入结果回写
      数据补漏措施
      响应数据强控
    系统扩展与集成
      RESTful API Adapter
      自定义脚本
      消息推送集成
    高阶运维
      CDC 实时同步
      异常处理机制
      性能优化
      高可用配置
      安全策略
```

## 适用场景

本章内容适用于以下业务场景：

| 场景类型 | 描述 | 推荐文档 |
| -------- | ---- | -------- |
| **复杂数据转换** | 需要处理嵌套数据结构、多层级映射、条件转换 | [高级数据转换](./data-transformation)、[自定义函数](./custom-scripts) |
| **大规模数据处理** | 处理海量单据、需要分组合并运算 | [数据聚合写入](./data-aggregation)、[批量数据处理](./batch-processing) |
| **实时数据同步** | 要求秒级延迟的数据同步场景 | [CDC 实时同步](./cdc-realtime) |
| **事件驱动架构** | 多系统联动、方案间相互触发 | [集成策略模式](#)、[链式触发方案](#) |
| **数据质量保障** | 需要保证数据一致性、完整性 | [数据补漏](#)、[写入结果回写](#) |
| **系统深度集成** | 对接外部系统、自定义 API 适配 | [RESTful API Adapter](#)、[开发者指南](../developer/guide) |

## 前置条件

学习本章内容前，请确保已具备以下基础：

1. **平台基础操作**
   - 已完成[快速开始](../quick-start/first-integration)章节学习
   - 熟悉[使用指南](../guide/platform-overview)中的基础功能
   - 掌握连接器配置与数据映射的基本操作

2. **技术知识储备**
   - 了解 JSON 数据格式与基本操作
   - 熟悉 RESTful API 基本概念
   - 具备基础的数据库查询知识（SQL）

3. **环境准备**
   - 已注册并登录轻易云 iPaaS 平台
   - 拥有集成方案的配置权限
   - 企业版用户可使用全部高级功能

> [!TIP]
> 建议在正式环境应用高级功能前，先在测试环境充分验证配置效果。

## 推荐学习路径

根据你的业务需求，可选择以下学习路径：

### 路径一：数据处理专家

适合需要深度处理复杂数据结构的场景。

```mermaid
flowchart LR
    A[高级数据转换] --> B[自定义函数]
    B --> C[解析器应用]
    C --> D[数据聚合写入]
    D --> E[批量数据处理]

    style A fill:#e3f2fd
    style E fill:#e8f5e9
```

学习顺序：
1. [高级数据转换](./data-transformation) — 掌握复杂映射规则
2. [自定义函数](./custom-scripts) — 学习 `_function` 表达式与 `_findCollection` 查询
3. [解析器应用](#) — 了解内置解析器的使用场景
4. [数据聚合写入](./data-aggregation) — 掌握分组合并运算
5. [批量数据处理](./batch-processing) — 优化大数据量处理性能

### 路径二：集成架构师

适合设计复杂集成架构、多系统联动场景。

```mermaid
flowchart LR
    A[集成策略模式] --> B[链式触发方案]
    B --> C[事件驱动架构]
    C --> D[CDC 实时同步]
    D --> E[高可用配置]

    style A fill:#e3f2fd
    style E fill:#e8f5e9
```

学习顺序：
1. [集成策略模式](#) — 理解定时异步、实时同步、事件触发等模式
2. [链式触发方案](./chain-trigger) — 掌握方案间相互触发的配置方法
3. [CDC 实时同步](./cdc-realtime) — 实现基于数据库日志的实时同步
4. [异常处理机制](./error-handling) — 设计容错与恢复策略
5. [高可用配置](./high-availability) — 部署集群与故障转移

### 路径三：数据质量工程师

适合关注数据一致性、完整性的场景。

```mermaid
flowchart LR
    A[高级查询条件引擎] --> B[数据联查关系]
    B --> C[写入结果回写]
    C --> D[数据补漏措施]
    D --> E[业务数据建模]

    style A fill:#e3f2fd
    style E fill:#e8f5e9
```

学习顺序：
1. [高级查询条件引擎](#) — 精准过滤源数据
2. [数据联查关系](#) — 实现跨方案数据关联
3. [写入结果回写](#) — 确保上下游数据一致性
4. [数据补漏措施](#) — 处理异常与缺失数据
5. [业务数据建模](./data-modeling) — 规范数据类型与结构

## 核心功能详解

### 数据转换与处理

#### 自定义函数

平台支持通过 `_function` 前缀编写高级表达式，实现复杂的数据计算：

```sql
-- 时间戳转换
_function FROM_UNIXTIME({{LAST_SYNC_TIME}}-600, '%Y-%m-%d %H:%i:%s')

-- 数值计算
_function {{details_list.tax}} * 100

-- 条件判断
_function CASE '{{FOrgId}}' WHEN '100' THEN {{price}}*{{qty}} WHEN '200' THEN '201' ELSE '{{FOrgId}}' END

-- 聚合计算
_function SUM({{details_list.qty}})
```

#### 跨方案数据查询

使用 `_findCollection` 从其他集成方案中查询关联数据：

```sql
_findCollection find FPOOrderEntry_FEntryId from 8e620793-bebb-3167-95a4-9030368e5262 where FBillNo={{outer_no}} FMaterialId_FNumber={{details_list.goods_no}}
```

> [!NOTE]
> 语法各部分之间必须使用**单个英文空格**分隔，多个条件为 `AND` 关系。

### 集成策略模式

平台支持 8 种策略模式组合，满足不同的业务场景需求：

| 读取策略 | 写入策略 | 适用场景 |
| -------- | -------- | -------- |
| 定时异步 | 定时异步 | 常规批量同步，最常用模式 |
| 定时异步 | 实时同步 | 批量读取后实时写入 |
| 定时异步 | 事件触发 | 读取后触发下游方案 |
| 事件触发 | 实时同步 | 全链路实时处理 |
| 事件触发 | 事件触发 | 多级方案链式触发 |

### 数据聚合写入

处理海量单据时，可通过配置 `groupCalculate` 实现分组合并运算：

```json
{
  "groupCalculate": {
    "headerGroup": ["shop_no", "stock_no"],
    "bodyGroup": ["details_spec"],
    "bodyName": "details",
    "targetBodyName": "FEntity",
    "bodyMaxLine": 50,
    "calculate": {
      "details_num": "$sum",
      "details_amount": "$sum"
    }
  }
}
```

支持的聚合表达式：`$sum`、`$avg`、`$min`、`$max`、`$push`、`$addToSet`、`$first`、`$last`。

## 章节导航

| 文档 | 说明 | 难度 |
| ---- | ---- | ---- |
| [高级数据转换](./data-transformation) | 复杂数据转换规则与函数 | ⭐⭐⭐ |
| [自定义脚本](./custom-scripts) | 使用脚本实现自定义逻辑 | ⭐⭐⭐⭐ |
| [CDC 实时同步](./cdc-realtime) | 基于 CDC 的实时数据捕获 | ⭐⭐⭐⭐ |
| [批量数据处理](./batch-processing) | 大批量数据处理最佳实践 | ⭐⭐⭐ |
| [异常处理机制](./error-handling) | 容错设计与异常恢复 | ⭐⭐⭐ |
| [性能优化](./performance-tuning) | 提升集成任务执行效率 | ⭐⭐⭐⭐ |
| [高可用配置](./high-availability) | 集群部署与故障转移 🅿️RO | ⭐⭐⭐⭐⭐ |
| [安全策略](./security-policies) | 数据加密与访问控制 🅿️RO | ⭐⭐⭐⭐ |

> [!TIP]
> 标注 🅿️RO 的内容需要企业版授权使用。

## 最佳实践

### 1. 渐进式应用

不要一次性应用所有高级功能。建议：
- 先在单个方案中验证高级功能效果
- 确认无误后再推广到生产环境
- 保留基础配置作为回退方案

### 2. 性能考量

| 功能 | 性能影响 | 优化建议 |
| ---- | -------- | -------- |
| 自定义函数 | 中等 | 避免在循环中调用复杂函数 |
| 数据聚合 | 较高 | 合理设置 `bodyMaxLine` 限制 |
| 跨方案查询 | 较高 | 确保被查询方案已建立索引 |
| CDC 实时同步 | 低 | 监控数据库日志增长情况 |

### 3. 调试技巧

- 使用[调试器](../guide/debugger)逐步验证数据转换结果
- 开启详细日志记录中间状态
- 利用[数据与队列管理](../guide/data-queue-management)查看处理详情

## 相关资源

- [使用指南](../guide/platform-overview) — 基础功能参考
- [开发者文档](../developer/guide) — 扩展开发指南
- [FAQ](../faq) — 常见问题解答
- [API 参考](../api-reference/README) — 开放接口文档

---

> [!NOTE]
> 本章文档持续更新中，如有疑问请通过平台内反馈渠道或查阅[更新日志](../changelog)了解最新变更。
