import os
import shutil


def post_task():
    if os.path.exists("temp/raw"):
        shutil.rmtree("temp/raw")
    else:
        print(f"Directory temp/raw does not exist.")
        
    if os.path.exists("temp/refine"):
        shutil.rmtree("temp/refine")
    else:
        print(f"Directory temp/refine does not exist.")
    
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} 已删除")
    else:
        print(f"{file_path} 不存在")
        