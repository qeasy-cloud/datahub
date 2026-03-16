# 认证授权

本文档介绍轻易云 iPaaS 平台的认证授权机制，帮助您安全地访问平台资源。

## 认证方式

轻易云 iPaaS 支持多种认证方式，适用于不同的使用场景：

```mermaid
flowchart TB
    subgraph 认证方式
        A[API Key] --> B[服务器端调用]
        C[OAuth 2.0] --> D[第三方应用]
        E[JWT Token] --> F[前端应用]
        G[Webhook 签名] --> H[回调验证]
    end
```

### 方式对比

| 认证方式 | 安全等级 | 有效期 | 适用场景 |
|---------|---------|-------|---------|
| API Key | ⭐⭐⭐ | 长期 | 服务端脚本、定时任务 |
| OAuth 2.0 | ⭐⭐⭐⭐⭐ | 2 小时 | 第三方应用授权 |
| JWT Token | ⭐⭐⭐⭐ | 24 小时 | Web 应用、移动应用 |
| Webhook 签名 | ⭐⭐⭐⭐ | 单次 | Webhook 回调验证 |

## API Key 认证

API Key 是最简单的认证方式，适合服务器端调用。

### 获取 API Key

1. 登录轻易云控制台
2. 进入「开发者中心」→「API 密钥管理」
3. 点击「创建密钥」
4. 复制并安全保存 API Key

> [!CAUTION]
> API Key 只在创建时显示一次，请务必妥善保存。如泄露，请立即删除并重新创建。

### 使用 API Key

在 HTTP 请求头中添加认证信息：

```http
GET /api/v1/schemes HTTP/1.1
Host: api.qeasy.cloud
Authorization: Bearer ak_live_1234567890abcdef
X-API-Version: v1
```

### 代码示例

**cURL:**

```bash
curl -X GET "https://api.qeasy.cloud/api/v1/schemes" \
  -H "Authorization: Bearer ak_live_1234567890abcdef"
```

**Python:**

```python
import requests

headers = {
    "Authorization": "Bearer ak_live_1234567890abcdef"
}

response = requests.get(
    "https://api.qeasy.cloud/api/v1/schemes",
    headers=headers
)
```

**Java:**

```java
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.qeasy.cloud/api/v1/schemes"))
    .header("Authorization", "Bearer ak_live_1234567890abcdef")
    .build();

HttpResponse<String> response = client.send(request, BodyHandlers.ofString());
```

## OAuth 2.0 认证

OAuth 2.0 适合第三方应用接入，支持授权码模式和客户端凭证模式。

### 授权码模式

适用于有用户交互的场景：

```mermaid
sequenceDiagram
    participant User as 用户
    participant App as 第三方应用
    participant IPaaS as 轻易云 iPaaS

    User->>App: 点击登录
    App->>IPaaS: 重定向到授权页面
    User->>IPaaS: 登录并授权
    IPaaS-->>App: 返回授权码
    App->>IPaaS: 用授权码换取 Token
    IPaaS-->>App: 返回 Access Token
    App->>IPaaS: 使用 Token 访问 API
```

### 实现步骤

**1. 引导用户授权**

```text
https://www.qeasy.cloud/oauth/authorize?
  response_type=code&
  client_id=YOUR_CLIENT_ID&
  redirect_uri=YOUR_REDIRECT_URI&
  scope=read,write&
  state=RANDOM_STATE
```

**2. 换取 Access Token**

```http
POST /oauth/token HTTP/1.1
Host: www.qeasy.cloud
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=AUTHORIZATION_CODE&
client_id=YOUR_CLIENT_ID&
client_secret=YOUR_CLIENT_SECRET&
redirect_uri=YOUR_REDIRECT_URI
```

**3. 使用 Token**

```http
GET /api/v1/schemes HTTP/1.1
Host: api.qeasy.cloud
Authorization: Bearer {access_token}
```

### Token 刷新

Access Token 有效期为 2 小时，使用 Refresh Token 刷新：

```http
POST /oauth/token HTTP/1.1
Host: www.qeasy.cloud
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token={refresh_token}&
client_id=YOUR_CLIENT_ID&
client_secret=YOUR_CLIENT_SECRET
```

## JWT Token 认证

JWT Token 适合前端应用，通过登录接口获取。

### 获取 Token

```http
POST /api/v1/auth/login HTTP/1.1
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}

Response:
{
  "code": 0,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "expiresIn": 86400,
    "tokenType": "Bearer"
  }
}
```

### 使用 Token

```javascript
// Axios 配置
axios.defaults.headers.common['Authorization'] = 'Bearer ' + accessToken;

// 请求拦截器 - Token 过期自动刷新
axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response.status === 401) {
      // 刷新 Token
      const newToken = await refreshToken();
      // 重试原请求
      error.config.headers['Authorization'] = 'Bearer ' + newToken;
      return axios(error.config);
    }
    return Promise.reject(error);
  }
);
```

## Webhook 签名验证

接收 Webhook 回调时，需要验证请求的真实性。

### 签名算法

轻易云使用 HMAC-SHA256 算法生成签名：

```text
Signature = HMAC-SHA256(
  timestamp + "." + body,
  webhook_secret
)
```

### 验证示例

**Python:**

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret, timestamp):
    # 检查时间戳（防止重放攻击）
    current_time = int(time.time())
    if abs(current_time - int(timestamp)) > 300:  # 5 分钟
        return False
    
    # 计算签名
    message = f"{timestamp}.{payload}"
    expected = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, signature)
```

**Node.js:**

```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signature, secret, timestamp) {
  // 检查时间戳
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - parseInt(timestamp)) > 300) {
    return false;
  }
  
  // 计算签名
  const message = `${timestamp}.${payload}`;
  const expected = crypto
    .createHmac('sha256', secret)
    .update(message)
    .digest('hex');
  
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}
```

## 权限管理

### 权限模型

轻易云 iPaaS 采用 RBAC（基于角色的访问控制）模型：

```mermaid
flowchart TB
    subgraph RBAC 模型
        A[用户] --> B[角色]
        B --> C[权限]
        C --> D[资源]
    end
```

### 预置角色

| 角色 | 权限范围 |
|-----|---------|
| 超级管理员 | 全部权限 |
| 管理员 | 除用户管理外的全部权限 |
| 开发者 | 方案管理、连接器配置 |
| 运维 | 任务监控、日志查看 |
| 只读 | 仅查看权限 |

### 权限列表

| 权限 | 说明 |
|-----|------|
| scheme:read | 查看方案 |
| scheme:write | 创建/修改方案 |
| scheme:delete | 删除方案 |
| scheme:execute | 执行方案 |
| connector:read | 查看连接器 |
| connector:write | 配置连接器 |
| task:read | 查看任务 |
| task:manage | 管理任务 |
| log:read | 查看日志 |
| setting:manage | 系统设置 |

## 安全建议

### 1. 密钥管理

```mermaid
flowchart LR
    A[密钥生成] --> B[安全存储]
    B --> C[定期轮换]
    C --> D[泄露应急]

    style B fill:#fff3e0
    style D fill:#ffebee
```

- 使用环境变量存储密钥，不要硬编码
- 定期轮换 API Key（建议 90 天）
- 发现泄露立即吊销

### 2. 传输安全

- 始终使用 HTTPS
- 验证 SSL 证书
- 禁用不安全的 TLS 版本

### 3. 访问控制

- 配置 IP 白名单
- 限制 API Key 权限范围
- 启用操作审计

### 4. 错误处理

不要在错误信息中暴露敏感信息：

```python
# 不好的做法
raise Exception(f"认证失败: {api_key}")

# 好的做法
raise Exception("认证失败，请检查 API Key")
```

## 常见问题

**Q: API Key 和 OAuth 2.0 该用哪个？**

A: 
- 服务器端脚本、内部系统：使用 API Key
- 第三方应用、需要用户授权：使用 OAuth 2.0

**Q: Token 过期了怎么办？**

A:
- API Key：不会过期，除非主动删除
- OAuth 2.0：使用 Refresh Token 刷新
- JWT：重新登录获取

**Q: 如何吊销泄露的 API Key？**

A:
1. 立即登录控制台
2. 进入「开发者中心」→「API 密钥管理」
3. 找到对应的密钥，点击「删除」
4. 创建新的密钥并更新到应用中
