import sys
import os 

# third-party pkg
import toml

def validate(file_path):
    try:
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