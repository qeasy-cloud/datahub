# 金蝶云星空集成专题

本文档详细介绍轻易云 iPaaS 平台与金蝶云星空（K3Cloud）的集成配置方法，涵盖连接器配置、基础资料同步、实时库存同步、附件上传下载、反执行操作等高级功能场景。

## 概述

金蝶云星空（Kingdee Cloud Galaxy）是金蝶软件面向大中型企业推出的 ERP 云平台。轻易云 iPaaS 提供专用的金蝶云星空连接器，支持以下核心能力：

- **基础数据同步**：组织、物料、客户、供应商等主数据双向同步
- **业务单据集成**：采购、销售、库存、财务单据的自动化流转
- **实时库存监控**：基于 Python 脚本的库存变动实时推送
- **附件管理**：单据附件的上传、下载与绑定
- **操作回滚**：单据反审核、反执行等逆向操作支持

## 连接器配置

### 创建连接器

1. 登录轻易云 iPaaS 控制台，进入**连接器管理**页面
2. 点击**新建连接器**，选择 **ERP** 分类下的**金蝶云星空**
3. 填写连接参数（详见下方参数说明）
4. 点击**测试连接**验证连通性
5. 连接成功后点击**保存**

### 连接参数说明

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `server_url` | string | ✅ | 金蝶服务器地址，格式如 `https://k3cloud.example.com/K3Cloud/` |
| `app_id` | string | ✅ | 第三方系统登录授权的应用 ID |
| `app_secret` | string | ✅ | 第三方系统登录授权的应用密钥 |
| `account_id` | string | ✅ | 数据中心 ID（租户 ID） |
| `username` | string | ✅ | 集成用户账号 |
| `password` | string | ✅ | 集成用户密码 |

> [!IMPORTANT]
> 登录网址最后需要添加 `/`，例如 `https://k3cloud.example.com/K3Cloud/`。

### 适配器选择

| 场景 | 查询适配器 | 写入适配器 |
| ---- | ---------- | ---------- |
| 标准单据查询/写入 | `K3CloudQueryAdapter` | `K3CloudExecuteAdapter` |
| 附件上传 | `K3CloudQueryAdapter` | `K3CloudUploadExecuteAdapter` |
| 附件下载 | `BillViewQueryAdapter` | `AttachmentDownloadAdapter` |
| 反执行操作 | — | `K3CloudExcuteOperationAdapter` |
| 旗舰版附件查询 | `KdGalaxyAttachmentQueryAdapter` | `KdGalaxyAttachmentExecuteAdapter` |

## 第三方系统登录授权配置

金蝶云星空支持开通第三方系统登录授权，通过管理员 `administrator` 账户登录后台系统完成配置。

### 开通授权服务步骤

1. **进入授权功能菜单**
   
   使用管理员账号登录金蝶云星空，进入【第三方系统登录授权】功能菜单。

2. **新增应用**
   
   点击【新增】按钮创建新的第三方应用。

3. **获取应用 ID**
   
   点击【获取应用 ID】按钮，系统会跳转到金蝶云官网授权页面。

4. **金蝶官网授权**
   
   使用金蝶账号登录官网，选择环境类型与用途，点击提交获取授权信息。

5. **回填授权信息**
   
   将获取到的授权信息复制粘贴回金蝶系统的授权页面，点击确认。

6. **配置应用信息**
   
   填写应用名称，选择**集成用户**（该用户必须拥有集成相关的操作权限），点击保存。

7. **记录密钥信息**
   
   分别记录【应用 ID】和【应用密钥】，用于轻易云连接器配置。

8. **获取数据中心 ID**
   
   进入菜单【公共设置】→【WebAPI】，在左侧任意选择一个业务对象，即可获取【数据中心 ID】。

> [!TIP]
> 完成以上配置后，将应用 ID、应用密钥、数据中心 ID、服务器地址等信息提供给集成开发人员。

## 基础资料同步配置

### 列表查询接口注意事项

金蝶云星空的列表查询接口支持多种过滤条件，配置时需注意：

- 使用 `FormId` 指定业务对象表单 ID
- 使用 `FilterString` 设置过滤条件，支持 SQL 语法
- 分页参数 `Limit` 和 `StartRow` 控制返回数据量

### 批量保存方法

金蝶云星空支持批量保存操作，通过 `BatchSave` 操作类型实现：

```json
{
  "Creator": "Administrator",
  "NeedUpDateFields": [],
  "Model": [
    {
      "FBillTypeID": {
        "FNumber": "BD_MATERIAL"
      },
      "FNumber": "TEST001",
      "FName": "测试物料"
    }
  ]
}
```

### 基础资料分配组织

金蝶云星空的基础资料同步需要分配组织操作。在目标平台源码配置中增加 `distributionOrg` 参数：

```json
{
  "distributionOrg": "100016,100017,100018,100019"
}
```

> [!NOTE]
> 此处使用的是**组织 ID**，而不是组织编码。金蝶的多组织编码可以通过直接 SQL 报表查询：
> ```sql
> SELECT * FROM T_ORG_Organizations
> ```

### 单据自动审核配置

在写入配置中，通过设置 `Operation` 参数控制单据审核行为：

- `Save`：仅保存单据
- `Submit`：保存并提交
- `Audit`：保存并审核

如需单独发起审核接口，可在写入后通过 `K3CloudExcuteOperationAdapter` 调用审核操作。

## 实时库存同步专题

通过向金蝶库存单据注册 Python 脚本，实现实时监听库存单据审核/反审核事件，并将变动数据发送到 DataHub。

### 库存变动单据表名对照

| 库存变动表单 | 表头（主表） | 表体（分录表） |
| ------------ | ------------ | -------------- |
| 采购入库单 | `t_STK_InStock` | `T_STK_INSTOCKENTRY` |
| 采购退料单 | `t_PUR_MRB` | `T_PUR_MRBENTRY` |
| 销售出库单 | `T_SAL_OUTSTOCK` | `T_SAL_OUTSTOCKENTRY` |
| 销售退货单 | `T_SAL_RETURNSTOCK` | `T_SAL_RETURNSTOCKENTRY` |

> [!TIP]
> 更多表单名与字段可查阅金蝶 BOS 平台。

### 注册列表插件

将以下 Python 脚本注册为金蝶列表插件，监听审核按钮事件：

```python
import clr
clr.AddReference("System")
clr.AddReference("System.Web.Extensions")
clr.AddReference("Kingdee.BOS.Core")
clr.AddReference("Kingdee.BOS")
clr.AddReference('Kingdee.BOS.App')
clr.AddReference("Kingdee.BOS.DataEntity")
clr.AddReference("Kingdee.BOS.ServiceHelper")
clr.AddReference("Newtonsoft.Json")
import sys
from System import *
from System.Collections.Generic import *
from System.Web.Script.Serialization import *
from System.Security.Cryptography import *
from System.Text import *
from System.Net import *
from System.IO import *
from System.Threading import *
from System.Collections.Generic import Dictionary
from Newtonsoft.Json import *
from Newtonsoft.Json.Linq import *
from Kingdee.BOS.ServiceHelper import *
from Kingdee.BOS.Core.DynamicForm import *
from Kingdee.BOS.App.Data import *
reload(sys)
sys.setdefaultencoding('utf-8')

# ==========================================
# 配置参数 - 根据实际环境修改
# ==========================================

# 开启 debug 调试消息提醒
SHOW_DEBUG = True

# DataHub Host 服务器主机
DATAHUB_HOST = 'http://datahub-service.kdyunchuang.com'

# StrategyId 集线器 ID
STRATEGY_ID = '2509d92a-a91e-30a3-ae4e-33eead036a97'

# 当前表名
MAIN_NAME = '外购入库'

# 当前表的主表名
MAIN_TABLE = 't_STK_InStock'

# 当前表的分录表名
ENTRY_TABLE = 'T_STK_INSTOCKENTRY'

# 当前表的单据编码字段
BILL_FIELD = 'FBILLNO'

# 物料字段名
MATERIAL_FIELD = 'FMATERIALID'

# 仓库字段名
STOCK_FIELD = 'FSTOCKID'

# 库位字段名
STOCKLOC_FIELD = 'FSTOCKLOCID'

# 批次号字段名
LOT_FIELD = 'FLOT'

# 货主字段名
OWNER_FIELD = 'FOWNERID'

# ==========================================
# 库存查询类
# ==========================================

class Inventory:
    def __init__(self, BarItemKey):
        keys = this.ListView.SelectedRowsInfo.GetPrimaryKeyValues()
        self.BarItemKey = BarItemKey
        self.PKS = ','.join(keys)

    def fetch(self):
        return DBServiceHelper.ExecuteDynamicObject(
            this.Context, self.__generateSQL())

    def collectionToJson(self, collection):
        json = '['
        for row in collection:
            json += ('{"FID":"' + row[0].ToString() + '"'
                + ',"FStockId":"' + row[1].ToString() + '"'
                + ',"FMaterialId":"' + row[2].ToString() + '"'
                + ',"FBaseQty":"' + row[3].ToString() + '"'
                + ',"FBaseAVBQty":"' + row[4].ToString() + '"'
                + ',"FLot":"' + row[5].ToString() + '"'
                + ',"FUpdateTime":"' + row[6].ToString() + '"'
                + ',"FOwnerId":"' + row[7].ToString() + '"'
                + ',"FKeeperId":"' + row[8].ToString() + '"'
                + ',"FStockOrgId":"' + row[9].ToString() + '"'
                + ',"FOwnerTypeId":"' + row[10].ToString() + '"'
                + ',"FMaterialId_FNumber":"' + row[11].ToString() + '"'
                + ',"FOwnerId_FNumber":"' + row[12].ToString() + '"'
                + ',"FKeeperId_FNumber":"' + row[13].ToString() + '"'
                + ',"FStockOrgId_FNumber":"' + row[14].ToString() + '"'
                + ',"FProduceDate":"' + row[15].ToString() + '"'
                + ',"FMtoNo":"' + row[16].ToString() + '"'
                + ',"FStockStatusId":"' + row[17].ToString() + '"'
                + ',"FBILLNO":"' + row[18].ToString() + '"'
                + ',"id":"' + row[0].ToString() + '"'
                + ',"FormName":"' + MAIN_NAME + '"},')
        json = json.rstrip(',') + ']'
        return '{"idCheck":false,"content":' + json + ',"multiple":true,"id":1}'

    def __generateSQL(self):
        sqlArray = [
            'SELECT DISTINCT',
            'INV.FID,',
            'INV.FStockId,',
            'INV.FMaterialId,',
            'INV.FBaseQty,',
            'INV.FBaseAVBQty,',
            'INV.FLot,',
            'INV.FUpdateTime,',
            'INV.FOwnerId,',
            'INV.FKeeperId,',
            'INV.FStockOrgId,',
            'INV.FOwnerTypeId,',
            'MATE.FNUMBER AS FMaterialId_FNumber,',
            'ORG1.FNUMBER AS FOwnerId_FNumber,',
            'ORG2.FNUMBER AS FKeeperId_FNumber,',
            'ORG3.FNUMBER AS FStockOrgId_FNumber,',
            'INV.FProduceDate,',
            'INV.FMtoNo,',
            'INV.FStockStatusId,',
            "'0' AS FBillNo",
            'FROM T_STK_INVENTORY INV',
            'LEFT JOIN ' + ENTRY_TABLE + ' BILL ON',
            'INV.FMATERIALID = BILL.' + MATERIAL_FIELD,
            'AND INV.FSTOCKID = BILL.' + STOCK_FIELD,
            'AND INV.FSTOCKLOCID = BILL.' + STOCKLOC_FIELD,
            'AND INV.FLOT = BILL.' + LOT_FIELD,
            'AND INV.FOWNERID = BILL.' + OWNER_FIELD,
            'LEFT JOIN t_bd_material MATE ON INV.FMATERIALID = MATE.FMATERIALID',
            'LEFT JOIN t_ORG_Organizations ORG1 ON INV.FOwnerId = ORG1.FORGID',
            'LEFT JOIN t_ORG_Organizations ORG2 ON INV.FKeeperId = ORG2.FORGID',
            'LEFT JOIN t_ORG_Organizations ORG3 ON INV.FStockOrgId = ORG3.FORGID',
            'LEFT JOIN ' + MAIN_TABLE + ' MAIN ON BILL.FID = MAIN.FID',
            'WHERE BILL.FID IN (' + self.PKS + ')',
        ]
        sql = ' '.join(sqlArray)
        if self.BarItemKey == 'tbApprove':
            sql += " AND MAIN.FDOCUMENTSTATUS = 'C'"
        else:
            sql += " AND MAIN.FDOCUMENTSTATUS = 'D'"
        return sql

# ==========================================
# 事件处理函数
# ==========================================

def AfterBarItemClick(e):
    if e.BarItemKey == 'tbApprove' or e.BarItemKey == 'tbReject':
        if len(this.ListView.SelectedRowsInfo.GetPrimaryKeyValues()) > 0:
            handle(e.BarItemKey)

def handle(BarItemKey):
    inv = Inventory(BarItemKey)
    url = DATAHUB_HOST + '/api/open/operation/' + STRATEGY_ID
    collection = inv.fetch()
    if len(collection) == 0:
        return
    webRequest = post(url, inv.collectionToJson(collection))
    result = JObject.Parse(webRequest)
    if SHOW_DEBUG == True:
        this.View.ShowMessage(webRequest)

def post(url, postdata):
    webRequest = HttpWebRequest.Create(url)
    webRequest.Method = "POST"
    webRequest.Accept = "application/json, text/plain, */*"
    webRequest.ContentType = "application/json;charset=UTF-8"
    data = Encoding.ASCII.GetBytes(postdata)
    webRequest.ContentLength = data.Length
    webRequest.GetRequestStream().Write(data, 0, data.Length)
    webRequest.GetRequestStream().Flush()
    webRequest.GetRequestStream().Close()
    webResponse = webRequest.GetResponse()
    streamReader = StreamReader(
        webResponse.GetResponseStream(), Encoding.GetEncoding("utf-8"))
    result = streamReader.ReadToEnd()
    return result
```

> [!IMPORTANT]
> 正式运行时将 `SHOW_DEBUG` 设置为 `False`，避免弹窗干扰用户操作。

### 注册表单插件

如需监听单据数据变动事件（如单据审核状态变更），使用以下表单插件：

```python
# 核心事件处理逻辑
def DataChanged(e):
    # 监听审核事件：创建 -> 已审核
    if (e.Key.ToString() == 'FDocumentStatus' 
        and e.OldValue.ToString() == 'B' 
        and e.NewValue.ToString() == 'C'):
        handle()
    # 监听反审核事件：已审核 -> 重新审核
    elif (e.Key.ToString() == 'FDocumentStatus' 
          and e.OldValue.ToString() == 'C' 
          and e.NewValue.ToString() == 'D'):
        handle()
```

## 附件上传与下载专题

### 上传附件到金蝶并绑定单据

#### 开发思路

1. 先保存单据，获取保存后的单据 ID（`InterId`）
2. 调用上传附件方法，将附件写入对应单据

#### 适配器配置

- **适配器**：`\Adapter\K3Cloud\K3CloudUploadExecuteAdapter`
- **写入调度者配置**：在 `metadata` 中增加 `isUploadFile: true`

```json
{
  "isUploadFile": true
}
```

#### 附件字段映射

| 字段名 | 说明 | 示例值 |
| ------ | ---- | ------ |
| `attachment` | 附件数组 | `file_list` |
| `path` | 文件本地绝对路径 | `/www/wwwroot/storage/IMG001.jpg` |
| `filename` | 文件名 | `IMG001.jpg` |

#### 上传附件参数

```json
{
  "FormId": "SAL_SaleOrder",
  "InterId": 101412,
  "BillNO": "120",
  "FileId": "",
  "EntryinterId": "-1",
  "attachment": {
    "path": "/www/wwwroot/service/storage/IMG001.jpg",
    "filename": "IMG001.jpg",
    "size": 3973931
  },
  "attachmentIndex": 0,
  "attachmentTotal": 2
}
```

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `FormId` | String | ✅ | 业务对象表单 ID，如销售订单 `SAL_SaleOrder` |
| `InterId` | Int | ✅ | 单据内码 ID |
| `BillNO` | String | ✅ | 单据编号 |
| `FileId` | String | — | 文件 ID（新增时为空） |
| `EntryinterId` | String | — | 单据体分录 ID（单据头附件传 `-1`） |
| `attachment.path` | String | ✅ | 文件本地绝对路径 |
| `attachment.filename` | String | ✅ | 文件名（含扩展名） |
| `attachmentIndex` | Int | ✅ | 当前附件索引（从 0 开始） |
| `attachmentTotal` | Int | ✅ | 附件总数 |

#### 保存单据并绑定附件

```json
[
  "SAL_SaleOrder",
  {
    "Operation": "BatchSave",
    "IsVerifyBaseDataField": true,
    "NeedUpDateFields": [],
    "attachment": [
      {
        "path": "/www/wwwroot/service/storage/IMG001.jpg",
        "filename": "IMG001.jpg"
      }
    ],
    "Model": [
      {
        "FID": "",
        "FBillTypeID": {
          "FNumber": "XSDD01_SYS"
        },
        "FBillNo": "120",
        "FSaleOrgId": {
          "FNumber": "100"
        },
        "FDate": "2026-02-26",
        "FCustId": {
          "FNumber": "16"
        },
        "FNote": "/www/wwwroot/service/storage/IMG001.jpg"
      }
    ]
  }
]
```

> [!WARNING]
> 上传附件时不要使用上传并审核操作，因为审核后的单据无法修改，附件将无法上传。建议先上传附件，再单独调用审核接口。

### 从金蝶下载附件

#### 适配器配置

- **查询适配器**：`K3CloudQueryAdapter`
- **写入适配器**：`K3CloudUploadExecuteAdapter`

#### 查询配置参数

在查询配置中增加 `otherResponse` 参数：

```json
{
  "DownloadAttachment": true,
  "AttachmentFields": "附件字段名"
}
```

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `DownloadAttachment` | Boolean | ✅ | 是否下载附件，`true` 表示下载 |
| `AttachmentFields` | String | ✅ | 附件字段名 |

### 附件下载方案配置示例

#### 方案流程

1. 首先查询对应单据数据
2. 查询单据时，系统自动生成附件下载队列
3. 附件下载完成后，将附件字段更新到单据中

#### 查询销售订单适配器

- **查询适配器**：`\Adapter\K3Cloud\BillViewQueryAdapter`
- **查询附件适配器**：`\Adapter\K3Cloud\AttachmentDownloadAdapter`

#### 请求调度者配置

**查询销售订单时增加参数**：

```json
{
  "DownloadAttachment": true,
  "downStrategyId": "下载附件方案ID"
}
```

**下载附件参数**：

```json
{
  "DownloadAttachment": true,
  "AttachmentFields": "附件字段",
  "AttachmentFileName": "附件文件名字段",
  "SourceStrategyId": "源销售订单方案ID"
}
```

### 金蝶旗舰版附件配置

> [!IMPORTANT]
> 旗舰版附件适配器 `KdGalaxyAttachmentQueryAdapter` 和 `KdGalaxyAttachmentExecuteAdapter` 需要金蝶方进行对应的接口开发工作。

#### 查询附件配置

**其他响应参数（`otherResponse`）**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `DownloadAttachment` | Bool | ✅ | 是否下载附件，`true` 表示下载 |
| `downloadRequest` | 子表对象 | 条件必填 | 附件下载请求参数，`DownloadAttachment` 为 `true` 时必填 |
| `downloadapi` | String | — | 下载 API 路径，如 `/kapi/v2/s7w7/basedata/base/query` |

**`downloadRequest` 子表对象参数**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `formId` | String | ✅ | 页面编码（表单 ID） |
| `billNo` | String | ✅ | 订单编号/业务单据编号 |
| `filePanel` | String | ✅ | 附件面板标识，通常为 `attachmentpanel` |

**客户附件查询示例**：

```json
{
  "formId": "bd_customer",
  "billNo": "实际客户编码",
  "filePanel": "s7w7_attachmentpanelap"
}
```

**销售订单附件查询示例**：

```json
{
  "formId": "sm_salorder",
  "billNo": "订单编号",
  "filePanel": "attachmentpanel"
}
```

#### 写入附件配置

**其他响应参数（`otherResponse`）**：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `uploadAttachment` | Bool | ✅ | 是否上传附件，`true` 表示上传 |
| `upload` | 多行分录 | ✅ | 附件上传请求参数 |

**`upload` 子表对象参数**（支持多个附件一起上传）：

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `formId` | String | ✅ | 页面编码（表单 ID） |
| `billNo` | String | ✅ | 订单编号/业务单据编号 |
| `filePanel` | String | ✅ | 附件面板标识 |
| `file` | Object | ✅ | 附件对象，包含文件本地绝对路径 |

**客户附件上传示例**：

```json
{
  "uploadAttachment": true,
  "uploadRequest": [
    {
      "formId": "bd_customer",
      "billNo": "billno",
      "filePanel": "s7w7_attachmentpanelap",
      "file": "/www/wwwroot/deploy/public/k3cloud/2025-09/ERPOA_1757573811_756544248.xlsx"
    }
  ],
  "uploadapi": "/kapi/v2/s7w7/basedata/base/upload"
}
```

## 反执行操作配置

### 适配器选择

使用 `K3CloudExcuteOperationAdapter` 适配器执行反操作。

### 方案配置参数

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `FormId` | String | ✅ | 业务对象表单 ID，如生产订单 `PRD_MO` |
| `Operation` | String | ✅ | 执行操作，如反下达 `UndoToRelease` |
| `CreateOrgId` | String | — | 创建者组织内码 |
| `Numbers` | String | — | 单据编码集合 |
| `Ids` | String | — | 单据内码集合 |
| `PkEntryIds` | String | — | 单据分录内码 |
| `NetworkCtrl` | Boolean | — | 是否启用网控 |
| `IgnoreInterationFlag` | Boolean | — | 是否允许忽略交互 |

### 接口信息配置

接口信息请填写：`excuteOperation`

### 常用反操作类型

| 操作类型 | 说明 |
| -------- | ---- |
| `UndoToRelease` | 反下达 |
| `UndoToStart` | 反开工 |
| `UndoToReport` | 反汇报 |
| `UndoToComplete` | 反完工 |

> [!TIP]
> 根据金蝶 WebAPI 文档找到对应参数，填入配置对应位置。

## 单据关联关系说明

### 收料通知单 → 采购入库

| 项目 | 说明 |
| ---- | ---- |
| 数据库关联表 | `T_STK_INSTOCKENTRY_LK` |
| 反写字段 | `FSRCBILLTYPEID`（源单类型：`PUR_ReceiveBill`）、`FSRCBillNo`（源单编号）、`FPOOrderNo`（订单编号） |
| 所属单据体 | `FInStockEntry` |
| 源单表 | `T_PUR_ReceiveEntry` |
| 单据转换规则 | `PUR_ReceiveBill-STK_InStock` |

### 采购订单 → 采购入库

| 项目 | 说明 |
| ---- | ---- |
| 数据库关联表 | `T_STK_INSTOCKENTRY_LK` |
| 反写字段 | `FSRCBILLTYPEID`（源单类型：`PUR_PurchaseOrder`）、`FSRCBillNo`（源单编号）、`FPOOrderNo`（订单编号） |
| 所属单据体 | `FInStockEntry` |
| 源单表 | `t_PUR_POOrderEntry` |
| 单据转换规则 | `PUR_PurchaseOrder-STK_InStock` |

### 采购入库 → 应付单

| 项目 | 说明 |
| ---- | ---- |
| 数据库关联表 | `T_AP_PAYABLE_LK` |
| 反写字段 | `FSOURCETYPE`（源单类型：`STK_InStock`）、`FSOURCEBILLNO`（源单编码）、`FSRCROWID`（源单行内码） |
| 所属单据体 | `FEntityDetail` |
| 源单表 | `T_STK_INSTOCKENTRY` |
| 单据转换规则 | `AP_InStockToPayableMap` |

### 应付单 → 付款单

| 项目 | 说明 |
| ---- | ---- |
| 数据库关联表 | `T_AP_PAYBILLSRCENTRY_LK` |
| 反写字段 | `FSOURCETYPE`（源单类型：`AP_Payable`）、`FSRCBILLNO`（源单编号） |
| 所属单据体 | `FPAYBILLSRCENTRY` |
| 源单表 | `T_AP_PAYABLEPLAN` |
| 单据转换规则 | `AP_PayableToPayBill` |

### 采购入库 → 采购退料

| 项目 | 说明 |
| ---- | ---- |
| 数据库关联表 | `T_PUR_MRBENTRY_LK` |
| 反写字段 | `FSRCBILLTYPEID`（源单类型：`STK_InStock`）、`FSRCBILLNO`（源单编号）、`FORDERNO`（订单单号） |
| 所属单据体 | `FPURMRBENTRY` |
| 源单表 | `T_STK_INSTOCKENTRY` |
| 单据转换规则 | `STK_InStock-PUR_MRB` |

### 采购退料 → 应付单

| 项目 | 说明 |
| ---- | ---- |
| 数据库关联表 | `T_AP_PAYABLE_LK` |
| 反写字段 | `FSOURCETYPE`（源单类型：`PUR_MRB`）、`FSOURCEBILLNO`（源单编号） |
| 所属单据体 | `FEntityDetail` |
| 源单表 | `T_PUR_MRBENTRY` |
| 单据转换规则 | `AP_MRBToPayableMap` |

### 销售出库 → 应收单

| 项目 | 说明 |
| ---- | ---- |
| 数据库关联表 | `t_AR_receivableEntry_lk` |
| 反写字段 | `FSOURCETYPE`（源单类型：`SAL_OUTSTOCK`）、`FSourceBillNo`（源单编码）、`FSRCROWID`（源单行内码） |
| 所属单据体 | `FEntityDetail` |
| 源单表 | `T_SAL_OUTSTOCKENTRY` |
| 单据转换规则 | `AR_OutStockToReceivableMap` |

### 应收单 → 收款单

| 项目 | 说明 |
| ---- | ---- |
| 数据库关联表 | `T_AR_RECEIVEBILLSRCENTRY_LK` |
| 源单表 | `t_AR_receivablePlan` |
| 单据转换规则 | `AR_recableToRecBill` |

## 快速配置案例：OKKICRM 对接金蝶云星空

本案例演示如何快速实现 OKKICRM 与金蝶云星空的数据对接。

### 准备工作

1. 注册 OKKICRM 用户并启用系统
2. 准备好金蝶云星空 5.0 以上版本环境
3. 完成金蝶第三方系统登录授权配置（详见上文）

### 第一步：配置连接器

1. 进入轻易云 iPaaS 控制台，创建两个连接器：
   - **OKKICRM 连接器**：选择 CRM 类型，填写 OKKICRM 的 API 认证信息
   - **金蝶云星空连接器**：选择 ERP 类型，填写金蝶服务器地址、应用 ID、应用密钥等信息

2. 测试两个连接器的连通性，确保连接成功

### 第二步：建立集成方案

1. 进入**集成方案**页面，点击**新建方案**
2. 选择源平台为 **OKKICRM**，目标平台为 **金蝶云星空**
3. 选择要同步的业务对象，例如**销售订单**
4. 配置方案基本信息：方案名称、同步方向、冲突处理策略等

### 第三步：配置同步策略

**设置同步时间**：
- 选择同步方式：实时同步或定时同步
- 如选择定时同步，设置 Cron 表达式定义执行周期

**设置字段映射**：
1. 进入**数据映射**页面
2. 配置源字段与目标字段的对应关系：
   - OKKICRM 客户编号 → 金蝶客户编码
   - OKKICRM 订单编号 → 金蝶单据编号
   - OKKICRM 产品编号 → 金蝶物料编码
   - OKKICRM 数量 → 金蝶数量
   - OKKICRM 金额 → 金蝶价税合计
3. 配置值格式化规则（如需要）

### 第四步：启动与监控

1. 点击**启动**按钮，启动集成方案
2. 进入**监控中心**，查看数据传递情况：
   - 成功记录数
   - 失败记录数
   - 异常日志详情
3. 如有失败记录，查看错误信息并进行修复

> [!TIP]
> 建议首次运行时选择少量测试数据进行验证，确认数据映射正确后再进行全量同步。

## 常见问题

### Q：连接金蝶时提示 "认证失败"？

A：请检查以下配置：
- 服务器地址是否正确，是否以 `/` 结尾
- 应用 ID 和应用密钥是否匹配
- 集成用户是否有足够的操作权限
- 数据中心 ID 是否正确

### Q：单据保存成功但数据未写入金蝶？

A：检查以下方面：
- 确认 `FormId` 填写正确
- 检查必填字段是否都已赋值
- 查看金蝶返回的错误详情，可能是基础资料不存在

### Q：如何获取金蝶的表单 ID？

A：登录金蝶 BOS 设计器，打开对应的业务对象，表单 ID 显示在属性窗口中。常见表单 ID：
- 销售订单：`SAL_SaleOrder`
- 采购订单：`PUR_PurchaseOrder`
- 采购入库单：`STK_InStock`
- 销售出库单：`SAL_OUTSTOCK`

### Q：附件上传失败？

A：请检查：
- 文件路径是否为服务器本地绝对路径
- 文件是否存在且可读
- 单据是否已保存（附件上传需要单据内码）
- 单据是否已审核（审核后的单据无法上传附件）

### Q：实时库存同步数据不准确？

A：检查脚本配置：
- 确认 `MAIN_TABLE` 和 `ENTRY_TABLE` 配置正确
- 检查 `MATERIAL_FIELD`、`STOCK_FIELD` 等字段名是否与金蝶实际字段一致
- 确认 `STRATEGY_ID` 与 DataHub 集线器 ID 匹配
