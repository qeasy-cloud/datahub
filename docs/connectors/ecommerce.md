# 电商 / WMS 类连接器概览

轻易云 iPaaS 平台提供全面的电商和仓储管理系统（WMS）连接器，支持主流电商平台、ERP 电商模块以及专业 WMS 系统，帮助企业实现订单、库存、物流数据的实时同步和高效管理。

## 电商连接器介绍

电商连接器是连接企业业务系统与电商平台、WMS 系统的桥梁，实现以下核心能力：

- **订单同步**：电商平台订单自动下载到 ERP / 业务系统
- **库存同步**：实时库存数据推送到电商平台，防止超卖
- **物流回传**：发货信息自动回传到电商平台
- **售后处理**：退款、退货信息的自动同步
- **商品管理**：商品信息、价格、库存的批量管理

```mermaid
flowchart TB
    subgraph Platform[电商平台]
        A[淘宝/天猫]
        B[京东]
        C[拼多多]
        D[抖音电商]
        E[其他平台]
    end
    
    subgraph iPaaS[轻易云 iPaaS]
        F[电商连接器]
        G[数据转换引擎]
        H[路由分发]
    end
    
    subgraph Backend[后端系统]
        I[ERP 系统]
        J[WMS 系统]
        K[财务系统]
        L[CRM 系统]
    end
    
    A --> F
    B --> F
    C --> F
    D --> F
    E --> F
    F --> G
    G --> H
    H --> I
    H --> J
    H --> K
    H --> L
    
    style Platform fill:#e3f2fd
    style iPaaS fill:#fff3e0
    style Backend fill:#e8f5e9
```

## 支持的电商平台列表

### 综合电商平台

| 平台名称 | 连接器标识 | 主要功能 | 支持模式 |
|---------|-----------|---------|---------|
| [旺店通](./ecommerce/wangdian) | `wangdian` | 订单、库存、商品 | 主流通用 |
| [聚水潭](./ecommerce/jushuitan) | `jushuitan` | 订单、库存、采购 | 电商 ERP |
| [管易云](./ecommerce/guanyi) | `guanyi` | 订单、仓储、财务 | 金蝶生态 |
| [网店管家](./ecommerce/wangdianguanjia) | `wangdianguanjia` | 订单、库存、售后 | 老牌电商 ERP |
| [网店精灵](./ecommerce/wangdianjingling) | `wangdianjingling` | 订单处理、批量操作 | 店铺管理工具 |

### 垂直领域平台

| 平台名称 | 连接器标识 | 主要功能 | 适用场景 |
|---------|-----------|---------|---------|
| [万里牛](./ecommerce/maliniu) | `maliniu` | 订单、库存、分销 | 多平台店铺 |
| [快麦](./ecommerce/kuaimai) | `kuaimai` | 订单、仓储、数据 | 光云科技 |
| [班牛](./ecommerce/banniu) | `banniu` | 客服工单、售后 | 客服协同 |
| [易仓](./ecommerce/ecang) | `ecang` | 跨境 ERP | 跨境电商 |

### 平台官方接口

| 平台名称 | 连接器标识 | 主要功能 | 接入方式 |
|---------|-----------|---------|---------|
| 淘宝/天猫 | `taobao` | 订单、商品、物流 | TOP 接口 |
| 京东 | `jd` | 订单、库存、售后 | 宙斯接口 |
| 拼多多 | `pdd` | 订单、物流、售后 | 开放平台 |
| 抖音电商 | `douyin` | 订单、商品、物流 | 抖店接口 |
| 快手电商 | `kuaishou` | 订单、商品、物流 | 开放平台 |

## 订单库存同步说明

### 订单同步流程

```mermaid
sequenceDiagram
    participant Platform
    participant iPaaS
    participant ERP
    participant WMS
    
    Platform->>iPaaS: 新订单推送
    iPaaS->>iPaaS: 数据清洗转换
    iPaaS->>ERP: 创建销售订单
    ERP-->>iPaaS: 返回订单号
    iPaaS->>WMS: 推送发货指令
    WMS-->>iPaaS: 确认接单
    iPaaS-->>Platform: 订单确认
    
    Note over WMS,Platform: 发货环节
    WMS->>iPaaS: 发货完成
    iPaaS->>ERP: 更新订单状态
    iPaaS->>Platform: 上传物流单号
    Platform-->>买家: 显示物流信息
```

### 库存同步策略

```mermaid
flowchart TD
    A[库存变动事件] --> B{同步策略}
    B -->|实时同步| C[立即推送]
    B -->|定时同步| D[批量汇总]
    B -->|阈值同步| E[达到阈值推送]
    
    C --> F[更新平台库存]
    D --> F
    E --> F
    
    style B fill:#fff3e0
```

#### 同步策略对比

| 策略 | 实时性 | 系统压力 | 适用场景 |
|------|--------|---------|---------|
| 实时同步 | 最高 | 高 | 高并发、爆款商品 |
| 定时同步 | 一般 | 低 | 常规商品、多店铺 |
| 阈值同步 | 较高 | 中 | 库存预警、安全库存 |

#### 库存同步公式

```text
可售库存 = 实际库存 - 锁定库存 - 安全库存
         = 可用库存 - 平台在途订单
```

### 数据映射规范

#### 订单字段映射

| 电商平台字段 | 标准字段 | ERP 字段 | 说明 |
|------------|---------|---------|------|
| `tid` | `orderNo` | `FBillNo` | 订单编号 |
| `buyer_nick` | `buyerName` | `FCustName` | 买家昵称 |
| `payment` | `paymentAmount` | `FAmount` | 实付金额 |
| `created` | `orderTime` | `FDate` | 下单时间 |
| `receiver_name` | `receiverName` | `FReceiveName` | 收货人 |
| `receiver_mobile` | `receiverPhone` | `FPhone` | 联系电话 |

#### 商品映射

```mermaid
flowchart LR
    A[平台 SKU] --> B{映射关系}
    B -->|一对一| C[ERP 物料编码]
    B -->|多对一| D[SPU 编码]
    B -->|组合商品| E[套装编码]
    
    style B fill:#fff3e0
```

## 通用配置说明

### 连接配置参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `app_key` | string | ✅ | 应用标识 |
| `app_secret` | string | ✅ | 应用密钥 |
| `shop_id` | string | ✅ | 店铺 ID |
| `platform` | string | ✅ | 平台类型 |
| `session` | string | — | 授权令牌 |
| `environment` | string | — | 环境（prod/sandbox）|

### 适配器选择

| 适配器名称 | 用途 | 适用场景 |
|-----------|------|---------|
| `EcommerceQueryAdapter` | 订单查询 | 拉取平台订单 |
| `EcommerceExecuteAdapter` | 订单操作 | 确认、取消订单 |
| `InventorySyncAdapter` | 库存同步 | 推送库存数据 |
| `LogisticsAdapter` | 物流回传 | 上传物流信息 |

### 分页配置

```json
{
  "pagination": {
    "pageSize": 100,
    "startTime": "{{LAST_SYNC_TIME}}",
    "endTime": "{{CURRENT_TIME}}",
    "status": "WAIT_SELLER_SEND_GOODS"
  }
}
```

## 最佳实践

### 1. 订单状态管理

```mermaid
stateDiagram-v2
    [*] --> 待付款: 下单
    待付款 --> 待发货: 付款
    待付款 --> 已关闭: 取消/超时
    待发货 --> 已发货: 发货
    已发货 --> 已收货: 签收
    已发货 --> 退款中: 申请退款
    退款中 --> 已退款: 同意退款
    退款中 --> 已发货: 拒绝退款
    已收货 --> 已完成: 确认收货
    已完成 --> [*]
    已关闭 --> [*]
    已退款 --> [*]
```

### 2. 库存防超卖机制

```mermaid
flowchart TD
    A[订单创建] --> B{库存检查}
    B -->|库存充足| C[锁定库存]
    B -->|库存不足| D[拒绝订单]
    C --> E[支付超时检查]
    E -->|超时未付| F[释放库存]
    E -->|支付成功| G[扣减库存]
    F --> H[库存回滚]
    
    style B fill:#fff3e0
    style E fill:#fff3e0
```

### 3. 异常处理策略

| 异常类型 | 处理策略 | 重试机制 |
|---------|---------|---------|
| 接口限流 | 指数退避 | 3 次 |
| 网络超时 | 立即重试 | 5 次 |
| 数据异常 | 记录日志 | 人工介入 |
| 授权失效 | 刷新令牌 | 自动刷新 |

## 常见问题

### Q: 如何处理平台接口限流？

建议采用以下策略：
1. 合理设置同步频率，避免频繁调用
2. 实现请求队列，平滑处理突发流量
3. 配置指数退避重试机制

```python
# 伪代码示例
def request_with_retry(api, params, max_retries=3):
    for i in range(max_retries):
        try:
            return call_api(api, params)
        except RateLimitError:
            time.sleep(2 ** i)  # 指数退避
    raise MaxRetryExceeded()
```

### Q: 多店铺如何统一管理库存？

建议使用中央库存池模式：

```mermaid
flowchart TB
    subgraph Pool[中央库存池]
        A[总库存]
        B[锁定库存]
        C[可用库存]
    end
    
    subgraph Shops[各平台店铺]
        D[天猫店]
        E[京东店]
        F[拼多多店]
    end
    
    C --> D
    C --> E
    C --> F
    D -->|订单| B
    E -->|订单| B
    F -->|订单| B
    
    style Pool fill:#fff3e0
```

## 相关文档

- [旺店通连接器](./ecommerce/wangdian)
- [聚水潭连接器](./ecommerce/jushuitan)
- [管易云连接器](./ecommerce/guanyi)
- [订单集成方案](../standard-schemes/order-integration)
- [库存同步方案](../standard-schemes/inventory-sync)

> [!NOTE]
> 电商平台的接口会定期更新，请及时关注平台公告和轻易云更新日志。
