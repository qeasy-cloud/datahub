# 企业微信连接器

企业微信是腾讯微信团队打造的企业通讯与办公工具，提供即时通讯、审批流程、考勤管理、日程会议等丰富的企业级功能。通过轻易云 iPaaS 企业微信连接器，您可以实现企业微信与 ERP、CRM、HRM 等业务系统的深度集成，构建高效的数字化办公 workflow。

## 前置准备

在使用企业微信连接器之前，您需要完成以下配置：

### 1. 获取企业凭证

1. 登录 [企业微信管理后台](https://work.weixin.qq.com/wework_admin/frame)
2. 在**我的企业**页面获取以下信息：

| 参数 | 说明 | 获取位置 |
| ---- | ---- | -------- |
| `CorpID` | 企业唯一标识 | 管理后台 → 我的企业 |
| `AgentId` | 应用标识 | 应用管理 → 应用详情 |
| `Secret` | 应用密钥 | 应用管理 → 应用详情 |

### 2. 创建企业应用

1. 进入企业微信管理后台的**应用管理**
2. 点击**创建应用**
3. 填写应用名称（如"轻易云集成"）并上传应用 Logo
4. 记录生成的 **AgentId** 和 **Secret**

### 3. 配置应用可见范围

1. 在应用详情页的**可见范围**中，选择需要使用该应用的组织架构或成员
2. 确保需要集成的员工在可见范围内

### 4. 设置可信域名与 IP 白名单

1. 进入应用详情的**网页授权及 JS-SDK**配置
2. 设置**可信域名**：`pro.qliang.cloud`
3. 在**企业可信 IP** 中添加轻易云服务器的出口 IP

> [!WARNING]
> 若未配置正确的 IP 白名单，接口调用将返回 "not allow to access from your ip" 错误。

## 创建连接器

完成企业微信端配置后，在轻易云平台创建连接器：

1. 进入**连接器管理**页面，点击**新建连接器**
2. 选择连接器类型为**企业微信**
3. 填写配置参数：

| 参数 | 说明 | 示例值 |
| ---- | ---- | ------ |
| **CorpID** | 企业唯一标识 | `wwxxxxxxxxxxxxxxxx` |
| **AgentId** | 应用标识 | `1000002` |
| **Secret** | 应用密钥 | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

4. 点击**测试连接**验证配置
5. 保存连接器

## 审批流集成

### 获取审批模板 ID

在配置审批集成前，需要获取审批模板的 ID：

1. 登录企业微信管理后台，进入**应用管理** → **审批**
2. 点击编辑对应的表单模板
3. 从浏览器地址栏中复制模板 ID（即 URL 中的 template_id 参数）

### 查询审批模板详情

使用以下配置查询表单模板的字段结构：

**适配器**：`\Adapter\Wxwork\WxworkV2QueryAdapter`

**接口**：`/cgi-bin/oa/gettemplatedetail`

**请求参数配置**：

| 字段 | 字段名 | 字段值 | 字段类型 |
| ---- | ------ | ------ | -------- |
| `template_id` | 表单 ID | `模板ID` | 字符串 |
| `detailkey` | 详情 Key | `template_content` | 字符串 |

**响应参数配置**：

| 字段 | 字段名 | 字段值 | 字段类型 |
| ---- | ------ | ------ | -------- |
| `statusKey` | 响应状态字段 | `errcode` | 字符串 |
| `statusValue` | 成功状态值 | `0` | 字符串 |
| `dataKey` | 返回数据字段 | `template_content` | 字符串 |
| `pageKey` | 分页 Key | `cursor` | 字符串 |
| `islist` | 是列表还是详情 | `detail` | 字符串 |

> [!TIP]
> 查询成功后，可在数据管理中查看审批表单的所有控件字段信息，包括控件类型（Text、Textarea、Date、Selector 等）和控件 ID。

## 获取审批数据

### 查询审批单号列表

使用以下配置获取审批实例列表：

**适配器**：`\Adapter\Wxwork\WxworkV2QueryAdapter`

**接口**：`/cgi-bin/oa/getapprovalinfo`

**请求参数配置**：

| 字段 | 字段名 | 字段值 | 字段类型 |
| ---- | ------ | ------ | -------- |
| `starttime` | 开始时间 | `{{LAST_SYNC_TIME}}` | 字符串 |
| `endtime` | 结束时间 | `{{CURRENT_TIME}}` | 字符串 |
| `cursor` | 游标 | `0` | 字符串 |
| `size` | 每页大小 | `100` | 整型 |
| `filters` | 请求过滤 | - | 子表对象 |
| `filters.0` | 过滤条件 | - | 子表对象 |
| `filters.0.key` | 过滤字段 | `template_id` | 字符串 |
| `filters.0.value` | 过滤值 | `模板ID` | 字符串 |

**其他请求参数**：

| 字段 | 字段名 | 字段值 | 字段类型 |
| ---- | ------ | ------ | -------- |
| `otherapi` | 详情接口 | `/cgi-bin/oa/getapprovaldetail` | 字符串 |
| `otherkey` | 详情 Key | `sp_no` | 字符串 |
| `detailkey` | 详情字段 | `info` | 字符串 |

**响应参数配置**：

| 字段 | 字段名 | 字段值 | 字段类型 |
| ---- | ------ | ------ | -------- |
| `statusKey` | 响应状态字段 | `errcode` | 字符串 |
| `statusValue` | 成功状态值 | `0` | 整型 |
| `dataKey` | 返回数据字段 | `sp_no_list` | 字符串 |
| `pageKey` | 分页 Key | `cursor` | 字符串 |
| `islist` | 是否是列表 | `list` | 字符串 |

## 发起审批

### 审批发起配置

使用以下配置在企业微信中发起审批流程：

**适配器**：`\Adapter\Wxwork\WxworkV2ExecuteAdapter`

**接口**：`/cgi-bin/oa/applyevent`

### 请求参数说明

| 字段 | 字段名 | 字段值 | 字段类型 |
| ---- | ------ | ------ | -------- |
| `creator_userid` | 申请人 UserID | `申请人ID` | 字符串 |
| `template_id` | 模板 ID | `模板ID` | 字符串 |
| `use_template_approver` | 审批人模式 | `1` | 字符串 |

### 表单控件配置

审批表单中的控件需要按以下格式配置：

#### 普通输入框

| 字段 | 字段名 | 字段值 | 字段类型 |
| ---- | ------ | ------ | -------- |
| `apply_data_1.control` | 控件类型 | `Text` | 字符串 |
| `apply_data_1.id` | 控件 ID | `Text-xxxxxxxxxxxxx` | 字符串 |
| `apply_data_1.value` | 控件值 | `{{字段值}}` | 字符串 |

#### 明细表格

| 字段 | 字段名 | 字段值 | 字段类型 |
| ---- | ------ | ------ | -------- |
| `apply_data_2.control` | 控件类型 | `Table` | 字符串 |
| `apply_data_2.id` | 控件 ID | `Table-xxxxxxxxxxxxx` | 字符串 |
| `apply_data_2.children` | 子表内容 | - | 多行分录 |

> [!NOTE]
> 控件 ID 需要从模板详情查询中获取。多个控件时，通过更改 `apply_data_X` 的后缀序号进行配置（如 `apply_data_0`、`apply_data_1` 等）。

### 响应参数配置

| 字段 | 字段名 | 字段值 | 字段类型 |
| ---- | ------ | ------ | -------- |
| `statusKey` | 响应状态字段 | `errcode` | 字符串 |
| `statusValue` | 成功状态值 | `0` | 整型 |

## 应用机器人配置

企业微信机器人可用于接收系统消息推送、审批通知等场景。

### 1. 创建企业应用

1. 登录 [企业微信管理后台](https://work.weixin.qq.com/wework_admin/loginpage_wx)
2. 进入**应用管理**，点击**创建应用**
3. 填写应用名称，支持小程序类型

### 2. 获取应用凭证

创建完成后，记录以下信息：

- **AgentId**：如 `1000XXXXXX`，应用唯一标识
- **Secret**：应用密钥

### 3. 配置接收消息

1. 在应用详情的**接收消息**中，设置**接收消息服务器配置**
2. 服务器地址格式：

```json
{{服务域名}}/api/wxwork/oa/{{方案ID}}
```

3. 在轻易云平台配置回调参数（Token、EncodingAESKey 等）

### 4. 方案配置

创建集成方案并配置写入调度者：

1. **源平台**：可选择轻易云
2. **目标平台**：企业微信
3. **适配器**：`WxWorkGPTAdapter`
4. 配置应用 ID 和其他参数

### 5. 设置 IP 白名单

在企业微信应用的**企业可信 IP**中，添加轻易云服务器的出口 IP。

## 打卡考勤获取

### 查询用户 ID 列表

首先配置查询用户 ID 的方案：

**适配器**：`\Adapter\Wxwork\WxworkQueryAdapter`

**接口**：`/cgi-bin/user/list_id`

### 获取打卡日报

使用以下配置获取员工的打卡日报信息：

**适配器**：`\Adapter\Wxwork\WxworkDKQueryAdapter`

**请求参数配置**：

| 字段 | 字段名 | 字段值 | 字段类型 |
| ---- | ------ | ------ | -------- |
| `starttime` | 开始时间 | `_function UNIX_TIMESTAMP(DATE_ADD(CURDATE(), INTERVAL -1 DAY))` | 整型 |
| `endtime` | 结束时间 | `_function UNIX_TIMESTAMP(DATE_ADD(CURDATE(), INTERVAL -1 DAY))` | 整型 |
| `dep_strategy` | 关联方案 ID | `查询用户ID方案的ID` | 字符串 |
| `joinField` | 关联字段 | `userid` | 字符串 |

**主键配置**：`{{random}}`

**编码配置**：`base_info.name`

**其他响应参数**：

| 字段 | 字段值 |
| ---- | ------ |
| `listkey` | `datas` |

> [!TIP]
> `starttime` 和 `endtime` 使用 Unix 时间戳格式。上例中获取的是前一天的打卡数据。

## 控件类型说明

企业微信审批表单支持多种控件类型，配置时需注意：

| 控件类型 | 说明 | 值格式 |
| -------- | ---- | ------ |
| `Text` | 单行文本 | 纯文本字符串 |
| `Textarea` | 多行文本 | 纯文本字符串 |
| `Number` | 数字 | 数值字符串 |
| `Money` | 金额 | 数值字符串 |
| `Date` | 日期 | Unix 时间戳（秒） |
| `DateRange` | 日期范围 | 开始时间,结束时间 |
| `Selector` | 单选/多选 | 选项 ID |
| `Contact` | 成员/部门 | 成员 UserID 或部门 ID |
| `Table` | 明细表格 | 子表对象 |
| `File` | 附件 | 文件 ID |

## 常见问题

### Q: 如何获取审批模板 ID？

1. 登录企业微信管理后台
2. 进入**应用管理** → **审批**
3. 点击编辑目标表单模板
4. 从浏览器地址栏中复制 `template_id` 参数值

### Q: 如何获取 UserID？

1. 在通讯录中查看成员详情
2. 或通过接口 `/cgi-bin/user/list_id` 获取企业内所有用户 ID

### Q: 审批数据获取返回空列表？

请检查：

1. `starttime` 和 `endtime` 是否为 Unix 时间戳格式
2. `filters` 中的 `template_id` 是否正确
3. 应用是否有审批数据读取权限
4. 时间范围内是否确实有审批数据

### Q: 审批发起失败，提示参数错误？

1. 检查控件 ID 是否从模板详情中正确获取
2. 确认控件值格式与控件类型匹配（如日期类型需传入时间戳）
3. 验证申请人 UserID 是否有效且在应用可见范围内

### Q: 如何获取审批人模式？

`use_template_approver` 参数：

- `0`：自定义审批人，需传入审批人列表
- `1`：使用模板配置的审批流程
- `2`：同时启用自定义审批人和模板审批人

### Q: 打卡数据获取不完整？

1. 检查 `starttime` 和 `endtime` 的时间范围是否合理
2. 确认关联方案是否正确返回了用户 ID 列表
3. 验证应用是否有打卡数据的读取权限

## 相关文档

- [企业微信开发者文档](https://developer.work.weixin.qq.com/document)
- [审批流集成方案](../../standard-schemes/oa-integration)
- [配置连接器](../../guide/configure-connector)
- [OA / 协同类连接器概览](./README)
