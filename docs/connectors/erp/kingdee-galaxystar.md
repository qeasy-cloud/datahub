# 金蝶星瀚集成专题

本文档详细介绍轻易云 iPaaS 平台与金蝶星瀚（Kingdee Galaxstar）的集成配置方法，涵盖连接器配置、第三方应用授权、接口说明及常见问题解决方案。金蝶星瀚是金蝶面向大型企业推出的数字化平台，接口规范与金蝶云苍穹类似。

## 概述

金蝶星瀚（Kingdee Galaxstar）是金蝶软件面向大型企业推出的企业级数字化平台，基于云原生架构构建，提供财务、供应链、人力、协同等全业务领域的数字化能力。轻易云 iPaaS 提供专用的金蝶星瀚连接器，支持以下核心能力：

- **基础数据同步**：组织、物料、客户、供应商等主数据双向同步
- **业务单据集成**：采购、销售、库存、财务单据的自动化流转
- **OAuth 2.0 认证**：支持标准的 OAuth 2.0 授权流程，确保访问安全
- **API 标准化**：基于 RESTful 规范的 OpenAPI，接口风格与金蝶云苍穹一致

## 连接器配置

### 创建连接器

1. 登录轻易云 iPaaS 控制台，进入**连接器管理**页面
2. 点击**新建连接器**，选择 **ERP** 分类下的**金蝶星瀚**
3. 填写连接参数（详见下方参数说明）
4. 点击**测试连接**验证连通性
5. 连接成功后点击**保存**

### 连接参数说明

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `server_url` | string | ✅ | 金蝶星瀚服务器地址，格式如 `https://galaxstar.example.com/` |
| `client_id` | string | ✅ | 第三方应用的 Client ID（应用 ID） |
| `client_secret` | string | ✅ | 第三方应用的 Client Secret（应用密钥） |
| `account_id` | string | ✅ | 数据中心 ID（租户 ID） |
| `username` | string | ✅ | 集成用户账号 |
| `password` | string | ✅ | 集成用户密码 |

> [!IMPORTANT]
> 服务器地址最后需要添加 `/`，例如 `https://galaxstar.example.com/`。

### 适配器选择

| 场景 | 查询适配器 | 写入适配器 |
| ---- | ---------- | ---------- |
| 标准单据查询/写入 | `\Adapter\Kingdee\XhQueryAdapter` | `\Adapter\Kingdee\XhExecuteAdapter` |

## 第三方应用授权配置

金蝶星瀚采用 OAuth 2.0 认证机制，需要在金蝶开发者平台创建第三方应用并获取授权凭证。

### 官方文档参考

金蝶星瀚官方接口文档地址：
[https://vip.kingdee.com/knowledge/specialDetail/226337046514476288](https://vip.kingdee.com/knowledge/specialDetail/226337046514476288?category=239331354741842688&id=218694224487485696&productLineId=29&lang=zh-CN)

> [!NOTE]
> 金蝶星瀚的接口规范与金蝶云苍穹类似，可参考金蝶云苍穹的接口文档理解参数含义。

### 创建第三方应用步骤

1. **登录开发者平台**

   使用管理员账号登录金蝶星瀚开发者平台，进入**第三方应用管理**功能菜单。

2. **创建应用**

   点击**新建应用**按钮，填写应用基本信息：
   - 应用名称：如"轻易云集成平台"
   - 应用类型：选择"第三方系统"
   - 描述：简要说明应用用途

   ![创建第三方应用](https://pic.qeasy.cloud/2024-10-11/1728638654-275982-image.png)

3. **配置访问策略**

   进入应用编辑界面，新增访问策略：
   - 允许访问的数据中心
   - 允许的 IP 白名单（可选）
   - 接口权限范围

   ![配置访问策略](https://pic.qeasy.cloud/2024-10-11/1728638662-522238-image.png)

4. **设置认证密钥**

   在安全设置中，配置 `accesstoken` 认证密钥：
   - 生成 Client ID（应用 ID）
   - 生成 Client Secret（应用密钥）

   > [!WARNING]
   > Client Secret 仅在首次生成时显示，请妥善保存。如遗失需重新生成。

   ![设置认证密钥](https://pic.qeasy.cloud/2024-10-11/1728638672-320585-image.png)

5. **获取 Token 示例**

   在开发者平台的 API 调试界面，可以获取用于测试的 Access Token。该 Token 可用于验证接口连通性。

   ![获取 Token 示例](https://pic.qeasy.cloud/2024-10-11/1728638685-778459-image.png)

6. **记录配置信息**

   完成以上配置后，记录以下信息用于轻易云连接器配置：
   - Client ID（应用 ID）
   - Client Secret（应用密钥）
   - 数据中心 ID
   - 服务器地址

### 轻易云平台参数配置

在轻易云 iPaaS 控制台配置连接器时，请按以下方式填写：

![连接器参数配置](https://pic.qeasy.cloud/2024-10-11/1728638710-739286-image.png)

| 配置项 | 值 |
| ------ | --- |
| 认证类型 | OAuth 2.0 |
| Client ID | 从金蝶获取的应用 ID |
| Client Secret | 从金蝶获取的应用密钥 |
| Token 刷新周期 | 建议设置为 3500 秒（Token 有效期为 3600 秒） |

## 接口说明

### 接口规范

金蝶星瀚提供基于 RESTful 规范的 OpenAPI，主要特点：

- **协议**：HTTPS
- **数据格式**：JSON
- **字符编码**：UTF-8
- **认证方式**：OAuth 2.0 Bearer Token

### 常用接口列表

| 接口类别 | 接口路径 | 说明 |
| -------- | -------- | ---- |
| 认证 | `/oauth/token` | 获取 Access Token |
| 元数据 | `/kapi/v2/metadata/query` | 查询表单元数据 |
| 数据查询 | `/kapi/v2/data/query` | 查询业务数据 |
| 数据写入 | `/kapi/v2/data/save` | 保存业务数据 |
| 数据删除 | `/kapi/v2/data/delete` | 删除业务数据 |
| 数据提交 | `/kapi/v2/data/submit` | 提交单据 |
| 数据审核 | `/kapi/v2/data/audit` | 审核单据 |

### 查询数据示例

```json
{
  "formId": "bd_material",
  "filterString": "FMaterialGroup = '01'",
  "fieldKeys": "FMaterialId, FNumber, FName, FSpecification",
  "topRowCount": 100,
  "startRow": 0
}
```

### 写入数据示例

```json
{
  "formId": "bd_material",
  "data": {
    "FNumber": "MAT001",
    "FName": "测试物料",
    "FSpecification": "规格A",
    "FMaterialGroup": {
      "FNumber": "01"
    }
  }
}
```

## 方案配置示例

### 基础方案配置

完整实施方案可参考：[轻易云金蝶星瀚集成方案](https://pro.qliang.cloud/strategy/detail/22a2ada7-a9ba-34b6-9a48-a0174edf3b1a#BasicSummary)

### 适配器配置

| 场景 | 适配器路径 |
| ---- | ---------- |
| 查询数据 | `\Adapter\Kingdee\XhQueryAdapter` |
| 写入数据 | `\Adapter\Kingdee\XhExecuteAdapter` |

### 查询配置示例

```json
{
  "formId": "bd_material",
  "filterString": "FUseOrgId = '100001'",
  "fieldKeys": "FMaterialId, FNumber, FName, FSpecification, FUseOrgId_FNumber"
}
```

### 写入配置示例

```json
{
  "formId": "bd_material",
  "operation": "Save",
  "isVerifyBaseDataField": true,
  "data": {
    "FNumber": "{{source.material_code}}",
    "FName": "{{source.material_name}}",
    "FSpecification": "{{source.specification}}",
    "FUseOrgId": {
      "FNumber": "{{source.org_code}}"
    }
  }
}
```

## 常见问题

### Q：连接金蝶星瀚时提示 "认证失败"？

A：请检查以下配置：

- 服务器地址是否正确，是否以 `/` 结尾
- Client ID 和 Client Secret 是否匹配
- 集成用户是否有足够的操作权限
- 数据中心 ID 是否正确
- Token 是否已过期，尝试重新获取 Token

### Q：如何获取金蝶星瀚的表单 ID？

A：登录金蝶星瀚 BOS 设计器，打开对应的业务对象，表单 ID 显示在属性窗口中。常见表单 ID：

- 物料：`bd_material`
- 客户：`bd_customer`
- 供应商：`bd_supplier`
- 销售订单：`sal_saleorder`
- 采购订单：`pur_purchaseorder`

### Q：接口调用返回 "权限不足"？

A：请检查：

- 第三方应用的访问策略是否包含所需的数据中心
- 集成用户是否具有对应业务对象的查看/编辑权限
- 接口权限范围是否包含所需的 API

### Q：金蝶星瀚与金蝶云苍穹有什么区别？

A：主要区别如下：

| 维度 | 金蝶星瀚 | 金蝶云苍穹 |
| ---- | -------- | ---------- |
| 定位 | 大型企业数字化平台 | 企业级 PaaS 平台 |
| 目标客户 | 大型集团企业 | 中大型企业 |
| 核心能力 | 财务、人力、供应链 | 低代码开发、微服务 |
| 接口风格 | 与苍穹类似 | RESTful API |

### Q：单据保存成功但数据未写入？

A：检查以下方面：

- 确认 `formId` 填写正确
- 检查必填字段是否都已赋值
- 查看金蝶返回的错误详情，可能是基础资料不存在
- 检查数据格式是否符合接口规范（特别是引用类型字段）

### Q：如何调试接口调用？

A：建议采用以下调试方法：

1. 使用金蝶开发者平台的 API 调试工具测试接口
2. 在轻易云平台开启调试模式，查看完整的请求/响应日志
3. 使用 Postman 等工具模拟请求，验证参数正确性

### Q：Token 过期如何处理？

A：轻易云连接器支持自动刷新 Token 机制：

- 在连接器配置中设置合适的 Token 刷新周期（建议 3500 秒）
- 确保 Client Secret 未过期或失效
- 如遇到刷新失败，检查网络连通性和认证服务器状态

## 相关资源

- [金蝶云苍穹集成专题](./kingdee-cloud-cosmos) — 接口规范相似的连接器参考
- [配置连接器](../../guide/configure-connector) — 连接器基础使用指南
- [自定义连接器开发](../../developer/custom-connector) — 开发自定义连接器
- [金蝶星瀚官方文档](https://vip.kingdee.com/knowledge/specialDetail/226337046514476288) — 官方接口文档

---

> [!NOTE]
> 本文档持续更新中，如有疑问请联系轻易云技术支持团队。
