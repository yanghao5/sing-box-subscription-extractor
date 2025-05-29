# tmpl 

一个 sing-box 配置文件有五部分
```json
{
    "log":{},
    "experimental":{},
    "dns":{},
    "inbounds":{},
    "outbounds":{},
    "route":{}
}
```

模板文件，只修改 `outbounds` 部分.

具体来说，是带有 `outbounds` 的 `outbounds`.

sbse 会做两件事
- 将所有的节点添加到 `outbounds` 中
- 将 `outbounds` 中 `{xxxx}` 替换成相应的一些列 tag
    - 如果包含 `filter` 字段，会先对 `{xxxx}` 过滤，再替换 

```json
    {
      "tag": "Proxy",
      "type": "selector",
      "outbounds": [
        "auto",
        "direct",
        "{all}"
      ]
    },
```

## 关于 `{xxxx}`

sbse 会将所有的订阅节点，放到 `{all}`.

同时，我们在 providers.toml 中定义的订阅 `tag` 会对应生成一个 `{tag}`

你可以使用 `{all}` 或者 `{tag}`

## 关于 filter 字段

```json
"filter": {
    "action": "include",
    "keywords": "🇭🇰|HK|hk|香港|港|HongKong"
}
```
- action 有两种 `include` 或 `exclude` ，作用，顾名思义，保留包含关键字的节点，排除包含关键字的节点
- keyword 就是关键字，用 `|` 隔开





