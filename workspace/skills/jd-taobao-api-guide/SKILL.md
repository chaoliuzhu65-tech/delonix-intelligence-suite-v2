# 京东/淘宝个人API申请指南

> **适用场景**：德胧采购底价雷达 - 无需企业资质，纯个人账号即可申请
> **Skill**: jd-taobao-api-guide
> **Version**: 1.0
> **更新**: 2026-04-16

---

## 一、核心结论

| 平台 | 账号类型 | 资质要求 | 审核时间 | 调用限制 |
|------|---------|---------|---------|---------|
| **京东** | 个人开发者 | 身份证 + 人脸识别 | 10分钟~2小时 | 100次/天（基础接口） |
| **淘宝** | 个人开发者 | 支付宝实名认证 | 1-3个工作日 | 10次/分钟 |

**结论**：完全可以用**个人账号**申请，无需营业执照！

---

## 二、京东开放平台 API 申请流程

### 2.1 申请入口
- **官网**：https://open.jd.com
- **开发者中心**：https://jos.jd.com/

### 2.2 注册个人开发者账号

**步骤1**：打开 https://open.jd.com，点击【注册】→ 选择【个人开发者】

**步骤2**：填写信息
- 手机号 + 验证码
- 设置登录密码
- 完成实名认证（需身份证正反面照片）
- 审核时间：10分钟~2小时

### 2.3 创建应用（获取AppKey和AppSecret）

**步骤1**：进入【开发者中心】→【应用管理】→【创建应用】

**步骤2**：填写应用信息
- 应用名称：随便填（如「德胧价格雷达测试」）
- 应用类型：选「**工具应用**」（最适合个人学习）
- 应用描述：简单写（如「酒店采购价格查询，不商用」）
- 回调地址：随便填一个网址（如 https://www.baidu.com）
- 图标：可不传

**步骤3**：提交后等待审核（约10分钟，测试应用基本秒过）

### 2.4 获取API密钥

审核通过后，在【应用管理】→【应用信息】页面找到：
- **AppKey**：调用API的用户名
- **AppSecret**：调用API的密码，**不能泄露！**

### 2.5 申请API权限

**步骤1**：在开放平台首页点击【API文档】

**步骤2**：搜索需要的接口，常用接口：
- `jingdong.item.base.info.get` - 商品基础信息查询
- `jingdong.item.search.search` - 商品搜索
- `jingdong.price.read.get` - 价格查询

**步骤3**：点击【申请权限】→ 选择刚创建的应用 → 提交

**步骤4**：商品查询类接口个人开发者基本**秒过**

### 2.6 常用接口清单

| 接口名称 | 功能 | 个人权限 | 调用限制 |
|---------|------|---------|---------|
| jingdong.item.base.info.get | 商品基础信息 | ✅ 可用 | 100次/天 |
| jingdong.item.search.search | 商品搜索 | ✅ 可用 | 100次/天 |
| jingdong.price.read.get | 价格查询 | ✅ 可用 | 100次/天 |
| jingdong.skus.list.get | SKU列表 | ✅ 可用 | 100次/天 |

---

## 三、淘宝开放平台 API 申请流程

### 3.1 申请入口
- **官网**：https://open.taobao.com
- **控制台**：https://developer.alibaba.com/

### 3.2 注册开发者账号

**步骤1**：访问 open.taobao.com，使用淘宝/支付宝账号登录

**步骤2**：完成开发者实名认证
- 个人开发者：绑定支付宝并完成实名认证
- 企业开发者：需提交营业执照等资质

### 3.3 创建应用

**步骤1**：进入【控制台】→【应用管理】→【创建应用】

**步骤2**：选择应用类型
- 个人开发者：选「**自用型应用**」
- 填写应用名称、简介
- 提交审核（1-3个工作日）

### 3.4 获取凭证

审核通过后获取：
- **AppKey**：应用唯一标识
- **AppSecret**：加密密钥

### 3.5 常用接口

| 接口名称 | 功能 | 个人权限 |
|---------|------|---------|
| taobao.item.get | 获取商品信息 | ✅ 基础可用 |
| taobao.items.search | 商品搜索 | ✅ 基础可用 |
| taobao.item.price.update | 价格更新 | ⚠️ 部分受限 |

---

## 四、Python调用代码示例

### 4.1 京东API调用

```python
import requests
import hashlib
import time
import json

# ========== 配置区 ==========
APP_KEY = "你的AppKey"
APP_SECRET = "你的AppSecret"
ITEM_ID = "商品ID"  # 如 "100012345678"
# ============================

def get_jd_price(sku_id):
    """获取京东商品价格"""
    api_url = "https://api.jd.com/routerjson"
    
    params = {
        "app_key": APP_KEY,
        "method": "jingdong.item.base.info.get",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "format": "json",
        "v": "2.0",
        "360buy_param_json": json.dumps({"skuId": sku_id})
    }
    
    # 生成签名
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    sign_str = "".join([f"{k}{v}" for k, v in sorted_params]) + APP_SECRET
    sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()
    params["sign"] = sign
    
    response = requests.get(api_url, params=params, timeout=10)
    if response.status_code == 200:
        return response.json()
    return None

# 使用示例
result = get_jd_price("100012345678")
print(result)
```

### 4.2 淘宝API调用

```python
import requests
import hashlib
import time
import urllib.parse

# ========== 配置区 ==========
APP_KEY = "你的AppKey"
APP_SECRET = "你的AppSecret"
# ============================

def get_taobao_item(item_id):
    """获取淘宝商品信息"""
    api_url = "https://gw.api.taobao.com/router/rest"
    
    params = {
        "app_key": APP_KEY,
        "method": "taobao.item.get",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "format": "json",
        "v": "2.0",
        "item_id": item_id
    }
    
    # 生成签名
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    sign_str = "".join([f"{k}{v}" for k, v in sorted_params]) + APP_SECRET
    sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()
    params["sign"] = sign
    
    response = requests.get(api_url, params=params, timeout=10)
    return response.json()

result = get_taobao_item("123456789")
print(result)
```

---

## 五、注意事项

### 5.1 调用限制
| 平台 | 个人开发者限制 |
|------|--------------|
| 京东 | 100次/天（基础接口） |
| 淘宝 | 10次/分钟 |

### 5.2 用途限制
- ⚠️ API数据仅供学习研究，不能用于商业爬虫
- ⚠️ 批量调用可能触发风控，建议加延迟

### 5.3 签名生成
- 京东/淘宝都使用 **MD5签名**
- 签名规则：把所有参数按字母排序 + 拼接AppSecret → MD5加密 → 转大写

---

## 六、申请检查清单

- [ ] 注册京东开放平台账号（个人开发者）
- [ ] 完成实名认证（上传身份证）
- [ ] 创建应用（工具应用/自用型）
- [ ] 获取 AppKey 和 AppSecret
- [ ] 申请商品查询/价格查询接口权限
- [ ] 测试调用成功

---

## 七、相关Skill

| Skill | 用途 |
|-------|------|
| `delonix-procurement-radar` | 德胧采购底价雷达（主Skill） |
| `hotel-procurement-price-check` | 基础价格查询 |
| `1688-api-key-guide` | 1688 API申请指引（企业版） |

---

*Version: 1.0*
*维护者：小柱*
*更新：2026-04-16 基于CSDN教程整合*
