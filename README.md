# sing-box-subscription-extractor （sing-box 订阅聚合）

有越来越多的机场开始提供 sing-box 格式的订阅.

`sing-box-subscription-extractor` 可以将多个机场的订阅整合到一个 json 文件里.

它也可以提取多个机场订阅中的节点，并将其存放到一个 json 文件中.

# 使用

- 你可以在本地运行此项目
- 或者使用 github action 和 cloudflare worker 部署一个简单的订阅服务.

## 机场订阅

首先，你要确定，你的机场是提供的 sing-box 订阅的，不然一切白搭.

```bash
# htttps://xxxxx 是你的机场订阅链接
wget --user-agent="sing-box" https://xxxx -O xxxx.json
```

## 本地运行

- 本地需要有 python 环境
- 你需要配置文件 providers.toml

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

> chatGPT 是一个好帮手
>
> 我建议你先在本地运行，学会编辑 providers.toml 文件，再来尝试

### 准备工作

- 在你 Cloudflare 账号中创建一个名为 `Proxy` 的 KV 数据库 
- 申请 Cloudflare API
- 准备好 providers.toml 文件
    - 参考 [providers](https://github.com/yanghao5/sing-box-subscription-extractor/blob/main/docs/providers.md)
- 你的本地电脑需要有 nodejs 环境
    - 如果你懂 cf worker 的开发，你直接参考 src/index.ts 自己创建一个 worker 就行了

### cloudflare worker

```bash
# clone repo
git clone --depth= 1 https://github.com/yanghao5/sing-box-subscription-extractor.git sbse && cd sbse

cd cfworker/webget

# install deps
pnpm install

# login
pnpx wrangler login

# edit wrangler.jsonc
	"kv_namespaces": [
		{
		"binding": "Proxy",
		"id": "xxxxxxxxxxxxxxxxxxx"
		}
	],
# 你需要把 KV 数据库的 id 填上

# 部署
pnpx wrangler deploy
```

- worker 的链接一般是 xxxx.yyyy.worker.com 
- yyyy 是你的账号名称，假设是 king
- 那么访问 [https://webget.king.worker.dev/whoami](https://webget.king.worker.com/whoami)
- 你会看到自己的 ip，你可以在 cloudflare 的 dash 中查看具体链接
- cf worker 就搞好了

### github action
- fork 一份本仓库
- 在仓库设置中打开 action 的 issue 创建权限
- Settings -> Actions secrets and variables -> Action -> Variables 创建一个 Repository variables
    - 名称为 PROVIDERS，值为 providers.toml 中的内容
- 在 action 中，有一个 extract workflow 手动运行，它用于提取订阅，并将其上传到 cf kv 中
- 根据你在 providers 中定义的 token 去访问对应的链接

```
https://webget.king.worker.dev/subscribe?token=xxxxxxxxxxxxxxxxxxxx
```
- update action 每天凌晨运行一次，判断需不需要，更新订阅，如果需要，它会创建一个 issue ，提醒你该更新了

> 为什么不全部做成自动的？
> 
> 因为从机场下载订阅，判断是否更新订阅，再到聚合订阅，再到上传订阅到 cf kv ，每一个步骤都有很大的不确定性.
>
> 所以，我觉得要把，该不该更新，交给人来做最终判断