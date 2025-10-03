# providers.toml

providers 文件是配置文件.
其中的要求和每一个配置选项的含义如下.

# 基础

```json
    // required, string，值只能为 full tmpl nodes
    // tmpl 只输出配置文件
    // nodes 只输出节点
    // full 全部输出
    "mode": "full", 
    // 生成配置的模版
    "tmpl_path": "tmpl/myself.json",
    // 配置保存的文件路径
    "config_save_path": "./config.json",
    // 节点文件保存的文件路径
    "nodes_save_path": "./nodes.json",
```

# cf
```json
    "cf": {
        "CLOUDFLARE_ACCOUNT_ID": "xxxxxxxxxxxxxxxxxxxxx",
        "CLOUDFLARE_API_KEY": "xxxxxxxxxxxxxxxxxxxxx",
        "CLOUDFLARE_EMAIL": "xxxxxxxxxxxxxxxxxxxxx",
        "CLOUDFLARE_KV_NAMESPACE_ID": "xxxxxxxxxxxxxxxxxxxxx",
        // 数组
        // 每个 token 仅由数字和小写字母组成
        // 每个 token 长度需大于等于 32
        "USER_TOKEN": [
            "xxxxxxxxxxxxxxxxxxxxx"
        ]
    }
```

- 提供操作 cloudflare kv 的配置
- CLOUDFLARE_ACCOUNT_ID 你的 cloudflare 账号 id
- CLOUDFLARE_API_KEY 你的 cloudflare api
- CLOUDFLARE_EMAIL 你的 cloudflare 账号邮箱
- CLOUDFLARE_KV_NAMESPACE_ID 你创建的 KV 数据库 id
- USER_TOKEN 用最终的 worker 订阅连接
    - 仅由数字和小写字母组成，长度需大于等于 32
```
https://webget.xxx.worker.dev/subscribe?token=xxxxxxxxxxxxxxxxxxx
```

# subscribe

```
"subscription": [
    {
        "url": "https://xxxxxxxxxxxxxxxxxxxxx",
        "tag": "s1",
        "prefix": "",
        "exclude_keywords": "自动|网站|官网|流量|过期|到期|收藏|超时|重置",
        "exclude_protocol": ""
    },
    {
        "url": "https://xxxxxxxxxxxxxxxxxxxxx",
        "tag": "hostall"
    }
],
```

- [[subscribe]] 用于机场订阅的设置
- url 机场订阅链接
- tag 你为机场设定的 tag 
- prefix 为不同的机场设置前缀，最终会体现在每个节点的名称上
- exclude_keywords 按照关键字排除某些节点，使用 `|` 隔开关键字
- exclude_keywords 按照节点协议排除某些节点，使用 `|` 隔开协议名称

# sort
```
[[sort]]
range = "Proxy"
keywords = [ # 数组长度要大于等于 2
    "auto",
    "direct",
    "🇭🇰|HK|hk|香港|港|HongKong",
    "🇹🇼|TW|tw|台湾|臺灣|台|Taiwan",
    "🇸🇬|SG|sg|新加坡|狮|Singapore",
    "🇯🇵|JP|jp|日本|日|Japan",
    "🇺🇸|US|us|美国|美|United States",
    "others",
]

[[sort]]
range = "Jpan|Singapore|HongKong"
keywords = [
    "专线",
    "亚马逊",
    "搬瓦工",
    "0.1倍率",
    "IPv6|ipv6",
    "others",
]
```
- [[sort]] 用于节点排序
- range 是订阅文件中 outbounds 的 tag，使用 `|` 隔开不同的 tag
- keywords 是排序规则，节点名称包含的关键字顺序，就是节点顺序