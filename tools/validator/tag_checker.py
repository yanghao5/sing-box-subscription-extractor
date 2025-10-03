def validate(s):
    if not s:
        return False
    
    if s[0].isdigit():
        return False
    
    for char in s:
        if not (char.isalnum() or char == '_'):
            return False
    
    return True