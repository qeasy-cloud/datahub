# 易仓连接器

本文档详细介绍轻易云 iPaaS 平台与易仓（EcCang）的集成配置方法。易仓是国内领先的跨境电商 SaaS 平台，专注于为跨境电商企业提供订单管理、仓储物流、供应链管理等一体化解决方案。

> [!TIP]
> 如需了解连接器的基础使用方法，请先阅读 [配置连接器](../../guide/configure-connector)。

## 概述

易仓平台覆盖跨境电商业务全流程，提供以下核心能力：

| 功能模块 | 说明 |
|----------|------|
| **订单管理** | 多平台订单聚合、订单处理、售后管理 |
| **仓储管理** | 海外仓、FBA、自营仓多仓协同管理 |
| **物流管理** | 对接全球主流物流渠道，智能路由选择 |
| **供应链管理** | 采购、库存、供应商协同管理 |
| **财务管理** | 成本核算、利润分析、结算管理 |

轻易云 iPaaS 提供专用的易仓连接器，支持以下核心能力：

- **订单数据同步**：销售订单、出库单、售后订单的自动抓取
- **库存实时同步**：多仓库库存数据实时获取
- **基础资料管理**：商品、仓库、物流渠道等主数据同步
- **地址簿管理**：发货地址、收货地址等数据同步
- **灵活适配器**：支持查询和写入两种操作模式

## 准备工作

在开始配置连接器之前，需要完成以下准备工作：

### 所需材料清单

| 序号 | 材料 | 说明 | 获取方式 |
|------|------|------|----------|
| 1 | 易仓账号 | 易仓平台登录账号 | 客户提供 |
| 2 | 应用 Key | 生态中心创建应用后获取 | 客户自行创建 |
| 3 | 应用密钥 | 应用对应的 Secret | 创建应用后查看 |
| 4 | Service ID | 服务授权标识 | 授权后查看 |

## 开放平台应用创建

### 访问开放平台

易仓开放平台文档地址：[https://open.eccang.com](https://open.eccang.com/#/documentCenter?docId=307&catId=0-172-172,0-171)

### 创建应用

1. 登录易仓生态中心，访问应用管理页面：[https://home.eccang.com/#/company/develop/app-manager](https://home.eccang.com/#/company/develop/app-manager)
2. 点击 **创建应用**
3. 填写应用名称和相关信息
4. 选择需要的接口权限
5. 提交后等待审核（如需要）

### 获取应用凭证

应用创建成功后，在应用管理页面的 **授权状态** 列点击 **查看**，即可获取以下关键信息：

| 参数 | 说明 |
|------|------|
| `app_key` | 应用 Key，用于接口认证 |
| `app_secret` | 应用密钥，用于签名计算 |
| `service_id` | 服务 ID，用于标识授权的服务 |

> [!IMPORTANT]
> 请妥善保存 `app_secret`，不要泄露给未授权人员。密钥信息一旦丢失，需要重新创建应用。

## 连接器配置

### 创建连接器

1. 登录轻易云 iPaaS 控制台，进入 **连接器管理** 页面
2. 点击 **新建连接器**，选择 **电商 / WMS 类** 下的 **易仓**
3. 填写连接参数（详见下方参数说明）
4. 点击 **测试连接** 验证连通性
5. 连接成功后点击 **保存**

### 连接参数说明

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `host` | string | ✅ | 接口请求地址，固定值为 `http://openapi-web.eccang.com/openApi/api/unity` |
| `app_key` | string | ✅ | 应用 Key，从易仓开放平台获取 |
| `app_secret` | string | ✅ | 应用密钥，从易仓开放平台获取 |
| `service_id` | string | ✅ | 服务 ID，从应用授权状态中获取 |

> [!NOTE]
> `host` 地址为固定值，请勿修改。易仓所有接口均通过此统一入口调用。

## 集成方案配置

### 适配器介绍

易仓连接器提供两种专用适配器，分别用于不同场景：

| 适配器 | 用途 | 适配器类名 |
|--------|------|-----------|
| **查询适配器** | 从易仓查询数据 | `EcCangV2QueryAdapter` |
| **写入适配器** | 向易仓写入数据 | `EcCangV2ExecuteAdapter` |

### 配置示例

在集成方案的 **基础配置** 或 **高级配置** 中，根据操作类型选择对应的适配器：

#### 查询数据场景

```text
\Adapter\EcCang\V2\EcCangV2QueryAdapter
```

#### 写入数据场景

```text
\Adapter\EcCang\V2\EcCangV2ExecuteAdapter
```

### API 参数配置

易仓接口通过 `interface_method` 参数指定具体的 API 操作。查看易仓开放平台文档，获取需要的接口方法名：

| 接口名称 | 说明 | 常用场景 |
|----------|------|----------|
| `getShipAddressBooks` | 获取发货地址簿 | 同步发货地址信息 |
| `getOrderList` | 获取订单列表 | 销售订单同步 |
| `getInventory` | 获取库存数据 | 库存同步 |
| `getProductList` | 获取商品列表 | 商品资料同步 |

> [!TIP]
> 具体接口名称和参数请参考 [易仓开放平台文档](https://open.eccang.com/#/documentCenter?docId=111803&catId=0-189-189,0-177)。

## 请求参数说明

### Request 参数配置

在集成方案的 **Request** 区域配置请求参数，常用参数如下：

| 参数名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `page` | int | 页码 | `1` |
| `page_size` | int | 每页条数 | `50` |
| `posted_date_site_from` | string | 开始时间 | `2024-01-01 00:00:00` |
| `posted_date_site_to` | string | 结束时间 | `2024-01-31 23:59:59` |

### 其他请求参数（Other Request）

易仓接口采用签名认证机制，默认签名字段顺序如下：

```typescript
1. app_key
2. biz_content
3. charset
4. interface_method
5. nonce_str
6. service_id
7. sign (空值占位)
8. sign_type
9. timestamp
10. version
```

如果接口要求的签名顺序与默认顺序不一致，需要在 **其他请求参数** 中自定义配置。

#### 其他请求参数字段说明

| 字段名 | 说明 | 配置值 |
|--------|------|--------|
| `app_key` | 应用 Key | 填入 `app_key`，自动取连接器配置的 `app_key` |
| `biz_content` | 请求头参数 | 填入 `biz_content`，自动将 Request 参数 JSON 格式化 |
| `charset` | 字符编码 | 默认 `UTF-8` |
| `interface_method` | 接口方法名 | 自动取当前方案配置的 API |
| `nonce_str` | 随机字符串 | 需要配置生成规则 |
| `service_id` | 服务 ID | 填入 `service_id`，自动取连接器配置的 `service_id` |
| `sign` | 签名 | 填入 `sign`，自动生成签名 |
| `sign_type` | 签名类型 | 默认 `MD5` |
| `timestamp` | 时间戳 | 填入 `timestamp`，每次请求使用新的时间戳 |
| `version` | 版本号 | 默认 `1.0.0` |

> [!WARNING]
> 签名顺序必须与接口文档要求一致，否则会导致 **签名错误**。如有疑问，请联系易仓技术支持确认签名顺序。

## 响应参数处理

### 标准响应参数

在集成方案中配置响应解析参数：

| 参数名 | 说明 | 示例值 |
|--------|------|--------|
| `statusKey` | 响应状态字段 | `code` / `status` |
| `statusValue` | 成功状态值 | `200` / `success` |
| `dataKey` | 返回数据字段 | `data` / `items` |
| `pageKey` | 分页字段 | `pagination` |

### 特殊格式处理

在某些场景下，需要对数据进行特殊格式转换。例如将对象转换为二维数组：

**原始数据格式：**

```json
{
  "default_purchase_cost_fee": -0.16,
  "default_purchase_fee": -0.16,
  "default_purchase_shipping_fee": 0,
  "default_purchase_tariff_fee": 0
}
```

**目标转换格式：**

```json
{
  "_Fcost": [
    {
      "key": "default_purchase_cost_fee",
      "value": -0.16
    },
    {
      "key": "default_purchase_fee",
      "value": -0.16
    },
    {
      "key": "default_purchase_shipping_fee",
      "value": 0
    }
  ]
}
```

#### 配置方法

在 **其他响应参数** 中添加 `cost_array_key` 参数，指定需要转换的 Key：

| 参数名 | 说明 | 配置值 |
|--------|------|--------|
| `statusKey` | 响应状态字段 | `code` |
| `statusValue` | 成功状态值 | `200` |
| `dataKey` | 返回数据字段 | `data` |
| `pageKey` | 分页字段 | `pagination` |
| `cost_array_key` | 需要转换为二维数组的 Key | `default_purchase_cost_fee,default_purchase_fee,default_purchase_shipping_fee` |

## 数据映射参考

### 订单常用字段

| 易仓字段 | 说明 | 备注 |
|----------|------|------|
| `order_id` | 订单编号 | 易仓内部订单号 |
| `platform_order_id` | 平台订单号 | 电商平台原始订单号 |
| `platform` | 电商平台 | 如 Amazon、eBay、Shopify 等 |
| `warehouse_code` | 仓库编码 | 发货仓库标识 |
| `shipping_method` | 物流方式 | 物流渠道代码 |
| `order_status` | 订单状态 | 待处理、已发货、已完成等 |
| `order_time` | 下单时间 | 订单创建时间 |
| `pay_time` | 付款时间 | 订单付款时间 |
| `ship_time` | 发货时间 | 实际发货时间 |

### 库存常用字段

| 易仓字段 | 说明 |
|----------|------|
| `sku` | SKU 编码 |
| `warehouse_code` | 仓库编码 |
| `available_qty` | 可用库存数量 |
| `onway_qty` | 在途库存数量 |
| `reserved_qty` | 预留库存数量 |

### 商品常用字段

| 易仓字段 | 说明 |
|----------|------|
| `product_sku` | 商品 SKU |
| `product_name` | 商品名称 |
| `product_name_en` | 英文名称 |
| `category` | 商品分类 |
| `brand` | 品牌 |
| `weight` | 重量 |
| `length` / `width` / `height` | 尺寸信息 |

## 常见问题

### Q：如何确认签名顺序是否正确？

如果接口返回签名错误，请：

1. 仔细核对易仓开放平台文档中的签名算法说明
2. 确认 `otherRequest` 中字段顺序与文档要求一致
3. 检查 `app_secret` 是否正确
4. 联系易仓技术支持获取帮助

### Q：接口调用频率限制是多少？

易仓接口有频率限制，具体限制根据接口类型和账号等级不同而有所差异。建议：

- 合理设置同步频率，建议 5-10 分钟一次
- 使用轻易云 iPaaS 的队列机制进行流量控制
- 关注接口返回的限流提示，做好重试机制

### Q：如何处理分页查询？

易仓接口通常采用分页返回数据，在集成方案中：

1. 配置 `pageKey` 和 `pageSize` 参数
2. 在 **调度配置** 中启用 **自动分页** 功能
3. 系统会自动遍历所有分页数据

### Q：如何选择查询适配器还是写入适配器？

| 场景 | 适配器选择 |
|------|------------|
| 从易仓查询订单、库存、商品等数据 | `EcCangV2QueryAdapter` |
| 向易仓推送订单状态、库存更新等 | `EcCangV2ExecuteAdapter` |

### Q：对接完成后如何测试？

1. 使用轻易云 iPaaS 的 **调试模式** 验证单条数据流转
2. 检查订单、库存等关键数据的完整性与准确性
3. 进行小批量数据试运行（建议 10-50 条）
4. 配置监控告警，关注失败通知和数据延迟告警
5. 确认无误后开启正式调度

### Q：如何获取接口文档中未列出的字段？

如需获取特殊字段或自定义字段，请：

1. 查阅易仓开放平台最新文档
2. 联系易仓技术支持确认字段可用性
3. 在集成方案的 **数据加工厂** 中进行字段扩展处理

## 相关资源

- [配置连接器](../../guide/configure-connector) — 连接器基础使用指南
- [旺店通集成专题](./wangdian) — 旺店通连接器文档
- [聚水潭集成专题](./jushuitan) — 聚水潭连接器文档
- [电商 / WMS 类连接器概览](./README) — 电商连接器总览
- [标准集成方案 — 跨境电商](../../standard-schemes/crossborder) — 跨境电商集成最佳实践
- [解决方案 — 跨境电商](../../solutions/crossborder-ecommerce) — 跨境电商行业集成方案
- [易仓开放平台文档](https://open.eccang.com/#/documentCenter?docId=307&catId=0-172-172,0-171) — 官方接口文档

---

> [!NOTE]
> 本文档持续更新中，如有疑问请联系轻易云技术支持团队。
