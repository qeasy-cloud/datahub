# 钉钉连接器

钉钉是阿里巴巴集团打造的企业级智能移动办公平台，提供审批流程、考勤管理、组织架构、消息推送等丰富功能。通过轻易云 iPaaS 钉钉连接器，您可以实现钉钉与 ERP、财务等业务系统的深度集成，构建高效的企业数字化 workflow。

## 前置准备

在使用钉钉连接器之前，您需要在钉钉开放平台完成以下配置：

### 1. 获取企业 CorpID

1. 登录 [钉钉开放平台](https://open-dev.dingtalk.com/#/)
2. 在页面右侧查看并记录 **CorpID**

![钉钉 CorpID 位置](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1631259726393-8d3d3cb9-c662-4eb9-9be5-174359fe4daa_20260306_200703_818160.png)

### 2. 创建自建应用

1. 进入钉钉开放平台的**应用开发**页面
2. 点击**创建应用**，选择**企业内部应用**
3. 填写应用名称（如"轻易云集成"）并创建

![创建应用](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1631259564648-01bfbdc2-b223-4b9e-b538-37ed03d0e9bf_20260306_200704_346600.png)

### 3. 保存应用凭证

创建应用后，记录以下关键信息：

| 参数 | 说明 | 获取位置 |
| ---- | ---- | -------- |
| `AgentId` | 应用代理标识 | 应用详情页 |
| `AppKey` | 应用标识 | 应用详情页 |
| `AppSecret` | 应用密钥 | 应用详情页 |

![应用凭证](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1631259669247-b185ca97-ba91-4a0d-9308-017f57208137_20260306_200704_839738.png)

### 4. 配置服务器 IP 白名单

1. 进入应用详情的**开发配置**页面
2. 配置**服务器出口 IP**：
   - 填写轻易云服务器的出口 IP（如 `116.63.136.29`，请以实际提供为准）
3. 配置**应用首页地址**：
   - 填写 `https://pro.qliang.cloud`（轻易云平台地址）

![IP 白名单配置](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1631259858404-ac2438b0-2a52-4567-a02d-a5a5d09afe1f_20260306_200705_371747.png)

![首页地址配置](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1631259925517-83ddd3d2-f391-441a-bd5d-5b643dfdafb3_20260306_200705_947443.png)

### 5. 开通接口权限

进入**权限管理**页面，根据业务需要开通以下权限：

| 权限类别 | 权限名称 | 说明 |
| -------- | -------- | ---- |
| OA 审批 | 审批实例读取 | 获取审批单据数据 |
| OA 审批 | 审批实例写入 | 提交审批意见 |
| 通讯录 | 通讯录部门信息读 | 获取组织架构 |
| 通讯录 | 通讯录成员信息读 | 获取员工信息 |
| 文件存储 | Storage.File.Write | 上传附件到钉盘 |
| 考勤 | 考勤数据读取 | 获取打卡记录 |

![权限配置](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1631260074183-85faede5-d51b-433d-a824-fa6fe8b50860_20260306_200706_510152.png)

## 创建连接器

完成钉钉端配置后，在轻易云平台创建连接器：

1. 进入**连接器管理**页面，点击**新建连接器**
2. 选择连接器类型为**钉钉**
3. 填写配置参数：

| 参数 | 说明 | 示例值 |
| ---- | ---- | ------ |
| **CorpID** | 企业唯一标识 | `dingxxxxxxxxxxxxxxxx` |
| **AgentId** | 应用代理标识 | `123456789` |
| **AppKey** | 应用标识 | `dingxxxxxxxxxxxxxxxx` |
| **AppSecret** | 应用密钥 | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

4. 点击**测试连接**验证配置
5. 保存连接器

![连接器配置](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1631260268966-b773b93d-939d-4937-97ce-7c0257f73386_20260306_200706_921513.png)

## 配置说明

### 查询适配器

使用 `DingTalkQueryAdapter` 进行数据查询。

**常用接口**：

| 接口 | 说明 |
| ---- | ---- |
| `topapi/processinstance/listids` | 查询审批实例 ID 列表 |
| `topapi/processinstance/get` | 获取审批实例详情 |
| `topapi/smartwork/hrm/employee/queryonjob` | 查询在职员工列表 |
| `topapi/attendance/list` | 查询考勤打卡记录 |

**请求参数示例**（查询审批实例）：

```json
{
  "process_code": "PROC-12345678-1234-1234-1234-123456789012",
  "start_time": "{{LAST_SYNC_TIME|timestamp_ms}}",
  "end_time": "{{CURRENT_TIME|timestamp_ms}}"
}
```

### 写入适配器

使用 `DingTalkExecuteAdapter` 进行数据写入。

**常用接口**：

| 接口 | 说明 |
| ---- | ---- |
| `topapi/processinstance/create` | 创建审批实例 |
| `topapi/processinstance/comment/add` | 添加审批评论 |
| `topapi/message/corpconversation/asyncsend_v2` | 发送工作通知 |

## 回调事件接收配置

如需实时接收钉钉审批事件，需配置回调接收方案。

### 1. 启用钉钉事件监听

1. 进入钉钉应用的**事件与回调**页面
2. 点击**生成**按钮，让钉钉自动生成 **EncodingAESKey** 和 **Token**

![事件与回调配置](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1659528331306-874aff9d-eb8b-43cc-835d-b6f2f41ba44f_20260306_200707_444636.png)

![生成密钥](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1659528397041-d8a92ad6-973f-49fa-8581-7cd4bcd93cb5_20260306_200708_072213.png)

3. 复制以下信息到轻易云平台的连接器**更多信息**中的 `callback.dingtalk` 配置：
   - **aes_key**：钉钉生成的 EncodingAESKey
   - **token**：钉钉生成的 Token

4. 将轻易云生成的**回调 URL** 复制到钉钉的**请求网址**字段

![回调配置](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1659528491042-d528bcfe-49ad-4939-b34c-ff210a11cbe5_20260306_200708_687498.png)

### 2. 设置监听事件

在钉钉**事件与回调**页面，勾选需要监听的事件类型：

| 事件类型 | 说明 |
| -------- | ---- |
| `bpms_instance_change` | 审批实例状态变更 |
| `bpms_task_change` | 审批任务状态变更 |

![设置监听事件](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1659528585730-f0e63586-c00e-4321-85f4-366697ee2f0b_20260306_200709_400414.png)

### 3. 配置回调接收者方案

在轻易云平台创建**回调接收者方案**：

1. **源平台**：选择钉钉
2. **接口**：选择**钉钉审批事件分发者**
3. **目标平台**：选择**轻易云集成平台**
4. **接口**：选择**写入空操作**（或实际业务接口）

#### 配置要监听的表单

在方案配置中，指定要监听的钉钉审批表单 ID：

![配置表单 ID](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1659528997955-153fe81b-9969-4286-9afc-49fdc2bb58ce_20260306_200710_149132.png)

#### 配置分发适配器

如需将事件分发给特定集成方案处理，配置适配器为：

```text
\Adapter\Dingtalk\DingTalkRecipient
```

![配置分发适配器](https://qeasy.obs.cn-southwest-2.myhuaweicloud.com/datahub/7_integrated/1659529032618-abe0dda1-a369-463d-87a2-cf7e0e12b6be_20260306_200711_295328.png)

## 提交审批意见并上传附件

### 场景说明

在审批流程集成中，常需在钉钉审批单中提交处理意见并上传附件（如盖章后的合同扫描件）。

### 适配器配置

使用专用适配器 `DingtalkApprovalFilesExecute`。

> [!TIP]
> 参考方案链接：[钉钉审批意见提交方案](https://pro.qliang.cloud/strategy/detail/fe421bf1-1cdd-3779-8e54-1ef117f85a18#BasicSummary)

### 请求参数配置

接口：`topapi/processinstance/create`

请求方法：`POST`

关键参数说明：

| 参数 | 类型 | 说明 |
| ---- | ---- | ---- |
| `originator_user_id` | string | 审批发起人的 UserID |
| `dept_id` | number | 发起人所在部门 ID |
| `unionId` | string | 发起人的 UnionID |

> [!NOTE]
> 以上参数在获取审批详情时会返回，可通过映射关系获取。

**配置示例**：

```json
{
  "agent_id": "{{DINGTALK_AGENT_ID}}",
  "process_code": "PROC-XXXX-XXXX",
  "originator_user_id": "{{originator_user_id}}",
  "dept_id": "{{dept_id}}",
  "form_component_values": [
    {
      "name": "审批意见",
      "value": "已审核通过"
    }
  ]
}
```

### 队列执行效果

配置完成后，审批意见提交和附件上传会以队列形式异步执行，确保可靠性：

![队列效果](https://pic.qeasy.cloud/2023-11-07/1699339076-397652-image.png)

### 所需权限

确保钉钉应用已开通以下权限：

1. **OA 审批** — 审批实例写入权限
2. **Storage.File.Write** — 钉盘文件写入权限
3. **获取凭证** — 访问接口凭证
4. **钉盘** — 钉盘空间访问权限
5. **存储** — 文件存储权限

## 常见问题

### Q: 如何获取审批模板的 process_code？

1. 登录 [钉钉开放平台](https://open-dev.dingtalk.com/)
2. 进入**应用详情** → **审批模板管理**
3. 找到目标模板，复制模板编码（即 process_code）

### Q: 回调验证失败怎么办？

1. 检查 **EncodingAESKey** 和 **Token** 是否正确复制
2. 确认回调 URL 已正确填写到钉钉后台
3. 检查服务器出口 IP 是否已添加到白名单
4. 确保应用已发布并可见范围包含测试人员

### Q: 审批附件如何自动下载？

在源平台配置中启用**附件下载**选项：

1. 编辑集成方案的源平台配置
2. 勾选**下载审批附件**
3. 在数据映射中使用 `attachments` 字段获取附件列表

### Q: 如何获取用户的 UnionID？

调用钉钉接口 `topapi/user/getbyunionid` 或使用审批详情中的 `originator_user_id` 关联查询。

### Q: 审批意见提交失败？

请检查：

1. 应用是否具备审批写入权限
2. 审批实例是否处于可评论状态
3. 上传附件大小是否超过限制（单文件最大 50MB）
4. 钉盘空间是否已满

## 相关文档

- [钉钉开放平台文档](https://open.dingtalk.com/document/)
- [审批流集成方案](../../standard-schemes/oa-integration)
- [配置连接器](../../guide/configure-connector)
- [OA / 协同类连接器概览](./README)
