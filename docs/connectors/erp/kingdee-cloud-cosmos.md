# 金蝶云苍穹连接器

金蝶云苍穹是金蝶推出的云原生企业 PaaS 平台，本文档介绍如何在轻易云 iPaaS 中配置和使用金蝶云苍穹连接器。

## 连接器概述

| 属性 | 说明 |
|-----|------|
| 连接器名称 | kingdee-cloud-cosmos |
| 支持版本 | 金蝶云苍穹 全部版本 |
| 连接方式 | OpenAPI |
| 认证方式 | AppKey + AppSecret |

## 前置条件

在使用金蝶云苍穹连接器前，您需要：

1. 拥有金蝶云苍穹的访问权限
2. 在苍穹平台注册应用并获取凭证
3. 开通所需的 API 接口权限

## 配置参数

### 连接配置

| 参数 | 必填 | 说明 |
|-----|------|------|
| serverUrl | 是 | 苍穹服务地址 |
| acctId | 是 | 数据中心 ID |
| appKey | 是 | 应用标识 |
| appSecret | 是 | 应用密钥 |
| username | 是 | 用户名 |
| password | 是 | 密码 |

### 配置示例

```json
{
  "serverUrl": "https://api.kingdee.com",
  "acctId": "20240101",
  "appKey": "your_app_key",
  "appSecret": "your_app_secret",
  "username": "administrator",
  "password": "your_password"
}
```

## 获取凭证步骤

1. 登录金蝶云苍穹管理后台
2. 进入「系统管理」→「第三方应用管理」
3. 点击「新建应用」
4. 填写应用信息并保存
5. 记录生成的 AppKey 和 AppSecret
6. 开通需要的 API 权限

## 支持的操作

### 数据查询

支持查询苍穹平台的业务数据：

```json
{
  "formId": "BD_MATERIAL",
  "filterString": "FMaterialGroup.FNumber = '01'",
  "fieldKeys": "FMaterialId,FNumber,FName,FSpecification"
}
```

### 数据写入

支持向苍穹平台写入数据：

```json
{
  "formId": "BD_MATERIAL",
  "data": {
    "Creator": "Administrator",
    "FNumber": "M001",
    "FName": "测试物料",
    "FSpecification": "规格型号"
  }
}
```

### 单据操作

支持苍穹平台单据的完整生命周期：

| 操作 | 说明 |
|-----|------|
| Save | 保存单据 |
| Submit | 提交单据 |
| Audit | 审核单据 |
| UnAudit | 反审核单据 |
| Delete | 删除单据 |
| Allocate | 分配单据 |

## 数据映射

### 常用字段映射

| 苍穹字段 | 类型 | 说明 |
|---------|------|------|
| FId | String | 单据内码 |
| FNumber | String | 编码 |
| FName | String | 名称 |
| FCreatorId | String | 创建人 |
| FCreateDate | DateTime | 创建日期 |
| FModifierId | String | 修改人 |
| FModifyDate | DateTime | 修改日期 |

## 常见问题

### 连接失败

检查以下配置：
- 服务地址是否正确
- 数据中心 ID 是否匹配
- 用户名密码是否正确
- 网络是否能访问苍穹服务

### 权限不足

- 确认应用已开通对应 API 权限
- 检查用户是否有业务数据的操作权限

### 数据格式错误

- 参照苍穹 API 文档确认字段类型
- 使用苍穹平台的「在线测试」功能验证

## 参考资料

- [金蝶云苍穹开放平台](https://open.kingdee.com)
- [苍穹 API 文档](https://openapi.kingdee.com)
