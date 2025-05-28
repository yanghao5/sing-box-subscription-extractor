from typing import List, Optional
from dataclasses import dataclass

# third-party pkg
import toml

# 定义一个 Cloudflare 配置类
@dataclass
class Cloudflare:
    CLOUDFLARE_ACCOUNT_ID: str
    CLOUDFLARE_API_KEY: str
    CLOUDFLARE_EMAIL: str  
    CLOUDFLARE_KV_NAMESPACE_ID: str
    SUBSCRIBE_USER_TOKEN: List[str]

# 定义一个 Subscribe 配置类
@dataclass
class Subscribe:
    url: str
    tag: str
    prefix: Optional[str] = None
    exclude_keywords: Optional[str] = None
    exclude_protocol: Optional[str] = None

# 定义一个 Sort 配置类
@dataclass
class Sort:
    rang: str
    #mixed: bool
    keywords: List[str]

# 定义主配置类
@dataclass
class Providers:
    mode: str
    tmpl_path: str
    config_save_path: str
    nodes_save_path: str
    cloudflare: Optional[Cloudflare] = None
    subscribe: List[Subscribe] = None  # 默认值设置为空列表
    sort: Optional[List[Sort]] = None

def reader(toml_file: str) -> Providers:
    with open(toml_file, 'r', encoding='utf-8') as f:
        data = toml.load(f)
    
    cloudflare = None
    if 'cloudflare' in data:
        cloudflare_data = data['cloudflare']
        cloudflare = Cloudflare(
            CLOUDFLARE_ACCOUNT_ID=cloudflare_data['CLOUDFLARE_ACCOUNT_ID'],
            CLOUDFLARE_API_KEY=cloudflare_data['CLOUDFLARE_API_KEY'],
            CLOUDFLARE_EMAIL=cloudflare_data['CLOUDFLARE_EMAIL'],
            CLOUDFLARE_KV_NAMESPACE_ID=cloudflare_data['CLOUDFLARE_KV_NAMESPACE_ID'],
            SUBSCRIBE_USER_TOKEN=cloudflare_data['SUBSCRIBE_USER_TOKEN']
        )
    
    subscribe_list = []
    for sub in data.get('subscribe', []):
        subscribe_item = Subscribe(
            url=sub['url'],
            tag=sub['tag'],
            prefix=sub.get('prefix', None),
            exclude_keywords=sub.get('exclude_keywords', None),
            exclude_protocol=sub.get('exclude_protocol', None)
        )
        subscribe_list.append(subscribe_item)
    
    sort_list = []
    for sort in data.get('sort', []):
        sort_item = Sort(
            rang=sort['range'],
            #mixed=sort['mixed'],
            keywords=sort['keywords']
        )
        sort_list.append(sort_item) 

    return Providers(
        mode=data['mode'],
        tmpl_path=data['tmpl_path'],
        config_save_path=data['config_save_path'],
        nodes_save_path=data['nodes_save_path'],
        cloudflare=cloudflare,
        subscribe=subscribe_list,
        sort=sort_list
    )

if __name__=="__main__":
    config = reader('config.toml')
    print(config)