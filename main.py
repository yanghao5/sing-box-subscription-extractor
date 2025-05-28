import sys
import os

# internal
import validator
from provider import provider
from subscribe import subscribe, processor
from extractor.extractor import ext
from posttask import posttask
from generator import generator

if __name__ == "__main__":
    
    # Step 1 validate providers.toml
    validator.providers.validate("providers.toml")

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
    
    # if not p.cloudflare:
    #     upload.cf(p.cloudflare, p.config_save_path, p.nodes_save_path)
        
    # Step 7 post task
    #posttask.post_task()
