# 氚云连接器

氚云是一款面向数字化管理员的低代码开发平台，提供可视化表单设计、自动化流程、智能报表和丰富的 API 接口。通过氚云连接器，您可以轻松实现氚云与 ERP、财务等业务系统的数据集成。

## 前置准备

在使用氚云连接器之前，您需要准备以下信息：

| 参数 | 说明 | 获取方式 |
| ---- | ---- | -------- |
| `enginecode` | 引擎编码 | 氚云后台 → 个人中心 → 系统管理 → 系统集成 |
| `enginesecret` | 引擎密钥 | 同上 |
| `Host` | API 请求地址 | 固定为 `https://www.h3yun.com/OpenApi/Invoke` |

> [!TIP]
> 详细授权配置请参考 [氚云官方文档](https://help.h3yun.com/contents/1005/1631.html)

## 创建连接器

1. 进入**连接器管理**页面，点击**新建连接器**
2. 选择连接器类型为**氚云**
3. 填写配置参数：
   - **Host**：`https://www.h3yun.com/OpenApi/Invoke`
   - **enginecode**：从氚云后台获取的引擎编码
   - **enginesecret**：从氚云后台获取的引擎密钥
4. 点击**测试连接**验证配置
5. 保存连接器

## 配置说明

### 查询适配器

使用 `ChuanYunQueryAdapter` 进行数据查询。

**常用接口**：

| 接口 | 说明 |
| ---- | ---- |
| `LoadBizObject` | 加载单条业务对象数据 |
| `LoadBizObjects` | 批量加载业务对象数据 |

**请求参数示例**：

```json
{
  "SchemaCode": "D2857047bf88e9f78cf42f9a2f1e24dbecffb8b",
  "Filter": {
    "FromRowNum": "0",
    "ToRowNum": "100",
    "RequireCount": "true"
  }
}
```

### 写入适配器

使用 `ChuanYunExecuteAdapter` 进行数据写入。

**常用接口**：

| 接口 | 说明 |
| ---- | ---- |
| `CreateBizObject` | 创建业务对象 |
| `UpdateBizObject` | 更新业务对象 |
| `RemoveBizObject` | 删除业务对象 |

**请求参数示例**：

```json
{
  "SchemaCode": "D2857047bf88e9f78cf42f9a2f1e24dbecffb8b",
  "BizObject": {
    "F0000001": "测试数据",
    "F0000002": "2024/5/14 0:00:00"
  },
  "IsSubmit": true
}
```

## 获取表单信息

### 表单编码（SchemaCode）

在氚云表单设计页面获取：

1. 进入氚云后台 → 表单设计
2. 选择目标表单
3. 在表单设置中查看表单编码

### 字段编码

在表单设计器中查看字段属性：

1. 选中需要集成的表单字段
2. 在右侧属性面板中找到字段编码（如 `F0000001`）
3. 记录该编码用于数据映射

> [!NOTE]
> 子表单字段需要按照特定格式配置，详情参考旧版文档。

## 关联子表查询

查询主表数据时同时获取关联子表数据：

```json
{
  "SchemaCode": "主表编码",
  "Filter": {
    "FromRowNum": "0",
    "ToRowNum": "100"
  },
  "joinFormModelIds": "关联表id:关联表名:关联表外键"
}
```

## 常见问题

### Q: 如何获取表单的所有字段编码？

在表单设计页面，选择**扩展功能** → **数据推送** → **字段对照表**，可以查看完整的字段编码列表。

### Q: 写入数据时提示权限不足？

请检查：
1. 引擎编码和密钥是否正确
2. 该表单是否开启了 OpenAPI 权限
3. 操作人是否有该表单的写入权限

## 相关文档

- [氚云官方 API 文档](https://help.h3yun.com/contents/1008/1634.html)
- [OA / 协同类连接器概览](./README)
