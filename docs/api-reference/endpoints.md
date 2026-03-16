# 接口列表

本文档详细列出轻易云 iPaaS 开放 API 的所有接口端点，包括认证、数据写入、数据查询和调度者管理等功能模块。所有接口均遵循 RESTful 设计风格，使用 HTTPS 协议进行通信。

> [!IMPORTANT]
> 调用接口前，请确保已完成[应用授权](./authentication)配置，获取有效的 `app_key` 和 `app_secret`。

## 接口规范

### 基础信息

| 项目 | 说明 |
| ---- | ---- |
| 协议 | HTTPS |
| 编码 | UTF-8 |
| 请求格式 | JSON |
| 响应格式 | JSON |
| Content-Type | `application/json` |

### 请求频率限制

> [!WARNING]
> 请保持 1 分钟内不超过 60 次的调用频率。如接口响应请求过于频繁，将触发限流机制，需等待 5 分钟后重新调用。

### 公共响应参数

所有接口均返回以下公共参数：

| 参数 | 类型 | 说明 |
| ---- | ---- | ---- |
| `success` | boolean | 接口是否调用成功 |
| `code` | integer | 接口调用状态码，成功为 `0` |
| `message` | string | 接口提示信息 |
| `content` | object/array | 接口返回的具体业务数据 |

---

## 认证接口

### 获取 Access Token

使用应用密钥换取访问令牌，所有业务接口均需携带此令牌进行身份验证。

#### 请求信息

| 项目 | 内容 |
| ---- | ---- |
| 请求方法 | `POST` |
| 请求路径 | `/v2/oauth` |
| 需要认证 | 否 |

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `app_key` | string | ✅ | 应用授权的 12 位字符串 |
| `app_secret` | string | ✅ | 应用授权密钥的 20 位字符串 |

#### 请求示例

```json
{
  "app_key": "012345678911",
  "app_secret": "11111111115555555555"
}
```

#### 响应参数

| 参数 | 类型 | 说明 |
| ---- | ---- | ---- |
| `content.access_token` | string | 访问令牌，用于后续接口调用 |
| `content.expires_in` | integer | 令牌有效期，单位：秒 |

#### 响应示例（成功）

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "content": {
    "access_token": "PSJthMmsVmc62d4c8528567be9b92435f0266cde05",
    "expires_in": 7200
  }
}
```

#### 响应示例（失败）

```json
{
  "success": false,
  "code": 40101,
  "message": "app_key 或 app_secret 错误",
  "content": null
}
```

#### 代码示例

**Java (OkHttp)**

```java
OkHttpClient client = new OkHttpClient().newBuilder()
    .build();
MediaType mediaType = MediaType.parse("application/json");
RequestBody body = RequestBody.create(mediaType, "{\n    \"app_key\": \"012345678911\",\n    \"app_secret\": \"11111111115555555555\"\n}");
Request request = new Request.Builder()
    .url("https://api.qeasy.cloud/v2/oauth")
    .method("POST", body)
    .addHeader("content-type", "application/json")
    .build();
Response response = client.newCall(request).execute();
```

**cURL**

```bash
curl -X POST "https://api.qeasy.cloud/v2/oauth" \
  -H "Content-Type: application/json" \
  -d '{
    "app_key": "012345678911",
    "app_secret": "11111111115555555555"
  }'
```

---

## 数据写入接口

### 写入集成方案数据

向指定集成方案写入业务数据，支持批量写入。

#### 请求信息

| 项目 | 内容 |
| ---- | ---- |
| 请求方法 | `POST` |
| 请求路径 | `/v2/open-api/business/{scheme_id}/store` |
| 需要认证 | 是（Bearer Token） |

#### 路径参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `scheme_id` | string | ✅ | 集成方案 ID |

#### 查询参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `access_token` | string | ✅ | 通过认证接口获取的访问令牌 |

#### 请求体参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `content` | array | ✅ | 写入的数据内容数组，支持批量写入多条数据 |
| `content[].field_n` | any | 视配置而定 | 具体字段根据集成方案的源平台请求参数定义 |

> [!NOTE]
> 字段必填性取决于集成平台中的配置。只有标记为必填的字段，接口才会进行校验。未在平台定义的字段仍可正常写入。

#### 请求示例

```json
{
  "content": [
    {
      "FStockId": "123123",
      "FNumber": "123123123",
      "FName": "示例物料",
      "FSpecification": "规格型号",
      "FQty": 100,
      "arr": [
        {
          "subField": "子表数据"
        }
      ],
      "obj": {
        "extField": "扩展字段值"
      }
    }
  ]
}
```

#### 响应示例（成功）

```json
{
  "success": true,
  "code": 0,
  "message": "数据写入成功",
  "content": {
    "inserted": 1,
    "failed": 0
  }
}
```

#### 响应示例（失败）

```json
{
  "success": false,
  "code": 40001,
  "message": "必填字段缺失: FNumber",
  "content": null
}
```

#### 代码示例

**Java (OkHttp)**

```java
OkHttpClient client = new OkHttpClient().newBuilder()
    .build();
MediaType mediaType = MediaType.parse("application/json");
RequestBody body = RequestBody.create(mediaType, "{\n    \"content\": [\n        {\n            \"FStockId\": \"123123\",\n            \"FNumber\": \"123123123\",\n            \"FName\": \"示例物料\"\n        }\n    ]\n}");
Request request = new Request.Builder()
    .url("https://api.qeasy.cloud/v2/open-api/business/0166a725-2b9a-30e4-91c5-3529176302c4/store?access_token=YOUR_ACCESS_TOKEN")
    .method("POST", body)
    .addHeader("content-type", "application/json")
    .build();
Response response = client.newCall(request).execute();
```

---

## 数据查询接口

### 查询数据列表

查询集成方案中的数据列表，支持分页和自定义过滤条件。

#### 请求信息

| 项目 | 内容 |
| ---- | ---- |
| 请求方法 | `POST` |
| 请求路径 | `/v2/open-api/business/{scheme_id}/query` |
| 需要认证 | 是（Bearer Token） |

#### 路径参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `scheme_id` | string | ✅ | 集成方案 ID |

#### 查询参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `access_token` | string | ✅ | 访问令牌 |

#### 请求体参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `page` | integer | ✅ | 页码，从 1 开始 |
| `pageSize` | integer | ✅ | 每页条数，范围 1~100 |
| `begin_at` | integer | ✅ | 创建时间戳起始（秒级 Unix 时间戳） |
| `end_at` | integer | ✅ | 创建时间戳结束（秒级 Unix 时间戳） |
| `CONTENT_{field}` | string/object | 否 | 根据字段名自定义过滤条件，支持 MongoDB 查询语法 |

> [!TIP]
> 过滤条件支持 MongoDB 查询操作符，如 `$gte`（大于等于）、`$lte`（小于等于）、`$in`（包含）等。字符串类型字段默认进行模糊匹配。

#### 请求示例

```json
{
  "page": 1,
  "pageSize": 10,
  "begin_at": 1646892000,
  "end_at": 1646978400,
  "CONTENT_FNumber": "MAT",
  "CONTENT_FQty": { "$gte": 100 }
}
```

#### 响应参数

| 参数 | 类型 | 说明 |
| ---- | ---- | ---- |
| `content` | array | 数据列表 |
| `content[].field` | any | 方案中定义的返回字段 |
| `content.total` | integer | 总记录数 |
| `content.page` | integer | 当前页码 |
| `content.pageSize` | integer | 每页条数 |

#### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "content": {
    "list": [
      {
        "_id": "64a1b2c3d4e5f6g7h8i9j0k1",
        "FStockId": "123123",
        "FNumber": "MAT001",
        "FName": "示例物料",
        "FQty": 150,
        "created_at": 1646892733
      }
    ],
    "total": 256,
    "page": 1,
    "pageSize": 10
  }
}
```

---

### 查询数据链路

查询集成方案的数据链路详情，包含源系统和目标系统的完整执行信息。

#### 请求信息

| 项目 | 内容 |
| ---- | ---- |
| 请求方法 | `POST` |
| 请求路径 | `/v2/open-api/business/{scheme_id}/data-link` |
| 需要认证 | 是（Bearer Token） |

#### 路径参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `scheme_id` | string | ✅ | 集成方案 ID |

#### 查询参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `access_token` | string | ✅ | 访问令牌 |

#### 请求体参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `page` | integer | ✅ | 页码，从 1 开始 |
| `pageSize` | integer | ✅ | 每页条数，范围 1~100 |
| `begin_at` | integer | ✅ | 创建时间戳起始（秒级 Unix 时间戳） |
| `end_at` | integer | ✅ | 创建时间戳结束（秒级 Unix 时间戳） |
| `CONTENT_{field}` | string/object | 否 | 自定义过滤条件 |

#### 响应参数

| 参数 | 类型 | 说明 |
| ---- | ---- | ---- |
| `content.links` | array | 数据链路列表 |
| `content.links[].source` | object | 源系统执行信息 |
| `content.links[].source.dispatch` | object | 源系统调度者信息 |
| `content.links[].source.job` | object | 源系统队列任务信息 |
| `content.links[].source.response` | object | 源系统响应信息 |
| `content.links[].target` | object | 目标系统执行信息 |
| `content.links[].target.dispatch` | object | 目标系统调度者信息 |
| `content.links[].target.job` | object | 目标系统队列任务信息 |
| `content.links[].target.response` | object | 目标系统响应信息 |
| `content.total` | integer | 总记录数 |
| `content.condition` | object | 实际执行的 MongoDB 查询条件 |

#### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "content": {
    "links": [
      {
        "source": {
          "dispatch": {
            "trigger_begin": 1646892733.15547,
            "adapter_class": "\\Adapter\\ERP\\KingdeeAdapter",
            "trigger_end": 1646892733.15547
          },
          "job": {
            "created_at": 1646892733.15547,
            "handle_at": 1646892733.430782,
            "response_at": 1646892733.425977,
            "protocol": "http",
            "SDK": "\\Adapter\\ERP\\SDK\\KingdeeSDK",
            "api": "/api/material/query",
            "exec": {
              "url": "https://api.kingdee.com/material",
              "method": "GET",
              "header": {
                "content-type": "application/json"
              },
              "content": {
                "id": 100000000
              }
            }
          },
          "response": {
            "code": "200",
            "message": "操作成功",
            "data": {},
            "url": "https://api.kingdee.com/material"
          }
        },
        "target": {
          "dispatch": {
            "trigger_begin": 1646892733.612526,
            "adapter_class": "\\Adapter\\WMS\\WangdianAdapter",
            "trigger_end": 1646892733.656357
          },
          "job": {
            "created_at": 1646892733.656357,
            "handle_at": 1646892733.93131,
            "response_at": 1646892733.926631,
            "protocol": "http",
            "SDK": "\\Adapter\\WMS\\SDK\\WangdianSDK",
            "api": "goods.push",
            "exec": {
              "url": "https://api.wangdian.cn/openapi",
              "method": "POST",
              "header": [
                "Content-Type: application/x-www-form-urlencoded"
              ],
              "content": {
                "goods_list": "",
                "sid": "xxxxx",
                "app_key": "xxxxxxxx"
              }
            }
          },
          "response": {
            "flag": "success",
            "code": 0,
            "message": "推送成功",
            "request_id": "xxxxxxxxxxx"
          }
        }
      }
    ],
    "total": 1,
    "condition": []
  }
}
```

---

### 根据主键查询单条数据

根据数据主键查询单条记录的详细信息。

#### 请求信息

| 项目 | 内容 |
| ---- | ---- |
| 请求方法 | `GET` |
| 请求路径 | `/v2/open-api/business/{scheme_id}/find-one/{data_id}` |
| 需要认证 | 是（Bearer Token） |

#### 路径参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `scheme_id` | string | ✅ | 集成方案 ID |
| `data_id` | string | ✅ | 数据主键 ID（在集成平台中定义的数据唯一标识） |

#### 查询参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `access_token` | string | ✅ | 访问令牌 |

#### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "success",
  "content": {
    "_id": "64a1b2c3d4e5f6g7h8i9j0k1",
    "FStockId": "123123",
    "FNumber": "MAT001",
    "FName": "示例物料",
    "FSpecification": "规格A",
    "FQty": 150,
    "created_at": 1646892733,
    "updated_at": 1646892733
  }
}
```

---

## 调度者管理接口

### 激活源平台调度者

手动触发源平台调度者执行数据抓取任务。

#### 请求信息

| 项目 | 内容 |
| ---- | ---- |
| 请求方法 | `GET` |
| 请求路径 | `/v2/open-api/business/{scheme_id}/dispatch-source` |
| 需要认证 | 是（Bearer Token） |

#### 路径参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `scheme_id` | string | ✅ | 集成方案 ID |

#### 查询参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `access_token` | string | ✅ | 访问令牌 |

#### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "源平台调度者已激活",
  "content": {
    "dispatch_id": "disp_123456789",
    "status": "pending"
  }
}
```

---

### 激活目标平台调度者

手动触发目标平台调度者执行数据推送任务。

#### 请求信息

| 项目 | 内容 |
| ---- | ---- |
| 请求方法 | `GET` |
| 请求路径 | `/v2/open-api/business/{scheme_id}/dispatch-target` |
| 需要认证 | 是（Bearer Token） |

#### 路径参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `scheme_id` | string | ✅ | 集成方案 ID |

#### 查询参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `access_token` | string | ✅ | 访问令牌 |

#### 响应示例

```json
{
  "success": true,
  "code": 0,
  "message": "目标平台调度者已激活",
  "content": {
    "dispatch_id": "disp_987654321",
    "status": "pending"
  }
}
```

---

## 接口速查表

| 功能分类 | 接口名称 | 请求方法 | 请求路径 |
| -------- | -------- | -------- | -------- |
| **认证** | 获取 Access Token | `POST` | `/v2/oauth` |
| **数据写入** | 写入集成方案数据 | `POST` | `/v2/open-api/business/{scheme_id}/store` |
| **数据查询** | 查询数据列表 | `POST` | `/v2/open-api/business/{scheme_id}/query` |
| **数据查询** | 查询数据链路 | `POST` | `/v2/open-api/business/{scheme_id}/data-link` |
| **数据查询** | 根据主键查询单条 | `GET` | `/v2/open-api/business/{scheme_id}/find-one/{data_id}` |
| **调度者** | 激活源平台调度者 | `GET` | `/v2/open-api/business/{scheme_id}/dispatch-source` |
| **调度者** | 激活目标平台调度者 | `GET` | `/v2/open-api/business/{scheme_id}/dispatch-target` |

---

## 错误码参考

| 错误码 | 含义 | 排查方法 |
| ------ | ---- | -------- |
| `0` | 成功 | — |
| `40001` | 参数错误 | 检查请求参数是否符合接口要求 |
| `40101` | 认证失败 | 检查 `app_key` 和 `app_secret` 是否正确 |
| `40102` | Token 无效或过期 | 重新获取 `access_token` |
| `40301` | 权限不足 | 检查应用授权范围是否包含当前操作 |
| `40401` | 资源不存在 | 检查 `scheme_id` 或 `data_id` 是否正确 |
| `42901` | 请求过于频繁 | 降低请求频率，等待限流重置 |
| `50001` | 服务器内部错误 | 联系技术支持 |

> [!TIP]
> 更多错误码说明请参考[错误码文档](./error-codes)。
