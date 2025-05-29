# providers.toml

providers 文件是配置文件.
其中的要求和每一个配置选项的含义如下.

# 基础

```
mode = "full" # required, string，值只能为 full tmpl nodes, 不可以为空
tmpl_path = "tmpl/RealDNS_Tun_RuleSet.json" # required, string, 不可以为空
config_save_path = "./config.json" # required, string, 可以为空
nodes_save_path = "./nodes.json" # required, string, 可以为空
```
- mode: tmpl 模式，用模板生成订阅文件，nodes 模式只生成节点文件，full 模式，两者都生成
- tmpl_path 模板路径，模板可以自己制作，也可以使用预制的（tmpl目录中）
    - 关于模板，参考 doc
- config_save_path 订阅文件的保存路径，为空时，使用默认路径
- nodes_save_path 节点文件的保存路径，为空时，使用默认路径

# [cloudflare] 
```
# optional 要么不写，写就需要写全，每一项都不能为空
[cloudflare] 
CLOUDFLARE_ACCOUNT_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CLOUDFLARE_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CLOUDFLARE_EMAIL="xxxxx@gmail.com" # 必须是合法的邮箱地址
CLOUDFLARE_KV_NAMESPACE_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# 数组
# 每个 token 仅由数字和小写字母组成
# 每个 token 长度需大于等于 32
SUBSCRIBE_USER_TOKEN=[
    "y5vswuhsfrona3y464yii8xc8zk6ffv7",
    "6vunx1j0y3qont9vvqyf421nvj1psfnx",
    "dngg9c4batg7wbxbfhs44hbx0jvezhrp"
]
```

- [cloudflare] 提供操作 cloudflare kv 的配置
- CLOUDFLARE_ACCOUNT_ID 你的 cloudflare 账号 id
- CLOUDFLARE_API_KEY 你的 cloudflare api
- CLOUDFLARE_EMAIL 你的 cloudflare 账号邮箱
- CLOUDFLARE_KV_NAMESPACE_ID 你创建的 KV 数据库 id
- SUBSCRIBE_USER_TOKEN 用最终的 worker 订阅连接，也就是 xxxxxxxxxxx 的部分
    - 仅由数字和小写字母组成，长度需大于等于 32
```
https://webget.xxx.worker.dev/subscribe?token=xxxxxxxxxxxxxxxxxxx
```

# subscribe

```
# required, 至少要有一个 [[subscribe]]，
# 如果一个都没有，则报错
# url 和 tag 必须存在，且值不能为空
# 剩余项，必须存在，但值可以为空
[[subscribe]]
url = "https://xxx.com/subscribe?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
tag = "AA"
prefix = "A-"
exclude_keywords="自动|网站|官网|流量|过期|到期|收藏|超时|重置"
exclude_protocol = "ssh" 
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