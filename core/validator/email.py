from email_validator import validate_email, EmailNotValidError

def validate(email: str) -> None:
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError as e:
        raise ValueError(f"无效的邮箱地址: {str(e)}")

if __name__=="__main__":
    mail = "xxxxx@example.org"
    try:
        validate(mail)
        print("ok")      
    except ValueError as e:
        print(str(e))