# 用友 NC 连接器

用友 NC 是用友面向大型集团企业的 ERP 系统，本文档介绍如何在轻易云 iPaaS 中配置和使用用友 NC 连接器。

## 连接器概述

| 属性 | 说明 |
|-----|------|
| 连接器名称 | yonyou-nc |
| 支持版本 | NC 5.x, NC 6.x |
| 连接方式 | NC SOAP API / 数据库 |
| 认证方式 | 用户名密码 / Token |

## 前置条件

1. 拥有用友 NC 系统访问权限
2. 开通 NC 的外部接口权限
3. 获取 NC 系统管理员分配的账号

## 配置参数

### API 连接方式

| 参数 | 必填 | 说明 |
|-----|------|------|
| serverUrl | 是 | NC 服务地址 |
| username | 是 | 用户名 |
| password | 是 | 密码 |
| accountCode | 是 | 账套编码 |
| langCode | 否 | 语言编码，默认 simpchn |

### 数据库连接方式

| 参数 | 必填 | 说明 |
|-----|------|------|
| host | 是 | 数据库主机 |
| port | 是 | 数据库端口 |
| database | 是 | 数据库名称 |
| username | 是 | 数据库用户名 |
| password | 是 | 数据库密码 |

## 支持的操作

### 查询操作

支持查询 NC 的基础档案和业务单据：

- 组织架构
- 人员档案
- 供应商档案
- 客户档案
- 物料档案
- 会计凭证
- 出入库单据

### 写入操作

支持向 NC 写入数据：

- 会计凭证
- 出入库单据
- 应收应付单据
- 资产卡片

## 常用接口

### 凭证导入

```xml
<ufinterface account="001" billtype="gl" subtype="" operation="save">
  <voucher>
    <voucher_head>
      <year>2024</year>
      <period>1</period>
      <memo>测试凭证</memo>
    </voucher_head>
    <voucher_body>
      <entry>
        <account_code>1001</account_code>
        <debit_amount>1000</debit_amount>
      </entry>
    </voucher_body>
  </voucher>
</ufinterface>
```

## 数据映射

### 凭证字段映射

| NC 字段 | 说明 | 示例 |
|---------|------|------|
| year | 会计年度 | 2024 |
| period | 会计期间 | 1 |
| voucher_type | 凭证类别 | 记 |
| memo | 摘要 | 测试凭证 |
| account_code | 科目编码 | 1001 |
| debit_amount | 借方金额 | 1000 |
| credit_amount | 贷方金额 | 1000 |

## 常见问题

### 接口调用失败

- 检查 NC 接口服务是否启动
- 确认账号具有接口调用权限
- 验证账套编码是否正确

### 编码问题

- 确保传输数据使用 UTF-8 编码
- 中文字段需要正确转码

### 大数据量处理

- 建议使用分页查询
- 批量数据分批导入
- 避免高峰期大批量操作

## 参考资料

- [用友 NC 官方文档](https://www.yonyou.com)
