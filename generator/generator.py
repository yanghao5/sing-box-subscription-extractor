import os
import shutil
import json
from typing import List, Optional
from dataclasses import dataclass

# internal
from extractor.extractor import Sub
from provider.provider import Providers, Sort


@dataclass
class SubsTag:
    subtag: str
    tags: List[str]


def Filter(
    subscribe_tag: List[str],
    filter_action: str,
    filter_keywords: str,
) -> List[str]:
    ret = []

    keywords = filter_keywords.split("|")

    if filter_action == "include":
        for tag in subscribe_tag:
            for k in keywords:
                if k in tag:
                    ret.append(tag)
                    break

    if filter_action == "exclude":
        for tag in subscribe_tag:
            skip = False
            for k in keywords:
                if k in tag:
                    skip = True
                    break
            if skip:
                continue
            ret.append(tag)

    return ret


# GetTags(tag,subs_tag,filter_enable,filter_action,filter_keywords)
def GetTags(
    tag: str,
    substag: List[SubsTag],
    filter_enable: bool,
    filter_action: str,
    filter_keywords: str,
) -> List[str]:
    subscribe_tags = []
    for t in substag:
        if tag == t.subtag:
            subscribe_tags = t.tags
    ret = []
    if filter_enable:
        ret = Filter(subscribe_tags, filter_action, filter_keywords)
    else:
        ret = subscribe_tags
    return ret


def Sort(Data: dict, sorts: Sort):
    for sort in sorts:
        key_words = sort.keywords
        ranges = sort.rang.split("|")
        # mixed=sort.mixed
        # 查找 "others" 的索引位置
        if "others" in key_words:
            others_index = key_words.index("others")
        else:
            others_index = len(
                key_words
            )  # 如果没有 "others"，则将其位置设为 keywords 的长度

        # 遍历 ranges 和 Data["outbounds"]
        for r in ranges:
            for o in Data["outbounds"]:
                if r == o["tag"]:

                    def sort_key(item: str):
                        # 遍历关键词，查看 item 是否包含该关键词
                        for idx, keyword_group in enumerate(key_words):
                            # 如果 item 包含某个关键字组
                            if any(
                                keyword in item for keyword in keyword_group.split("|")
                            ):
                                return idx  # 返回匹配到的关键词组的索引
                        return (
                            others_index  # 如果没有匹配任何关键词，返回 "others" 的索引
                        )

                    # 对 outbounds 中的元素进行排序
                    o["outbounds"].sort(key=sort_key)


def gen(Subs: List[Sub], p: Providers):
    # Step 1 save_path
    configSavePath = ""
    if p.config_save_path == "":
        configSavePath = "./config.json"
    else:
        configSavePath = p.config_save_path

    nodesSavePath = ""
    if p.nodes_save_path == "":
        nodesSavePath = "./nodes.json"
    else:
        nodesSavePath = p.nodes_save_path

    # Step 2 read tmpl file
    with open(p.tmpl_path, "r") as f:
        tmpl = json.load(f)

    # Step 3 generate all_tag for {all}
    all_tag = SubsTag(subtag="{all}", tags=[])
    for sub in Subs:
        for t in sub.nodes:
            all_tag.tags.append(sub.prefix + t["tag"])

    # Step 4 generate subs_tag for {subscribe_tag}
    subs_tag = []
    for sub in Subs:
        # get nodes tag list
        temp = []
        for t in sub.nodes:
            temp.append(sub.prefix + t["tag"])  # add prefix

        subs_tag.append(SubsTag(subtag="{" + sub.tag + "}", tags=temp))

    # Step 5 combine tags
    subs_tag.append(all_tag)

    # Step 6 add tag to tmpl
    for o in tmpl["outbounds"]:
        # skip
        if "outbounds" not in o:
            continue

        filter_enable = False
        filter_action = ""
        filter_keywords = ""

        if "filter" in o:
            filter_enable = True
            filter_action = o["filter"]["action"]
            filter_keywords = o["filter"]["keywords"]

        for tag in o["outbounds"]:
            for t in subs_tag:
                if tag == t.subtag:
                    o["outbounds"].remove(tag)
                    filtered_tags = GetTags(
                        tag, subs_tag, filter_enable, filter_action, filter_keywords
                    )
                    o["outbounds"].extend(filtered_tags)
                    o.pop("filter", None)
    # for-end

    # Step 6 Test
    # for o in tmpl["outbounds"]:
    #     if o.get("tag") == "Proxy":
    #         print(json.dumps(o, ensure_ascii=False, indent=4))
    #     if o.get("tag") == "HongKong":
    #         print(json.dumps(o, ensure_ascii=False, indent=4))
    #     if o.get("tag") == "Others":
    #         print(json.dumps(o, ensure_ascii=False, indent=4))

    # Step 7 sort outbounds
    Sort(tmpl, p.sort)

    # Step 8 add nodes to tmpl file
    for sub in Subs:
        for n in sub.nodes:
            n["tag"] = sub.prefix + n["tag"]
            tmpl["outbounds"].append(n)

    # Step 8 gen nodes.json data
    nodesjson = []
    for sub in Subs:
        nodesjson.extend(sub.nodes)

    # Step 9 gen cloudflare data
    with open("./temp/config.json", "w") as file:
        json.dump(tmpl, file, indent=4, ensure_ascii=False)

    with open("./temp/nodes.json", "w") as file:
        json.dump(nodesjson, file, indent=4, ensure_ascii=False)

    # Step 10
    if p.mode == "nodes":
        shutil.copy("./temp/nodes.json", nodesSavePath)
        print("\033[31m nodes file saved as " + nodesSavePath + "\033[0m")
    if p.mode == "tmpl":
        shutil.copy("./temp/config.json", configSavePath)
        print("\033[31m sing-box config file saved as " + nodesSavePath + "\033[0m")
    if p.mode == "full":
        shutil.copy("./temp/config.json", configSavePath)
        print("\033[31m sing-box config file saved as " + configSavePath + "\033[0m")
        
        shutil.copy("./temp/nodes.json", nodesSavePath)
        print("\033[31m nodes file saved as " + nodesSavePath + "\033[0m")
