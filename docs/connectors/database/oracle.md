# Oracle 集成专题

本文档详细介绍轻易云 iPaaS 平台与 Oracle 数据库的集成配置方法，涵盖驱动安装、连接器配置、TNS 配置、权限要求、大对象（BLOB/CLOB）处理以及性能优化建议。Oracle 是业界领先的企业级关系型数据库，广泛应用于金融、电信、制造等行业的核心系统。

---

## 概述

Oracle Database 是全球领先的企业级关系型数据库管理系统，以其高可用性、安全性和强大的事务处理能力著称。轻易云 iPaaS 提供专用的 Oracle 连接器，支持以下核心能力：

- **数据抽取**：支持全量抽取和增量 CDC（Change Data Capture，变更数据捕获）抽取
- **数据写入**：支持单条写入和批量写入，适配高并发场景
- **SQL 查询**：支持自定义 SQL 查询和存储过程调用
- **大对象支持**：完整支持 BLOB、CLOB 等大对象类型读写
- **实时同步**：基于 Oracle LogMiner 实现近实时的数据变更捕获

### 适用版本

| Oracle 版本 | 支持状态 | 说明 |
|-------------|----------|------|
| Oracle 11g | ✅ 支持 | 基础功能完全支持 |
| Oracle 12c | ✅ 支持 | 支持多租户架构 |
| Oracle 18c | ✅ 支持 | 自治数据库特性 |
| Oracle 19c | ✅ 推荐 | 长期支持版本，稳定性最佳 |
| Oracle 21c | ✅ 推荐 | 最新特性支持 |

---

## 驱动安装说明

Oracle 连接依赖 Oracle Instant Client 和 PHP OCI8 扩展。根据您的部署环境，选择以下安装方式。

### Linux 环境安装

#### 1. 下载 Oracle Instant Client

访问 [Oracle 官方下载页面](https://www.oracle.com/cn/database/technologies/instant-client/linux-x86-64-downloads.html) 获取适合您系统的版本：

| 组件包 | 说明 |
|--------|------|
| `oracle-instantclient-basic` | 基础运行时库（必需） |
| `oracle-instantclient-devel` | 开发头文件和静态库（编译 OCI8 必需） |
| `oracle-instantclient-sqlplus` | SQL*Plus 命令行工具（推荐） |

> [!NOTE]
> 建议选择与目标 Oracle 数据库版本相近的客户端版本，或选择通用的 11.2/12.2 版本以获得最佳兼容性。

#### 2. 安装 RPM 包

```bash
# 将安装包放入到以下目录
cd /usr/local/src

# 安装 Oracle Instant Client RPM 包
rpm -Uvh oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm
rpm -Uvh oracle-instantclient11.2-devel-11.2.0.4.0-1.x86_64.rpm
rpm -Uvh oracle-instantclient11.2-sqlplus-11.2.0.4.0-1.x86_64.rpm

# 验证安装
cd /usr/lib/oracle
ls -la
```

#### 3. 配置环境变量

```bash
# 编辑 ~/.bashrc 或 /etc/profile
export ORACLE_HOME=/usr/lib/oracle/11.2/client64
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH
export PATH=$ORACLE_HOME/bin:$PATH

# 使配置生效
source ~/.bashrc
```

#### 4. 安装 PHP OCI8 扩展

```bash
# 下载 OCI8 扩展源码
cd ~
wget https://pecl.php.net/get/oci8-2.2.0.tgz
tar zxvf oci8-2.2.0.tgz
cd oci8-2.2.0

# 编译安装
phpize
./configure --with-php-config=/www/server/php/74/bin/php-config
sudo make && sudo make install

# 启用扩展
echo "extension=oci8.so" >> /www/server/php/74/etc/php.ini
echo "extension=oci8.so" >> /www/server/php/74/etc/php-cli.ini

# 重启 PHP-FPM
systemctl restart php-fpm

# 验证安装
php -m | grep oci8
```

#### 5. 安装 Laravel OCI8 包

```bash
# 在项目目录下执行
composer require yajra/laravel-oci8
```

### Windows 环境安装

#### 1. 下载 Windows 版 Instant Client

1. 访问 [Oracle Instant Client 下载页](https://www.oracle.com/cn/database/technologies/instant-client/winx64-64-downloads.html)
2. 下载 `instantclient-basic-windows.x64-xx.x.x.x.x.zip`
3. 解压到 `C:\oracle\instantclient_xx_x`

#### 2. 配置系统环境变量

```text
ORACLE_HOME=C:\oracle\instantclient_xx_x
PATH=%ORACLE_HOME%;%PATH%
```

#### 3. 安装 PHP OCI8 扩展

1. 下载与 PHP 版本匹配的 `php_oci8.dll` 或 `php_oci8_11g.dll`
2. 将 DLL 文件放入 PHP 的 `ext` 目录
3. 在 `php.ini` 中添加：`extension=oci8`
4. 重启 Web 服务器

> [!TIP]
> Windows 环境下建议使用与 Oracle 版本匹配的 DLL 文件。对于 Oracle 11g，使用 `php_oci8_11g.dll`；对于 Oracle 12c+，使用 `php_oci8.dll`。

### 验证安装

```bash
# 检查 Instant Client 版本
sqlplus -v

# 检查 PHP OCI8 扩展
php -m | grep -i oci

# 测试连接（命令行）
sqlplus username/password@//hostname:port/service_name
```

---

## TNS 配置

TNS（Transparent Network Substrate）是 Oracle 的网络连接配置方式，可通过 `tnsnames.ora` 文件定义数据库连接别名。

### TNS 配置文件位置

| 操作系统 | 默认路径 |
|----------|----------|
| Linux | `$ORACLE_HOME/network/admin/tnsnames.ora` |
| Windows | `%ORACLE_HOME%\network\admin\tnsnames.ora` |

### 配置示例

```ini
# tnsnames.ora
ORCL =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.100)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orcl)
    )
  )

ORCL_PDB =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.100)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orclpdb)
    )
  )
```

### 连接方式对比

| 连接方式 | 示例 | 适用场景 |
|----------|------|----------|
| 完整连接描述符 | `//hostname:1521/service_name` | 快速连接，无需 TNS 配置 |
| TNS 别名 | `ORCL` | 多环境管理，配置集中化 |
| Easy Connect | `username/password@//host:port/service_name` | 简单场景，配置最少 |

> [!TIP]
> 生产环境建议使用 TNS 别名方式，便于统一管理连接配置，在数据库迁移时只需修改 tnsnames.ora 文件即可。

---

## 连接器配置

### 创建连接器

1. 登录轻易云 iPaaS 控制台，进入**连接器管理**页面
2. 点击**新建连接器**，选择**数据库**分类下的 **Oracle**
3. 填写连接参数（详见下方参数说明）
4. 点击**测试连接**验证连通性
5. 连接成功后点击**保存**

### 连接参数说明

#### 基础连接参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `host` | string | ✅ | Oracle 服务器地址，如 `oracle.example.com` |
| `port` | number | ✅ | Oracle 监听端口，默认为 `1521` |
| `service_name` | string | ✅ | Oracle 服务名（如 `orcl`）或 SID |
| `username` | string | ✅ | 连接用户名 |
| `password` | string | ✅ | 连接密码 |
| `charset` | string | — | 字符集，建议 `AL32UTF8` |

#### 高级连接参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `connection_timeout` | number | — | `30000` | 连接超时时间，单位毫秒 |
| `read_timeout` | number | — | `60000` | 读取超时时间，单位毫秒 |
| `pool_size` | number | — | `10` | 连接池大小 |
| `use_ssl` | boolean | — | `false` | 是否使用 SSL 加密连接 |
| `wallet_location` | string | — | — | Oracle Wallet 路径（启用 SSL 时） |

#### 连接字符串示例

```json
{
  "host": "oracle.example.com",
  "port": 1521,
  "service_name": "orcl",
  "username": "easypaas_user",
  "password": "your_secure_password",
  "charset": "AL32UTF8",
  "connection_timeout": 30000,
  "pool_size": 10
}
```

> [!IMPORTANT]
> 对于 Oracle 12c+ 的多租户架构，请使用 PDB（Pluggable Database）的服务名进行连接，而非 CDB 的 SID。

---

## 权限配置

### 最小权限原则

为保障数据库安全，建议创建专用账号并授予最小必要权限。

### 基础读写权限

如需仅进行数据查询和写入操作，执行以下 SQL 授权：

```sql
-- 创建专用用户
CREATE USER easypaas_user IDENTIFIED BY your_secure_password
DEFAULT TABLESPACE users
QUOTA UNLIMITED ON users;

-- 授予会话权限
GRANT CREATE SESSION TO easypaas_user;

-- 授予基础读写权限（指定表）
GRANT SELECT, INSERT, UPDATE, DELETE ON schema.table_name TO easypaas_user;

-- 或授予全局读写权限（谨慎使用）
GRANT SELECT ANY TABLE, INSERT ANY TABLE, UPDATE ANY TABLE, DELETE ANY TABLE TO easypaas_user;
```

### CDC 实时同步权限

如需使用 LogMiner 实时同步功能，需额外授予以下权限：

```sql
-- 授予 LogMiner 所需权限
GRANT EXECUTE_CATALOG_ROLE TO easypaas_user;
GRANT SELECT_CATALOG_ROLE TO easypaas_user;
GRANT FLASHBACK ANY TABLE TO easypaas_user;

-- 授予访问数据字典的权限
GRANT SELECT ON SYS.V_$DATABASE TO easypaas_user;
GRANT SELECT ON SYS.V_$THREAD TO easypaas_user;
GRANT SELECT ON SYS.V_$PARAMETER TO easypaas_user;
GRANT SELECT ON SYS.V_$NLS_PARAMETERS TO easypaas_user;
GRANT SELECT ON SYS.V_$TIMEZONE_NAMES TO easypaas_user;
GRANT SELECT ON SYS.ALL_INDEXES TO easypaas_user;
GRANT SELECT ON SYS.ALL_OBJECTS TO easypaas_user;
GRANT SELECT ON SYS.ALL_USERS TO easypaas_user;
GRANT SELECT ON SYS.CDB_OBJECTS TO easypaas_user;
GRANT SELECT ON SYS.DBA_OBJECTS TO easypaas_user;
GRANT SELECT ON SYS.V_$LOGMNR_CONTENTS TO easypaas_user;
GRANT SELECT ON SYS.V_$LOGMNR_LOGS TO easypaas_user;
GRANT SELECT ON SYS.V_$LOG TO easypaas_user;
GRANT SELECT ON SYS.V_$LOGFILE TO easypaas_user;
GRANT SELECT ON SYS.V_$ARCHIVED_LOG TO easypaas_user;
GRANT SELECT ON SYS.V_$ARCHIVE_DEST TO easypaas_user;
```

### 权限对照表

| 操作类型 | 所需权限 | 适用场景 |
|----------|----------|----------|
| 数据查询 | `SELECT` | 源数据抽取 |
| 数据插入 | `INSERT` | 目标数据写入 |
| 数据更新 | `UPDATE` | 数据同步更新 |
| 数据删除 | `DELETE` | 数据清理 |
| 会话连接 | `CREATE SESSION` | 建立数据库连接 |
| CDC 同步 | `EXECUTE_CATALOG_ROLE`、`SELECT_CATALOG_ROLE` | LogMiner 解析 |

> [!WARNING]
> 请勿使用 `SYS`、`SYSTEM` 或超级管理员账号配置连接器。建议创建专用账号并限制访问来源 IP。

---

## 大对象（BLOB/CLOB）处理注意事项

Oracle 支持多种大对象数据类型（LOB），包括 BLOB（二进制大对象）和 CLOB（字符大对象）。在处理这些数据类型时需要注意以下事项。

### LOB 类型说明

| 类型 | 最大容量 | 用途 |
|------|----------|------|
| `CLOB` | 4 GB | 存储大量文本数据（如 HTML、JSON、长文本） |
| `BLOB` | 4 GB | 存储二进制数据（如图片、文件、多媒体） |
| `NCLOB` | 4 GB | 存储国家字符集文本 |

### CLOB 字段处理

#### 读取 CLOB

```sql
-- 直接查询 CLOB 字段
SELECT id, title, content FROM documents WHERE id = 1;

-- 处理超长 CLOB（超过 4000 字符）
SELECT id, 
       DBMS_LOB.SUBSTR(content, 4000, 1) as content_part1,
       DBMS_LOB.SUBSTR(content, 4000, 4001) as content_part2
FROM documents WHERE id = 1;
```

#### 写入 CLOB

```sql
-- 单条插入
INSERT INTO documents (id, title, content)
VALUES (1, '文档标题', '这里是 CLOB 内容...');

-- 使用 TO_CLOB 转换
INSERT INTO documents (id, title, content)
VALUES (2, '文档标题2', TO_CLOB('长文本内容...'));
```

### BLOB 字段处理

#### 读取 BLOB

BLOB 字段通常需要通过程序处理，建议：

1. **分段读取**：大 BLOB 文件应分段读取，避免内存溢出
2. **流式传输**：将 BLOB 数据以流的方式传输到目标系统

```php
// PHP 示例：分段读取 BLOB
$stmt = oci_parse($conn, "SELECT id, file_name, file_data FROM attachments WHERE id = :id");
oci_bind_by_name($stmt, ":id", $id);
oci_execute($stmt);

$row = oci_fetch_array($stmt, OCI_ASSOC);
$lob = $row['FILE_DATA'];

// 分块读取
$chunk_size = 8192;
while (!$lob->eof()) {
    $data = $lob->read($chunk_size);
    // 处理数据块
}
$lob->free();
```

#### 写入 BLOB

```sql
-- 使用 EMPTY_BLOB() 初始化
INSERT INTO attachments (id, file_name, file_data)
VALUES (1, 'example.pdf', EMPTY_BLOB())
RETURNING file_data INTO :blob_locator;

-- 然后通过程序写入数据
```

### LOB 处理最佳实践

| 场景 | 建议 |
|------|------|
| 小文本 (< 4000 字符) | 使用 `VARCHAR2` 替代 `CLOB`，性能更好 |
| 大文本读写 | 使用 LOB 定位器模式，避免全量加载到内存 |
| 文件存储 | 考虑使用对象存储（如 OSS/S3），数据库存储 URL |
| 批量导入 | 先导入元数据，再单独处理 LOB 字段 |

> [!CAUTION]
> 处理超过 100 MB 的 BLOB 数据时，务必使用流式处理，避免内存溢出导致应用崩溃。

### 常见问题

#### Q: CLOB 字段查询返回截断？

**原因**：部分客户端工具对 CLOB 有默认长度限制。

**解决**：
```sql
-- 设置 LONG 类型显示长度
SET LONG 1000000;
SET LONGCHUNKSIZE 1000000;

-- 或使用 SUBSTR 分段获取
SELECT DBMS_LOB.GETLENGTH(content) as lob_length FROM documents;
```

#### Q: BLOB 数据损坏或无法读取？

**排查步骤**：
1. 确认字符集设置正确（客户端与数据库一致）
2. 检查数据传输过程中是否被转换（避免自动字符集转换）
3. 验证存储的 MIME 类型与实际数据格式匹配

---

## 适配器选择

### 查询适配器

| 适配器 | 用途 | 适用场景 |
|--------|------|----------|
| `OracleQueryAdapter` | 标准 SQL 查询 | 常规数据查询 |
| `OracleCDCAdapter` | LogMiner 实时同步 | 增量数据捕获 |

### 写入适配器

| 适配器 | 用途 | 适用场景 |
|--------|------|----------|
| `OracleExecuteAdapter` | 单条 SQL 执行 | 逐条写入、更新 |
| `OracleBatchExecuteAdapter` | 批量 SQL 执行 | 大数据量批量写入 |

> [!IMPORTANT]
> 大数据量场景强烈推荐使用 `OracleBatchExecuteAdapter`，可显著提升写入性能。

---

## 批量写入适配器

### 概述

`OracleBatchExecuteAdapter` 是专为大数据量写入场景设计的批量执行适配器，通过将多条记录合并为单次 INSERT 语句执行，大幅减少网络往返和数据库开销。

### 配置参数

#### 写入配置

配置接口信息时，API 请使用：`batchexecute`

#### request 参数配置

需要配置写入数据库的参数，字段需与写入 SQL 语句中的字段顺序和数量保持一致。

#### otherRequest 参数配置

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `main_sql` | string | ✅ | 具体的 INSERT 语句模板 |
| `limit` | number | ✅ | 单次合并的数据条数，限制 1000 条以内 |

> [!WARNING]
> SQL 语句中的字段顺序必须与 `request` 参数中的字段顺序一致，且数量保持相同。

### 最佳实践

1. **合理设置批量大小**：建议 `limit` 设置在 100~1000 之间，根据记录大小和网络延迟调整
2. **使用绑定变量**：Oracle 对绑定变量有优化，可提高执行效率
3. **错误处理**：批量写入时单条记录错误会导致整批失败，建议开启错误记录和重试机制
4. **主键处理**：确保写入数据的主键唯一性，避免主键冲突导致写入失败

---

## 性能优化

### 读取优化

#### 1. 分页查询

对于大表查询，使用分页避免一次性加载过多数据：

```sql
-- Oracle 12c+ 分页语法
SELECT * FROM large_table 
WHERE update_time > DATE '2024-01-01'
ORDER BY id 
OFFSET 0 ROWS FETCH NEXT 1000 ROWS ONLY;

-- 传统分页语法（兼容旧版本）
SELECT * FROM (
  SELECT t.*, ROWNUM rn FROM (
    SELECT * FROM large_table WHERE update_time > DATE '2024-01-01' ORDER BY id
  ) t WHERE ROWNUM <= 1000
) WHERE rn > 0;
```

#### 2. 增量抽取

使用 CDC 模式或时间戳字段实现增量抽取：

```sql
-- 基于时间戳的增量查询
SELECT * FROM orders 
WHERE last_modified > TO_TIMESTAMP_TZ(:last_sync_time, 'YYYY-MM-DD"T"HH24:MI:SS.FF3TZH:TZM');
```

#### 3. 索引优化

确保查询条件字段已建立索引：

```sql
-- 检查索引
SELECT index_name, column_name FROM user_ind_columns WHERE table_name = 'YOUR_TABLE';

-- 为常用查询字段添加索引
CREATE INDEX idx_orders_update_time ON orders(update_time);
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
-- 临时调整会话参数（大数据量导入时）
ALTER SESSION SET COMMIT_WRITE = 'BATCH,NOWAIT';

-- 并行 DML
ALTER SESSION ENABLE PARALLEL DML;

-- 直接路径插入（跳过缓冲区，适合大批量）
INSERT /*+ APPEND */ INTO target_table SELECT * FROM source_table;
COMMIT;
```

> [!CAUTION]
> 使用 `APPEND` 提示进行直接路径插入时，会在表上持有排他锁，其他会话无法同时写入该表。

### 网络优化

| 优化项 | 建议配置 | 效果 |
|--------|----------|------|
| 连接池大小 | 5~20 | 减少连接建立开销 |
| SDU（Session Data Unit） | 8 KB ~ 32 KB | 根据网络延迟调整 |
| 压缩传输 | 启用 | 减少网络带宽占用 |

---

## CDC 实时同步配置

### 开启归档日志

CDC 模式依赖 Oracle 的归档日志和 LogMiner 功能。

```sql
-- 检查归档日志状态
ARCHIVE LOG LIST;

-- 开启归档日志（如未开启，需重启数据库）
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
ALTER DATABASE ARCHIVELOG;
ALTER DATABASE OPEN;

-- 配置最小补充日志（必需）
ALTER DATABASE ADD SUPPLEMENTAL LOG DATA;
```

### CDC 配置步骤

1. **确认归档日志已开启**且配置了补充日志
2. **创建 CDC 专用账号**并授予 LogMiner 相关权限
3. **在轻易云配置 CDC 适配器**，指定起始 SCN 或时间
4. **启动同步任务**，监控延迟和吞吐量

> [!IMPORTANT]
> CDC 模式需要数据库持续开启归档日志，且会占用一定的磁盘和 I/O 资源，请确保服务器资源充足。

---

## 常见问题

### Q: 连接测试失败，提示 "ORA-12154: TNS: could not resolve the connect identifier"？

**排查步骤：**

1. 检查 TNS 配置是否正确
2. 确认 `tnsnames.ora` 文件路径正确且客户端能读取
3. 尝试使用 Easy Connect 语法直接连接：`//host:port/service_name`
4. 检查网络连通性：`tnsping service_name`

### Q: 中文显示乱码？

**解决方案：**

1. 确保连接字符集为 `AL32UTF8`：
   ```json
   { "charset": "AL32UTF8" }
   ```

2. 设置客户端环境变量：
   ```bash
   export NLS_LANG="AMERICAN_AMERICA.AL32UTF8"
   ```

3. 检查数据库字符集：
   ```sql
   SELECT parameter, value FROM nls_database_parameters WHERE parameter = 'NLS_CHARACTERSET';
   ```

### Q: ORA-01555: snapshot too old？

**原因与解决：**

- **原因**：查询执行时间过长，UNDO 表空间中的旧数据被覆盖
- **解决**：
  1. 优化查询性能，减少执行时间
  2. 增大 UNDO 表空间大小
  3. 增加 `UNDO_RETENTION` 参数值

```sql
-- 查看当前 UNDO 配置
SHOW PARAMETER undo_retention;

-- 调整 UNDO 保留时间
ALTER SYSTEM SET undo_retention = 3600;
```

### Q: 批量写入时提示 "ORA-00001: unique constraint violated"？

**解决策略：**

| 策略 | SQL 示例 | 适用场景 |
|------|----------|----------|
| 忽略重复 | `INSERT /*+ IGNORE_ROW_ON_DUPKEY_INDEX(table, index) */` | Oracle 11g+ |
| 合并更新 | `MERGE INTO ... USING ... ON ... WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT` | 数据同步 |

```sql
-- 使用 MERGE 语句实现 UPSERT
MERGE INTO target_table t
USING (SELECT * FROM source_table WHERE batch_id = :batch_id) s
ON (t.id = s.id)
WHEN MATCHED THEN
  UPDATE SET t.name = s.name, t.update_time = SYSDATE
WHEN NOT MATCHED THEN
  INSERT (id, name, create_time) VALUES (s.id, s.name, SYSDATE);
```

### Q: 如何处理 CLOB/BLOB 数据同步缓慢？

**优化建议：**

1. 对于大 BLOB 文件（> 10 MB），考虑在目标系统存储文件路径而非内容
2. 使用分块读取和写入，避免一次性加载完整数据到内存
3. 在源系统启用 LOB 存储的缓存机制
4. 考虑使用数据库链路（DB Link）直接传输大对象

---

## 相关资源

- [数据库类连接器概览](./README) — 查看所有支持的数据库连接器
- [配置连接器](../../guide/configure-connector) — 连接器基础配置指南
- [CDC 实时同步](../../advanced/cdc-realtime) — CDC 配置与最佳实践
- [数据映射](../../guide/data-mapping) — 字段映射配置方法
- [MySQL 集成](./mysql) — MySQL 数据库集成指南

---

> [!NOTE]
> 本文档持续更新中，如有疑问请联系轻易云技术支持团队。
