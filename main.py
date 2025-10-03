import json

from tools.validator import validator
from tools.provider import provider
from tools.subscribe import subscribe, processor
from tools.extractor.extractor import ext
from tools.generator import generator
from tools.cf import cf  

if __name__ == "__main__":
     # Step 1 validate providers.json
     validator.Json("providers.json")
     # Step 2 read providers.json
     p = provider.Read("providers.json")
     # Step 3 download_subscribe
     raw_data_list = subscribe.fetcher(p)
     # Step 4 process raw subscribe data
     processor.refine_raw_data(raw_data_list)
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