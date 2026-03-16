# MySQL 集成专题

本文档详细介绍轻易云 iPaaS 平台与 MySQL 数据库的集成配置方法，涵盖连接器配置、连接参数、权限要求、批量写入适配器使用以及性能优化建议。

---

## 概述

MySQL 是全球最流行的开源关系型数据库管理系统之一，广泛应用于 Web 应用、企业信息系统、数据仓库等场景。轻易云 iPaaS 提供专用的 MySQL 连接器，支持以下核心能力：

- **数据抽取**：支持全量抽取和增量 CDC（Change Data Capture，变更数据捕获）抽取
- **数据写入**：支持单条写入和批量写入，大幅提升数据同步效率
- **SQL 查询**：支持自定义 SQL 查询，灵活获取所需数据
- **事务支持**：保证数据一致性和完整性
- **Binlog 实时同步**：基于 MySQL Binlog 实现近实时的数据变更捕获

### 适用版本

| MySQL 版本 | 支持状态 | 说明 |
|------------|----------|------|
| MySQL 5.6 | ✅ 支持 | 基础功能完全支持 |
| MySQL 5.7 | ✅ 推荐 | 性能优化，推荐版本 |
| MySQL 8.0 | ✅ 推荐 | 最新特性，性能最佳 |
| MariaDB 10.x | ✅ 支持 | 兼容 MySQL 协议 |

---

## 连接器配置

### 创建连接器

1. 登录轻易云 iPaaS 控制台，进入**连接器管理**页面
2. 点击**新建连接器**，选择**数据库**分类下的 **MySQL**
3. 填写连接参数（详见下方参数说明）
4. 点击**测试连接**验证连通性
5. 连接成功后点击**保存**

### 连接参数说明

#### 基础连接参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `host` | string | ✅ | MySQL 服务器地址，如 `localhost` 或 `mysql.example.com` |
| `port` | number | ✅ | MySQL 服务端口，默认为 `3306` |
| `database` | string | ✅ | 数据库名称 |
| `username` | string | ✅ | 连接用户名 |
| `password` | string | ✅ | 连接密码 |

#### 高级连接参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `charset` | string | — | `utf8mb4` | 字符集编码，建议使用 `utf8mb4` 以支持 Emoji |
| `connection_timeout` | number | — | `30000` | 连接超时时间，单位毫秒 |
| `read_timeout` | number | — | `60000` | 读取超时时间，单位毫秒 |
| `write_timeout` | number | — | `60000` | 写入超时时间，单位毫秒 |
| `pool_size` | number | — | `10` | 连接池大小 |
| `use_ssl` | boolean | — | `false` | 是否使用 SSL 加密连接 |
| `ssl_ca` | string | — | — | SSL CA 证书路径（启用 SSL 时必填） |

> [!TIP]
> 生产环境建议启用 SSL 加密连接，确保数据传输安全。

#### 连接字符串示例

```json
{
  "host": "mysql.example.com",
  "port": 3306,
  "database": "easypaas_db",
  "username": "easypaas_user",
  "password": "your_secure_password",
  "charset": "utf8mb4",
  "connection_timeout": 30000,
  "read_timeout": 60000,
  "pool_size": 10
}
```

---

## 权限配置

### 最小权限原则

为保障数据库安全，建议创建专用账号并授予最小必要权限。

### 基础读写权限

如需仅进行数据查询和写入操作，执行以下 SQL 授权：

```sql
-- 创建专用用户
CREATE USER 'easypaas_user'@'%' IDENTIFIED BY 'your_secure_password';

-- 授予基础读写权限
GRANT SELECT, INSERT, UPDATE, DELETE ON your_database.* TO 'easypaas_user'@'%';

-- 刷新权限
FLUSH PRIVILEGES;
```

### CDC 实时同步权限

如需使用 Binlog 实时同步功能，需额外授予复制权限：

```sql
-- 授予复制权限（CDC 同步必需）
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'easypaas_user'@'%';

-- 刷新权限
FLUSH PRIVILEGES;
```

### 权限对照表

| 操作类型 | 所需权限 | 适用场景 |
|----------|----------|----------|
| 数据查询 | `SELECT` | 源数据抽取 |
| 数据插入 | `INSERT` | 目标数据写入 |
| 数据更新 | `UPDATE` | 数据同步更新 |
| 数据删除 | `DELETE` | 数据清理 |
| 结构查询 | `SHOW`、`INFORMATION_SCHEMA` | 元数据获取 |
| 实时同步 | `REPLICATION SLAVE`、`REPLICATION CLIENT` | CDC Binlog 解析 |

> [!WARNING]
> 请勿使用 `root` 或超级管理员账号配置连接器。建议创建专用账号并限制访问来源 IP。

---

## 适配器选择

### 查询适配器

| 适配器 | 用途 | 适用场景 |
|--------|------|----------|
| `MySQLQueryAdapter` | 标准 SQL 查询 | 常规数据查询 |
| `MySQLCDCAdapter` | Binlog 实时同步 | 增量数据捕获 |

### 写入适配器

| 适配器 | 用途 | 适用场景 |
|--------|------|----------|
| `MySQLExecuteAdapter` | 单条 SQL 执行 | 逐条写入、更新 |
| `MySQLBatchExecuteAdapter` | 批量 SQL 执行 | 大数据量批量写入 |

> [!IMPORTANT]
> 大数据量场景强烈推荐使用 `MySQLBatchExecuteAdapter`，可显著提升写入性能。

---

## 批量写入适配器

### 概述

`MySQLBatchExecuteAdapter` 是专为大数据量写入场景设计的批量执行适配器，通过将多条记录合并为单次 INSERT 语句执行，大幅减少网络往返和数据库开销。

### 工作原理

```mermaid
flowchart LR
    A[数据记录 1] --> D[批量合并]
    B[数据记录 2] --> D
    C[数据记录 N] --> D
    D --> E[单次 INSERT 执行]
    E --> F[MySQL 数据库]
    
    style D fill:#fff3e0
    style E fill:#e8f5e9
```

### 配置参数

#### 写入配置

配置接口信息时，API 请使用：`batchexecute`

#### request 参数配置

需要配置写入数据库的参数，字段需与写入 SQL 语句中的字段顺序和数量保持一致。建议单批次不超过 100 个字段。

#### otherRequest 参数配置

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `main_sql` | string | ✅ | 具体的 INSERT 语句模板 |
| `limit` | number | ✅ | 单次合并的数据条数，限制 1000 条以内 |

> [!WARNING]
> SQL 语句中的字段顺序必须与 `request` 参数中的字段顺序一致，且数量保持相同。

### 配置示例

#### SQL 模板配置

```sql
INSERT INTO `middle_order_prdmq` 
  (`order_code`, `FBillNo`, `FStatus`, `create_time`, `update_time`, 
   `FMATERIALID_FNumber`, `FPlanStartDate`, `FPlanFinishDate`) 
VALUES
```

#### 请求示例

```json
{
  "sql": {
    "main_sql": "INSERT INTO `middle_order_prdmq` (`order_code`, `FBillNo`, `FStatus`, `create_time`, `update_time`, `FMATERIALID_FNumber`, `FPlanStartDate`, `FPlanFinishDate`) VALUES"
  },
  "params": {
    "main_params": [
      {
        "order_code": "FCN202403185879",
        "FBillNo": "MO022077",
        "FStatus": "4",
        "create_time": "2024-03-18 16:21:29",
        "update_time": "2024-03-19 10:31:04",
        "FMATERIALID_FNumber": "1001060050",
        "FPlanStartDate": "2024-03-18 09:12:46",
        "FPlanFinishDate": "2024-03-20 09:12:46"
      }
    ]
  }
}
```

### 最佳实践

1. **合理设置批量大小**：建议 `limit` 设置在 100~1000 之间，根据记录大小和网络延迟调整
2. **字段数量控制**：单批次字段数量建议不超过 100 个，避免 SQL 过长
3. **错误处理**：批量写入时单条记录错误会导致整批失败，建议开启错误记录和重试机制
4. **主键处理**：确保写入数据的主键唯一性，避免主键冲突导致写入失败

---

## 批量读写性能优化

### 读取优化

#### 1. 分页查询

对于大表查询，使用分页避免一次性加载过多数据：

```sql
-- 使用 LIMIT 分页
SELECT * FROM large_table 
WHERE update_time > '2024-01-01' 
ORDER BY id 
LIMIT 1000 OFFSET 0;
```

#### 2. 增量抽取

使用 CDC 模式或时间戳字段实现增量抽取：

```sql
-- 基于时间戳的增量查询
SELECT * FROM orders 
WHERE last_modified > '${last_sync_time}';
```

#### 3. 索引优化

确保查询条件字段已建立索引：

```sql
-- 检查索引
SHOW INDEX FROM your_table;

-- 为常用查询字段添加索引
CREATE INDEX idx_update_time ON your_table(update_time);
```

### 写入优化

#### 1. 批量写入参数调优

| 参数 | 建议值 | 说明 |
|------|--------|------|
| 批量大小 | 500~1000 | 平衡内存占用和写入效率 |
| 并发线程数 | 3~5 | 根据数据库性能调整 |
| 事务批次 | 每 1000 条提交一次 | 避免事务过大 |

#### 2. 数据库参数优化

```sql
-- 临时调整 innodb 缓冲区（会话级）
SET SESSION innodb_buffer_pool_size = 2147483648;

-- 禁用唯一性检查（大数据量导入时）
SET SESSION unique_checks = 0;

-- 禁用外键检查（如确认数据无误）
SET SESSION foreign_key_checks = 0;
```

> [!CAUTION]
> 禁用 `unique_checks` 和 `foreign_key_checks` 需谨慎，仅在确认数据无误时使用，完成后务必恢复。

#### 3. 索引策略

大数据量导入时的索引优化策略：

```mermaid
flowchart TD
    A[开始导入] --> B{数据量>10万?}
    B -->|是| C[删除非必要索引]
    B -->|否| D[保留索引直接导入]
    C --> E[批量导入数据]
    E --> F[重建索引]
    D --> G[完成]
    F --> G
    
    style C fill:#fff3e0
    style F fill:#e8f5e9
```

### 网络优化

| 优化项 | 建议配置 | 效果 |
|--------|----------|------|
| 连接池大小 | 5~20 | 减少连接建立开销 |
| 连接超时 | 30000 ms | 避免网络抖动导致重连 |
| 读取超时 | 60000~300000 ms | 适应大数据量查询 |
| 压缩传输 | 启用 | 减少网络带宽占用 |

---

## CDC 实时同步配置

### 开启 Binlog

编辑 MySQL 配置文件（`my.cnf` 或 `my.ini`）：

```ini
[mysqld]
# 开启 Binlog
log-bin=mysql-bin

# 设置 Binlog 格式为 ROW（必需）
binlog_format=ROW

# 设置 Server ID（主从架构必需）
server-id=1

# 保留 Binlog 天数
expire_logs_days=7
```

重启 MySQL 服务后验证：

```sql
-- 检查 Binlog 是否开启
SHOW VARIABLES LIKE 'log_bin';

-- 检查 Binlog 格式
SHOW VARIABLES LIKE 'binlog_format';
```

### CDC 配置步骤

1. **确认 Binlog 已开启**且格式为 `ROW`
2. **创建 CDC 专用账号**并授予 `REPLICATION` 权限
3. **在轻易云配置 CDC 适配器**，指定起始位置或时间
4. **启动同步任务**，监控延迟和吞吐量

> [!IMPORTANT]
> CDC 模式需要数据库持续开启 Binlog，且会占用一定的磁盘和 I/O 资源，请确保服务器资源充足。

---

## 常见问题

### Q: 连接测试失败，提示 "Access denied"？

**排查步骤：**

1. 检查用户名和密码是否正确
2. 确认用户是否有从远程主机连接的权限（`user@'%'`）
3. 验证用户是否具备所需的数据库权限

```sql
-- 查看用户权限
SHOW GRANTS FOR 'easypaas_user'@'%';
```

### Q: 中文显示乱码？

**解决方案：**

1. 确保连接字符集为 `utf8mb4`：
   ```json
   { "charset": "utf8mb4" }
   ```

2. 检查数据库和表字符集：
   ```sql
   -- 查看数据库字符集
   SHOW CREATE DATABASE your_database;
   
   -- 查看表字符集
   SHOW CREATE TABLE your_table;
   ```

3. 必要时转换字符集：
   ```sql
   ALTER TABLE your_table CONVERT TO CHARACTER SET utf8mb4;
   ```

### Q: 批量写入时提示 "Data too long"？

**原因与解决：**

- **原因**：数据长度超过字段定义
- **解决**：检查字段类型和长度，必要时修改表结构或截断数据

```sql
-- 查看字段定义
SHOW FULL COLUMNS FROM your_table;

-- 修改字段长度
ALTER TABLE your_table MODIFY COLUMN your_column VARCHAR(500);
```

### Q: CDC 同步延迟较大？

**优化建议：**

1. 检查 Binlog 生成频率，避免单事务过大
2. 优化网络连接，使用内网或专线
3. 调整消费者线程数和批量处理大小
4. 监控 MySQL 服务器 I/O 性能

### Q: 如何处理主键冲突？

**策略选择：**

| 策略 | SQL 示例 | 适用场景 |
|------|----------|----------|
| 忽略重复 | `INSERT IGNORE` | 允许部分数据丢失 |
| 更新覆盖 | `ON DUPLICATE KEY UPDATE` | 以新数据为准 |
| 替换插入 | `REPLACE INTO` | 完全替换旧数据 |

```sql
-- 使用 ON DUPLICATE KEY UPDATE
INSERT INTO users (id, name, email) 
VALUES (1, '张三', 'zhangsan@example.com')
ON DUPLICATE KEY UPDATE 
  name = VALUES(name), 
  email = VALUES(email);
```

---

## 相关资源

- [数据库类连接器概览](./README) — 查看所有支持的数据库连接器
- [配置连接器](../../guide/configure-connector) — 连接器基础配置指南
- [CDC 实时同步](../../advanced/cdc-realtime) — CDC 配置与最佳实践
- [数据映射](../../guide/data-mapping) — 字段映射配置方法
- [MongoDB 集成](./mongodb) — 文档型数据库集成指南

---

> [!NOTE]
> 本文档持续更新中，如有疑问请联系轻易云技术支持团队。
