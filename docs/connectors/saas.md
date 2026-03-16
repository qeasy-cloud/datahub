# CRM / SaaS 类连接器概览

轻易云 iPaaS 平台提供丰富的 SaaS 应用连接器，覆盖 CRM、人力资源、营销自动化等多个领域，帮助企业实现 SaaS 应用与企业内部系统的无缝集成。

## SaaS 连接器介绍

SaaS（Software as a Service，软件即服务）连接器帮助企业在云应用与本地系统之间建立数据桥梁，实现以下核心能力：

- **客户数据同步**：CRM 系统与 ERP、电商平台客户信息同步
- **销售流程集成**：销售线索、商机、订单的自动流转
- **营销自动化**：营销数据与客户行为数据的整合分析
- **人力资源集成**：招聘、考勤、薪酬数据的统一管理
- **服务管理对接**：工单、服务请求的全流程跟踪

```mermaid
flowchart TB
    subgraph SaaS[SaaS 应用]
        A[CRM 系统]
        B[HR 系统]
        C[营销自动化]
        D[客服系统]
    end
    
    subgraph iPaaS[轻易云 iPaaS]
        E[SaaS 连接器]
        F[数据映射]
        G[流程编排]
    end
    
    subgraph Enterprise[企业系统]
        H[ERP 系统]
        I[财务系统]
        J[OA 系统]
        K[数据中台]
    end
    
    A <--> E
    B <--> E
    C <--> E
    D <--> E
    E --> F
    F --> G
    G --> H
    G --> I
    G --> J
    G --> K
    
    style SaaS fill:#e3f2fd
    style iPaaS fill:#fff3e0
    style Enterprise fill:#e8f5e9
```

## 支持的 SaaS 应用列表

### CRM 系统

| 系统名称 | 连接器标识 | 主要功能 | 适用场景 |
|---------|-----------|---------|---------|
| [Salesforce](./saas/salesforce) | `salesforce` | 销售、服务、营销 | 跨国企业 |
| [HubSpot](./saas/hubspot) | `hubspot` | 营销、销售、服务 | 中小企业 |
| [纷享销客](./saas/fenxiangxiaoke) | `fenxiangxiaoke` | 销售管理、CRM | 国内企业 |
| [销售易](./saas/xiaoshouyi) | `xiaoshouyi` | 移动 CRM | 销售团队 |
| [Zoho CRM](./saas/zoho) | `zoho` | 全功能 CRM | 中小企业 |

### 人力资源

| 系统名称 | 连接器标识 | 主要功能 | 适用场景 |
|---------|-----------|---------|---------|
| [北森](./saas/beisen) | `beisen` | 招聘、测评、人事 | 中大型组织 |
| [Moka](./saas/moka) | `moka` | 招聘管理 | 招聘流程 |
| [盖雅工场](./saas/guayagongchang) | `guaya` | 劳动力管理 | 考勤排班 |
| [薪人薪事](./saas/xinrenxinshi) | `xinrenxinshi` | 薪酬管理 | 薪资核算 |

### 营销自动化

| 系统名称 | 连接器标识 | 主要功能 | 适用场景 |
|---------|-----------|---------|---------|
| [ConvertLab](./saas/convertlab) | `convertlab` | 营销自动化 | 数字营销 |
| [神策数据](./saas/sensorsdata) | `sensorsdata` | 用户行为分析 | 数据驱动 |
| [GrowingIO](./saas/growingio) | `growingio` | 增长分析 | 产品优化 |

### 客服与支持

| 系统名称 | 连接器标识 | 主要功能 | 适用场景 |
|---------|-----------|---------|---------|
| [Udesk](./saas/udesk) | `udesk` | 智能客服 | 客户服务 |
| [智齿科技](./saas/zhichi) | `zhichi` | 在线客服 | 客服机器人 |
| [美洽](./saas/meiqia) | `meiqia` | 在线客服 | 网站客服 |

### 其他 SaaS

| 系统名称 | 连接器标识 | 主要功能 | 适用场景 |
|---------|-----------|---------|---------|
| [WordPress](./saas/wordpress) | `wordpress` | 内容管理 | 网站建设 |
| [Outreach](./saas/outreach) | `outreach` | 销售参与 | 销售外联 |
| [管荚婆](./saas/guanjiapo) | `guanjiapo` | 进销存 | 小微企业 |
| [小帮帮](./saas/xiaobangbang) | `xiaobangbang` | 业务管理 | 团队协作 |
| [沃时管家婆](./saas/wsgjp) | `wsgjp` | 进销存 | 小微企业 |
| [指掌天下](./saas/zhizhangtianxia) | `zhizhangtianxia` | 业务管理 | 销售管理 |

## 通用配置说明

### 连接配置参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `client_id` | string | ✅ | 应用客户端 ID |
| `client_secret` | string | ✅ | 应用客户端密钥 |
| `access_token` | string | ✅ | 访问令牌 |
| `refresh_token` | string | — | 刷新令牌 |
| `instance_url` | string | — | 实例地址 |
| `api_version` | string | — | API 版本 |

### OAuth 认证流程

```mermaid
sequenceDiagram
    participant User
    participant App
    participant iPaaS
    participant SaaS
    
    User->>App: 授权请求
    App->>SaaS: 跳转授权页
    User->>SaaS: 登录并授权
    SaaS-->>App: 返回授权码
    App->>iPaaS: 提交授权码
    iPaaS->>SaaS: 换取令牌
    SaaS-->>iPaaS: 返回 Access Token
    iPaaS->>iPaaS: 保存令牌
    iPaaS-->>App: 授权成功
```

### 适配器选择

| 适配器名称 | 用途 | 适用场景 |
|-----------|------|---------|
| `SaaSQueryAdapter` | 标准查询 | 数据拉取 |
| `SaaSExecuteAdapter` | 标准写入 | 数据推送 |
| `SaaSBatchAdapter` | 批量操作 | 大数据量 |
| `SaaSEventAdapter` | 事件监听 | 实时同步 |

## 集成场景示例

### 场景一：CRM 与 ERP 客户同步

```mermaid
flowchart LR
    A[CRM 系统] -->|新增客户| B[轻易云 iPaaS]
    B -->|数据转换| C[ERP 系统]
    C -->|创建客户| D[财务系统]
    D -->|信用评估| A
    
    style B fill:#fff3e0
```

**数据映射**：

| CRM 字段 | ERP 字段 | 转换规则 |
|---------|---------|---------|
| `account_name` | `customer_name` | 直接映射 |
| `industry` | `customer_type` | 行业分类映射 |
| `annual_revenue` | `credit_limit` | 收入转信用额度 |
| `billing_address` | `address` | 地址格式化 |

### 场景二：销售订单全链路集成

```mermaid
flowchart TB
    A[CRM 商机] -->|赢单| B[创建报价]
    B -->|审批通过| C[生成订单]
    C --> D[轻易云 iPaaS]
    D --> E[ERP 系统]
    E -->|库存检查| F[库存充足?]
    F -->|是| G[确认订单]
    F -->|否| H[采购/生产]
    G --> I[WMS 发货]
    I --> J[财务开票]
    
    style D fill:#fff3e0
    style F fill:#fff3e0
```

### 场景三：营销数据归因分析

```mermaid
flowchart LR
    A[广告投放] -->|点击数据| B[营销自动化]
    C[网站行为] -->|浏览数据| B
    D[CRM 线索] -->|转化数据| B
    B --> E[轻易云 iPaaS]
    E --> F[数据仓库]
    F --> G[归因分析]
    
    style E fill:#fff3e0
    style F fill:#e8f5e9
```

## 最佳实践

### 1. 数据一致性保障

```mermaid
flowchart TD
    A[数据变更] --> B{来源判断}
    B -->|SaaS 为主| C[SaaS 数据优先]
    B -->|ERP 为主| D[ERP 数据优先]
    B -->|冲突| E[人工介入]
    C --> F[更新目标系统]
    D --> F
    E --> G[记录冲突日志]
    
    style B fill:#fff3e0
    style E fill:#ffebee
```

### 2. 增量同步策略

```json
{
  "syncStrategy": {
    "mode": "incremental",
    "syncField": "last_modified_time",
    "batchSize": 500,
    "conflictResolution": "source_priority",
    "schedule": "0 */30 * * * *"
  }
}
```

### 3. 异常重试机制

| 异常类型 | 重试策略 | 最大重试次数 |
|---------|---------|-------------|
| 网络超时 | 立即重试 | 3 次 |
| 限流错误 | 指数退避 | 5 次 |
| 授权失效 | 刷新令牌 | 自动处理 |
| 数据错误 | 记录日志 | 人工介入 |

## 常见问题

### Q: 如何处理 SaaS 接口限流？

SaaS 应用通常有 API 调用频率限制，建议：

1. **请求队列化**：使用队列缓冲请求
2. **速率限制**：控制请求频率
3. **缓存策略**：缓存不经常变化的数据
4. **批量操作**：尽可能使用批量接口

```python
# 速率限制示例
import time
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=100, period=60)  # 每分钟 100 次
def call_api():
    return api_client.request()
```

### Q: OAuth 令牌过期如何处理？

轻易云 iPaaS 支持自动刷新令牌：

```mermaid
sequenceDiagram
    participant iPaaS
    participant SaaS
    
    iPaaS->>SaaS: 请求 API (过期令牌)
    SaaS-->>iPaaS: 401 未授权
    iPaaS->>iPaaS: 使用 Refresh Token
    iPaaS->>SaaS: 请求新令牌
    SaaS-->>iPaaS: 返回新令牌
    iPaaS->>SaaS: 重试原请求
    SaaS-->>iPaaS: 返回结果
```

### Q: 如何映射不同系统的字段类型？

字段类型映射参考：

| SaaS 类型 | 标准类型 | ERP 类型 | 说明 |
|----------|---------|---------|------|
| `string` | string | VARCHAR | 字符串 |
| `number` | decimal | DECIMAL | 数值 |
| `integer` | int | INT | 整数 |
| `datetime` | datetime | DATETIME | 日期时间 |
| `boolean` | bool | TINYINT | 布尔值 |
| `picklist` | enum | VARCHAR | 枚举值 |

## 相关文档

- [Salesforce 连接器](./saas/salesforce)
- [纷享销客连接器](./saas/fenxiangxiaoke)
- [北森连接器](./saas/beisen)
- [SaaS 集成最佳实践](../standard-schemes/saas-integration)
- [配置连接器](../guide/configure-connector)

> [!NOTE]
> SaaS 应用的 API 会定期更新，请及时关注官方文档和轻易云更新日志，以获取最新功能支持。
