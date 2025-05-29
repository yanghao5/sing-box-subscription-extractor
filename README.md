# sing-box-subscription-extractor （sing-box 订阅聚合）

有越来越多的机场开始提供 sing-box 格式的订阅.

`sing-box-subscription-extractor` 可以将多个机场的订阅整合到一个 json 文件里.

它也可以提取多个机场订阅中的节点，并将其存放到一个 json 文件中.

# 使用

- 你可以在本地运行此项目
- 或者使用 github action 和 cloudflare worker 部署一个简单的订阅服务.

## 机场订阅

首先，你要能确定，你的机场是提供的 sing-box 订阅的，不然一切白搭.

```bash
# htttps://xxxxx 是你的机场订阅链接
wget --user-agent="sing-box" https://xxxx -O xxxx.json
```

## 本地运行

```bash
# clone repo
git clone --depth= 1 https://github.com/yanghao5/sing-box-subscription-extractor.git sbse && cd sbse

# install deps
pip install -r  requirements.txt -q

# edit providers.toml
# refer to doc https://github.com/yanghao5/sing-box-subscription-extractor/blob/main/docs/providers.md 

# go
python3 main.py
```

## 使用 github 和 cf worker

fork 一份本仓库

（未完待续）