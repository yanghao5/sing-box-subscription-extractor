import json, base64, os
from typing import List


def eliminate_unicode(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        content = json.load(file)
    return json.dumps(content, ensure_ascii=False)

def is_base64_encoded(file_path: str) -> bool:
    try:
        with open(file_path, "rb") as file:
            content = file.read()

        # 尝试解码文件内容
        base64.b64decode(content, validate=True)
        return True
    except Exception as e:
        return False


def refine_raw_data(rawdata_list: List):
    refine_data = []
    for f in rawdata_list:
        data = ""
        with open(f, "rb") as file:
            data = file.read()

        if is_base64_encoded(f):
            data = base64.b64decode()

        data = eliminate_unicode(f)
        refine_data.append(data)
    os.makedirs("temp/refine", exist_ok=True)
    for f in rawdata_list:
        # read json
        with open(f, "r") as infile:
            data = json.load(infile)

        # file_path
        file_path = f.replace("raw", "refine")

        # write refined data to a new file
        with open(file_path, "w") as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
            
        print(f"\033[34m The refine subscription JSON file has been written to \033[33m {file_path} \033[0m\n")