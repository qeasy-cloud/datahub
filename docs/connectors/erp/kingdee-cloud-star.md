# 金蝶云星辰集成专题

本文档详细介绍轻易云 iPaaS 平台与金蝶云星辰（Kingdee Cloud Star）的集成配置方法，涵盖基础连接配置、帐套查询、星辰 V2 轻智造适配器配置等内容。金蝶云星辰面向小微企业，提供财务、进销存、零售等一体化云服务。

## 概述

金蝶云星辰（Kingdee Cloud Star）是金蝶软件面向小微企业推出的 SaaS 化 ERP 产品。轻易云 iPaaS 提供专用的金蝶云星辰连接器，支持以下核心能力：

- **基础数据同步**：商品、客户、供应商等主数据双向同步
- **业务单据集成**：销售、采购、库存、财务单据的自动化流转
- **星辰 V2 轻智造适配**：支持云蝶轻智造扩展模块的数据对接
- **帐套管理与查询**：多帐套环境下的数据路由配置

## 连接器配置

### 创建连接器

1. 登录轻易云 iPaaS 控制台，进入**连接器管理**页面
2. 点击**新建连接器**，选择 **ERP** 分类下的**金蝶云星辰**
3. 填写连接参数（详见下方参数说明）
4. 点击**测试连接**验证连通性
5. 连接成功后点击**保存**

### 连接参数说明

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `app_id` | string | ✅ | 应用 ID，固定值 `213582` |
| `app_secret` | string | ✅ | 应用密钥，固定值 `d5005d5f55a4882eb98c73f570f41f1a` |
| `username` | string | ✅ | 金蝶云星辰登录手机号 |
| `password` | string | ✅ | 金蝶云星辰登录密码 |
| `group_name` | string | ✅ | 调用鉴权接口获得的组名 |
| `account_id` | string | ✅ | 调用帐套查询接口获得的帐套 ID |

> [!IMPORTANT]
> `group_name` 和 `account_id` 需要通过调用帐套查询接口获取，详见下文**帐套查询配置**章节。

## 帐套查询配置

在正式配置集成方案前，需要先获取帐套信息（组名和帐套 ID）。以下是获取步骤：

### 创建查询集成方案

1. 进入**集成方案**页面，点击**新建方案**
2. 方案名称填写「金蝶云星辰帐套查询」
3. 源平台选择**金蝶云星辰**
4. 目标平台选择**空平台**（仅用于查询）

### 配置查询接口

在方案配置中，选择以下查询接口：

| 配置项 | 值 |
| ------ | ---- |
| 接口类型 | 平台接口 |
| 平台选择 | 金蝶云星辰 |
| 接口名称 | 帐套查询 |

### 获取帐套信息

执行查询方案后，返回结果中包含以下关键字段：

| 字段名 | 说明 |
| ------ | ---- |
| `group_name` | 帐套所属组名 |
| `account_id` | 帐套唯一标识 ID |
| `account_name` | 帐套名称 |

> [!TIP]
> 如果企业有多个帐套，需要记录每个帐套对应的 `group_name` 和 `account_id`，在创建连接器时选择对应的帐套。

## 星辰 V2 轻智造适配器配置

金蝶云星辰 V2 版本支持「云蝶轻智造」扩展模块，本文档说明如何通过适配器与轻智造模块进行数据对接。

### 适配器映射

| 适配器类型 | 适配器名称 | 功能描述 |
| ---------- | ---------- | -------- |
| 写入适配器 | `\Adapter\Kingdee\YxcZhiZhaoExecuteAdapter` | 执行/下发操作到轻智造 |
| 查询适配器 | `\Adapter\Kingdee\YxcZhiZhaoQueryAdapter` | 从轻智造查询数据 |

### 前提条件

- 已开通星辰平台服务管理员账号
- 已获取服务方提供的加密 RSA 公钥
- 可访问云蝶轻智造认证接口与 API

### 获取 AppKey 与授权

1. **获取 AppKey**
   
   登录星辰平台 → 账套 → 生态应用 → 前往应用中心 → 已授权应用（云蝶轻智造）→ 管理 → 授权详情，复制 **AppKey**。

2. **加密 AppKey**
   
   使用服务方提供的 **RSA 公钥** 对 AppKey 进行加密，得到 `appKeyCipher`。

3. **获取临时凭证**
   
   调用云蝶认证接口获取临时访问凭证：

```bash
curl --location "https://www.zsyundee.com/appKeyV2?appKey=<YOUR_APPKEY>&appKeyCipher=<YOUR_APPKEY_CIPHER>"
```

> [!NOTE]
> 成功返回后，使用返回的认证结果进行后续 API 调用。

### 认证与加密说明

#### RSA 公钥示例

以下为示例公钥（实际以服务方提供为准）：

```text
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCrCl69udzQug/7hysNbneRXLjXWcX+AfCGflD7xawR/71judDA34J6ttw5l4HlwVJMBljsIeHmY8Ov8n+gswOjmhDfgpV3KcMVqSL1riBP8iKNefSeezjt3/QgpGbMbx5Yl7B+G6NsttUrK4mDZHWN+2zY5qeqkRmYgQD70UxURwIDAQAB
```

> [!WARNING]
> 公钥可能会变更，请以服务方最新通知为准。

#### Java 加密示例代码

以下为 RSA 公钥加密 AppKey 的示例实现：

```java
public static String encryptAppKey(String plainText) throws NoSuchAlgorithmException, InvalidKeySpecException,
        UnsupportedEncodingException, NoSuchPaddingException, InvalidKeyException, IllegalBlockSizeException,
        BadPaddingException {
    byte[] encryptedBytes;
    // PUBLIC_KEY 为服务方提供的公钥（Base64）
    X509EncodedKeySpec keySpec = new X509EncodedKeySpec(Base64.decodeBase64(PUBLIC_KEY));
    KeyFactory keyFactory = KeyFactory.getInstance("RSA");
    PublicKey publicKey = keyFactory.generatePublic(keySpec);
    Cipher cipher = Cipher.getInstance("RSA");
    cipher.init(Cipher.ENCRYPT_MODE, publicKey);

    // 将字符串转换为字节数组并加密
    encryptedBytes = cipher.doFinal(plainText.getBytes());
    // 将加密后的字节转为 Base64 字符串
    String encodeBase64String = Base64.encodeBase64String(encryptedBytes);
    // URL 编码加密后的 Base64 字符串
    return URLEncoder.encode(encodeBase64String, "UTF-8");
}
```

### 轻智造接口配置

#### 基础信息

| 配置项 | 值 |
| ------ | ---- |
| API 主机 | `https://api.kingdee.com/mxocminimes/` |
| 认证接口 | `https://www.zsyundee.com/appKeyV2` |
| 接口文档 | 详见云蝶轻智造 API 文档 |

#### 连接器参数配置

在集成平台配置连接器时，使用以下参数：

```json
{
  "app_key": "ylJUuPhR",
  "groupName": "ns-fork57",
  "account_id": "1764170105846272114"
}
```

| 参数名 | 说明 |
| ------ | ---- |
| `app_key` | 应用唯一标识密钥 |
| `groupName` | 所属分组名称 |
| `account_id` | 账户唯一标识符 |

#### 方案配置示例

**接口路径**：

```text
/mxoc_pom/mxoc_pom_instocknew_query
```

**请求参数**：

```json
{
  "formId": "mxoc_pom_instocknew",
  "unpage": "",
  "pageSize": "10",
  "pageIndex": "1",
  "search": "",
  "billstatus": "all",
  "dateSearch": "all"
}
```

**参数说明**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| ------ | ---- | ---- | ------ | ---- |
| `formId` | string | 是 | - | 表单唯一标识，固定为 `mxoc_pom_instocknew` |
| `unpage` | string | 否 | `""` | 分页控制字段（通常留空） |
| `pageSize` | string | 否 | `"10"` | 每页返回记录数 |
| `pageIndex` | string | 否 | `"1"` | 当前页码（从 1 开始） |
| `search` | string | 否 | `""` | 全局搜索关键词（留空表示不筛选） |
| `billstatus` | string | 否 | `"all"` | 单据状态筛选，`"all"` 表示不限制 |
| `dateSearch` | string | 否 | `"all"` | 日期范围筛选，`"all"` 表示不限制 |

> [!NOTE]
> 所有参数值均以字符串形式传递，即使为数字也需加引号。

## 数据映射配置

### 基础资料映射

| 金蝶云星辰字段 | 说明 | 常见映射源字段 |
| -------------- | ---- | -------------- |
| `FNumber` | 编码 | 商品编码、客户编码 |
| `FName` | 名称 | 商品名称、客户名称 |
| `FSpecification` | 规格型号 | 规格字段 |
| `FUnitID` | 单位 | 计量单位 |
| `FCategoryID` | 分类 | 商品分类、客户分类 |

### 单据字段映射

以销售订单为例，常用字段映射如下：

| 星辰字段 | 说明 | 示例值 |
| -------- | ---- | ------ |
| `FBillTypeID` | 单据类型 | `XS01`（销售订单） |
| `FBillNo` | 单据编号 | 系统自动生成或外部传入 |
| `FDate` | 业务日期 | `2026-03-13` |
| `FCustId` | 客户 ID | 客户编码 |
| `FSaleOrgId` | 销售组织 | 组织编码 |
| `FMaterialId` | 物料 ID | 物料编码 |
| `FQty` | 数量 | 10 |
| `FPrice` | 单价 | 100.00 |
| `FAmount` | 金额 | 1000.00 |

## 常见问题

### Q：连接失败，提示"认证失败"？

请检查以下配置：

- 确认 `app_id` 和 `app_secret` 填写正确（固定值）
- 确认 `username` 和 `password` 为有效的金蝶云星辰账号
- 确认 `group_name` 和 `account_id` 通过帐套查询接口正确获取
- 检查账号是否有足够的接口调用权限

### Q：如何获取星辰 V2 轻智造的 AppKey？

登录星辰平台后，按以下路径获取：

```text
账套 → 生态应用 → 前往应用中心 → 已授权应用 → 云蝶轻智造 → 管理 → 授权详情
```

### Q：轻智造接口返回"认证过期"？

云蝶轻智造的临时凭证有有效期限制，建议：

- 在凭证过期前重新调用认证接口获取新凭证
- 或在接收到 401/403 错误码时自动刷新凭证

### Q：单据写入失败，提示"基础资料不存在"？

金蝶云星辰对基础资料的依赖校验较为严格，请确保：

- 商品、客户、供应商等基础资料已预先同步
- 基础资料编码与金蝶系统中的编码一致
- 多组织环境下，基础资料已分配到目标组织

### Q：如何查询星辰的表单 ID？

登录金蝶云星辰管理后台，进入【开发平台】→【表单管理】，可查看各业务对象的表单 ID。常见表单 ID：

| 业务对象 | 表单 ID |
| -------- | ------- |
| 销售订单 | `SAL_SaleOrder` |
| 采购订单 | `PUR_PurchaseOrder` |
| 入库单 | `STK_InStock` |
| 出库单 | `SAL_OUTSTOCK` |

## 相关资源

- [配置连接器](../../guide/configure-connector) — 连接器基础使用指南
- [金蝶云星空集成专题](./kingdee-cloud-galaxy) — 金蝶云星空连接器文档
- [金蝶云苍穹集成专题](./kingdee-cloud-cosmos) — 金蝶云苍穹连接器文档
- [标准集成方案](../../standard-schemes/erp-integration) — ERP 对接最佳实践

---

> [!NOTE]
> 本文档持续更新中，如有疑问请联系轻易云技术支持团队。
