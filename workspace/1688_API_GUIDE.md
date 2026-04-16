# 1688 API 调用攻略

> 为德胧采购比价系统提供商品批发价数据

**更新：2026-04-15**

---

## 方案一：官方开放平台 API（推荐，已验证）

### 1.1 接入流程

| 步骤 | 说明 | 预计时间 |
|------|------|----------|
| 1. 注册开发者账号 | https://open.1688.com，用企业/个人支付宝登录 | 即时 |
| 2. 创建自研应用 | 控制台 → 应用管理 → 创建自研应用 | 即时 |
| 3. 申请商品搜索权限 | 能力市场搜索 `alibaba.item.search` 或 `offer.search` | 5分钟~1天 |
| 4. 获取 AppKey + AppSecret | 应用详情页获取 | 即时 |

**关键信息**：
- 自研应用（不对外分发）可自助开通，审核快
- 商品搜索基础权限通常**即时通过**，无需人工审核
- 个人开发者可申请，但企业认证权限更全

### 1.2 API Endpoint

```
https://gw.open.1688.com/openapi/param2/1/portals.open.api.item.search/{appKey}
```

### 1.3 必填系统参数

| 参数 | 说明 |
|------|------|
| `app_key` | 应用Key |
| `method` | `alibaba.item.search` |
| `timestamp` | `yyyy-MM-dd HH:mm:ss` 格式 |
| `v` | `2.0` |
| `sign_method` | `md5` |
| `sign` | 签名（见1.4） |

### 1.4 签名算法（MD5 模式，经验证正确）

```python
import hashlib

def generate_sign(params: dict, app_secret: str) -> str:
    """
    1688 官方签名算法：
    1. 参数按 ASCII 升序排列
    2. 拼接成 k1=v1&k2=v2
    3. 首尾拼接 AppSecret
    4. MD5 大写
    """
    sorted_pairs = sorted(params.items(), key=lambda x: x[0])
    query_str = "&".join([f"{k}={v}" for k, v in sorted_pairs])
    raw = f"{app_secret}{query_str}{app_secret}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest().upper()
```

### 1.5 业务参数

| 参数 | 说明 |
|------|------|
| `q` | 搜索关键词 |
| `page` | 页码（默认1） |
| `pageSize` | 每页条数（最大50） |
| `sort` | `sale`（销量）/ `priceAsc`（价格升）/ `priceDesc`（价格降） |

### 1.6 完整调用示例

```python
import requests, time, hashlib

APP_KEY = "你的AppKey"
APP_SECRET = "你的AppSecret"

def generate_sign(params, app_secret):
    sorted_pairs = sorted(params.items(), key=lambda x: x[0])
    query_str = "&".join([f"{k}={v}" for k, v in sorted_pairs])
    raw = f"{app_secret}{query_str}{app_secret}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest().upper()

def search(keyword, page=1, page_size=20):
    url = f"https://gw.open.1688.com/openapi/param2/1/portals.open.api.item.search/{APP_KEY}"
    params = {
        "app_key": APP_KEY,
        "method": "alibaba.item.search",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "v": "2.0",
        "sign_method": "md5",
        "q": keyword,
        "page": page,
        "pageSize": page_size,
        "sort": "sale",
    }
    params["sign"] = generate_sign(params, APP_SECRET)
    resp = requests.get(url, params=params, timeout=15)
    data = resp.json()
    if data.get("error_code"):
        raise RuntimeError(f"API错误: {data}")
    # 返回商品列表
    return data["result"]["products"]

products = search("酒店门锁")
for p in products[:5]:
    print(p.get("subject"), p.get("price"))
```

---

## 方案二：第三方聚合 API（无需申请，即开即用）

### 2.1 订单侠 (dingdanxia.com)

```
接口地址: https://api.ds.dingdanxia.com/1688/item_search
参数: apikey, keyword, page, pageSize
注册: https://www.dingdanxia.com（注册送免费调用次数）
```

### 2.2 万邦 (onebound.cn)

```
接口地址: https://api-gw.onebound.cn/1688/
参数: key, secret, num_iid / keyword
```

### 2.3 淘宝/天猫代用（通用电商接口）

部分第三方平台提供统一的电商数据接口，覆盖1688、淘宝、天猫等：
- `item_search` 关键词搜索
- `item_get` 商品详情

---

## 方案三：1688 开放平台能力市场（自研应用）

在 https://open.1688.com/ability-market.html 搜索：
- `offer.search` — 搜索供应信息
- `alibaba.cps.similar.offer.search` — 分销商品搜索
- `alibaba.product.search` — 商品搜索

自研应用权限**即时生效**，无需审核。

---

## 踩坑指南（实战总结）

1. **签名算法是最大坑**：必须 `secret + 排序字符串 + secret`，顺序/大小写错一位就 403
2. **laupta.1688.com 游客接口已下线**：返回 404，不可用
3. **1688 搜索页全部 JS 渲染**：无法直接抓 HTML 获取数据，必须走 API
4. **AccessToken**：OAuth2 模式需先获取 token，有效期2小时，需刷新
5. **频率限制**：官方 300次/分钟，建议脚本加 `time.sleep(1.5)`
6. **自研 vs 第三方**：自研应用权限申请快，但部分商品搜索接口需企业认证

---

## 其他 B2B 平台 API 参考

| 平台 | API 地址 | 备注 |
|------|----------|------|
| 阿里巴巴国际站 | https://developer.alibaba.com | 企业认证 |
| 慧聪网 | https://www.hc360.com | 有开放API |
| 工品优选 | https://www.gongping360.com | 工业品 B2B |

---

*最后更新：2026-04-15*
