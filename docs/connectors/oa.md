# OA / 协同类连接器概览

轻易云 iPaaS 平台提供全面的 OA（Office Automation，办公自动化）系统连接器，支持钉钉、飞书、企业微信、泛微、致远等主流协同办公平台，帮助企业实现审批流程、组织架构、消息通知等业务的无缝集成。

## OA 连接器介绍

OA 系统是企业日常办公和流程管理的核心平台，涵盖审批流程、考勤管理、组织架构、消息推送等功能。轻易云 iPaaS 的 OA 连接器通过标准化的 API 对接，实现以下核心能力：

- **审批流程集成**：审批单据的自动发起、状态同步、结果回传
- **组织架构同步**：部门、人员信息的实时同步
- **消息通知推送**：系统消息的自动发送和提醒
- **考勤数据对接**：打卡记录、请假数据的自动采集
- **文件附件传输**：审批附件的上传下载

```mermaid
flowchart TB
    subgraph OA[OA 系统]
        A[审批流程]
        B[组织架构]
        C[考勤管理]
        D[消息中心]
    end
    
    subgraph iPaaS[轻易云 iPaaS]
        E[OA 连接器]
        F[流程编排]
        G[事件监听]
    end
    
    subgraph Business[业务系统]
        H[ERP 系统]
        I[HR 系统]
        J[财务系统]
        K[自定义应用]
    end
    
    A <--> E
    B <--> E
    C <--> E
    D <--> E
    E --> F
    F --> H
    F --> I
    F --> J
    F --> K
    G --> A
    
    style OA fill:#e3f2fd
    style iPaaS fill:#fff3e0
    style Business fill:#e8f5e9
```

## 支持的 OA 系统列表

### 互联网协同平台

| 系统名称 | 连接器标识 | 主要功能 | 适用场景 |
|---------|-----------|---------|---------|
| [钉钉](./oa/dingtalk) | `dingtalk` | 审批、考勤、消息、组织架构 | 阿里生态企业 |
| [飞书](./oa/feishu) | `feishu` | 审批、多维表格、消息、会议 | 字节生态企业 |
| [企业微信](./oa/wecom) | `wecom` | 审批、客户联系、应用消息 | 微信生态企业 |

### 传统 OA 系统

| 系统名称 | 连接器标识 | 主要功能 | 适用场景 |
|---------|-----------|---------|---------|
| [泛微 e-cology](./oa/weaver-ecology) | `weaver-ecology` | 复杂流程、知识管理 | 大型集团 |
| [泛微 e-office](./oa/weaver-eoffice) | `weaver-eoffice` | 标准办公、轻量流程 | 中小型企业 |
| [泛微云桥](./oa/fanwei) | `fanwei` | 泛微云产品对接 | 云端部署 |
| [致远 OA](./oa/seeyon-oa) | `seeyon-oa` | 协同办公、业务生成器 | 中大型组织 |
| [致远 A8+](./oa/seeyon-a8) | `seeyon-a8` | 集团管控、多组织 | 大型集团 |
| [蓝凌 OA](./oa/landray) | `landray` | 知识管理、智慧办公 | 知识密集型企业 |

### 低代码平台

| 系统名称 | 连接器标识 | 主要功能 | 适用场景 |
|---------|-----------|---------|---------|
| [简道云](./oa/jiandaoyun) | `jiandaoyun` | 表单、流程、仪表盘 | 快速搭建业务应用 |
| [氚云](./oa/chuanyun) | `chuanyun` | 表单、流程、报表 | 钉钉生态低代码 |
| [道一云](./oa/daoyiyun) | `daoyiyun` | 七巧低代码平台 | 企业微信生态 |
| [H3 BPM](./oa/h3yun) | `h3yun` | 流程管理、业务集成 | 复杂流程场景 |

### 费控报销系统

| 系统名称 | 连接器标识 | 主要功能 | 适用场景 |
|---------|-----------|---------|---------|
| [汇联易](./oa/huilianyi) | `huilianyi` | 费用报销、差旅管理 | 企业费用管控 |

## 审批流集成说明

### 集成模式

```mermaid
flowchart LR
    subgraph Mode1[模式一: 事件触发]
        A[OA 审批事件] --> B[轻易云监听]
        B --> C[业务系统处理]
    end
    
    subgraph Mode2[模式二: 反向发起]
        D[业务系统] --> E[轻易云转换]
        E --> F[发起 OA 审批]
    end
    
    subgraph Mode3[模式三: 双向同步]
        G[OA 审批] <--> H[轻易云] <--> I[业务系统]
    end
    
    style Mode1 fill:#e3f2fd
    style Mode2 fill:#fff3e0
    style Mode3 fill:#e8f5e9
```

#### 模式一：事件触发模式

OA 系统中的审批事件触发业务系统动作：

```mermaid
sequenceDiagram
    participant User
    participant OA
    participant iPaaS
    participant ERP
    
    User->>OA: 提交审批
    OA->>iPaaS: 推送审批事件
    iPaaS->>iPaaS: 数据转换
    iPaaS->>ERP: 创建业务单据
    ERP-->>iPaaS: 返回结果
    iPaaS-->>OA: 回写单据号
    OA->>User: 审批完成通知
```

**适用场景**：
- 采购申请审批通过后自动生成采购订单
- 费用报销审批通过后自动生成财务凭证
- 销售订单审批通过后自动下发仓库

#### 模式二：反向发起模式

业务系统数据触发 OA 审批流程：

```mermaid
sequenceDiagram
    participant ERP
    participant iPaaS
    participant OA
    participant Approver
    
    ERP->>iPaaS: 业务数据推送
    iPaaS->>iPaaS: 生成审批数据
    iPaaS->>OA: 发起审批流程
    OA->>Approver: 通知审批
    Approver->>OA: 审批操作
    OA-->>iPaaS: 审批结果回调
    iPaaS->>ERP: 回写审批状态
```

**适用场景**：
- 电商平台大额订单触发特价审批
- 库存预警触发补货申请审批
- 客户信用超额触发特批发审批

### 审批状态映射

| OA 状态 | 业务含义 | 建议映射 |
|---------|---------|---------|
| `RUNNING` | 审批中 | 待处理 |
| `AGREE` | 已通过 | 已批准 |
| `REFUSE` | 已拒绝 | 已驳回 |
| `TRANSFER` | 已转交 | 处理中 |
| `REVERT` | 已撤销 | 已取消 |

### 常见集成场景

#### 场景一：费用报销集成

```mermaid
flowchart TB
    A[员工提交报销] --> B[OA 审批流程]
    B --> C{审批结果}
    C -->|通过| D[轻易云转换]
    C -->|驳回| E[返回员工]
    D --> F[生成财务凭证]
    F --> G[ERP 财务模块]
    G --> H[付款执行]
    
    style B fill:#fff3e0
    style D fill:#e8f5e9
```

#### 场景二：采购申请集成

```mermaid
flowchart LR
    A[部门提交采购申请] --> B[OA 审批]
    B -->|审批通过| C[轻易云]
    C --> D[生成采购订单]
    D --> E[ERP 系统]
    E --> F[供应商协同]
    
    style B fill:#fff3e0
    style C fill:#e8f5e9
```

#### 场景三：人事审批集成

```mermaid
flowchart TB
    A[员工提交申请] --> B[OA 审批]
    B -->|入职/离职/调岗| C[轻易云]
    C --> D[组织架构同步]
    D --> E[HR 系统]
    D --> F[ERP 系统]
    D --> G[其他业务系统]
    
    style B fill:#fff3e0
    style C fill:#e8f5e9
```

## 通用配置说明

### 连接配置参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `corp_id` | string | ✅ | 企业 ID |
| `app_key` | string | ✅ | 应用标识 |
| `app_secret` | string | ✅ | 应用密钥 |
| `agent_id` | string | — | 应用代理 ID（部分平台需要）|
| `webhook_url` | string | — | 事件回调地址 |

### 事件监听配置

```json
{
  "eventListener": {
    "enabled": true,
    "events": [
      "bpms_instance_change",
      "bpms_task_change",
      "user_add_org",
      "user_modify_org"
    ],
    "callbackUrl": "https://your-domain.com/callback"
  }
}
```

### 常用适配器

| 适配器名称 | 用途 | 适用平台 |
|-----------|------|---------|
| `OAQueryAdapter` | 数据查询 | 通用 |
| `OAExecuteAdapter` | 数据写入 | 通用 |
| `OAEventAdapter` | 事件监听 | 钉钉、飞书 |
| `OAApprovalAdapter` | 审批操作 | 钉钉、飞书、企业微信 |

## 最佳实践

### 1. 审批模板标准化

建议企业统一审批表单的字段命名和数据格式：

| 标准字段 | 字段类型 | 说明 |
|---------|---------|------|
| `applicant` | string | 申请人 |
| `apply_time` | datetime | 申请时间 |
| `amount` | number | 金额 |
| `department` | string | 所属部门 |
| `business_type` | string | 业务类型 |

### 2. 异常重试机制

配置合理的重试策略，确保消息可靠投递：

```json
{
  "retryPolicy": {
    "maxRetries": 3,
    "retryInterval": 5000,
    "exponentialBackoff": true
  }
}
```

### 3. 数据一致性保障

```mermaid
flowchart TD
    A[事件接收] --> B{验证签名}
    B -->|验证通过| C[处理事件]
    B -->|验证失败| D[丢弃事件]
    C --> E{处理结果}
    E -->|成功| F[返回成功]
    E -->|失败| G[记录日志]
    G --> H[进入重试队列]
    
    style B fill:#fff3e0
    style E fill:#fff3e0
```

## 相关文档

- [钉钉连接器](./oa/dingtalk)
- [飞书连接器](./oa/feishu)
- [企业微信连接器](./oa/wecom)
- [审批流集成方案](../standard-schemes/oa-integration)
- [配置连接器](../guide/configure-connector)

> [!TIP]
> 如需了解更多 OA 系统的集成细节，请访问对应连接器的详细文档页面。
