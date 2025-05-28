import json
from typing import List, Optional
from dataclasses import dataclass

# internal
from core.provider.provider import Subscribe


@dataclass
class Sub:
    url: str
    tag: str
    filepath: str
    nodes: List[dict]
    prefix: Optional[str] = None
    exclude_keywords: Optional[str] = None
    exclude_protocol: Optional[str] = None

def ext(subscribes: List[Subscribe]) -> List:
    Subs = []
    for sub in subscribes:
        item = Sub(
            url=sub.url,
            tag=sub.tag,
            filepath="temp/refine/" + sub.tag + ".json",
            nodes=[],
            prefix=sub.prefix,
            exclude_keywords=sub.exclude_keywords,
        )
        if sub.exclude_protocol == "":
            item.exclude_protocol = "direct|block|dns|selector|urltest"
        else:
            item.exclude_protocol = (
                "direct|block|dns|selector|urltest" + "|" + sub.exclude_protocol
            )
        Subs.append(item)
    
    for sub in Subs:
        # Split exclude protocols and keywords into lists
        exclude_protocols = sub.exclude_protocol.split("|") if sub.exclude_protocol else []
        exclude_keywords = sub.exclude_keywords.split("|") if sub.exclude_keywords else []
                
        # Read JSON file
        with open(sub.filepath, "r") as f:
            data = json.load(f)

        # Extract 'outbounds' field, using .get() to avoid KeyError
        outbounds = data.get("outbounds", [])
        outbound_list = []
        
        for ob in outbounds:
            # Skip the entry if 'type' is in the excluded protocols list
            if ob["type"] in exclude_protocols:
                continue
            
            # Skip the entry if 'tag' contains any of the excluded keywords
            skip=False
            for k in exclude_keywords:
                if k in ob["tag"]:
                    skip=True
            if skip:
                continue
                                
            # Add the valid outbound to the list
            outbound_list.append(ob)
        
        # Update the 'nodes' field of the Sub object
        sub.nodes = outbound_list

    return Subs
