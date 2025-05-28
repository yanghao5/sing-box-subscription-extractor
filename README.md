# sing-box-subscription-extractor （sing-box 订阅聚合）

有越来越多的机场开始提供 sing-box 格式的订阅.

`sing-box-subscription-extractor` 可以将多个机场的订阅整合到一个 json 文件里.

它也可以提取多个机场订阅中的节点，并将其存放到一个 json 文件中.

# 使用

- 你可以在本地运行此项目
- 或者使用 github action 和 cloudflare worker 部署一个简单的订阅服务.

## 本地运行

```bash
# clone repo
git clone --depth= 1 https://github.com/yanghao5/sing-box-subscription-extractor.git sbse && cd sbse

# install deps
pip install -r  requirements.txt -q

# edit providers.toml
# refer to doc 

# go
python3 main.py
```
