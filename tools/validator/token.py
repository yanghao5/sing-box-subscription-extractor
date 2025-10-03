def validate(token)->bool:
    # 校验 token 长度
    if len(token) < 32:
        return False
    
    # 校验 token 是否仅包含小写字母和数字
    for char in token:
        if not (char.islower() or char.isdigit()):
            return False
    return True