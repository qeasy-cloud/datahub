# 飞书连接器

飞书（Feishu/Lark）是字节跳动推出的企业级协同办公平台，提供审批流程、多维表格、即时通讯、日历等丰富的办公能力。轻易云 iPaaS 平台通过飞书连接器，帮助企业实现飞书与 ERP、财务、人力资源等业务系统的深度集成，支持审批数据自动推送、多维表格数据同步、消息通知等场景。

> [!TIP]
> 飞书连接器支持双向数据同步：既可以将飞书审批数据推送至业务系统，也可以将业务系统的数据写入飞书多维表格或发送消息通知。

## 功能特性

| 功能模块 | 支持情况 | 说明 |
| -------- | -------- | ---- |
| 审批流程集成 | ✅ | 审批状态变更实时推送、审批结果回写 |
| 多维表格 | ✅ | 数据写入、记录新增、批量导入 |
| 消息通知 | ✅ | 应用消息、群机器人消息 |
| 组织架构 | ✅ | 部门、人员信息同步 |
| 考勤数据 | ✅ | 打卡记录、请假数据获取 |
| 附件下载 | ✅ | 审批附件自动下载与传输 |

## 前置准备

### 创建飞书应用

在使用飞书连接器前，需要在飞书开放平台创建自建应用并获取连接凭证：

1. 登录 [飞书开放平台](https://open.feishu.cn/)
2. 进入**开发者后台**，点击**创建企业自建应用**
3. 填写应用名称、描述、图标等基本信息
4. 在**凭证与基础信息**页面获取 **App ID** 和 **App Secret**

> [!NOTE]
> 详细的企业自建应用创建流程，请参考[飞书官方文档](https://open.feishu.cn/document/home/introduction-to-custom-app-development/self-built-application-development-process)。

### 配置应用权限

根据集成需求，为应用添加相应的 API 权限：

| 功能场景 | 所需权限 | 权限标识 |
| -------- | -------- | -------- |
| 审批数据读取 | 审批 | `approval:approval` |
| 多维表格操作 | 多维表格 | `bitable:bitable` |
| 消息发送 | 发送消息 | `im:message` |
| 组织架构读取 | 通讯录 | `contact:contact` |
| 考勤数据 | 考勤 | `attendance:attendance` |

### 发布应用

完成权限配置后，需要发布应用版本：

1. 进入**版本管理与发布**页面
2. 点击**创建版本**，填写版本号和更新说明
3. 提交审核（企业内部应用可免审直接发布）
4. 点击**发布**使应用生效

> [!WARNING]
> 应用未发布时，部分 API 接口可能无法正常调用。建议在开发调试完成后及时发布应用。

## 配置连接器

### 基础连接配置

在轻易云 iPaaS 平台创建飞书连接器：

1. 进入**连接器管理**页面，点击**新建连接器**
2. 选择连接器类型为**飞书**
3. 填写连接参数：

| 参数 | 必填 | 说明 |
| ---- | ---- | ---- |
| App ID | ✅ | 飞书应用的 App ID |
| App Secret | ✅ | 飞书应用的 App Secret |
| 数据源编码 | — | 自定义标识，用于区分不同连接 |

4. 点击**测试连接**，验证配置是否正确
5. 连接成功后，点击**保存**

### 回调配置（审批推送场景）

当需要接收飞书审批的实时推送时，需要配置回调参数：

1. 在飞书应用的**事件与回调**页面，启用加密密钥：
   - **Encrypt Key**（加密密钥）：用于消息加密
   - **Verification Token**（验证令牌）：用于验证请求来源

2. 在轻易云方案中配置回调参数：
   - 进入**方案信息** → **回调参数设置**
   - 将飞书的 Encrypt Key 填入 **EncodingAESKey**
   - 将飞书的 Verification Token 填入 **token**
   - 如不开启加密，可将 EncodingAESKey 留空

3. 获取回调地址：
   - 格式：`{集成平台地址}/api/open/feishu/oa/{方案ID}`
   - 也可在方案信息的回调参数区域直接复制

4. 在飞书应用的事件配置中：
   - 选择**将事件发送到开发者服务器**
   - 填入上述回调地址
   - 保存并验证回调配置

> [!IMPORTANT]
> 回调地址必须公网可访问，且支持 HTTPS 协议。内网环境需要使用内网穿透工具。

## 多维表格集成

### 获取多维表格 Token

飞书多维表格通过 `app_token` 进行标识，获取方式如下：

#### 方式一：通过接口创建获取

使用飞书[创建多维表格](https://open.feishu.cn/document/server-docs/docs/bitable-v1/app/create)接口创建表格，接口返回值中的 `app_token` 即为多维表格标识。

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "app_token": "bascnxxxxxxxxx",  // 多维表格 token
    "table_id": "tblxxxxxxxx",
    "revision": 1
  }
}
```

#### 方式二：从 URL 获取（Base 类型）

如果多维表格 URL 以 `feishu.cn/base` 开头，`app_token` 为 URL 中高亮部分：

```text
https://www.feishu.cn/base/bascnxxxxxxxxx?table=tblxxxx
                     ↑↑↑↑↑↑↑↑
                   app_token
```

#### 方式三：通过接口获取（Wiki 类型）

如果多维表格 URL 以 `feishu.cn/wiki` 开头，需要调用[获取知识空间节点信息](https://open.feishu.cn/document/server-docs/docs/wiki-v2/space-node/get_node)接口获取 `app_token`：

- 接口路径：`POST /open-apis/wiki/v2/spaces/get_node`
- 请求参数中的 `obj_token` 即为多维表格的 `app_token`

### 写入数据到多维表格

获取到 `app_token` 后，可通过[新增记录](https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table-record/create)接口向多维表格写入数据。

在轻易云方案中配置数据写入：

1. 配置源平台（如 ERP、数据库等）的查询参数
2. 配置目标平台为飞书多维表格
3. 填写目标参数：
   - **app_token**：多维表格标识
   - **table_id**：目标数据表 ID（可选，默认为第一个表）
4. 配置字段映射，将源数据字段映射到多维表格字段
5. 保存并启动方案

> [!TIP]
> 多维表格字段名区分大小写，配置映射时请确保字段名称与飞书表格中完全一致。

## 审批推送集成

### 审批事件订阅

飞书审批表单默认不会触发事件推送，需要通过接口开启订阅：

1. 获取审批表单 ID：
   - 登录飞书审批后台
   - 进入表单设计页面
   - 从 URL 中获取表单 ID（如 `?id=123456789`）

2. 调用[订阅审批事件](https://open.feishu.cn/document/server-docs/approval-v4/event/event-interface/subscribe)接口开启订阅：
   - 在轻易云方案中使用 **FSSubscribeQueryAdapter** 适配器
   - 传入表单 ID 作为参数

```text
接口：POST /open-apis/approval/v4/subscriptions/subscribe
参数：{
  "approval_code": "表单ID"
}
```

> [!NOTE]
> **FSSubscribeQueryAdapter** 适配器专门用于处理订阅审批事件接口的调用，不支持其他接口。

### 配置回调事件

在飞书应用的**事件与回调**配置中，添加需要监听的事件类型：

| 事件类型 | 说明 | 适用场景 |
| -------- | ---- | -------- |
| 审批任务通过 | 审批节点通过时触发 | 审批通过后推送业务系统 |
| 审批任务拒绝 | 审批被拒绝时触发 | 记录审批驳回状态 |
| 审批任务转交 | 审批转交时触发 | 记录审批流转历史 |
| 审批任务撤回 | 审批撤回时触发 | 撤销业务单据 |

### 方案配置示例

配置飞书审批推送方案的请求参数：

```json
{
  "子表对象": [
    {
      "字段名": "审批表单ID",
      "result": "approval",
      "distribute_to": "目标方案ID"
    }
  ]
}
```

参数说明：

| 参数 | 必填 | 说明 |
| ---- | ---- | ---- |
| 字段名 | ✅ | 审批表单的 ID，作为子表对象的标识 |
| result | ✅ | 固定值 `approval`，表示审批推送类型 |
| distribute_to | ✅ | 数据分发目标方案的 ID |

> [!IMPORTANT]
> 飞书中有多种审批表单，包括系统预设表单和自定义表单，这些表单默认都不会触发事件推送，必须通过上述订阅接口逐个开启。

## 常见问题

### Q: 如何获取飞书应用的 App ID 和 App Secret？

登录飞书开放平台 → 进入应用详情 → **凭证与基础信息**页面，可以查看和复制 App ID 和 App Secret。注意 App Secret 仅在创建时完整显示，请妥善保存。

### Q: 回调地址验证失败怎么办？

请检查以下几点：

1. 回调地址是否公网可访问，且使用 HTTPS 协议
2. 方案 ID 是否正确填写在回调地址中
3. Verification Token 是否已正确配置到方案
4. 飞书应用的**事件与回调**配置是否已保存

### Q: 审批数据没有实时推送？

可能原因及解决方法：

1. **未开启事件订阅**：确认已通过 FSSubscribeQueryAdapter 订阅对应审批表单的事件
2. **回调配置错误**：检查回调地址和加密配置是否正确
3. **权限不足**：确认应用已获得 `approval:approval` 权限并已发布

### Q: 多维表格写入失败？

常见原因：

1. **app_token 错误**：请按照文档中的三种方式重新获取
2. **字段名不匹配**：检查字段映射配置，确保与飞书表格字段名完全一致
3. **数据类型不匹配**：飞书多维表格字段有类型限制（如数字、文本、日期等），请确保写入数据符合字段类型
4. **权限不足**：确认应用已获得 `bitable:bitable` 权限

### Q: 飞书和 Lark（国际版）的区别？

飞书（Feishu）和 Lark 是字节跳动推出的两套协同办公产品：

- **飞书**：面向中国大陆市场，服务器位于国内
- **Lark**：面向海外市场，服务器位于海外

两者的 API 接口基本一致，但域名和数据中心不同。轻易云飞书连接器同时兼容飞书和 Lark，配置时请根据实际使用的平台填写对应的 API 域名。

## 相关文档

- [钉钉连接器](./dingtalk) — 钉钉集成配置指南
- [企业微信连接器](./wecom) — 企业微信集成配置指南
- [OA 连接器概览](./README) — 所有 OA 协同类连接器
- [配置连接器](../../guide/configure-connector) — 连接器通用配置指南
- [新建集成方案](../../guide/create-integration) — 方案创建完整教程

## 外部参考

- [飞书开放平台](https://open.feishu.cn/)
- [飞书审批 API 文档](https://open.feishu.cn/document/server-docs/approval-v4/overview)
- [飞书多维表格 API 文档](https://open.feishu.cn/document/server-docs/docs/bitable-v1/overview)
