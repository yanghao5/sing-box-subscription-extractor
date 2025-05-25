import toml
import sys

def get_providers():
    # 获取环境变量
    providers = os.getenv('PROVIDERS')  # 假设通过环境变量存储 TOML 配置内容
    if providers:
        with open('providers.toml', 'w') as f:
            f.write(providers)
        print("Providers.toml has been created successfully.")
    else:
        print("No PROVIDERS environment variable found.")

def validate_toml(file_path):
    try:
        # 尝试加载 TOML 文件
        with open(file_path, 'r') as f:
            toml_data = toml.load(f)
        print(f"{file_path} is valid TOML.")
    except toml.TomlDecodeError as e:
        print(f"Error: Invalid TOML format in {file_path}")
        print(f"Details: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        sys.exit(1)

if __name__ == "__main__":
    # 验证 providers.toml 文件的合法性
    get_providers()
    validate_toml('providers.toml')
