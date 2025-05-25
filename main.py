import toml
import sys

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
    validate_toml('providers.toml')
