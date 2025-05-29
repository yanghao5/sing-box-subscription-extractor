import os 
import json

# internal pkg
from core.validator import toml
from core.validator import providers
from core.provider import provider
from core.subscribe import subscribe, processor
from core.extractor.extractor import ext
from core.posttask import posttask
from core.generator import generator
from core.cf import cf  

def get_providers():
    providers = os.getenv('PROVIDERS')
    cleaned_providers = providers.replace('\r', '')
    if providers:
        with open('providers.toml', 'w') as f:
            f.write(providers)
        print("Providers.toml has been created successfully.")
    else:
        print("No PROVIDERS environment variable found.")

if __name__ == "__main__":    
    # Step 1 get providers.toml
    get_providers()
    toml.validate('providers.toml')
    
    # Step 2 validate providers.toml
    providers.validate("providers.toml")

    # Step 3 read providers.toml
    p = provider.reader("providers.toml")

    # Step 4 download_subscribe
    rawdata_list = subscribe.fetcher(p)

    # Step 5 process raw subscribe data
    processor.refine_raw_data(rawdata_list)

    # Step 6 extract nodes
    subs=ext(p.subscribe)
    
    # Step 7 gen
    generator.gen(subs,p)
    
    # Step 8 upload to cloudflare kv  
    if p.cloudflare:
        # upload nodes
        with open("./temp/nodes.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        json_str = json.dumps(data, ensure_ascii=False)
        cf.upload(p.cloudflare,json_str,"nodes")
        
        # upload subscription
        with open("./temp/config.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        json_str = json.dumps(data, ensure_ascii=False)
        for t in p.cloudflare.SUBSCRIBE_USER_TOKEN:
            cf.upload(p.cloudflare,json_str,t)
