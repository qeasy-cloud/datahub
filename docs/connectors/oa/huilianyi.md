# 汇联易连接器

汇联易（Helios）是国内领先的企业费用管理平台，提供全面的报销管理、费用控制、发票管理和审批流程等功能。通过轻易云 iPaaS 汇联易连接器，您可以实现汇联易与 ERP、财务系统、OA 等业务系统的深度集成，实现费用数据的自动同步和审批流程的无缝对接。

## 前置准备

在使用汇联易连接器之前，您需要在汇联易开放平台完成以下配置：

### 1. 注册汇联易开放平台账号

1. 登录 [汇联易开放平台](https://opendocs.huilianyi.com/)
2. 完成企业实名认证
3. 进入**应用管理**页面创建应用

### 2. 获取应用凭证

创建应用后，记录以下关键信息：

| 参数 | 说明 | 获取位置 |
| ---- | ---- | -------- |
| `appKey` | 应用标识 | 应用详情页 |
| `appSecret` | 应用密钥 | 应用详情页 |
| `companyId` | 企业标识 | 企业信息页 |

> [!IMPORTANT]
> `appSecret` 仅在创建时显示，请妥善保存。如遗失需要重新生成。

### 3. 配置接口权限

根据业务需求，在开放平台申请以下接口权限：

| 权限类别 | 接口名称 | 说明 |
| -------- | -------- | ---- |
| 申请数据 | 申请列表查询 | 查询费用申请单列表 |
| 申请数据 | 申请详情查询 | 获取申请单详细信息 |
| 审批数据 | 审批历史查询 | 获取审批流程历史记录 |
| 基础数据 | 组织架构查询 | 获取部门、员工信息 |

### 4. 配置服务器白名单

将轻易云服务器的出口 IP 添加到汇联易白名单（请联系技术支持获取具体 IP 地址）。

## 创建连接器

完成汇联易端配置后，在轻易云平台创建连接器：

1. 进入**连接器管理**页面，点击**新建连接器**
2. 选择连接器类型为**汇联易**
3. 填写配置参数：

| 参数 | 说明 | 示例值 |
| ---- | ---- | ------ |
| **appKey** | 应用标识 | `hly_xxxxxxxxxxxxxxxx` |
| **appSecret** | 应用密钥 | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| **companyId** | 企业标识 | `xxxxxxxx` |
| **环境** | 对接环境 | `production` 或 `sandbox` |

4. 点击**测试连接**验证配置
5. 保存连接器

## 配置说明

### 查询适配器

使用 `HeliosApprovalQueryAdapter` 进行数据查询。

**常用接口**：

| 接口 | 说明 | 请求方式 |
| ---- | ---- | -------- |
| `/api/open/publicApplication` | 查询申请列表 | GET |
| `/api/open/publicApplication/{id}` | 查询申请详情 | GET |
| `/api/open/approvalHistory` | 查询审批历史 | GET |
| `/api/open/department` | 查询部门列表 | GET |
| `/api/open/employee` | 查询员工列表 | GET |

### 审批意见查询

#### 场景说明

在费用管理集成场景中，常需将汇联易中的审批意见（包括审批人、审批时间、审批结果、审批备注等）同步到 ERP 或财务系统，形成完整的费用审批记录。

#### 适配器配置

使用专用适配器 `HeliosApprovalQueryAdapter`。

> [!TIP]
> 参考方案链接：[汇联易审批意见查询方案](https://pro.qliang.cloud/strategy/detail/192eac7c-88c3-3bde-9760-49eaa6ee37c9#BasicSummary)

#### 配置步骤

**第一步：配置列表查询接口**

接口路径：`/api/open/publicApplication`

请求方法：`GET`

配置参数说明：

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `startTime` | string | ✅ | 查询开始时间（yyyy-MM-dd HH:mm:ss） |
| `endTime` | string | ✅ | 查询结束时间（yyyy-MM-dd HH:mm:ss） |
| `status` | string | — | 单据状态（如：`APPROVING` 审批中、`APPROVED` 已通过） |
| `page` | number | — | 页码，默认 1 |
| `pageSize` | number | — | 每页条数，默认 50 |

在数据映射中配置 `id` 和 `number` 字段，这两个字段将在查询申请详情时使用。

![列表查询配置](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/others_img_067_1698977460_179247_image_png_7Etplv_syqr462i7n_qeas.png?st=1)

**第二步：配置详情查询接口**

基于列表查询返回的 `id` 字段，配置详情查询接口：

接口路径：`/api/open/publicApplication/{id}`

请求方法：`GET`

![详情查询配置](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/others_img_068_1698977604_247847_image_png_7Etplv_syqr462i7n_qeas.png?st=1)

**第三步：配置审批历史查询**

接口路径：`/api/open/approvalHistory`

请求方法：`GET`

请求参数配置：

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `applicationId` | string | ✅ | 申请单 ID（使用列表查询返回的 id） |

![审批历史参数配置](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/others_img_069_1698977622_650765_image_png_7Etplv_syqr462i7n_qeas.png?st=1)

#### 队列执行效果

配置完成后，系统会以队列形式异步执行数据抓取：

1. 首先查询符合条件的申请单列表
2. 针对每个申请单查询详细信息
3. 查询每个申请单的审批历史记录
4. 将数据推送至目标系统

![队列效果 1](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/others_img_070_1698977658_543775_image_png_7Etplv_syqr462i7n_qeas.png?st=1)

![队列效果 2](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/others_img_071_1698977674_823040_image_png_7Etplv_syqr462i7n_qeas.png?st=1)

#### 返回数据示例

**审批历史接口返回示例**：

```json
{
  "code": 0,
  "data": [
    {
      "approverId": "EMP_123456",
      "approverName": "张三",
      "action": "APPROVE",
      "actionName": "同意",
      "comment": "费用合理，同意报销",
      "approveTime": "2023-11-03 14:30:25"
    },
    {
      "approverId": "EMP_789012",
      "approverName": "李四",
      "action": "APPROVE",
      "actionName": "同意",
      "comment": "审核通过",
      "approveTime": "2023-11-03 16:45:10"
    }
  ]
}
```

### 写入适配器

使用 `HeliosExecuteAdapter` 进行数据写入。

> [!NOTE]
> 汇联易开放平台的写入权限需要单独申请，请确保您的应用已获得相应权限。

**常用接口**：

| 接口 | 说明 | 请求方式 |
| ---- | ---- | -------- |
| `/api/open/publicApplication` | 创建申请单 | POST |
| `/api/open/publicApplication/{id}/cancel` | 撤销申请单 | POST |

## 数据映射参考

### 申请单字段映射

| 汇联易字段 | 类型 | 说明 | 示例值 |
| ---------- | ---- | ---- | ------ |
| `id` | string | 申请单唯一标识 | `APP_123456789` |
| `number` | string | 申请单号 | `BX20231103001` |
| `title` | string | 申请标题 | `11 月差旅报销` |
| `applicantId` | string | 申请人 ID | `EMP_123456` |
| `applicantName` | string | 申请人姓名 | `张三` |
| `departmentId` | string | 部门 ID | `DEPT_001` |
| `departmentName` | string | 部门名称 | `销售部` |
| `amount` | number | 申请金额 | `1580.50` |
| `currency` | string | 币种 | `CNY` |
| `status` | string | 单据状态 | `APPROVED` |
| `createTime` | string | 创建时间 | `2023-11-03 10:00:00` |
| `updateTime` | string | 更新时间 | `2023-11-03 16:45:10` |

### 审批记录字段映射

| 汇联易字段 | 类型 | 说明 | 示例值 |
| ---------- | ---- | ---- | ------ |
| `approverId` | string | 审批人 ID | `EMP_789012` |
| `approverName` | string | 审批人姓名 | `李四` |
| `action` | string | 审批动作 | `APPROVE` / `REJECT` / `TRANSFER` |
| `actionName` | string | 动作名称 | `同意` / `驳回` / `转交` |
| `comment` | string | 审批意见 | `费用合理，同意报销` |
| `approveTime` | string | 审批时间 | `2023-11-03 14:30:25` |
| `nodeName` | string | 审批节点名称 | `部门经理审批` |

## 常见问题

### Q: 如何获取申请单的完整审批流程？

调用审批历史查询接口 `/api/open/approvalHistory`，传入申请单 ID，即可获取该申请单的所有审批记录，按时间顺序排列。

### Q: 接口返回的审批时间与实际时间不一致？

汇联易接口返回的时间为北京时间（东八区）。如您的系统使用其他时区，请在数据映射中进行时区转换。

### Q: 如何处理审批意见中的特殊字符？

审批意见可能包含换行符、引号等特殊字符，建议在数据映射中使用以下处理方式：

```javascript
// 替换换行符为逗号
{{comment|replace('\n', ', ')}}

// 或使用转义
{{comment|json_encode}}
```

### Q: 如何同步已归档的历史单据？

如需同步历史数据，请在列表查询接口中：

1. 设置较大的时间范围（建议每次不超过 3 个月）
2. 调整分页参数 `pageSize`（最大支持 500）
3. 使用定时策略分批执行

> [!WARNING]
> 大批量历史数据同步可能影响接口调用频率限制，建议分批次执行并控制并发量。

### Q: 连接测试失败如何处理？

请检查以下配置项：

1. **appKey / appSecret** 是否正确（注意区分大小写）
2. **companyId** 是否对应正确的企业
3. **环境** 选择是否正确（生产环境 / 沙箱环境）
4. 服务器 IP 是否已添加到汇联易白名单
5. 应用是否已获得相应接口权限

### Q: 如何获取费用明细数据？

申请详情接口 `/api/open/publicApplication/{id}` 会返回完整的费用明细列表，包含费用类型、金额、发票信息等字段。

## 相关文档

- [汇联易开放平台文档](https://opendocs.huilianyi.com/)
- [审批历史查询接口文档](https://opendocs.huilianyi.com/implement/business-data/approval-history/query-approval-history.html)
- [配置连接器](../../guide/configure-connector)
- [新建集成方案](../../guide/create-integration)
- [OA / 协同类连接器概览](./README)
