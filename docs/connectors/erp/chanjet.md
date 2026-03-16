# 畅捷通集成专题

本文档详细介绍轻易云 iPaaS 平台与畅捷通系列产品（T+Cloud、好业财、T+ 低版本等）的集成配置方法，涵盖连接器授权配置、API 接口调用、通用报表查询等核心功能场景。

## 概述

畅捷通是用友集团旗下的云端财务及企业管理软件品牌，主要产品包括：

- **T+Cloud**：面向成长型企业的云端 ERP 平台
- **好业财**：面向中小微企业的业财一体化 SaaS 服务
- **畅捷通 T+**：本地化部署的 ERP 管理系统

轻易云 iPaaS 提供专用的畅捷通连接器，支持以下核心能力：

- **基础数据同步**：往来单位、商品、分类等主数据双向同步
- **业务单据集成**：销货单、采购入库单、库存单据的自动化流转
- **报表数据查询**：基于通用报表接口的数据抽取
- **库存管理**：现存量查询、出入库单据处理

## 连接器配置

### 创建连接器

1. 登录轻易云 iPaaS 控制台，进入**连接器管理**页面
2. 点击**新建连接器**，选择 **ERP** 分类下的**畅捷通 T+Cloud** 或**好业财**
3. 填写连接参数（详见下方参数说明）
4. 点击**测试连接**验证连通性
5. 连接成功后点击**保存**

### 连接参数说明

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `host` | string | ✅ | API 服务器地址，固定值为 `https://openapi.chanjet.com` |
| `appKey` | string | ✅ | 应用标识，开通授权后获取 |
| `appSecret` | string | ✅ | 应用密钥，开通授权后获取 |
| `refresh_token` | string | ✅ | 刷新令牌，授权流程完成后获取 |
| `access_token` | string | ✅ | 访问令牌，授权流程完成后获取 |
| `bookid` | string | ✅ | 账套 ID，对应具体的公司账套 |

> [!IMPORTANT]
> `appKey` 和 `appSecret` 为畅捷通开放平台分配的固定值，请联系畅捷通获取。

### 连接器配置示例

```json
{
  "host": "https://openapi.chanjet.com",
  "appKey": "WGI6B3h2",
  "appSecret": "BB6D0BD4ACFD3A85A0323538008EBD25",
  "refresh_token": "your_refresh_token_here",
  "access_token": "your_access_token_here",
  "bookid": "your_bookid_here"
}
```

## T+Cloud 授权配置

使用 T+Cloud 集成前，需要完成畅捷通开放平台的授权流程。

### 授权流程概览

```mermaid
flowchart LR
    A[登录畅捷通官网] --> B[开通集成服务]
    B --> C[选择授权公司]
    C --> D[确认授权协议]
    D --> E[获取授权信息]
    E --> F[配置连接器]
    
    style A fill:#e3f2fd
    style E fill:#fff3e0
    style F fill:#e8f5e9
```

### 步骤一：登录畅捷通官网

使用管理员手机号登录畅捷通官方网站：[https://www.chanjet.com](https://www.chanjet.com)

### 步骤二：开通集成服务

访问畅捷通应用市场，开通轻易云集成服务：[https://market.chanjet.com/proDetails/11276](https://market.chanjet.com/proDetails/11276)

### 步骤三：选择授权公司

在授权页面勾选需要授权的公司（TPlus 账套）：

1. 选择目标公司
2. 滚动至页面底部
3. 勾选**开通授权协议**
4. 点击**去开通**

### 步骤四：确认用户授权

开通成功后，页面将自动跳转：

1. 点击**去授权**按钮
2. 勾选**用户授权协议**
3. 点击**去授权**确认

### 步骤五：获取授权信息

授权成功后，页面将显示以下关键信息，请完整保存：

| 字段 | 说明 |
| ---- | ---- |
| `refresh_token` | 刷新令牌，用于获取新的访问令牌 |
| `access_token` | 访问令牌，用于 API 调用鉴权 |
| `bookid` | 账套 ID，标识授权的公司账套 |
| `company_name` | 公司名称 |

> [!TIP]
> 建议将授权信息整理成 Excel 表格，连同公司名称一并提供给集成开发人员。

### 多公司授权

如需授权多个公司，重复步骤二至步骤五的操作流程即可。

## API 接口参考

### 接口调用基础

畅捷通 OpenAPI 采用 RESTful 架构，所有接口均通过 HTTPS 协议访问。

**请求地址格式**：

```text
https://openapi.chanjet.com/{服务路径}/{bookid}
```

**通用请求头**：

```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {access_token}"
}
```

### 往来单位新增

用于创建客户或供应商档案。

**接口信息**

| 项目 | 内容 |
| ---- | ---- |
| 接口地址 | `POST /accounting/openapi/cc/party/custvendor/add/{bookid}` |
| 官方文档 | [https://open.chanjet.com/docs/file/apiFile/zplus/zjjcda/sp?id=30795](https://open.chanjet.com/docs/file/apiFile/zplus/zjjcda/sp?id=30795) |

**成功响应示例**

```json
{
  "success": true,
  "data": [
    {
      "code": "api-custvendor-0907",
      "data": 1145528816500738,
      "errCode": "000000",
      "errMessage": "000000",
      "success": "true"
    }
  ]
}
```

**失败响应示例**

```json
{
  "success": false,
  "code": "openapi.exxxx",
  "message": "其它错误,详见详细信息",
  "data": "e.getMessage()"
}
```

### 商品新增

用于创建商品（物料）档案，支持多规格商品。

**接口信息**

| 项目 | 内容 |
| ---- | ---- |
| 接口地址 | `POST /accounting/openapi/cc/product/add/{bookid}` |
| 官方文档 | [https://open.chanjet.com/docs/file/apiFile/zplus/zjjcda/sp?id=30795](https://open.chanjet.com/docs/file/apiFile/zplus/zjjcda/sp?id=30795) |

**字段映射特殊处理**

#### 特征类型字段（productFeatureTypeAppl）

用于定义商品的规格特征（如颜色、尺寸等）。

**数据源传入格式**：二维数组形式

```json
[
  {"颜色": "红色", "尺寸": "M"},
  {"颜色": "蓝色", "尺寸": "L"},
  {"颜色": "红色", "尺寸": "S"}
]
```

**目标接口要求格式**：按特征类型归集的结构

```json
[
  {
    "productFeatureTypeName": "颜色",
    "productFeatureGroup": {
      "productFeatureList": [
        {"productFeatureName": "红色"},
        {"productFeatureName": "蓝色"}
      ]
    },
    "isInvolvedInPricing": true
  },
  {
    "productFeatureTypeName": "尺寸",
    "productFeatureGroup": {
      "productFeatureList": [
        {"productFeatureName": "M"},
        {"productFeatureName": "L"},
        {"productFeatureName": "S"}
      ]
    },
    "isInvolvedInPricing": true
  }
]
```

#### 自定义字段（customizedField）

**数据源传入格式**：键值对形式

```json
{
  "品牌": "Apple",
  "产地": "中国"
}
```

**目标接口要求格式**：对象数组形式

```json
[
  {"name": "品牌", "value": "Apple"},
  {"name": "产地", "value": "中国"}
]
```

### 销货单新增

用于创建销售出库单据。

**接口信息**

| 项目 | 内容 |
| ---- | ---- |
| 接口地址 | `POST /accounting/openapi/cc/goodsissue/add/{bookid}` |
| 官方文档 | [https://open.chanjet.com/docs/file/apiFile/zplus/zjxsgl/xhd?id=31041](https://open.chanjet.com/docs/file/apiFile/zplus/zjxsgl/xhd?id=31041) |

**响应示例**

```json
{
  "success": true,
  "code": "openapi.e0000",
  "message": "",
  "data": {
    "id": 975865062883328
  }
}
```

### 采购入库单管理

#### 采购入库单新增

**接口信息**

| 项目 | 内容 |
| ---- | ---- |
| 接口地址 | `POST /accounting/openapi/cc/purchasestockin/add/{bookid}` |
| 官方文档 | [https://open.chanjet.com/docs/file/apiFile/zplus/zjkcgl/30644?id=32738](https://open.chanjet.com/docs/file/apiFile/zplus/zjkcgl/30644?id=32738) |

#### 采购入库单列表查询

**接口信息**

| 项目 | 内容 |
| ---- | ---- |
| 接口地址 | `GET /accounting/openapi/cc/purchasestockin/list/{bookid}` |
| 官方文档 | [https://open.chanjet.com/docs/file/apiFile/zplus/zjkcgl/30644?id=33283](https://open.chanjet.com/docs/file/apiFile/zplus/zjkcgl/30644?id=33283) |

**错误响应**

```json
{
  "code": "openapi.e0001",
  "msg": "接口鉴权信息错误"
}
```

### 库存管理接口

#### 其他入库单新增

**接口信息**

| 项目 | 内容 |
| ---- | ---- |
| 接口地址 | `POST /accounting/openapi/cc/stock/add/{bookid}` |
| 官方文档 | [https://open.chanjet.com/docs/file/apiFile/zplus/zjkcgl/qtrkd?id=32404](https://open.chanjet.com/docs/file/apiFile/zplus/zjkcgl/qtrkd?id=32404) |

#### 其他出入库单新增 V2

支持更灵活的出入库类型配置。

**接口信息**

| 项目 | 内容 |
| ---- | ---- |
| 接口地址 | `POST /accounting/openapi/cc/stock/{inoutFlag}/add/{bookid}` |
| 官方文档 | [https://open.chanjet.com/docs/file/apiFile/zplus/zjkcgl/qtrkd?id=32856](https://open.chanjet.com/docs/file/apiFile/zplus/zjkcgl/qtrkd?id=32856) |

| 参数 | 说明 |
| ---- | ---- |
| `inoutFlag` | 出入库标志，`in` 表示入库，`out` 表示出库 |

#### 查询现存量

**接口信息**

| 项目 | 内容 |
| ---- | ---- |
| 接口地址 | `GET /accounting/openapi/cc/inv/onhandqty/{bookid}` |
| 官方文档 | [https://open.chanjet.com/docs/file/apiFile/zplus/zjkcgl/kc?id=30797](https://open.chanjet.com/docs/file/apiFile/zplus/zjkcgl/kc?id=30797) |

### 商品管理接口

#### 商品列表查询

**接口信息**

| 项目 | 内容 |
| ---- | ---- |
| 接口地址 | `GET /accounting/openapi/cc/product/list/{bookid}` |
| 官方文档 | [https://open.chanjet.com/docs/file/apiFile/zplus/zjjcda/sp?id=30796](https://open.chanjet.com/docs/file/apiFile/zplus/zjjcda/sp?id=30796) |

#### 商品修改

**接口信息**

| 项目 | 内容 |
| ---- | ---- |
| 接口地址 | `POST /accounting/openapi/cc/product/update/{bookid}` |
| 官方文档 | [https://open.chanjet.com/docs/file/apiFile/zplus/zjjcda/sp?id=31059](https://open.chanjet.com/docs/file/apiFile/zplus/zjjcda/sp?id=31059) |

#### 查询商品分类

**接口信息**

| 项目 | 内容 |
| ---- | ---- |
| 接口地址 | `GET /accounting/openapi/cc/productCategory/list/{bookid}` |
| 官方文档 | [https://open.chanjet.com/docs/file/apiFile/zplus/zjjcda/sp?id=30794](https://open.chanjet.com/docs/file/apiFile/zplus/zjjcda/sp?id=30794) |

### 接口汇总表

#### 高优先级接口

| 序号 | 接口名称 | 接口路径 | 操作类型 |
| ---- | -------- | -------- | -------- |
| 1 | 往来单位新增 | `/accounting/openapi/cc/party/custvendor/add/{bookid}` | 新增 |
| 2 | 商品新增 | `/accounting/openapi/cc/product/add/{bookid}` | 新增 |
| 3 | 销货单新增 | `/accounting/openapi/cc/goodsissue/add/{bookid}` | 新增 |
| 4 | 商品列表查询 | `/accounting/openapi/cc/product/list/{bookid}` | 查询 |
| 5 | 其他入库单新增 | `/accounting/openapi/cc/stock/add/{bookid}` | 新增 |
| 6 | 其他出入库单新增 V2 | `/accounting/openapi/cc/stock/{inoutFlag}/add/{bookid}` | 新增 |
| 7 | 采购入库单列表查询 | `/accounting/openapi/cc/purchasestockin/list/{bookid}` | 查询 |
| 8 | 采购入库单新增 | `/accounting/openapi/cc/purchasestockin/add/{bookid}` | 新增 |
| 9 | 商品修改 | `/accounting/openapi/cc/product/update/{bookid}` | 修改 |

#### 中优先级接口

| 序号 | 接口名称 | 接口路径 | 操作类型 |
| ---- | -------- | -------- | -------- |
| 1 | 查询商品分类 | `/accounting/openapi/cc/productCategory/list/{bookid}` | 查询 |
| 2 | 销货单列表查询 | `/accounting/openapi/cc/goodsissue/list/{bookid}` | 查询 |
| 3 | 查询现存量 | `/accounting/openapi/cc/inv/onhandqty/{bookid}` | 查询 |
| 4 | 库存调拨单列表查询 | `/accounting/openapi/cc/inv/stocktransfer/list/{bookid}` | 查询 |
| 5 | 产成品入库单列表查询 | `/accounting/openapi/cc/inv/finishedgoodsstock/list/{bookid}` | 查询 |
| 6 | 其他入库单列表查询 | `/accounting/openapi/cc/inv/stockin/list/{bookid}` | 查询 |
| 7 | 其他出库单列表查询 | `/accounting/openapi/cc/inv/stockout/list/{bookid}` | 查询 |
| 8 | 销售出库单列表查询 | `/accounting/openapi/cc/salesstockout/list/{bookid}` | 查询 |
| 9 | 进货单列表查询 | `/accounting/openapi/cc/goodsreceipt/list/{bookid}` | 查询 |

## T+ 低版本通用报表查询

对于畅捷通 T+ 低版本产品，可通过通用报表查询接口获取业务数据。

### 核心概念

使用通用报表查询接口前，需要了解以下三个核心概念：

| 概念 | 说明 |
| ---- | ---- |
| **报表名称（ReportName）** | 标识要查询的报表类型 |
| **查询项（QueryParams）** | 用于过滤数据的查询条件 |
| **显示栏目（Columns）** | 指定接口返回的字段列表 |

### 获取报表名称

报表名称用于标识要查询的具体报表类型。

**操作步骤**：

1. 登录 T+ 系统，打开目标报表
2. 按住 `Ctrl` 键，在报表空白区域点击鼠标右键
3. 选择**查看框架源代码**
4. 在新打开的页面中，查找链接地址中的 `ReportName` 参数值

> [!TIP]
> 例如，销货单统计表的 ReportName 可能为 `SA_SaleDeliveryList`。

### 配置查询项

查询项用于设置数据过滤条件，支持日期范围、状态等多种条件类型。

#### 日期范围查询

```json
{
  "ColumnName": "VoucherDate",
  "BeginDefault": "2024-01-01",
  "BeginDefaultText": "2024-01-01",
  "EndDefault": "2024-01-31",
  "EndDefaultText": "2024-01-31"
}
```

#### 固定值查询

例如，查询状态为"已审核"的销货单：

```json
{
  "ColumnName": "voucherState",
  "BeginDefault": "189",
  "BeginDefaultText": "189",
  "EndDefault": "189",
  "EndDefaultText": "189"
}
```

> [!NOTE]
> `189` 通常表示已审核状态，具体编码请参考 T+ 系统字典。

#### 组合查询

多个查询条件可以组合使用：

```json
[
  {
    "ColumnName": "VoucherDate",
    "BeginDefault": "2024-01-01",
    "BeginDefaultText": "2024-01-01",
    "EndDefault": "2024-01-31",
    "EndDefaultText": "2024-01-31"
  },
  {
    "ColumnName": "voucherState",
    "BeginDefault": "189",
    "BeginDefaultText": "189",
    "EndDefault": "189",
    "EndDefaultText": "189"
  }
]
```

### 配置显示栏目

显示栏目指定接口返回的字段，需要根据实际需求配置。

**获取可用字段**：

1. 登录 T+ 系统，打开目标报表
2. 按 `F12` 打开浏览器开发者工具
3. 切换到**网络（Network）**页签
4. 点击报表的**查询**按钮
5. 在请求列表中找到对应请求，查看 `columns` 参数

> [!IMPORTANT]
> 如需返回被隐藏的字段，需要先在报表设置中勾选显示该字段，然后重新查询获取。

### 接口调用示例

```http
POST /api/report/query
Content-Type: application/json

{
  "ReportName": "SA_SaleDeliveryList",
  "QueryParams": [
    {
      "ColumnName": "VoucherDate",
      "BeginDefault": "2024-01-01",
      "BeginDefaultText": "2024-01-01",
      "EndDefault": "2024-01-31",
      "EndDefaultText": "2024-01-31"
    }
  ],
  "Columns": "ID,Code,VoucherDate,CustomerName,Amount"
}
```

## 数据映射配置

### 基础资料映射

| 畅捷通字段 | 说明 | 常见数据源字段 |
| ---------- | ---- | -------------- |
| `code` | 编码 | 客户编号、商品编号 |
| `name` | 名称 | 客户名称、商品名称 |
| `specification` | 规格型号 | 规格、型号 |
| `unit` | 计量单位 | 单位 |
| `category` | 分类 | 分类编码 |

### 单据字段映射

| 畅捷通字段 | 说明 | 常见数据源字段 |
| ---------- | ---- | -------------- |
| `voucherDate` | 单据日期 | 订单日期、出库日期 |
| `customerCode` | 客户编码 | 客户编号 |
| `warehouseCode` | 仓库编码 | 仓库编号 |
| `inventoryCode` | 存货编码 | 商品编号、SKU |
| `quantity` | 数量 | 数量、出库数量 |
| `price` | 单价 | 单价、成交价 |
| `amount` | 金额 | 金额、总价 |

## 常见问题

### Q：授权时提示"公司已授权给其他应用"？

A：请先登录畅捷通应用市场，解除该公司与其他集成应用的绑定关系，然后重新进行授权流程。

### Q：接口调用返回"接口鉴权信息错误"？

A：请检查以下配置：

- `access_token` 是否已过期，如过期需使用 `refresh_token` 重新获取
- `bookid` 是否正确对应授权的公司账套
- 请求头中的 `Authorization` 格式是否正确

### Q：商品新增时提示"商品已存在"？

A：畅捷通系统中商品编码唯一，请检查：

- 商品编码是否已在系统中存在
- 如需要更新商品信息，请使用**商品修改**接口而非新增接口

### Q：如何获取 `bookid`？

A：`bookid` 在授权流程完成后与 `access_token` 一同返回。如需查询所有已授权账套，可调用畅捷通账套查询接口。

### Q：T+ 低版本报表查询返回空数据？

A：请检查以下配置：

- `ReportName` 是否正确获取
- 查询条件是否与数据匹配（如日期范围内是否有数据）
- 显示栏目字段名是否正确（区分大小写）

### Q：特征类型字段转换失败？

A：特征类型字段需要进行格式转换，请确保：

- 数据源格式为二维数组
- 转换后的格式符合接口要求
- 特征类型名称与 T+ 系统中设置的完全一致

## 相关资源

- [畅捷通开放平台](https://open.chanjet.com)
- [畅捷通应用市场](https://market.chanjet.com)
- [畅捷通 T+Cloud 官网](https://www.chanjet.com)
