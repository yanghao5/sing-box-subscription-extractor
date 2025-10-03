# sing-box-subscription-extractor （sing-box 订阅提取）

- 有越来越多的机场开始提供 sing-box 格式的订阅
- `sing-box-subscription-extractor` 可以将多个机场的订阅整合到一个 json 文件里
- 它也可以提取多个机场订阅中的节点，并将其存放到一个 json 文件中

# 使用

## 检查机场订阅

首先，要确定，机场是否提供 sing-box 订阅.

```bash
# htttps://xxxxx 是你的机场订阅链接
wget --user-agent="sing-box" https://xxxx -O xxxx.json
```

## 本地运行

- 本地需要有 python 环境
- 你需要配置文件 providers.json

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

## cf worker （可选）

### 准备工作

- 在你 Cloudflare 账号中创建一个名为 `Proxy` 的 KV 数据库 
- 申请 Cloudflare API
- CF 相关数据填入到 providers.json 文件
    - 参考 [providers](https://github.com/yanghao5/sing-box-subscription-extractor/blob/main/docs/providers.md)
- 你的本地电脑需要有 nodejs 环境
    - 如果你懂 cf worker 的开发，你直接参考 src/index.ts 自己创建一个 worker 就行了

### deploy cloudflare worker

```bash

cd cfworker/webget

# 1. install deps
pnpm install

# 2. login
pnpx wrangler login

# 3. edit wrangler.jsonc
	"kv_namespaces": [
		{
		"binding": "Proxy",
		"id": "xxxxxxxxxxxxxxxxxxx"
		}
	],
# 4. 你需要把 KV 数据库的 id 填上

# 5. 部署
pnpx wrangler deploy
```

- worker 的链接一般是 xxxx.yyyy.worker.com 
- yyyy 是你的账号名称，假设是 king
- 那么访问 [https://webget.king.worker.dev/whoami](https://webget.king.worker.com/whoami)
- 如果能看到自己的 ip ，就说明正常
- 另外，你可以在 cloudflare 的 dash 中查看具体链接