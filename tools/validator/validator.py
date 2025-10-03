import warnings

# internal pkg
from tools.validator import email
from tools.validator import tag_checker
from tools.validator import token

# third-party pkg
import json


# validate providers.toml
def Json(file_path):
    try:
        # 打开 JSON 文件，指定编码为 utf-8
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # validate mode field
        mode= data.get('mode')
        if not (isinstance(mode, str) and mode in ["full", "config", "nodes"]):
            raise ValueError('providers.json mode field is required and must be one of ["full", "config", "nodes"]')
        
        # validate tmpl_path field
        tmpl_path=data.get("tmpl_path",None)    
        if tmpl_path is None:
            raise ValueError('providers.json tmpl_path field is required')
        else:
            pass
        
        # validate config_save_path field
        config_save_path=data.get("config_save_path",None)
        if config_save_path is None:
            raise ValueError('providers.json config_save_path field is required')
        else:
            pass

        # validate nodes_save_path field
        # nodes_save_path=data.get("nodes_save_path",None)
        # if nodes_save_path is None:
        #     raise ValueError('providers.toml nodes_save_path field is required')
        
        # # validate [cloudflare] field
        cloudflare=data.get("cf",None)
        if cloudflare is None:
            warnings.warn("providers.json lack cf field", DeprecationWarning)
        else:
            check_cloudflare(cloudflare)

        # 校验 Subscription
        subscribes=data.get("subscription",None)
        if subscribes is None:
            raise ValueError('providers.json [[subscribe]] field is required')
        else:
            check_subscribes(subscribes)

        # 校验 Sort
        sorts=data.get("sort",None)
        if sorts is None:
            warnings.warn('providers.toml lack [[sort]]', DeprecationWarning)
        else:
            check_sorts(sorts)

        print("\033[34m providers.toml file verification passed! \033[0m\n")
    
    except ValueError as ve:
        print(f"\033[34m Verification Error: {ve} \033[0m")
    except Exception as e:
        print(f"\033[34m Other Error: {e} \033[0m")


# validate cloudflare
def check_cloudflare(cloudflare):
    required_fields = ["CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_KEY", "CLOUDFLARE_EMAIL", "CLOUDFLARE_KV_NAMESPACE_ID", "USER_TOKEN"]
    for field in required_fields:
        field_value=cloudflare.get(field,None)
        if field_value is None:
            raise ValueError(f"{field} in cf is empty")
        
    # validate mail address
    try:
        mail = cloudflare.get("CLOUDFLARE_EMAIL")
        email.validate(mail)
    except AttributeError as e:
        raise ValueError(f"Invalid email format in [cloudflare] field: {mail}") from e
    
    # Check USER_TOKEN
    user_token = cloudflare.get("USER_TOKEN")
    if not isinstance(user_token, list):
        raise ValueError(
            "USER_TOKEN must be a list."
        )
    if not user_token: # Checks if list is empty
        raise ValueError(
            "SUBSCRIBE_USER_TOKEN cannot be empty."
        )
    for t in user_token:
        if not token.validate(t):
            raise ValueError(
                f"USER_TOKEN haves invalid token {t}."
            )
            

# validate subscribes
def check_subscribes(subscribe_list):
    tags=[]
    for index,subscribe in enumerate(subscribe_list):
        url=subscribe.get("url",None)
        if not url:
            raise ValueError(f'providers.json subscription {index} field "url" is required and cannot be empty.')
        else:
            pass
        
        tag=subscribe.get("tag",None)
        if not tag: # This handles both None and ""
            raise ValueError(f'providers.json subscription {index} field "tag" is required and cannot be empty.')
        else:
            if tag in tags:
                raise ValueError(f"providers.json subscription {index} field have duplicate tag {tag}")
            if tag_checker.validate(tag):
                tags.append(tag)
            else:
                raise ValueError(f"providers.json subscription {index} field have invalid tag {tag}")
                
        # prefix
        prefix=subscribe.get("prefix",None)
        if not prefix:
            warnings.warn(f'providers.json {index} subscription prefix field is empty', DeprecationWarning)

        # exclude_keywords
        exclude_keywords=subscribe.get("exclude_keywords",None)
        if not exclude_keywords:
            warnings.warn(f'providers.toml {index} subscription exclude_keywords field is empty', DeprecationWarning)
            
        # exclude_protocol
        exclude_protocol=subscribe.get("exclude_protocol",None)
        if not exclude_protocol:
            warnings.warn(f'providers.toml {index} subscription exclude_protocol field is empty', DeprecationWarning)


# validate sort
def check_sorts(sort_list):
    for index,sort in enumerate(sort_list):
        # range
        _range=sort.get("range",None)
        if _range is None:
            raise ValueError(f'providers.json {index} [[sort]] lack range field')
        if _range=="":
            raise ValueError(f'providers.json {index} [[sort]] range field is empty')
        
        # keywords
        keywords=sort.get("keywords",None)
        if keywords is None:
            raise ValueError(f'providers.json {index} [[sort]] lack keywords field')
        if not isinstance(keywords, list): # Ensure it's a list before checking length
            raise ValueError(f'providers.json [[sort]] index {index} "keywords" field must be a list.')
        if len(keywords)<2:
            raise ValueError(f'providers.json {index} [[sort]] keywords field must contain at least two keywords.') 


def test():
    print("xxxxxxxxxx")

# 调用示例
# if __name__ == "__main__":
#     validate("your_config.toml")
