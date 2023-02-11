import os           


def create_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def read_file(path: str):
    with open(path, encoding="utf-8") as file:
        for line in file:
            yield line


def init_output_dirs(output_dpath: str) -> tuple[str]:
    create_dir(output_dpath)

    urls_dpath = "/".join([output_dpath, "urls"])
    results_dpath = "/".join([output_dpath, "results"])
    create_dir(urls_dpath)
    create_dir(results_dpath)
    
    return urls_dpath, results_dpath