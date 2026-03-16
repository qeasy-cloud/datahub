# PostgreSQL 连接器

PostgreSQL 是全球最先进的开源关系型数据库之一，以其稳定性、功能丰富性和扩展性著称。轻易云 iPaaS 提供专用的 PostgreSQL 连接器，支持数据抽取、写入和 CDC 实时同步，帮助企业实现 PostgreSQL 与异构系统的数据集成。

## 连接器概述

### 产品简介

PostgreSQL 具有以下特点：

- **功能丰富**：支持复杂查询、事务、外键、视图、存储过程等
- **高度可扩展**：支持自定义数据类型、函数、操作符
- **并发性能**：多版本并发控制（MVCC）
- **数据完整性**：强大的数据校验机制
- **地理信息**：通过 PostGIS 扩展支持地理空间数据

### 适用版本

| 版本 | 支持状态 | 说明 |
|-----|---------|------|
| PostgreSQL 16 | ✅ 推荐 | 最新版本 |
| PostgreSQL 15 | ✅ 推荐 | 稳定版本 |
| PostgreSQL 14 | ✅ 支持 | 生产可用 |
| PostgreSQL 13 | ✅ 支持 | 成熟版本 |
| PostgreSQL 12 | ✅ 支持 | 广泛部署 |

```mermaid
mindmap
  root((PostgreSQL 连接器))
    数据抽取
      全量抽取
      增量 CDC
      SQL 查询
      分区表支持
    数据写入
      单条写入
      批量写入
      事务支持
      冲突处理
    高级功能
      JSON/JSONB
      全文检索
      地理信息
      数组类型
```

## 连接配置

### 基础连接参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `host` | string | ✅ | 服务器地址 |
| `port` | number | ✅ | 服务端口，默认 `5432` |
| `database` | string | ✅ | 数据库名称 |
| `username` | string | ✅ | 用户名 |
| `password` | string | ✅ | 密码 |
| `schema` | string | — | 默认 Schema，默认 `public` |

### 高级连接参数

| 参数名 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| `charset` | string | `UTF8` | 字符编码 |
| `ssl` | boolean | `false` | 是否启用 SSL |
| `sslMode` | string | `prefer` | SSL 模式 |
| `connectTimeout` | number | `30000` | 连接超时（毫秒） |
| `poolSize` | number | `10` | 连接池大小 |
| `applicationName` | string | `easypaas` | 应用名称 |

### 连接配置示例

```json
{
  "host": "postgres.example.com",
  "port": 5432,
  "database": "easypaas_db",
  "username": "easypaas_user",
  "password": "your_secure_password",
  "schema": "public",
  "ssl": false,
  "poolSize": 10
}
```

### 连接字符串

```yaml
postgresql://username:password@host:port/database?sslmode=prefer
```

## CDC 配置

### 前置条件

1. **配置 PostgreSQL 参数**

编辑 `postgresql.conf`：

```ini
# 开启逻辑复制
wal_level = logical

# 设置复制槽数量
max_replication_slots = 10

# 设置 WAL 发送进程数
max_wal_senders = 10
```

2. **重启 PostgreSQL 服务**

```bash
sudo systemctl restart postgresql
```

3. **验证配置**

```sql
-- 检查 WAL 级别
SHOW wal_level;

-- 检查复制槽配置
SHOW max_replication_slots;
```

4. **创建复制槽**

```sql
-- 创建逻辑复制槽
SELECT pg_create_logical_replication_slot('easypaas_slot', 'pgoutput');

-- 查看复制槽
SELECT * FROM pg_replication_slots;
```

5. **授予 CDC 权限**

```sql
-- 创建 CDC 专用用户
CREATE USER easypaas_cdc WITH REPLICATION LOGIN PASSWORD 'your_password';

-- 授予数据库连接权限
GRANT CONNECT ON DATABASE your_database TO easypaas_cdc;

-- 授予 Schema 使用权限
GRANT USAGE ON SCHEMA public TO easypaas_cdc;

-- 授予表读取权限
GRANT SELECT ON ALL TABLES IN SCHEMA public TO easypaas_cdc;

-- 授予复制权限
ALTER USER easypaas_cdc WITH REPLICATION;
```

### CDC 配置参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `slotName` | string | ✅ | 复制槽名称 |
| `publication` | string | ✅ | 发布名称 |
| `startLsn` | string | — | 起始 LSN 位置 |
| `includeSchema` | boolean | — | 是否包含 Schema 变更 |

### CDC 配置示例

```json
{
  "cdc": {
    "enabled": true,
    "slotName": "easypaas_slot",
    "publication": "easypaas_pub",
    "tables": [
      "public.orders",
      "public.customers"
    ],
    "startLsn": "0/16B1970"
  }
}
```

### 创建发布

```sql
-- 创建发布（包含所有表）
CREATE PUBLICATION easypaas_pub FOR ALL TABLES;

-- 或创建指定表的发布
CREATE PUBLICATION easypaas_pub FOR TABLE orders, customers;

-- 查看发布
SELECT * FROM pg_publication;
```

## 使用示例

### 查询数据

```json
{
  "api": "query",
  "method": "POST",
  "body": {
    "sql": "SELECT * FROM orders WHERE create_time > $1",
    "params": ["2026-01-01"]
  }
}
```

### 批量插入

```json
{
  "api": "batchInsert",
  "method": "POST",
  "body": {
    "table": "orders",
    "columns": ["order_no", "customer_id", "amount", "status"],
    "values": [
      ["SO001", 1, 100.00, "pending"],
      ["SO002", 2, 200.00, "paid"],
      ["SO003", 3, 150.00, "shipped"]
    ]
  }
}
```

### 增量查询

```json
{
  "api": "incrementalQuery",
  "method": "POST",
  "body": {
    "table": "orders",
    "timestampField": "update_time",
    "lastTimestamp": "2026-03-12 00:00:00",
    "pageSize": 1000
  }
}
```

## 适配器配置

### 查询适配器

```json
{
  "source": {
    "adapter": "PostgreSQLQueryAdapter",
    "sql": "SELECT * FROM orders WHERE update_time > $1",
    "params": ["{{lastSyncTime}}"],
    "pagination": {
      "enabled": true,
      "pageSize": 1000
    }
  }
}
```

### CDC 适配器

```json
{
  "source": {
    "adapter": "PostgreSQLCDCAdapter",
    "slotName": "easypaas_slot",
    "publication": "easypaas_pub",
    "tables": ["orders", "customers"]
  }
}
```

### 批量写入适配器

```json
{
  "target": {
    "adapter": "PostgreSQLBatchAdapter",
    "table": "orders",
    "columns": ["order_no", "customer_id", "amount"],
    "batchSize": 1000,
    "conflictAction": "upsert",
    "conflictTarget": ["order_no"]
  }
}
```

## 性能优化

### 查询优化

| 优化项 | 建议 |
|-------|------|
| 索引 | 为查询条件字段创建索引 |
| 分区 | 对大表进行分区 |
| 查询条件 | 使用索引友好的查询条件 |
| LIMIT | 大数据量使用 LIMIT 分页 |

### 写入优化

| 优化项 | 建议 |
|-------|------|
| 批量写入 | 使用批量插入代替单条插入 |
| 事务大小 | 合理控制事务大小 |
| 禁用触发器 | 大批量导入时临时禁用触发器 |
| 删除索引 | 大批量导入前删除索引，导入后重建 |

### 批量写入示例

```sql
-- 大批量导入优化
BEGIN;

-- 临时禁用索引
ALTER TABLE orders DISABLE TRIGGER ALL;

-- 批量插入
INSERT INTO orders (order_no, customer_id, amount) 
VALUES 
  ('SO001', 1, 100.00),
  ('SO002', 2, 200.00),
  ('SO003', 3, 150.00);

-- 重新启用索引
ALTER TABLE orders ENABLE TRIGGER ALL;

COMMIT;
```

### 冲突处理

```sql
-- INSERT ON CONFLICT (UPSERT)
INSERT INTO orders (order_no, customer_id, amount)
VALUES ('SO001', 1, 100.00)
ON CONFLICT (order_no) 
DO UPDATE SET 
  amount = EXCLUDED.amount,
  update_time = NOW();
```

## 常见问题

### Q: 连接失败，提示 "password authentication failed"？

**排查步骤：**

1. 检查用户名和密码是否正确
2. 确认用户是否有连接权限
3. 检查 `pg_hba.conf` 配置是否允许连接

```text
# pg_hba.conf 示例
host    all             all             0.0.0.0/0               md5
```

### Q: CDC 无法启动，提示 "replication slot does not exist"？

1. 检查复制槽是否存在：
   ```sql
   SELECT * FROM pg_replication_slots;
   ```

2. 如不存在，重新创建：
   ```sql
   SELECT pg_create_logical_replication_slot('easypaas_slot', 'pgoutput');
   ```

### Q: 如何处理 JSON 类型数据？

PostgreSQL 支持 JSON 和 JSONB 类型：

```sql
-- 查询 JSON 字段
SELECT data->>'name' AS name 
FROM users 
WHERE data @> '{"age": 25}';

-- 更新 JSON 字段
UPDATE users 
SET data = jsonb_set(data, '{name}', '"new_name"');
```

### Q: 如何查询分区表？

```sql
-- 查询父表会自动查询所有分区
SELECT * FROM orders WHERE create_time >= '2026-01-01';

-- 指定查询特定分区
SELECT * FROM orders_2026_01;
```

### Q: 如何处理主键冲突？

| 策略 | SQL 示例 |
|------|---------|
| 忽略 | `ON CONFLICT DO NOTHING` |
| 更新 | `ON CONFLICT DO UPDATE` |
| 报错 | 默认行为 |

## 相关资源

- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)
- [PostgreSQL CDC 文档](https://www.postgresql.org/docs/current/logical-replication.html)
- [MySQL 连接器](./mysql)
- [数据库连接器概览](../database)

> [!IMPORTANT]
> 使用 CDC 功能时，请确保 PostgreSQL 已配置逻辑复制，并授予足够的权限。
