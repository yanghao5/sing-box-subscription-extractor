import json

# internal
from core.validator import providers
from core.provider import provider
from core.subscribe import subscribe, processor
from core.extractor.extractor import ext
from core.posttask import posttask
from core.generator import generator
from core.cf import cf  

if __name__ == "__main__":
    
    # Step 1 validate providers.toml
    providers.validate("providers.toml")

    # Step 2 read providers.toml
    p = provider.reader("providers.toml")

    # Step 3 download_subscribe
    rawdata_list = subscribe.fetcher(p)

    # Step 4 process raw subscribe data
    processor.refine_raw_data(rawdata_list)

    # Step 5 extract nodes
    subs=ext(p.subscribe)
    
    # Step 5 gen
    generator.gen(subs,p)
    
    # Step 6 upload to cloudflare kv  
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
        
    # Step 7 post task
    #posttask.post_task()
