import sys
import os 

# internal pkg
from core.validator import toml

def get_providers():
    providers = os.getenv('PROVIDERS')
    cleaned_providers = providers.replace('\r', '')
    if providers:
        with open('providers.toml', 'w') as f:
            f.write(providers)
        print("Providers.toml has been created successfully.")
    else:
        print("No PROVIDERS environment variable found.")

if __name__ == "__main__":
    get_providers()
    toml.validate('providers.toml')
