import os
import json
import sys

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
    P = os.getenv("PROVIDERS")
    cleaned_providers = P.replace("\r", "")
    if P:
        with open("providers.toml", "w") as f:
            f.write(P)
        print("Providers.toml has been created successfully.")
    else:
        print("No PROVIDERS environment variable found.")

if __name__ == "__main__":
    # Step 1 get providers.toml
    get_providers()
    toml.validate("providers.toml")

    # Step 2 validate providers.toml
    providers.validate("providers.toml")

    # Step 3 read providers.toml
    p = provider.reader("providers.toml")

    # Step 4 download_subscribe
    rawdata_list = subscribe.fetcher(p)

    # Step 5 process raw subscribe data
    processor.refine_raw_data(rawdata_list)

    # Step 6 extract nodes
    subs = ext(p.subscribe)

    # Step 7 gen
    generator.gen(subs, p)

    # Step 9 get old nodes
    if p.cloudflare:
        oldnodes = cf.get(p.cloudflare, "nodes")
        
        with open("./temp/oldnodes.json", "w",encoding="utf-8") as json_file:
            json.dump(oldnodes, json_file, indent=4, ensure_ascii=False)

    with open("./temp/nodes.json", "r", encoding="utf-8") as newfile:
        newnodes = json.load(newfile)

    # Step 10 compare json obj
    if oldnodes != newnodes:
        sys.stderr.write("error: The JSON objects are different.\n")
    else:
        print("you don't need to update sunscription !!!")
