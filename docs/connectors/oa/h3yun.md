# 氚云连接器

氚云（H3Yun）是一款面向数字化管理员的低代码开发平台，提供可视化表单设计、自动化流程、智能报表和丰富的 OpenAPI 接口。通过氚云连接器，您可以轻松实现氚云与 ERP、财务等业务系统的数据集成，帮助企业快速实现一站式数字化管理。

## 前置准备

在使用氚云连接器之前，您需要准备以下信息：

| 参数 | 类型 | 说明 | 获取方式 |
| ---- | ---- | ---- | -------- |
| `enginecode` | string | 引擎编码 | 氚云后台 → 个人中心 → 系统管理 → 系统集成 |
| `enginesecret` | string | 引擎密钥 | 同上 |
| `Host` | string | API 请求地址 | 固定为 `https://www.h3yun.com/OpenApi/Invoke` |

> [!TIP]
> 详细授权配置请参考 [氚云官方文档 - 开发前必读](https://help.h3yun.com/contents/1005/1631.html)

### 获取授权信息步骤

1. 登录氚云后台
2. 进入**个人中心** → **系统管理** → **系统集成**
3. 复制 **EngineCode** 和 **EngineSecret** 值

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

#### 接口信息配置

- **API 地址**：填写氚云 OpenAPI 方法名，如 `LoadBizObjects`

#### 请求参数配置

**单条查询请求示例**：

```json
{
  "SchemaCode": "D2857047bf88e9f78cf42f9a2f1e24dbecffb8b",
  "BizObjectId": "e0c37dfc-d89d-4d32-878e-53605c679baa"
}
```

**列表查询请求示例**：

```json
{
  "SchemaCode": "D2857047bf88e9f78cf42f9a2f1e24dbecffb8b",
  "Filter": {
    "FromRowNum": "0",
    "ToRowNum": "100",
    "RequireCount": "true",
    "ReturnItems": [],
    "SortByCollection": [],
    "Matcher": {
      "Type": "",
      "And": "",
      "Matchers": []
    }
  }
}
```

#### 响应参数配置

| 参数 | 说明 |
| ---- | ---- |
| `StatusKey` | 接口响应状态字段，支持最多两级嵌套 |
| `StatusValue` | 接口响应成功状态的值 |
| `DataKey` | 接口响应数据的 Key，支持最多三级嵌套 |
| `PageKey` | 分页信息的 Key |

### 写入适配器

使用 `ChuanYunExecuteAdapter` 进行数据写入。

**常用接口**：

| 接口 | 说明 |
| ---- | ---- |
| `CreateBizObject` | 创建业务对象 |
| `UpdateBizObject` | 更新业务对象 |
| `RemoveBizObject` | 删除业务对象 |

#### 请求参数配置

**写入请求示例**：

```json
{
  "SchemaCode": "D2857047bf88e9f78cf42f9a2f1e24dbecffb8b",
  "BizObject": {
    "CreatedBy": "ff1311a6-ecc8-4445-83f2-1c8205d0af09",
    "OwnerId": "ff1311a6-ecc8-4445-83f2-1c8205d0af09",
    "F0000001": "测试001",
    "F0000002": "2024/5/14 0:00:00",
    "F0000003": "41545",
    "D285704Fa4152ce9f5b74d8eaa003aa4ccd0dc57": [
      {
        "F0000005": "123456",
        "F0000006": "12345689798"
      },
      {
        "F0000005": "f00005",
        "F0000006": "5"
      }
    ]
  },
  "IsSubmit": true
}
```

> [!NOTE]
> 子表单字段需按数组格式配置，数组内每个对象为一条子表记录。

#### 响应参数配置

与查询适配器的 OtherResponse 配置相同，配置 `StatusKey`、`StatusValue` 和 `DataKey`。

## 获取表单信息

### 表单编码（SchemaCode）

在氚云表单设计页面获取：

1. 进入氚云后台 → 表单设计
2. 选择目标表单
3. 在表单设置中查看**表单编码**（SchemaCode）

> [!TIP]
> 详细操作请参考 [氚云帮助中心 - 表单设计](https://help.h3yun.com/contents/1000/1614.html)

### 字段编码

在表单设计器中查看字段属性：

1. 选中需要集成的表单字段
2. 在右侧属性面板中找到**字段编码**（如 `F0000001`）
3. 记录该编码用于数据映射

> [!IMPORTANT]
> 表单的具体字段说明需要在表单设计中查看，字段编码是数据映射的关键标识。

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
1. 引擎编码（enginecode）和密钥（enginesecret）是否正确
2. 该表单是否开启了 OpenAPI 权限
3. 操作人是否有该表单的写入权限

### Q: 如何获取表单的控制编码？

在表单设计时，选中对应的表单控件，在属性面板中可以查看控制编码信息。

### Q: 分页查询如何配置？

使用 `Filter` 参数中的：
- `FromRowNum`：起始行号（从 0 开始）
- `ToRowNum`：结束行号
- `RequireCount`：是否返回总记录数

## 相关文档

- [氚云 OpenAPI 官方文档](https://help.h3yun.com/contents/1008/1634.html)
- [氚云帮助中心](https://help.h3yun.com/)
- [OA / 协同类连接器概览](./README)
