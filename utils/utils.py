import os           
import yaml 


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def read_file(path):
    with open(path, encoding="utf-8") as file:
        for line in file:
            yield line.rstrip("\n")

def init_output_dirs(output_dpath, web=""):
    create_dir(output_dpath)

    urls_dpath = "/".join([output_dpath, "urls", web])
    results_dpath = "/".join([output_dpath, "results", web])
    create_dir(urls_dpath)
    create_dir(results_dpath)
    
    return urls_dpath, results_dpath

def get_config(file_path):
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
    return config